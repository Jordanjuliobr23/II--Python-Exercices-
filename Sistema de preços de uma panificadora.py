print('PANIFICADORA DO BIRA')
p=float(input('Digite o preço do pão: R$')) 
print('TABELA DE PREÇOS!')
qtd=0
x=0
while qtd <= 50:
    qtd= p + x 
    x= x + 1
    print(f'{x} - R${qtd}')