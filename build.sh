#!/usr/bin/env bash
# Regera os artefatos de dist/ a partir de skills/planejamento-de-sistemas/.
set -euo pipefail
cd "$(dirname "$0")"
SKILL=skills/planejamento-de-sistemas
mkdir -p dist

# Arquivo ZIP reprodutível: ordem, timestamps e permissões fixas; sem cache Python.
python3 - "$SKILL" <<'PYZIP'
import pathlib, sys, zipfile
base = pathlib.Path(sys.argv[1])
with zipfile.ZipFile('dist/planejamento-de-sistemas.skill', 'w') as z:
    for file in sorted(base.rglob('*')):
        if not file.is_file() or '__pycache__' in file.parts or file.suffix in {'.pyc', '.pyo'} or file.name == '.DS_Store':
            continue
        name = pathlib.Path('planejamento-de-sistemas') / file.relative_to(base)
        info = zipfile.ZipInfo(name.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = (0o100644 << 16)
        z.writestr(info, file.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
PYZIP

python3 - "$SKILL" <<'PY'
import pathlib, sys
base = pathlib.Path(sys.argv[1])
ordem = ['SKILL.md',
 'references/entrevista.md','references/planejamento-mvp.md','references/estrutura-do-conjunto.md','references/documento-00.md',
 'references/continuidade-entre-sessoes.md','references/testes.md','references/anatomia-do-prompt.md',
 'references/sistema-existente.md','references/qualidade.md',
 'assets/00_visao_geral_e_decisoes.md','assets/README_indice.md','assets/NN_prompt.md',
 'assets/NN_contrato.md','assets/NN_manual.md','assets/NN_prompt_inicial_execucao.md',
 'assets/ESTADO.md','assets/decisoes/0000-modelo.md']
partes = ["""# Planejamento de sistemas — instruções completas

> Versão de arquivo único, para IAs que não têm sistema de skills. Cole como instrução do
> projeto/assistente, ou anexe à base de conhecimento, e comece dizendo o que quer planejar.
>
> Tudo o que a skill original divide em arquivos está aqui, na ordem de leitura. Onde o texto disser
> "leia `references/x.md`" ou "modelo em `assets/y.md`", role até a seção correspondente deste
> arquivo — os títulos de nível 1 marcam cada um.
>
> Gerado automaticamente a partir dos arquivos-fonte (sem data variável).

---
"""]
for rel in ordem:
    txt = (base/rel).read_text()
    if rel == 'SKILL.md':
        txt = txt.split('---', 2)[2].lstrip()
    partes.append(f"\n\n<!-- ═══ {rel} ═══ -->\n\n# ARQUIVO: {rel}\n\n{txt}\n\n---\n")
pathlib.Path('dist/planejamento-de-sistemas-completo.md').write_text(''.join(partes))
print("dist/planejamento-de-sistemas-completo.md")
PY
echo "dist/planejamento-de-sistemas.skill"
