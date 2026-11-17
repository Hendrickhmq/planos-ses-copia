#!/bin/bash
# Gera a v25 nas duas variantes (A: seis tomografos, um por polo no dimensionamento; B: so a carga de tomografia),
# limpa e marcada, a partir da v24A. Precisa de python com lxml, soffice e poppler.
# uso: gerar_v25.sh <python_com_lxml> <pasta_de_trabalho>
set -euo pipefail
PY="${1:?python com lxml}"
W="${2:?pasta de trabalho}"
AQUI="$(cd "$(dirname "$0")" && pwd)"
R4="$(cd "$AQUI/.." && pwd)"
BASE="$R4/versoes/plano_v24a_20261020.docx"

mkdir -p "$W/pdf"
(cd "$AQUI" && "$PY" calculo_v25.py > "$W/calculo.txt")
cp "$BASE" "$W/pdf/base.docx"
(cd "$W/pdf" && soffice --headless --convert-to pdf base.docx > /dev/null 2>&1)
for v in A B; do
  for m in limpo marcado; do
    rm -rf "${W:?}/$v/$m"
    mkdir -p "$W/$v/$m"
    unzip -q "$BASE" -d "$W/$v/$m"
    find "$W/$v/$m" -type l -delete
    "$PY" "$AQUI/aplicar_v25.py" "$W/$v/$m" "$m" "$v"
  done
  (cd "$W/$v/limpo" && rm -f "$W/pdf/v25${v}_limpo.docx" && zip -q -Xr "$W/pdf/v25${v}_limpo.docx" .)
  (cd "$W/pdf" && soffice --headless --convert-to pdf "v25${v}_limpo.docx" > /dev/null 2>&1)
  for m in limpo marcado; do
    "$PY" "$R4/calculo_v20/sumario_v20.py" "$W/$v/$m" "$m" "$W/pdf/base.pdf" "$W/pdf/v25${v}_limpo.pdf"
    rm -f "$W/v25${v}_$m.docx"
    (cd "$W/$v/$m" && zip -q -Xr "$W/v25${v}_$m.docx" .)
  done
done
echo "gerados: $W/v25A_limpo.docx, v25A_marcado.docx, v25B_limpo.docx e v25B_marcado.docx"
