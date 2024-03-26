ano=int(input('Qual ano voce quer analisar?'))
if ano % 4==0 and ano % 100 != 0 or ano % 400 == 0:
    print('O Ano {} é BISSEXTO'.format(ano))
else:
    print('O Ano {} não é BISSEXTO'.format(ano))




