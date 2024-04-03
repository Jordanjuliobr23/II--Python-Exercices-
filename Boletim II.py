print('=-'*100)
print('Boletim escolar')
n1=float(input('Digite sua Av1 aqui: '))
n2=float(input('Digite a Av2 aqui: '))
n3=float(input('Digite a Av3 aqui: '))
m= (n1 + n2 + n3) / 3
print('Média: {:.2f} '.format(m))
while m > 0 and m <= 10:
    if m <=0:
        print('O aluno teve um mau desempenho, e precisará de acompanhamento dos professores e da equipe pedagógica ')
        break
    if 0 < m < 6.0:
        print('O aluno teve um desempenho abaixo da média, precisando de um pouco de acompanhamento dos professores!  ')
        break
    if 6.0 < m < 9.5:
        print('O aluno teve um desempenho acima da média, precisando manter esse resultado até o final do ano para ser oficialmente aprovado!')
        break
    if 9.5 < m <= 9.9:
        print('O aluno teve um desempenho acima do esperado, chegando próximo aos 10 pontos de média. Parabéns!')
        break
    if m == 10:
        print('O aluno teve um desempenho excelente, chegando aos 10 pontos de média!! Parabéns, mantenha-se assim!')
        break

