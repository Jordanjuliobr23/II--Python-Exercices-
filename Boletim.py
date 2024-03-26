print('COLÉGIO TERESA')
Av1=float(input('Digite a Av1:'))
Av2=float(input('Digite a AV2:'))
Av3=float(input('Digite a Av3:'))
média= (Av1+Av2+Av3)/3
if média > 7.0 or média == 7.0:
    print('O aluno foi aprovado com a média de {:.1f}'.format(média))
else:
    print('O aluno foi reprovado com a média de {:.1f}'.format(média))