#!/bin/bash
# Gera a v24 nas duas variantes (A: tomografia nos seis polos; B: tomografia em rede), limpa e marcada, a partir da v23.
# Precisa de python com lxml, soffice e poppler.
# uso: gerar_v24.sh <python_com_lxml> <pasta_de_trabalho>
set -euo pipefail
PY="${1:?python com lxml}"
W="${2:?pasta de trabalho}"
AQUI="$(cd "$(dirname "$0")" && pwd)"
R4="$(cd "$AQUI/.." && pwd)"
BASE="$R4/versoes/plano_v23_20261008.docx"

mkdir -p "$W/pdf"
(cd "$AQUI" && "$PY" calculo_v24.py > "$W/calculo.txt")
cp "$BASE" "$W/pdf/base.docx"
(cd "$W/pdf" && soffice --headless --convert-to pdf base.docx > /dev/null 2>&1)
for v in A B; do
  for m in limpo marcado; do
    rm -rf "${W:?}/$v/$m"
    mkdir -p "$W/$v/$m"
    unzip -q "$BASE" -d "$W/$v/$m"
    find "$W/$v/$m" -type l -delete
    "$PY" "$AQUI/aplicar_v24.py" "$W/$v/$m" "$m" "$v"
  done
  # sumario: paginas medidas no LibreOffice, deslocamento sobre o sumario da v23
  (cd "$W/$v/limpo" && rm -f "$W/pdf/v24${v}_limpo.docx" && zip -q -Xr "$W/pdf/v24${v}_limpo.docx" .)
  (cd "$W/pdf" && soffice --headless --convert-to pdf "v24${v}_limpo.docx" > /dev/null 2>&1)
  for m in limpo marcado; do
    "$PY" "$R4/calculo_v20/sumario_v20.py" "$W/$v/$m" "$m" "$W/pdf/base.pdf" "$W/pdf/v24${v}_limpo.pdf"
    rm -f "$W/v24${v}_$m.docx"
    (cd "$W/$v/$m" && zip -q -Xr "$W/v24${v}_$m.docx" .)
  done
done
echo "gerados: $W/v24A_limpo.docx, v24A_marcado.docx, v24B_limpo.docx e v24B_marcado.docx"
