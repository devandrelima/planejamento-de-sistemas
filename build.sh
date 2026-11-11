#!/usr/bin/env bash
# Distribuição única da metodologia 2.0. Executar na raiz do repositório.
set -euo pipefail
cd "$(dirname "$0")"
SKILL=skills/planejamento-de-sistemas
mkdir -p dist

python3 - "$SKILL" <<'PY'
import pathlib
import sys
import zipfile

base = pathlib.Path(sys.argv[1])
dest = pathlib.Path("dist")
order = [
    "SKILL.md",
    "references/entrevista.md",
    "references/planejamento-mvp.md",
    "references/sistema-existente.md",
    "references/fluxo-v2.md",
    "references/contexto-v2.md",
    "references/testes-progressivos.md",
    "references/paralelismo-v2.md",
    "references/design-adaptativo.md",
    "references/qualidade.md",
    "assets/v2/00_visao_geral_e_decisoes.md",
    "assets/v2/README_indice.md",
    "assets/v2/SPRINT.md",
    "assets/v2/PROMPT_MAPA.md",
    "assets/v2/plano.json",
    "assets/v2/task.json",
    "assets/v2/ESTADO.json",
    "assets/v2/memoria-global.md",
    "assets/v2/memoria-dominio.md",
    "assets/v2/ADR.md",
]
for rel in order:
    if not (base / rel).is_file():
        raise SystemExit(f"Documento de distribuição inexistente: {rel}")

with zipfile.ZipFile(dest / "planejamento-de-sistemas.skill", "w") as archive:
    for file in sorted(base.rglob("*")):
        if not file.is_file() or "__pycache__" in file.parts or file.suffix in (".pyc", ".pyo") or file.name == ".DS_Store":
            continue
        name = pathlib.Path("planejamento-de-sistemas") / file.relative_to(base)
        item = zipfile.ZipInfo(name.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
        item.compress_type = zipfile.ZIP_DEFLATED
        item.external_attr = 0o100644 << 16
        archive.writestr(item, file.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

header = """# Planejamento de Sistemas 2.0 — instruções completas

> Documento único para assistentes sem suporte a skills. Para executar a CLI e seus testes,
> utilize o pacote da skill com o script scripts/fluxo.py.
> Este documento contém exclusivamente instruções e modelos da metodologia atual.
> Gerado de forma reproduzível a partir das fontes do repositório.

---
"""
parts = [header]
for rel in order:
    content = (base / rel).read_text(encoding="utf-8")
    if rel == "SKILL.md":
        content = content.split("---", 2)[2].lstrip()
    parts.append(f"\n\n<!-- ARQUIVO: {rel} -->\n\n# ARQUIVO: {rel}\n\n{content}\n\n---\n")
(dest / "planejamento-de-sistemas-completo.md").write_text("".join(parts), encoding="utf-8")
print("Dist da metodologia atual gerada com sucesso")
PY
