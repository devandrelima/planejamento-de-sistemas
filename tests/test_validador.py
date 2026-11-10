"""Testes determinísticos do validador, sem dependências externas."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/planejamento-de-sistemas/scripts/validar.py"
spec = importlib.util.spec_from_file_location("validar", SCRIPT)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

VISION = """# 00
## 5. Decisões
| # | Decisão | Motivo |
|---|---|---|
| D1 | CSV local | Sem API |
"""
PROMPT = """# 01
## Objetivo
Validar CSV conforme D1.
## Ordem de trabalho
Abrir ESTADO.md e fechar atualizando ESTADO.md.
## 1. Testes
- Entrada inválida retorna erro.
## Critérios de aceite
- [ ] Suíte de testes completa verde.
"""
INDEX = """# Índice
| Arquivo | Tipo | Depende de | Entrega |
|---|---|---|---|
| [00_visao_geral_e_decisoes.md](00_visao_geral_e_decisoes.md) | Referência | — | Decisões |
| [01_prompt_importacao.md](01_prompt_importacao.md) | Prompt | 00 | Importador |
| [02_prompt_inicial_execucao.md](02_prompt_inicial_execucao.md) | Arranque | 01 | Arranque |
"""


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.put("README.md", INDEX)
        self.put("00_visao_geral_e_decisoes.md", VISION)
        self.put("01_prompt_importacao.md", PROMPT)
        self.put("02_prompt_inicial_execucao.md", "# Arranque\n")

    def put(self, name, content):
        (self.base / name).write_text(content, encoding="utf-8")

    def codes(self, level=None):
        return {f.code for f in module.check(self.base) if level is None or f.level == level}

    def test_valid_case_has_no_errors(self):
        self.assertEqual(self.codes("error"), set())

    def test_missing_essential_file(self):
        (self.base / "00_visao_geral_e_decisoes.md").unlink()
        self.assertIn("ESSENTIAL_MISSING", self.codes("error"))

    def test_missing_acceptance(self):
        self.put("01_prompt_importacao.md", PROMPT.split("## Critérios de aceite")[0])
        self.assertIn("ACCEPTANCE_MISSING", self.codes("error"))

    def test_broken_link(self):
        self.put("01_prompt_importacao.md", PROMPT + "\nLeia [contrato](09_contrato_x.md).\n")
        self.assertIn("BROKEN_LINK", self.codes("error"))

    def test_unknown_decision(self):
        self.put("01_prompt_importacao.md", PROMPT + "\nConforme D99.\n")
        self.assertIn("DECISION_UNDEFINED", self.codes("error"))

    def test_self_cycle(self):
        self.put("README.md", INDEX.replace("| Prompt | 00 |", "| Prompt | 01 |"))
        self.assertIn("DEPENDENCY_CYCLE", self.codes("error"))

    def test_multi_step_cycle(self):
        self.put("README.md", INDEX.replace("| Prompt | 00 |", "| Prompt | 04 |") + "| [04_prompt_extra.md](04_prompt_extra.md) | Prompt | 01 | Extra |\n")
        self.put("04_prompt_extra.md", PROMPT)
        self.assertIn("DEPENDENCY_CYCLE", self.codes("error"))

    def test_missing_dependency(self):
        self.put("README.md", INDEX.replace("| Prompt | 00 |", "| Prompt | 09 |"))
        self.assertIn("DEPENDENCY_MISSING", self.codes("error"))

    def test_plain_reference(self):
        self.put("01_prompt_importacao.md", PROMPT + "\nConsulte 05_contrato_api.md.\n")
        self.assertIn("DOC_REF_MISSING", self.codes("error"))

    def test_unlisted_document_warns(self):
        self.put("03_manual_operacao.md", "# Manual\n")
        self.assertIn("NOT_INDEXED", self.codes("warning"))

    def test_missing_continuity_warns(self):
        self.put("01_prompt_importacao.md", PROMPT.replace("ESTADO.md", "progresso"))
        self.assertIn("CONTINUITY_UNCLEAR", self.codes("warning"))

    def test_cli_json_failure(self):
        self.put("01_prompt_importacao.md", PROMPT.split("## Critérios de aceite")[0])
        run = subprocess.run([sys.executable, str(SCRIPT), str(self.base), "--json"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)
        self.assertGreater(json.loads(run.stdout)["errors"], 0)


if __name__ == "__main__":
    unittest.main()
