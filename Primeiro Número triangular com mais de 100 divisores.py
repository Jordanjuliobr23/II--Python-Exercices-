from operator import truediv


print('=-'*100)
print('Primeiro número traingular com mais de 100 divisores')
triang=0 
x= 1
while True: 
    triang= triang + x
    # qtos divisores tem?
    ndiv= 0
    k=1
    while k <= triang:
        if triang % k == 0:
            ndiv= ndiv + 1 
        k= k + 1
    # se o número de dividores for maior que 100, essa é a resposta
    if ndiv >= 100:
        print(f'O primeiro número triangular que tem mais de 100 divisores é {triang} que possui {ndiv} divisores')
        break
    x= x + 1
    
