try: 
    FILENAME=input('Digite o nome do arquivo dessa forma (nome_arquivo.txt) ou o endereço onde o arquivo se encontra (C:\\Users\\JORDAN\\Downloads\\nome_arquivo.txt) :  ')
    Fd= open(FILENAME,'r') 
    count=0
    while Fd.readline():
        count += 1 
    print(f'O número de linhas presentes no arquivo {Fd} corresponde a {count}')
    Fd.close() 
except FileNotFoundError:
    print(f'O arquivo {Fd} não foi encontrado :(')
except Exception as e: 
    print(f'Arquivo encontrado :)')
    print(f'Ocorreu um erro no arquivo {Fd}')