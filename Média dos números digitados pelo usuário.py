soma= 0
qtd= 0 
n= int(input('Digite um número: '))
while n >= 0:
    soma= soma + n
    qtd= qtd + 1
    n= int(input('Digite um número: '))
if qtd > 0:
    media= soma/qtd
    print(f'A média dos números digitados é {soma} ')
# se o usuário digitar um n < 0
else:
    print('A média não poderá ser calculada!')


