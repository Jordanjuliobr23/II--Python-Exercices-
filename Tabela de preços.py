print('=-'*100)
print('LOJA QUASE DOIS - TABELA DE PREÇOS ')
qtd=0
p= 1.99
peso=0
while qtd < 50: 
    peso= peso + p
    qtd= qtd + 1
    print('{} - R${:.2f} '.format(qtd,peso))