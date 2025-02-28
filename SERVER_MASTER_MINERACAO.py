import threading
import socket
import ssl
import time
import requests 
import struct

# configuração do servidor

PORTA = 31471
IP = '0.0.0.0'
WINDOW_SIZE = 1000000 # Tamanho da janela responsável por buscar o nonce
TIMEOUT = 60 # Tempo limite antes de fechar a conexão para cliente inativos
pendentes = [] # Lista das transações pendentes
clientes = {}  # Dicionários com os clientes conectados

# 1- Função responsável por validar o nonce
def val_nonce(transacao, nonce, bits_zero):
    nonce_bin = bin(nonce)[2:].zfill(32) # Converte o nonce para uma string binária de 32 bits
    # converte os caracteres da transação para binário
    caracteres_bin = ''
    for c in transacao:
        caracteres_bin += format(ord(c), '08b')

    dados = nonce_bin + caracteres_bin
    return dados.startswith('0' * bits_zero) # Verifica se os bits iniciais são zeros


def atender_cliente(conn, addr):
    name = conn.recv(10).decode.strip() # Recebe o nome do cliente
    print(f'Cliente {name} conectado em {addr}')

     # Registro do nome do cliente ao dicionário clientes e o registro da sua última atividade(tempo), monitorando clientes inativos
    clientes[name] = {'conexao': conn, 'ultima_atividade': time.time()}
    try: 
        while True: 
            msg = conn.recv(4096).decode() 
            if not msg: 
                break 

            if msg == 'G': # Requisição de transação
                if pendentes: 
                    transacao, bits_zero = pendentes[0] # Extraindo a primeira transaçção e o valor de bits zero
                    n_transacao = 1 # ID da transação
                    n_clientes = len(clientes) # Quantidade de clientes conectados
                    resposta = bytearray()

                    # Empacotando valores 
                    resposta.extend(n_transacao.to_bytes(2, byteorder='big')) # 2 bytes para o ID da transação
                    resposta.extend(n_clientes.to_bytes(2, byteorder='big')) # 2 bytes para quantidade de clientes
                    resposta.extend(WINDOW_SIZE.to_bytes(4, byteorder='big')) # 4 bytes para o tamanho da janela
                    resposta.extend(bits_zero.to_bytes(1, byteorder='big')) # 1 byte para o valor de bits zero
                    resposta.extend(len(transacao)).to_bytes(4, byteorder='big') # 4 bytes para o tamanho da transação

                    # transação codificada em bytearray
                    resposta.extend(transacao.encode)
                    conn.sendall(resposta)
                
                else:
                    conn.sendall(b'W') # Não existe transação disponível

            elif msg == 'S': # Requisição de Nonce
                n_transacao, nonce = msg.split()
                nonce = int(nonce) 
                transacao, bits_zero = pendentes[0]

                if val_nonce(transacao, nonce, bits_zero):
                    print(f'Nonce válido encontrado por {name}: {nonce}')
                    conn.sendall(n_transacao.to_bytes(2, byteorder='big') + b'V')
                    pendentes.pop(0) # removendo a transação validada
                else: 
                    conn.sendall(n_transacao.to_bytes(2, byteorder='big') + b'R')
    except Exception as e: 
        print(f'Ocorreu um erro ao extrai a transação do cliente: {e}')
    
    print(f'Cliente {name} desconectado')
    conn.close()

def serv_config():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((IP, PORTA))
        server.listen(5)
        print(f'Servidor ouvindo na porta {PORTA}.....')

        while True:
            conn, addr = server.accept()
            threading.Thread(targed=atender_cliente, args=(conn, addr)).start() # Inicia uma Thread ao cliente

def add_transacao():
    while True: 
        comando = input('Comando: ')   
        if comando.startswith('/newtrans'):
            transacao, bits = comando.split()
            pendentes.append((transacao, int(bits))) # Add nova transação
        elif comando == '/validtrans':
            print(f'Transações validadas: {pendentes}')
        elif comando == '/pendtrans':
            print(f'Transações pendntes: {pendentes} ')

t= threading.Thread(target=serv_config)
t.start()
add_transacao()



# Arnaldo: ei o teu código do nonce ficou bom?  | yes | o meu tbm nao pq fiz com string invés de bytes jkkk | e como vai calcular o sha?
# Jordan: Aquele que Galileu pediu semestre passado? | não kkkk | tbm kkkkk | show | o ruim q n ele não quer que use hashlib | pse, to encabulado com isso, fzr esse cálculo manualmente sem nem pra onde vai
