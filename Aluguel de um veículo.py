d=float(input('Por quantos dias o carro foi alugado?:'))
km=float(input('Quantos km foram rodados?:'))
v1= d*60.00
v2= km*0.15
T= v1+v2
print('O total a se pagar será:R${}'.format(T))