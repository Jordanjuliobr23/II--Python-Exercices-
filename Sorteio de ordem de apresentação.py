import random
g1=str(input('Digite o nome do primeiro aluno:'))
g2=str(input('Digite o nome do segundo aluno:'))
g3=str(input('Digite o nome do terceiro aluno:'))
g4=str(input('Digite o nome do quarto aluno:'))
l=[g1,g2,g3,g4]
o=random.shuffle(l)
print('A ordem de apresentação será:')
print(l)