#!/usr/bin/env python3
"""Valida a estrutura de uma especificação executável. Python 3.10+, sem dependências."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

FILE_ID = re.compile(r"^(\d{2}[a-z]?)_(?:prompt|contrato|manual)(?:_|\.)", re.I)
DEPENDENCY = re.compile(r"(?<!\d)(\d{2}[a-z]?)(?!\d)", re.I)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
DOC_REF = re.compile(r"(?<![/\w])(?:docs/especificacao/)?\d{2}[a-z]?_[\w.-]+\.md\b")
DECISION = re.compile(r"\bD\d+\b")


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    file: str
    detail: str


def without_fences(text: str) -> str:
    return re.sub(r"(?ms)^\s*(\x60{3}|~~~~)[^\n]*\n.*?^\s*\1[^\n]*$", "", text)


def section(text: str, title: str) -> str | None:
    pat = re.compile(rf"(?im)^##\s+{title}\b[^\n]*\n")
    hit = pat.search(text)
    if not hit:
        return None
    end = re.search(r"(?m)^#{1,2}\s+", text[hit.end():])
    return text[hit.end():hit.end() + end.start()] if end else text[hit.end():]


def check(spec: Path) -> list[Finding]:
    spec = spec.resolve()
    findings: list[Finding] = []

    def report(level: str, code: str, file: str, detail: str) -> None:
        findings.append(Finding(level, code, file, detail))

    if not spec.is_dir():
        return [Finding("error", "DIR_MISSING", str(spec), "Diretório não encontrado")]

    files = {p.name: p for p in spec.glob("*.md") if p.is_file()}
    for needed in ("README.md", "00_visao_geral_e_decisoes.md"):
        if needed not in files:
            report("error", "ESSENTIAL_MISSING", needed, "Arquivo essencial ausente")
    prompts = sorted(p for n, p in files.items() if re.match(r"\d{2}[a-z]?_prompt_(?!inicial)", n, re.I))
    if not prompts:
        report("error", "NO_PROMPT", str(spec), "Nenhum prompt executável encontrado")

    texts = {n: p.read_text(encoding="utf-8") for n, p in files.items()}
    index = without_fences(texts.get("README.md", ""))
    entries: dict[str, tuple[str, str]] = {}
    indexed: set[str] = set()
    for line in index.splitlines():
        if not line.lstrip().startswith("|") or "[" not in line:
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 4:
            continue
        hit = LINK.search(cols[0])
        if not hit:
            continue
        target = hit.group(1).split("#", 1)[0]
        if not target.endswith(".md"):
            continue
        name = Path(target).name
        if name in indexed:
            report("error", "INDEX_DUPLICATE", "README.md", f"Entrada repetida: {name}")
        indexed.add(name)
        if name not in files:
            report("error", "INDEX_TARGET_MISSING", "README.md", f"Arquivo indexado não existe: {name}")
        ident = name.split("_", 1)[0]
        if ident in entries:
            report("error", "ID_DUPLICATE", "README.md", f"Identificador repetido: {ident}")
        entries[ident] = (name, cols[2])
        if not cols[3] or cols[3] in ("—", "-"):
            report("warning", "DELIVERY_UNCLEAR", "README.md", f"Entrega não descrita: {name}")

    for name in files:
        if (name == "00_visao_geral_e_decisoes.md" or FILE_ID.match(name)) and name not in indexed:
            report("warning", "NOT_INDEXED", name, "Arquivo não aparece no índice")

    graph: dict[str, set[str]] = {}
    for ident, (name, dep_text) in entries.items():
        if "prompt_" not in name or "prompt_inicial" in name:
            continue
        deps = {x.lower() for x in DEPENDENCY.findall(dep_text) if x != "00"}
        graph[ident.lower()] = deps
        for d in deps:
            if d not in {x.lower() for x in entries}:
                report("error", "DEPENDENCY_MISSING", name, f"Dependência {d} ausente no índice")
            if d.lower() == ident.lower():
                report("error", "DEPENDENCY_CYCLE", name, "Depende de si mesmo")

    visited: set[str] = set()
    active: set[str] = set()

    def walk(node: str) -> None:
        if node in active:
            report("error", "DEPENDENCY_CYCLE", entries[node][0], f"Ciclo envolvendo {node}")
            return
        if node in visited:
            return
        active.add(node)
        for dep in sorted(graph.get(node, set())):
            if dep in graph:
                walk(dep)
        active.remove(node)
        visited.add(node)

    for node in sorted(graph):
        walk(node)

    defined_decisions = set(re.findall(r"(?m)^\|\s*(D\d+)\s*\|", texts.get("00_visao_geral_e_decisoes.md", "")))
    for name, text in texts.items():
        stripped = without_fences(text)
        for link in LINK.findall(stripped):
            destination = link.split("#", 1)[0].strip().split(" ", 1)[0]
            if not destination or re.match(r"\w+://|mailto:", destination):
                continue
            if destination.startswith("docs/especificacao/"):
                destination = destination[len("docs/especificacao/"):]
            elif destination.startswith("/"):
                continue
            if destination.endswith(".md"):
                # ADRs fora da especificação não são rejeitados.
                if not destination.startswith("../") and not (spec / destination).is_file():
                    report("error", "BROKEN_LINK", name, f"Link local inexistente: {destination}")
        for ref in sorted(set(DOC_REF.findall(stripped))):
            local = ref.removeprefix("docs/especificacao/")
            if local not in files:
                report("error", "DOC_REF_MISSING", name, f"Referência inexistente: {ref}")
        if name != "00_visao_geral_e_decisoes.md":
            for decision in sorted(set(DECISION.findall(stripped))):
                if decision not in defined_decisions:
                    report("error", "DECISION_UNDEFINED", name, f"Decisão {decision} não declarada no documento 00")

    for p in prompts:
        text = texts[p.name]
        stripped = without_fences(text)
        acceptance = section(stripped, "Crit[eé]rios de aceite")
        if acceptance is None:
            report("error", "ACCEPTANCE_MISSING", p.name, "Seção 'Critérios de aceite' ausente")
        elif not re.search(r"(?m)^\s*-\s*\[[ xX]\]", acceptance):
            report("warning", "ACCEPTANCE_UNCHECKABLE", p.name, "Aceite sem checklist verificável")
        if section(stripped, "Objetivo") is None:
            report("warning", "OBJECTIVE_MISSING", p.name, "Seção de objetivo ausente")
        if "ESTADO.md" not in stripped or section(stripped, "Ordem de trabalho") is None:
            report("warning", "CONTINUITY_UNCLEAR", p.name, "Abertura/fechamento com ESTADO.md não está explícita")
        if not re.search(r"(?im)^##\s+(?:\d+\.\s+)?Testes\b", stripped):
            report("warning", "TESTS_UNCLEAR", p.name, "Sem seção de testes (ou justificativa explícita)")
        if acceptance is not None and not re.search(r"\b(?:su[ií]te|testes|verifica[cç][aã]o)\b", acceptance, re.I):
            report("warning", "TEST_ACCEPTANCE_UNCLEAR", p.name, "Aceite não menciona verificação de testes")

    if not any("prompt_inicial" in n for n in files):
        report("warning", "STARTUP_PROMPT_MISSING", str(spec), "Prompt de arranque não encontrado")
    return sorted(set(findings), key=lambda f: (f.level != "error", f.file, f.code, f.detail))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pasta", type=Path, help="Diretório da especificação (com README.md e 00_...md)")
    parser.add_argument("--json", action="store_true", help="Relatório JSON para automações")
    parser.add_argument("--strict", action="store_true", help="Avisos também resultam em saída 1")
    args = parser.parse_args()
    findings = check(args.pasta)
    errors = sum(f.level == "error" for f in findings)
    warnings = sum(f.level == "warning" for f in findings)
    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings, "findings": [asdict(f) for f in findings]}, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            print(f"{f.level.upper()} {f.code} {f.file}: {f.detail}")
        print(f"Resultado: {errors} erro(s), {warnings} aviso(s)")
    return int(errors > 0 or (args.strict and warnings > 0))


if __name__ == "__main__":
    sys.exit(main())
