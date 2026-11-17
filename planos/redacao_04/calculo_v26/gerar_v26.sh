#!/bin/bash
# Gera a v26 (a v25A como plano de trabalho de convenio, da proposta 36000720055202500), limpa e marcada, a partir
# da v25A. Precisa de python com lxml, soffice e poppler.
# uso: gerar_v26.sh <python_com_lxml> <pasta_de_trabalho>
set -euo pipefail
PY="${1:?python com lxml}"
W="${2:?pasta de trabalho}"
AQUI="$(cd "$(dirname "$0")" && pwd)"
R4="$(cd "$AQUI/.." && pwd)"
BASE="$R4/versoes/plano_v25a_20261021.docx"

mkdir -p "$W/pdf"
cp "$BASE" "$W/pdf/base.docx"
(cd "$W/pdf" && soffice --headless --convert-to pdf base.docx > /dev/null 2>&1)
for m in limpo marcado; do
  rm -rf "${W:?}/$m"
  mkdir -p "$W/$m"
  unzip -q "$BASE" -d "$W/$m"
  find "$W/$m" -type l -delete
  "$PY" "$AQUI/aplicar_v26.py" "$W/$m" "$m"
done
(cd "$W/limpo" && rm -f "$W/pdf/v26_limpo.docx" && zip -q -Xr "$W/pdf/v26_limpo.docx" .)
(cd "$W/pdf" && soffice --headless --convert-to pdf v26_limpo.docx > /dev/null 2>&1)
for m in limpo marcado; do
  "$PY" "$R4/calculo_v20/sumario_v20.py" "$W/$m" "$m" "$W/pdf/base.pdf" "$W/pdf/v26_limpo.pdf"
  rm -f "$W/v26_$m.docx"
  (cd "$W/$m" && zip -q -Xr "$W/v26_$m.docx" .)
done
(cd "$W" && soffice --headless --convert-to pdf v26_marcado.docx > /dev/null 2>&1)
echo "gerados: $W/v26_limpo.docx, v26_marcado.docx e v26_marcado.pdf"
