print('JEARNS 2022')
n=int(input('Digite o ano de nascimento:'))
i= 2022-n
print('O atleta tem {} anos'.format(i))
if i <= 9:
    print('Sua classificação é mirim, dirija-se a quadra 01')
elif i <= 14:
    print('Sua classificação é infantil, dirija-se a quadra 02')
elif i <= 19:
    print('Sua classificação é juvenil, dirija-se a quadra 03')
elif i <= 25:
    print('Sua classificação é Senior, dirije-se a quadra 04')
elif i <= 25:
    print('Sua classificação é master, dirija-se a quadra 05')