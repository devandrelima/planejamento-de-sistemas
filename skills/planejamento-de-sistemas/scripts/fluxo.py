#!/usr/bin/env python3
"""Planejamento 2.0: manifesto, contexto sob demanda e gates de sprint.

Uso: python3 fluxo.py [--repo DIRETORIO] [--spec docs/especificacao] COMANDO
Sem bibliotecas externas. Formato de plano: schema_version 2.0.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

TASK_ID = re.compile(r"^S\d{2}-P\d{2}-T\d{2}$")
SPRINT_ID = re.compile(r"^S\d{2}$")
PROMPT_ID = re.compile(r"^P\d{2}$")


class PlanError(Exception):
    pass


def path_within(root: Path, name: str) -> Path:
    """Resolve paths relative to an allowed root, refusing escapes and symlink escapes."""
    if not isinstance(name, str) or not name or "\\" in name:
        raise PlanError(f"Caminho inválido: {name!r}")
    candidate = Path(name)
    if candidate.is_absolute() or any(p in ("..", ".") for p in candidate.parts):
        raise PlanError(f"Caminho fora do escopo: {name}")
    root = root.resolve()
    result = (root / candidate).resolve()
    if not result.is_relative_to(root):
        raise PlanError(f"Caminho fora do escopo: {name}")
    return result


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise PlanError(f"Falha ao ler JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PlanError(f"JSON deve ser objeto: {path}")
    return value


def read_required(root: Path, name: str) -> str:
    path = path_within(root, name)
    if not path.is_file():
        raise PlanError(f"Arquivo obrigatório ausente: {name}")
    return path.read_text(encoding="utf-8")


def nonempty_list(value: object) -> bool:
    return isinstance(value, list) and len(value) > 0 and all(isinstance(x, str) and x.strip() for x in value)


def collides(a: str, b: str) -> bool:
    a, b = a.rstrip("/"), b.rstrip("/")
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


class Project:
    def __init__(self, repo: Path, spec: str = "docs/especificacao"):
        self.repo = repo.resolve()
        self.spec = path_within(self.repo, spec)
        self.plan = load_json(self.spec / "plano.json")
        self.state_file = self.repo / "ESTADO.json"
        self.sprints = self.plan.get("sprints", [])
        self.tasks: dict[str, dict] = {}
        self.task_order: list[str] = []
        self.task_sprint: dict[str, str] = {}
        self.task_prompt: dict[str, str] = {}
        self.issues: list[str] = []
        self._index()
        self.state = load_json(self.state_file) if self.state_file.is_file() else self.empty_state()

    def _issue(self, msg: str) -> None:
        self.issues.append(msg)

    def _index(self) -> None:
        if self.plan.get("schema_version") != "2.0":
            self._issue("schema_version deve ser '2.0'")
        if self.plan.get("human_gate") is not True:
            self._issue("human_gate deve ser true")
        if self.plan.get("coverage_min") != 80:
            self._issue("coverage_min deve ser 80")
        interval = self.plan.get("full_suite_every")
        if not isinstance(interval, int) or isinstance(interval, bool) or interval < 1:
            self._issue("full_suite_every deve ser inteiro positivo")
        if not nonempty_list(self.plan.get("global_context")):
            self._issue("global_context deve conter arquivos globais")
        else:
            for name in self.plan["global_context"]:
                try:
                    read_required(self.repo, name)
                except PlanError as exc:
                    self._issue(f"global_context: {exc}")
        if not isinstance(self.sprints, list) or not self.sprints:
            self._issue("sprints deve conter pelo menos uma sprint")
            return

        seen_sprints: set[str] = set()
        for sprint in self.sprints:
            if not isinstance(sprint, dict):
                self._issue("Sprint precisa ser objeto")
                continue
            sid = sprint.get("id")
            if not isinstance(sid, str) or not SPRINT_ID.fullmatch(sid) or sid in seen_sprints:
                self._issue(f"ID de sprint inválido ou repetido: {sid}")
                continue
            seen_sprints.add(sid)
            if not sprint.get("delivery") or not sprint.get("demo_command"):
                self._issue(f"{sid}: exige entrega utilizável e comando de demonstração")
            if not nonempty_list(sprint.get("regression_tests")):
                self._issue(f"{sid}: exige testes de regressão dos fluxos afetados")
            prompts = sprint.get("prompts", [])
            if not isinstance(prompts, list) or not (1 <= len(prompts) <= 3):
                self._issue(f"{sid}: são permitidos de 1 a 3 prompts")
                continue
            seen_prompts: set[str] = set()
            for prompt in prompts:
                if not isinstance(prompt, dict):
                    self._issue(f"{sid}: prompt deve ser objeto")
                    continue
                pid = prompt.get("id")
                if not isinstance(pid, str) or not PROMPT_ID.fullmatch(pid) or pid in seen_prompts:
                    self._issue(f"{sid}: prompt inválido ou repetido: {pid}")
                    continue
                seen_prompts.add(pid)
                try:
                    content = read_required(self.spec, prompt.get("map", ""))
                    if not content.strip():
                        self._issue(f"{sid}-{pid}: mapa está vazio")
                except PlanError as exc:
                    self._issue(str(exc))
                refs = prompt.get("tasks", [])
                if not nonempty_list(refs):
                    self._issue(f"{sid}-{pid}: faltam tasks")
                    continue
                for ref in refs:
                    try:
                        task = load_json(path_within(self.spec, ref))
                    except PlanError as exc:
                        self._issue(str(exc))
                        continue
                    tid = task.get("id")
                    if not isinstance(tid, str) or not TASK_ID.fullmatch(tid) or not tid.startswith(f"{sid}-{pid}-") or tid in self.tasks:
                        self._issue(f"Task com ID inválido/repetido: {tid}")
                        continue
                    self.tasks[tid] = task
                    self.task_order.append(tid)
                    self.task_sprint[tid] = sid
                    self.task_prompt[tid] = pid
                    for key in ("context", "writes", "tests", "acceptance"):
                        if not nonempty_list(task.get(key)):
                            self._issue(f"{tid}: {key} deve ser lista não vazia")
                    if not isinstance(task.get("depends_on"), list) or not all(isinstance(x, str) for x in task["depends_on"]):
                        self._issue(f"{tid}: depends_on deve ser lista")
                    if not isinstance(task.get("reads", []), list):
                        self._issue(f"{tid}: reads deve ser lista")
                    if not task.get("instruction") or not task.get("result"):
                        self._issue(f"{tid}: instruction e result são obrigatórios")
                    if task.get("kind") == "interface":
                        design = task.get("design", {})
                        if not isinstance(design, dict) or not design.get("review") or not design.get("skills_selection"):
                            self._issue(f"{tid}: interface exige revisão visual e seleção contextual de skills")
                    budget = task.get("context_budget_tokens")
                    if not isinstance(budget, int) or isinstance(budget, bool) or budget <= 0:
                        self._issue(f"{tid}: context_budget_tokens inválido")
                    for key in ("context", "reads", "writes"):
                        for name in task.get(key, []):
                            try:
                                if key == "context":
                                    read_required(self.repo, name)
                                else:
                                    path_within(self.repo, name)
                            except (PlanError, TypeError) as exc:
                                self._issue(f"{tid}: {exc}")

        # Validate dependencies including cross-sprint direction.
        index = {tid: n for n, tid in enumerate(self.task_order)}
        graph: dict[str, list[str]] = {}
        for tid, task in self.tasks.items():
            deps = task.get("depends_on", [])
            graph[tid] = deps if isinstance(deps, list) else []
            for dep in graph[tid]:
                if dep not in self.tasks:
                    self._issue(f"{tid}: dependência desconhecida {dep}")
                elif index[dep] >= index[tid]:
                    # Earlier tasks in other prompts may run in parallel; only future sprint is forbidden.
                    sprint_a = [s.get("id") for s in self.sprints].index(self.task_sprint[tid])
                    sprint_b = [s.get("id") for s in self.sprints].index(self.task_sprint[dep])
                    if sprint_b > sprint_a:
                        self._issue(f"{tid}: dependência em sprint futura {dep}")
        active: set[str] = set()
        done: set[str] = set()

        def dfs(tid: str) -> None:
            if tid in active:
                self._issue(f"Dependência circular envolvendo {tid}")
                return
            if tid in done:
                return
            active.add(tid)
            for dep in graph.get(tid, []):
                if dep in self.tasks:
                    dfs(dep)
            active.remove(tid)
            done.add(tid)

        for tid in self.task_order:
            dfs(tid)

        for a, aid in enumerate(self.task_order):
            for bid in self.task_order[a + 1:]:
                x, y = self.tasks[aid], self.tasks[bid]
                if x.get("parallel_group") and x.get("parallel_group") == y.get("parallel_group"):
                    if any(collides(p, q) for p in x.get("writes", []) for q in y.get("writes", [])):
                        self._issue(f"Conflito paralelo: {aid} e {bid} escrevem nos mesmos caminhos")

    def empty_state(self) -> dict:
        return {
            "schema_version": "2.0",
            "tasks": {tid: {"status": "pendente"} for tid in self.tasks},
            "sprints": {s["id"]: {"status": "pendente", "human_approved": False} for s in self.sprints if isinstance(s, dict) and "id" in s}
        }

    def validate(self) -> list[str]:
        issues = self.issues.copy()
        if self.state.get("schema_version") != "2.0":
            issues.append("ESTADO.json: schema_version inválido")
        for unknown in set(self.state.get("tasks", {})) - set(self.tasks):
            issues.append(f"ESTADO.json: task órfã não pode ser descartada: {unknown}")
        for tid in self.tasks:
            entry = self.state.get("tasks", {}).get(tid)
            if not isinstance(entry, dict) or entry.get("status") not in ("pendente", "concluida"):
                issues.append(f"ESTADO.json: task sem estado válido {tid}")
            elif entry["status"] == "concluida" and (not entry.get("commit") or not entry.get("evidence")):
                issues.append(f"ESTADO.json: task {tid} concluída sem evidências declaradas")
        for sprint in self.sprints:
            if not isinstance(sprint, dict) or "id" not in sprint:
                continue
            sid = sprint["id"]
            entry = self.state.get("sprints", {}).get(sid)
            if not isinstance(entry, dict) or not isinstance(entry.get("human_approved"), bool):
                issues.append(f"ESTADO.json: sprint sem aprovação booleana {sid}")
            elif entry["human_approved"] and any(self.state.get("tasks", {}).get(t, {}).get("status") != "concluida" for t in self.task_order if self.task_sprint[t] == sid):
                issues.append(f"ESTADO.json: sprint {sid} aprovada com tasks pendentes")
        return sorted(set(issues))

    def require_valid(self) -> None:
        problems = self.validate()
        if problems:
            raise PlanError("Plano inválido:\n- " + "\n- ".join(problems))

    def synchronize(self) -> list[str]:
        """Register new tasks from a replan, preserving historical completion evidence."""
        if self.issues:
            raise PlanError("Plano estruturalmente inválido; não sincronizar")
        for tid in self.state.get("tasks", {}):
            if tid not in self.tasks:
                raise PlanError(f"Task antiga removida do plano: {tid}; preserve histórico e registre decisão")
        added: list[str] = []
        for sprint in self.sprints:
            sid = sprint["id"]
            entry = self.state.setdefault("sprints", {}).setdefault(
                sid, {"status": "pendente", "human_approved": False})
            new = [tid for tid in self.task_order
                   if self.task_sprint[tid] == sid and tid not in self.state.get("tasks", {})]
            if new and entry.get("human_approved"):
                raise PlanError(f"Não incluir tasks na sprint já aprovada: {sid}")
            for tid in new:
                self.state.setdefault("tasks", {})[tid] = {"status": "pendente"}
                added.append(tid)
        self.save()
        return added

    def pending_sprint(self) -> dict | None:
        for sprint in self.sprints:
            if not self.state["sprints"][sprint["id"]]["human_approved"]:
                return sprint
        return None

    def ready(self) -> dict:
        self.require_valid()
        sprint = self.pending_sprint()
        if sprint is None:
            return {"sprint": None, "ready": [], "parallel_batch": [], "gate": "projeto_aprovado"}
        sid = sprint["id"]
        subset = [tid for tid in self.task_order if self.task_sprint[tid] == sid]
        unfinished = [tid for tid in subset if self.state["tasks"][tid]["status"] != "concluida"]
        if not unfinished:
            return {"sprint": sid, "ready": [], "parallel_batch": [], "gate": "aguardando_avaliacao_humana"}
        ready = [
            tid for tid in unfinished
            if all(self.state["tasks"][dep]["status"] == "concluida" for dep in self.tasks[tid].get("depends_on", []))
        ]
        batch: list[str] = []
        for tid in ready:
            if not any(any(collides(a, b) for a in self.tasks[tid]["writes"] for b in self.tasks[other]["writes"]) for other in batch):
                batch.append(tid)
        return {"sprint": sid, "ready": ready, "parallel_batch": batch, "gate": "execucao"}

    def context(self, tid: str) -> tuple[str, dict]:
        ready = self.ready()
        if tid not in ready["ready"]:
            raise PlanError(f"Task {tid} não está liberada (sprint {ready['sprint']}; gate {ready['gate']})")
        task = self.tasks[tid]
        paths = list(dict.fromkeys(self.plan["global_context"] + task["context"] + task.get("reads", [])))
        sections = [
            f"# Execução isolada: {tid}\n",
            f"## Objetivo\n{task['instruction']}\n",
            f"## Entrega esperada\n{task['result']}\n",
            "## Alterações autorizadas\n" + "\n".join(f"- {p}" for p in task["writes"]) + "\n",
            "## Testes da task\n" + "\n".join(f"- {p}" for p in task["tests"]) + "\n",
            "## Critérios de aceite\n" + "\n".join(f"- {p}" for p in task["acceptance"]) + "\n",
            "## Dependências\n" + (", ".join(task.get("depends_on", [])) or "Nenhuma") + "\n"
        ]
        fingerprints = {}
        for name in paths:
            content = read_required(self.repo, name)
            fingerprints[name] = hashlib.sha256(content.encode("utf-8")).hexdigest()
            sections.append(f"\n## CONTEXTO: {name}\n\n{content}\n")
        body = "\n".join(sections)
        estimated = math.ceil(len(body) / 4)
        budget = task["context_budget_tokens"]
        if estimated > budget:
            raise PlanError(f"Contexto excede orçamento: estimativa {estimated} > {budget}; revise a task, sem truncar invariantes")
        return body, {"task": tid, "files": paths, "sha256": fingerprints, "estimated_tokens": estimated, "budget_tokens": budget}

    def save(self) -> None:
        tmp = self.state_file.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(self.state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(self.state_file)

    def finish_task(self, tid: str, commit: str, evidence: str) -> None:
        if tid not in self.ready()["ready"]:
            raise PlanError("Task ainda não está pronta para execução")
        if not re.fullmatch(r"[0-9a-f]{7,40}", commit):
            raise PlanError("Commit deve ser SHA Git (7-40 caracteres hexadecimais)")
        if not evidence.strip():
            raise PlanError("Descreva os testes realmente executados")
        self.state["tasks"][tid] = {"status": "concluida", "commit": commit, "evidence": evidence, "verification": "declarada; confira logs e Git"}
        self.save()

    def review(self, outcome: str, feedback: str, regression: str = "", changed: float | None = None,
               demo: str = "", full_suite: str = "", global_coverage: float | None = None) -> None:
        self.require_valid()
        sprint = self.pending_sprint()
        if sprint is None:
            raise PlanError("Todas as sprints já foram aprovadas")
        sid = sprint["id"]
        tids = [tid for tid in self.task_order if self.task_sprint[tid] == sid]
        if any(self.state["tasks"][tid]["status"] != "concluida" for tid in tids):
            raise PlanError("Não avaliar sprint com tasks pendentes")
        if not feedback.strip():
            raise PlanError("Registre o feedback humano")
        if outcome == "ajustar":
            self.state["sprints"][sid] = {"status": "ajustes_solicitados", "human_approved": False, "feedback": feedback}
            self.save()
            return
        if outcome != "aprovar":
            raise PlanError("Resultado de avaliação desconhecido")
        if not regression.strip() or not demo.strip():
            raise PlanError("Aceite exige evidências declaradas da regressão afetada e demonstração executada")
        if changed is None or not 80 <= changed <= 100:
            raise PlanError("Cobertura de código alterado deve ser medida e >= 80%")
        idx = next(i for i, item in enumerate(self.sprints) if item["id"] == sid) + 1
        need_full = (idx == len(self.sprints) or idx % self.plan["full_suite_every"] == 0
                     or sprint.get("requires_full_suite", False) or sprint.get("risk") in ("high", "critical"))
        if need_full and (not full_suite.strip() or global_coverage is None or not 80 <= global_coverage <= 100):
            raise PlanError("Checkpoint exige suíte completa e cobertura global medida >= 80%")
        self.state["sprints"][sid] = {
            "status": "aprovada", "human_approved": True, "human_feedback": feedback,
            "regression_evidence": regression, "demo_evidence": demo,
            "changed_coverage": changed,
            "full_suite_evidence": full_suite if need_full else None,
            "global_coverage": global_coverage if need_full else None,
            "verification": "evidências declaradas; não executadas pela CLI"
        }
        self.save()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", default=".", help="Raiz do projeto gerado")
    p.add_argument("--spec", default="docs/especificacao", help="Especificação relativa ao projeto")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("validar")
    sub.add_parser("sincronizar")
    sub.add_parser("prontas")
    ctx = sub.add_parser("contexto")
    ctx.add_argument("task")
    ctx.add_argument("--saida", help="Arquivo de saída, opcional")
    finish = sub.add_parser("concluir")
    finish.add_argument("task")
    finish.add_argument("--commit", required=True)
    finish.add_argument("--evidencia", required=True)
    review = sub.add_parser("avaliar")
    review.add_argument("resultado", choices=["aprovar", "ajustar"])
    review.add_argument("--feedback", required=True)
    review.add_argument("--regressao", default="")
    review.add_argument("--cobertura-alterada", type=float)
    review.add_argument("--demo", default="")
    review.add_argument("--suite-completa", default="")
    review.add_argument("--cobertura-global", type=float)
    args = p.parse_args(argv)
    try:
        project = Project(Path(args.repo), args.spec)
        if args.command == "validar":
            problems = project.validate()
            print(json.dumps({"errors": len(problems), "findings": problems}, ensure_ascii=False, indent=2))
            return int(bool(problems))
        if args.command == "sincronizar":
            added = project.synchronize()
            print(json.dumps({"added": added, "errors": project.validate()}, ensure_ascii=False, indent=2))
            return int(bool(project.validate()))
        if args.command == "prontas":
            print(json.dumps(project.ready(), ensure_ascii=False, indent=2))
        if args.command == "contexto":
            body, meta = project.context(args.task)
            if args.saida:
                output = Path(args.saida)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(body, encoding="utf-8")
                print(json.dumps(meta, ensure_ascii=False, indent=2))
            else:
                print(body)
                print("\n<!-- Metadados: " + json.dumps(meta, ensure_ascii=False) + " -->")
        if args.command == "concluir":
            project.finish_task(args.task, args.commit, args.evidencia)
            print("Task registrada como concluída (evidência declarada, verificar externamente).")
        if args.command == "avaliar":
            project.review(args.resultado, args.feedback, args.regressao, args.cobertura_alterada,
                           args.demo, args.suite_completa, args.cobertura_global)
            print("Avaliação registrada; aprovação requer ação humana explícita.")
        return 0
    except (PlanError, OSError, TypeError, KeyError, ValueError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
