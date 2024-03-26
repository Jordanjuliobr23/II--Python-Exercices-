frase=str(input('Digite uma frase:'))
print('A letra A aparece {} vezes na frase'.format(frase.count('a')))
print('A primeira letra A aparece na posição {}'.format(frase.find('a')))
print('A última letra A aparece na posição {}'.format(frase.rfind('a')))