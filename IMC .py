print('NATAL FIT')
p= float (input('Digite seu peso: (KG)'))
a= float (input('Digite sua alutra: (M)'))
imc= p/(a**2)
print('O seu indice de Massa Corporal é de {:.2f}'.format(imc))
if imc < 18.5:
    print('O seu indice de Massa Corporal está abaixo da média!')
elif 18.5 < imc and 25 > imc:
    print('Seu indice de Massa Corporal está Ideal!')
elif 25 < imc and 30 > imc:
    print('Seu indice de Massa Corporal está sobrepeso')
elif 30 < imc and 40 > imc:
    print('Seu indice de Massa corporal é Obeso')
elif 40 < imc:
    print('Seu indice de Massa Corporal é Obesidade Morbida')
