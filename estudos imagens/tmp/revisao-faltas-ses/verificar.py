import json, math, hashlib
from pathlib import Path
import openpyxl

base = Path(__file__).resolve().parent
original = Path('/Users/hendrick/Projetos/planos-ses/planos/redacao_04/estudos/estudo_filas_imagem_20261102_organizada.xlsx')
output = base.parent.parent / 'outputs/revisao-faltas-ses/estudo_filas_imagem_20261102_revisada_faltas_SES.xlsx'
old = openpyxl.load_workbook(original, data_only=False)
w = openpyxl.load_workbook(output, data_only=True)
formulas = openpyxl.load_workbook(output, data_only=False)
checks = 0
def equal(actual, expected, label, tolerance=1e-7):
    global checks
    checks += 1
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        assert math.isclose(actual, expected, abs_tol=tolerance, rel_tol=1e-10), (label, actual, expected)
    else:
        assert actual == expected, (label, actual, expected)

changed = {'Resumo','Enquadramento','Capacidade por polo','Pedidos novos','Encaminhamento SES','Faltas e pedidos','Filas do plano','Viabilidade','Rumo das filas','Fontes'}
for s in old:
    if s.title in changed:
        continue
    for row in s:
        for c in row:
            actual = formulas[s.title][c.coordinate].value
            equal(None if actual in (None,'') else actual, None if c.value in (None,'') else c.value, f'preservado {s.title}!{c.coordinate}')

rates = {}
slots = 0
improvement_slots = 0
for i in range(17):
    r = 21 + i
    done, absent = old['Faltas e pedidos'].cell(r, 3).value, old['Faltas e pedidos'].cell(r, 4).value
    rate = absent / (done + absent)
    name = old['Faltas e pedidos'].cell(r,1).value
    rates[name] = rate
    target = old['Faltas e pedidos'].cell(44+i,2).value
    expected_slots = math.ceil(target / (1-rate))
    equal(w['Faltas e pedidos'].cell(44+i,3).value, expected_slots, name+' vagas')
    equal(w['Faltas e pedidos'].cell(21+i,7).value, rate, name+' taxa')
    pr=23+i
    equal(sum(w['Premissas'].cell(pr,c).value for c in [4,5,9,10,11]),w['Premissas'].cell(pr,3).value,name+' situações')
    slots += expected_slots
    improvement_slots += math.ceil(target / .8)
equal(w['Faltas e pedidos']['C61'].value,slots,'total vagas')
equal(w['Faltas e pedidos']['G61'].value,improvement_slots,'total melhoria')

hours={'Ultrassom':0,'Tomografia':0}
clinical={'Ultrassom':0,'Tomografia':0}
cost_total=0
for r in range(17,64):
    name, fila, q, price, minutes = [old['Viabilidade'].cell(r,c).value for c in range(1,6)]
    modality='Tomografia' if name.startswith('TC') else 'Ultrassom'
    for c in range(1,6):
        equal(w['Viabilidade'].cell(r,c).value, old['Viabilidade'].cell(r,c).value, f'item preservado {r},{c}')
    clinical[modality] += q * minutes / 60
    hours[modality] += q * minutes / 60 / (1-rates[name])
    expected_cost=171.44 if modality=='Tomografia' else (100+5500/168)*minutes/60/(1-rates[name])+3
    equal(w['Viabilidade'].cell(r,12).value,expected_cost,f'custo {r}')
    equal(w['Viabilidade'].cell(r,13).value,price-expected_cost,f'margem {r}')
    cost_total += q*(price-expected_cost)
equal(w['Viabilidade']['N64'].value,cost_total,'margem total')
equal(w['Capacidade por polo']['G25'].value,hours['Ultrassom']/(20*1344),'uso US')
equal(w['Capacidade por polo']['H37'].value,hours['Tomografia']/(5*1344),'uso TC')
equal(w['Capacidade por polo']['C25'].value,clinical['Ultrassom'],'horas US')
equal(w['Capacidade por polo']['C37'].value,clinical['Tomografia'],'horas TC')
equal(w['Resumo']['B38'].value,math.ceil(hours['Ultrassom']/1344),'salas agregadas')
equal(w['Resumo']['B40'].value,math.ceil(hours['Tomografia']/1344),'TC agregada')

build=w['Cálculo por fila']
for item in range(1,48):
    regional=[row for row in build.iter_rows(min_row=62,max_row=343) if row[0].value==item]
    equal(len(regional),6,f'polos item {item}')
    equal(sum(row[5].value for row in regional),build.cell(4+item,5).value,f'conservação meta {item}')
    equal(sum(row[7].value for row in regional),build.cell(4+item,9).value,f'conservação horas {item}')
    equal(sum(row[9].value for row in regional),build.cell(4+item,10).value,f'conservação agenda {item}')

for i in range(17):
    r,rr=56+i,78+i
    stock,entries,agenda,production=[w['Encaminhamento SES'].cell(r,c).value for c in [2,3,4,5]]
    expected=max(0,stock+8*entries-8*production)
    equal(w['Encaminhamento SES'].cell(rr,6).value,expected,f'balanço {i}')
    equal(w['Encaminhamento SES'].cell(rr,7).value,0,f'transferência padrão {i}')

errors=[]
for s in w:
    for row in s:
        for c in row:
            if c.data_type=='e': errors.append((s.title,c.coordinate,c.value))
equal(errors,[],'erros exportados')
equal(w['Premissas']['B5'].value,1,'cenário restaurado')
equal(w['Premissas']['B7'].value,0,'recuperação restaurada')
equal(w['Premissas']['B8'].value,1,'retorno restaurado')
equal(w['Premissas']['B9'].value,8,'prazo restaurado')
report={'checks':checks,'vagas':slots,'vagas_melhoria':improvement_slots,'hours_agenda':hours,'original_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'formula_count':sum(c.data_type=='f' for s in formulas for row in s for c in row),'errors':errors,'unrelated_values_preserved':True,'scope':'Verificação independente de valores exportados e cálculos. Não verifica execução no Microsoft Excel.'}
(base/'verificacao_independente.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
