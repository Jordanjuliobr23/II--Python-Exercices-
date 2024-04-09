import math
print('CONVENIENCIA DO GRINGO')
print('Digite o valor do produto abaixo, para finalizar digite zero!')
z=float(input('Digite 0 se quiser finalizar a compra ou clique em qualquer número para continuar: '))
p=0
soma=0
pag=0
while z != 0: 
    n=float(input('Digite o valor do produto: '))
    p= p + 1
    soma= soma + n
    print('Produto {}: R${:.2f}'.format(p,n))
    if n==0: 
        pag=float(input('Digite o valor do pagamento: '))
        troco= pag - soma
        if pag < soma:
            print('O pagamento do cliente de R${} é menor que o preço total R${}, faltando R${} para completar o pagamento. Assim,não é possível realizar a compra!'.format(pag,soma,abs(troco)))
        print('Dinheiro: R${:.2f}'.format(soma))
        print('Troco: R${:.2f}'.format(troco))  