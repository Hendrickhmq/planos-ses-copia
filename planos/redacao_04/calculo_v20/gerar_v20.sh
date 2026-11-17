#!/bin/bash
# Gera a v20 (limpa e marcada) a partir da v6 da equipe. Precisa de python com lxml, soffice e poppler.
# uso: gerar_v20.sh <python_com_lxml> <pasta_de_trabalho>
set -euo pipefail
PY="${1:?python com lxml}"
W="${2:?pasta de trabalho}"
AQUI="$(cd "$(dirname "$0")" && pwd)"
R4="$(cd "$AQUI/.." && pwd)"
BASE="$R4/dados/PT_simplificado_exames_de_imagem_v6.docx"

mkdir -p "$W"
"$PY" "$AQUI/calculo_v20.py" > "$W/calculo.txt"
for m in limpo marcado; do
  rm -rf "${W:?}/$m"
  mkdir -p "$W/$m"
  unzip -q "$BASE" -d "$W/$m"
  find "$W/$m" -type l -delete
  "$PY" "$AQUI/aplicar_v20.py" "$W/$m" "$m"
done
# sumario: paginas medidas no LibreOffice, deslocamento sobre o sumario da v6
mkdir -p "$W/pdf"
cp "$BASE" "$W/pdf/v6.docx"
(cd "$W/limpo" && rm -f "$W/pdf/v20_limpo.docx" && zip -q -Xr "$W/pdf/v20_limpo.docx" .)
(cd "$W/pdf" && soffice --headless --convert-to pdf v6.docx v20_limpo.docx > /dev/null 2>&1)
for m in limpo marcado; do
  "$PY" "$AQUI/sumario_v20.py" "$W/$m" "$m" "$W/pdf/v6.pdf" "$W/pdf/v20_limpo.pdf"
  rm -f "$W/v20_$m.docx"
  (cd "$W/$m" && zip -q -Xr "$W/v20_$m.docx" .)
done
echo "gerados: $W/v20_limpo.docx e $W/v20_marcado.docx"
