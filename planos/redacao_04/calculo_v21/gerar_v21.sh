#!/bin/bash
# Gera a v21 (limpa e marcada) a partir da v7 FINAL da equipe. Precisa de python com lxml, soffice e poppler.
# uso: gerar_v21.sh <python_com_lxml> <pasta_de_trabalho>
set -euo pipefail
PY="${1:?python com lxml}"
W="${2:?pasta de trabalho}"
AQUI="$(cd "$(dirname "$0")" && pwd)"
R4="$(cd "$AQUI/.." && pwd)"
BASE="$R4/dados/PT_simplificado_exames_de_imagem_v7_FINAL.docx"

mkdir -p "$W"
"$PY" "$AQUI/calculo_v21.py" > "$W/calculo.txt"
for m in limpo marcado; do
  rm -rf "${W:?}/$m"
  mkdir -p "$W/$m"
  unzip -q "$BASE" -d "$W/$m"
  find "$W/$m" -type l -delete
  "$PY" "$AQUI/aplicar_v21.py" "$W/$m" "$m"
done
# sumario: paginas medidas no LibreOffice, deslocamento sobre o sumario da v7 FINAL
mkdir -p "$W/pdf"
cp "$BASE" "$W/pdf/base.docx"
(cd "$W/limpo" && rm -f "$W/pdf/v21_limpo.docx" && zip -q -Xr "$W/pdf/v21_limpo.docx" .)
(cd "$W/pdf" && soffice --headless --convert-to pdf base.docx v21_limpo.docx > /dev/null 2>&1)
for m in limpo marcado; do
  "$PY" "$R4/calculo_v20/sumario_v20.py" "$W/$m" "$m" "$W/pdf/base.pdf" "$W/pdf/v21_limpo.pdf"
  rm -f "$W/v21_$m.docx"
  (cd "$W/$m" && zip -q -Xr "$W/v21_$m.docx" .)
done
echo "gerados: $W/v21_limpo.docx e $W/v21_marcado.docx"
