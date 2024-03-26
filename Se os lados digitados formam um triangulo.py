r1=float(input('Digite o cateto oposto:'))
r2=float(input('Digite o cateto adjacente:'))
r3=float(input('Digite a hipotenusa:'))
if r1+r2 < r3:
    print('Esses valores PODEM formar um triangulo!')
else:
    print('Esses valores NÃO podem formar um triangulo equilátero!')