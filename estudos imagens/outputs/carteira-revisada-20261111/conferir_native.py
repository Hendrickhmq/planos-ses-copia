import hashlib,json,math,shutil
from fractions import Fraction
from pathlib import Path
import openpyxl

here=Path(__file__).parent
native=Path('/tmp/carteira_v3_native_final_20261111/carteira_final_v3_revisada_20261111.xlsx')
data=json.loads((here/'dados_modelo.json').read_text())
checks=json.loads((here/'verificacao.json').read_text())
wb=openpyxl.load_workbook(native,data_only=True)
errors=[(s.title,c.coordinate,c.value) for s in wb for row in s for c in row if c.data_type=='e']
assert not errors,errors[:10]
assert abs(wb['Resumo']['B5'].value-6442415.61)<.005
assert abs(wb['Resumo']['B6'].value-4194186.39)<.005
assert wb['Resumo']['B7'].value==51617
assert wb['Conferência']['B140'].value==656
assert all(wb['Conferência'][f'B{r}'].value==0 for r in range(141,145))
assert wb['Saídas']['B9'].value=='não'
assert wb['Saídas']['B6'].value=='agendamentos'
codes={c['code']:c for c in data['codes']}
for r,x in enumerate(data['filas'],5):
    c=codes[x['codigo']]
    weight=Fraction(x['agendadas_12m'] or 0,c['weight_offer']) if c['weight_offer'] else Fraction(x['fila'],c['weight_stock'])
    stock=x['fila'] if x['current'] is None else x['current']
    expected=max(0,math.floor(stock+(c['entries']-c['offer3annual'])*weight-x['reserve']))
    assert expected==wb['Demanda por fila'][f'S{r}'].value,(r,x['nome'],expected,wb['Demanda por fila'][f'S{r}'].value)
    used=wb['Demanda por fila'][f'U{r}'].value
    assert 0<=used<=expected
    if x['agendadas_12m'] is None:assert wb['Demanda por fila'][f'N{r}'].value is None
formula_book=openpyxl.load_workbook(native,data_only=False)
assert len(formula_book.sheetnames)==10
assert sum(len(s.data_validations.dataValidation) for s in formula_book)>=6
original=Path('/Users/hendrick/Projetos/planos-ses/planos/redacao_04/estudos/carteira_final_v2_20261111.xlsx')
assert hashlib.sha256(original.read_bytes()).hexdigest()==data['metadata']['original_sha256']
target=here/'carteira_final_v3_revisada_20261111.xlsx'
shutil.copy2(native,target)
result=dict(engine='LibreOffice Calc',formula_errors=0,independent_fila_checks=len(data['filas']),
    scenario_checks=checks,original_preserved=True,output=str(target),sha256=hashlib.sha256(target.read_bytes()).hexdigest())
(here/'verificacao_native.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False))
