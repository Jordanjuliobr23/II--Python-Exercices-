print('Olá!somos do Banco Bradesco, antes de realizar o seu emprestimo precisamos que as demandas do comprador sejam condizentes, por favor preencha o formulário a seguir!')
c=int(input('Digite o valor da casa:R$'))
s=int(input('O salário do comprador:R$'))
a=int(input('Quantos anos de financiamento?:'))
p=c/(a*12)
e= (s*30/100)
if s > p:
    print('Para pagar o imovel de R${} em {} anos a prestação será de R${}, o emprestimo pode ser concedido'.format(c,a,p))
else:
    print('Para pagar o imovel de R${} em {} anos a prestação será de R${},o emprestimo não pode ser concedido'.format(c,a,p))