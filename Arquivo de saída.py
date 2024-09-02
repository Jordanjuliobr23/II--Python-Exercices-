try: 
    FILENAME=input('Digite o nome do arquivo dessa forma (nome_arquivo.txt) ou o endereço onde o arquivo se encontra (C:\\Users\\JORDAN\\Downloads\\nome_arquivo.txt):  ')
    Fdin= open(FILENAME,'r') 
    Fdout= open(FILENAME + '.out','w')
    count = 0
    for linha in Fdin:
        ip= linha.strip()
        if count == 0:
            Fdout.write('[Endereços Ips VÁLIDOS]\n')
        elif count < 5: 
            Fdout.write(ip+'\n')
        elif count == 5:
            Fdout.write('[Encereços Ips INVÁLIDOS]\n')
            Fdout.write(ip+'\n')
        else:
            Fdout.write(ip+'\n')
        count += 1
    print('=-'*100)
    print('ARQUIVO DE SAÍDA: ')
    print(FILENAME + '.out')
    Fdin.close()
    Fdout.close()
except FileNotFoundError:
    print(f'O arquivo {Fdin} não foi encontrado :(')
except Exception as e: 
    print(f'Arquivo encontrado :)')
    print(f'Ocorreu um erro no arquivo {Fdin}')