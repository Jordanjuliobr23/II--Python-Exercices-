print('=-'*100)
print('DEPARTAMENTO DE METEROLOGIA DO RN')
d=int(input('Digite quantas temperaturas diferentes serão lidas pelo sistema: '))
qtd=0
dia=0
soma=0
while qtd < d: 
    n=float(input('Digite a temperatura em Graus Celsius em Natal/RN: '))
    dia= dia + 1
    qtd= qtd + 1
    soma= n + soma
    print(f'Dia {dia}: Temperatura de {n} Graus Celsius aproximadamente!')
    if qtd == d: 
        media= soma/qtd 
        print(f'A média entre as temperaturas será aproximadamente {int(media)}')
    
