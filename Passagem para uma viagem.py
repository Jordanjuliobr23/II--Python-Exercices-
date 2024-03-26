d=float(input('Qual a distancia da sua viagem?'))
print('Voce está prestes a começar sua viagem de {}KM'.format(d))
print('---'*30)
if d>200:
   v= d*0.45
   print('O preço da sua passagem será de {:.2f}R$'.format(v))
else:
    p= d*0.50
    print('O preço da sua passagem será de {:.2f}R$'.format(p))


