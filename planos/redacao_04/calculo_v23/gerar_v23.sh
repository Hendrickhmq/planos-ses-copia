#!/bin/bash
# Gera a v23 (limpa e marcada) a partir da v22. Precisa de python com lxml, soffice e poppler.
# uso: gerar_v23.sh <python_com_lxml> <pasta_de_trabalho>
set -euo pipefail
PY="${1:?python com lxml}"
W="${2:?pasta de trabalho}"
AQUI="$(cd "$(dirname "$0")" && pwd)"
R4="$(cd "$AQUI/.." && pwd)"
BASE="$R4/versoes/plano_v22_20261007.docx"

mkdir -p "$W"
for m in limpo marcado; do
  rm -rf "${W:?}/$m"
  mkdir -p "$W/$m"
  unzip -q "$BASE" -d "$W/$m"
  find "$W/$m" -type l -delete
  "$PY" "$AQUI/aplicar_v23.py" "$W/$m" "$m"
done
# sumario: paginas medidas no LibreOffice, deslocamento sobre o sumario da v22
mkdir -p "$W/pdf"
cp "$BASE" "$W/pdf/base.docx"
(cd "$W/limpo" && rm -f "$W/pdf/v23_limpo.docx" && zip -q -Xr "$W/pdf/v23_limpo.docx" .)
(cd "$W/pdf" && soffice --headless --convert-to pdf base.docx v23_limpo.docx > /dev/null 2>&1)
for m in limpo marcado; do
  "$PY" "$R4/calculo_v20/sumario_v20.py" "$W/$m" "$m" "$W/pdf/base.pdf" "$W/pdf/v23_limpo.pdf"
  rm -f "$W/v23_$m.docx"
  (cd "$W/$m" && zip -q -Xr "$W/v23_$m.docx" .)
done
echo "gerados: $W/v23_limpo.docx e $W/v23_marcado.docx"
