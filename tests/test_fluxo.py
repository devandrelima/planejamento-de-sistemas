"""Regressões da ferramenta de execução v2. Python 3.11+, somente stdlib."""
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills/planejamento-de-sistemas/scripts/fluxo.py"
loader = importlib.util.spec_from_file_location("fluxo_v2", SOURCE)
flow = importlib.util.module_from_spec(loader)
sys.modules[loader.name] = flow
loader.loader.exec_module(flow)


class FlowV2Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.spec = self.repo / "docs/especificacao"
        self.spec.mkdir(parents=True)
        self.put("docs/especificacao/memoria/global.md", "Invariantes: nunca registrar segredo.\n")
        self.put("docs/especificacao/memoria/auth.md", "Contrato da autenticação\n")
        self.put("docs/especificacao/memoria/design.md", "Critérios de interface e acessibilidade\n")
        self.put("docs/especificacao/prompts/P01.md", "# Mapa de execução 01\n")
        self.put("docs/especificacao/prompts/P02.md", "# Mapa de execução 02\n")
        self.tasks = {
            "S01-P01-T01": self.task("S01-P01-T01", [], ["src/contrato.py"], "docs/especificacao/memoria/auth.md"),
            "S01-P01-T02": self.task("S01-P01-T02", ["S01-P01-T01"], ["src/api.py"], "docs/especificacao/memoria/auth.md"),
            "S01-P02-T01": self.task("S01-P02-T01", ["S01-P01-T01"], ["src/ui.py"], "docs/especificacao/memoria/design.md", kind="interface"),
            "S01-P02-T02": self.task("S01-P02-T02", ["S01-P01-T02", "S01-P02-T01"], ["tests/test_login.py"], "docs/especificacao/memoria/auth.md")
        }
        self.sprint = {
            "id": "S01", "delivery": "Login utilizável", "demo_command": "python -m app",
            "regression_tests": ["python -m unittest tests/test_login.py"],
            "prompts": [
                {"id": "P01", "map": "prompts/P01.md", "tasks": ["tasks/T01.json", "tasks/T02.json"]},
                {"id": "P02", "map": "prompts/P02.md", "tasks": ["tasks/T03.json", "tasks/T04.json"]}
            ]
        }
        self.write_plan()

    def task(self, tid, deps, writes, memory, kind="backend"):
        data = {
            "id": tid, "depends_on": deps, "writes": writes, "reads": [],
            "context": [memory], "tests": ["python -m unittest tests/test_login.py"],
            "acceptance": ["Teste positivo e negativo cobertos"],
            "instruction": "Implementar fluxo conforme contrato", "result": "Código e testes",
            "context_budget_tokens": 1500, "kind": kind
        }
        if kind == "interface":
            data["design"] = {"review": "Conferir acessibilidade e responsividade",
                              "skills_selection": "Inventariar skills presentes e justificar a escolha"}
        return data

    def put(self, path, content):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def write_plan(self):
        for i, tid in enumerate(self.tasks):
            self.put(f"docs/especificacao/tasks/T0{i+1}.json", json.dumps(self.tasks[tid]))
        self.put("docs/especificacao/plano.json", json.dumps({
            "schema_version": "2.0", "human_gate": True, "coverage_min": 80,
            "full_suite_every": 3, "global_context": ["docs/especificacao/memoria/global.md"],
            "sprints": [self.sprint]
        }))
        self.put("ESTADO.json", json.dumps({
            "schema_version": "2.0",
            "tasks": {tid: {"status": "pendente"} for tid in self.tasks},
            "sprints": {"S01": {"status": "pendente", "human_approved": False}}
        }))

    def project(self):
        return flow.Project(self.repo)

    def finish(self, tid):
        self.project().finish_task(tid, "abc1234", "teste unitário executado e conferido")

    def test_sync_adds_new_task_without_erasing_old_evidence(self):
        self.finish("S01-P01-T01")
        fresh = self.task("S01-P02-T03", ["S01-P02-T02"], ["src/ajuste.py"],
                          "docs/especificacao/memoria/ui.md")
        self.tasks[fresh["id"]] = fresh
        self.write_plan()
        # Recreate the previously recorded completion as it would exist on disk.
        state = json.loads((self.repo / "ESTADO.json").read_text())
        state["tasks"]["S01-P01-T01"] = {"status": "concluida", "commit": "abc1234", "evidence": "passou"}
        state["tasks"].pop(fresh["id"])
        self.put("ESTADO.json", json.dumps(state))
        plan = json.loads((self.spec / "plano.json").read_text())
        plan["sprints"][0]["prompts"][1]["tasks"].append("tasks/T05.json")
        self.put("docs/especificacao/tasks/T05.json", json.dumps(fresh))
        self.put("docs/especificacao/plano.json", json.dumps(plan))
        project = self.project()
        self.assertIn("sem estado válido", " ".join(project.validate()))
        self.assertEqual(project.synchronize(), ["S01-P02-T03"])
        self.assertEqual(self.project().validate(), [])
        self.assertEqual(self.project().state["tasks"]["S01-P01-T01"]["commit"], "abc1234")

    def test_unknown_task_is_not_deleted_by_sync(self):
        state = json.loads((self.repo / "ESTADO.json").read_text())
        state["tasks"]["S01-P99-T99"] = {"status": "concluida", "commit": "abc1234", "evidence": "existe"}
        self.put("ESTADO.json", json.dumps(state))
        with self.assertRaisesRegex(flow.PlanError, "Task antiga removida"):
            self.project().synchronize()

    def test_missing_global_memory_fails_validation(self):
        (self.repo / "docs/especificacao/memoria/global.md").unlink()
        self.assertIn("global_context:", " ".join(self.project().validate()))

    def test_valid_plan(self):
        self.assertEqual(self.project().validate(), [])

    def test_first_task_ready(self):
        self.assertEqual(self.project().ready()["ready"], ["S01-P01-T01"])

    def test_parallel_after_contract(self):
        self.finish("S01-P01-T01")
        ready = self.project().ready()
        self.assertEqual(set(ready["parallel_batch"]), {"S01-P01-T02", "S01-P02-T01"})

    def test_context_loads_only_authorized_files(self):
        body, meta = self.project().context("S01-P01-T01")
        self.assertIn("Contrato da autenticação", body)
        self.assertIn("Invariantes", body)
        self.assertNotIn("Critérios de interface", body)
        self.assertEqual(len(meta["files"]), 2)

    def test_context_budget_rejects_not_truncates(self):
        self.tasks["S01-P01-T01"]["context_budget_tokens"] = 1
        self.write_plan()
        with self.assertRaisesRegex(flow.PlanError, "excede orçamento"):
            self.project().context("S01-P01-T01")

    def test_refuses_path_escape(self):
        self.tasks["S01-P01-T01"]["context"] = ["../../etc/passwd"]
        self.write_plan()
        self.assertIn("fora do escopo", " ".join(self.project().validate()))

    def test_detects_cycle(self):
        self.tasks["S01-P01-T01"]["depends_on"] = ["S01-P01-T02"]
        self.write_plan()
        self.assertIn("circular", " ".join(self.project().validate()))

    def test_detects_parallel_write_collision(self):
        self.tasks["S01-P01-T02"]["parallel_group"] = "g1"
        self.tasks["S01-P02-T01"]["parallel_group"] = "g1"
        self.tasks["S01-P02-T01"]["writes"] = ["src/api.py"]
        self.write_plan()
        self.assertIn("Conflito paralelo", " ".join(self.project().validate()))

    def test_blocks_completion_before_dependency(self):
        with self.assertRaisesRegex(flow.PlanError, "não está pronta"):
            self.finish("S01-P01-T02")

    def test_requires_human_approval_before_next_sprint(self):
        self.finish("S01-P01-T01")
        self.finish("S01-P01-T02")
        self.finish("S01-P02-T01")
        self.finish("S01-P02-T02")
        self.assertEqual(self.project().ready()["gate"], "aguardando_avaliacao_humana")
        with self.assertRaisesRegex(flow.PlanError, "Cobertura"):
            self.project().review("aprovar", "Aceito", "testes afetados verdes", 79, "Fluxo visto")
        self.project().review("aprovar", "Aceito", "testes afetados verdes", 84, "Fluxo visto")
        self.assertEqual(self.project().ready()["gate"], "projeto_aprovado")

    def test_three_sprints_need_global_checkpoint(self):
        for i in (2, 3):
            s = json.loads(json.dumps(self.sprint))
            s["id"] = f"S0{i}"
            s["prompts"] = []
            for p in self.sprint["prompts"]:
                new = json.loads(json.dumps(p))
                new["map"] = f"prompts/S0{i}_{p['id']}.md"
                self.put("docs/especificacao/" + new["map"], "# Mapa\n")
                new["tasks"] = []
                for j, source in enumerate(p["tasks"]):
                    original = json.loads((self.spec / source).read_text())
                    tid = f"S0{i}-{p['id']}-T0{j+1}"
                    original["id"] = tid
                    original["depends_on"] = []
                    target = f"tasks/{tid}.json"
                    self.put("docs/especificacao/" + target, json.dumps(original))
                    new["tasks"].append(target)
                s["prompts"].append(new)
            if i == 2:
                second = s
            else:
                third = s
        plan = json.loads((self.spec / "plano.json").read_text())
        plan["sprints"] = [self.sprint, second, third]
        self.put("docs/especificacao/plano.json", json.dumps(plan))
        state = json.loads((self.repo / "ESTADO.json").read_text())
        for s in (second, third):
            state["sprints"][s["id"]] = {"status": "pendente", "human_approved": False}
            for p in s["prompts"]:
                for ref in p["tasks"]:
                    task = json.loads((self.spec / ref).read_text())
                    state["tasks"][task["id"]] = {"status": "concluida", "commit": "abc1234", "evidence": "testado"}
        for tid in self.tasks:
            state["tasks"][tid] = {"status": "concluida", "commit": "abc1234", "evidence": "testado"}
        state["sprints"]["S01"]["human_approved"] = True
        state["sprints"]["S02"]["human_approved"] = True
        self.put("ESTADO.json", json.dumps(state))
        project = self.project()
        self.assertEqual(project.validate(), [])
        with self.assertRaisesRegex(flow.PlanError, "Checkpoint"):
            project.review("aprovar", "Aceito", "regressão verificada", 85, "demo executada")
        project.review("aprovar", "Aceito", "regressão verificada", 85, "demo executada", "suíte verde", 81)

    def test_unapproved_feedback_stays_blocked(self):
        for tid in list(self.tasks):
            self.finish(tid)
        self.project().review("ajustar", "Login ainda não responde corretamente")
        self.assertEqual(self.project().ready()["gate"], "aguardando_avaliacao_humana")


if __name__ == "__main__":
    unittest.main()
