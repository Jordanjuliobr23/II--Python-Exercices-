import hashlib
import time


# Criação da função find_nonce
def find_nonce(dataToHash: str, bitsToBeZero: int): 
    try:
        check= ''
        if bitsToBeZero % 4 == 0: 
            check = '0' * (bitsToBeZero // 4)  # Em hexadecimal, calcula-se ao padrão de '0' a qual o hash deverá começar.
        elif bitsToBeZero % 4 != 0: # Ajusta os '0' para os bits não mútiplos de 4
             check = '0' * (bitsToBeZero // 4) + '0'[:(bitsToBeZero % 4)] 
        b_data = dataToHash.encode() 

        

# Processo de cocatenar o valor atual do nonce ao hash e o tempo necessário.
        nonce = 0 
        inicio = time.time()
        hash = '' 
        lenght= len(check) # Tamanho da string de '0' que deverá ter no início do hash.

        while hash[:lenght] != check: # O laço será interrompido quando o tamanho dos primeiros caracteres '0' do hash, forem iguais ao tamanho dos primeiros caracteres '0' no inicio de check. 
            b_nonce = str(nonce).encode() 
            hash = hashlib.sha256(b_data + b_nonce).hexdigest() # Concatena os bytes do nonce com b_data, convertendo essa operação em uma string hexadecimal.
            nonce += 1 

        fim= time.time() 
        temp= fim - inicio # Tempo levado até o hash atender o padrão definido em 'check'
        return nonce, temp 
    except Exception as e:
        print(f"ERRO! Houve uma falha na função 'find_nonce': {e} ")
        return None 
# Função responsável pelos textos que irão compor a tabela
def tabela():
    try: 
        text = [
            "Esse é fácil", "Esse é fácil", "Esse é fácil",
            "Texto maior muda o tempo?", "Texto maior muda o tempo?", "Texto maior muda o tempo?",
            "É possível calcular esse?", "É possível calcular esse?", "É possível calcular esse?"
        ]
        qtd_bzero = [8, 10, 15, 8, 10, 15, 18, 19, 20] # Quantidade de bits '0' iniciais no hash

# Criação da tabela
        Fd_out= 'tabela_preenchida.txt'
        with open(Fd_out,'w') as outfile:
            outfile.write(f"{'Texto a validar (converta os bytes antes de chamar)':<60} {'Bits em zero':<15} {'Nonce':<10} {'Tempo (s)'}\n")
        
            for texto, bits in zip(text, qtd_bzero): # Une as listas 'text' e 'qtd_bzero'
                nonce, temp = find_nonce(texto, bits) # Armazenam o cálculo do nonce e o tempo necessário até o hash e nonce serem cotatenados.
                outfile.write(f"{texto:<60} {bits:<15} {nonce:<10} {temp:.2f}\n")
    
            print(f'A tabela foi salva com êxito no arquivo: {Fd_out} ')
    except Exception as e: 
        print(f'ERRO" Houve um erro no salvamento da tabela no arquivo! {e}')

try:
    tabela() 
except Exception as e:
    print(f'ERRO! Ocorreu uma falha inesperada na exibição da tabela!')
