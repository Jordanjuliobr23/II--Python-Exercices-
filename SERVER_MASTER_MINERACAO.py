import threading
import socket
import ssl
import time
import requests 
import struct


PORTA = 31471
IP = '0.0.0.0'
WINDOW_SIZE = 1000000 # Tamanho da janela responsável por buscar o nonce
TIMEOUT = 60 
clientes_pendentes = [] 
clientes = {}  
clientes_telegram = set()

API_TOKEN ='7359699123:AAH43iixaUcoYnsL5f_KiaK0jKDtFZ0n_K4'  
API_URL = f'https://api.telegram.org/bot{API_TOKEN}/'

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
    
    b_name = conn.recv(10) # Recebe o nome do cliente
    name = b_name.decode('utf-8')
    print(f'Cliente {name} conectado em {addr}')

     # Registro do nome do cliente ao dicionário clientes e o registro da sua última atividade(tempo), monitorando clientes inativos
    clientes[name] = {'conexao': conn, 'ultima_atividade': time.time()}
    try: 
        while True: 
            msg = conn.recv(4096)
            if not msg: 
                break 

            t_msg = msg[0]
            if t_msg == ord('T'): # Tipo da mensagem
                numTransacao = int.from_bytes(msg[1:3], byteorder='big')
                numCliente = int.from_bytes(msg[3:5], byteorder='big')
                tamJanela = int.fromm_bytes(msg[5:9], byteorder='big')
                bitZero = msg[9]
                tamTransacao = int.from_bytes(msg[10:14], byteorder='big')
                transacao = msg[14:14 + tamTransacao]
                break


            elif msg == b'G': # Requisição de transação
                if clientes_pendentes: 
                    transacao, bits_zero = clientes_pendentes[0] # Extraindo a primeira transaçção e o valor de bits zero
                    n_transacao = 1 # ID da transação
                    n_clientes = len(clientes) # Quantidade de clientes conectados
                    resposta = bytearray()

                    # Empacotando valores 
                    resposta.extend(n_transacao.to_bytes(2, byteorder='big')) # 2 bytes para o ID da transação
                    resposta.extend(n_clientes.to_bytes(2, byteorder='big')) # 2 bytes para quantidade de clientes
                    resposta.extend(WINDOW_SIZE.to_bytes(4, byteorder='big')) # 4 bytes para o tamanho da janela
                    resposta.extend(bits_zero.to_bytes(1, byteorder='big')) # 1 byte para o valor de bits zero
                    resposta.extend(len(transacao).to_bytes(4, byteorder='big')) # 4 bytes para o tamanho da transação

                    # transação codificada em bytearray
                    resposta.extend(transacao.encode())
                    conn.sendall(resposta)
                
                else:
                    conn.sendall(b'W') # Não existe transação disponível

            elif msg == b'S': # Requisição de Nonce
                n_transacao = int.from_bytes(msg[1:3], byteorder='big')
                nonce = int.from_bytes(msg[3:7], byteorder='big')
                transacao, bits_zero = clientes_pendentes[0]

                if val_nonce(transacao, nonce, bits_zero):
                    print(f'Nonce válido encontrado por {name}: {nonce}')
                    conn.sendall(n_transacao.to_bytes(2, byteorder='big') + b'V')
                    clientes_pendentes.pop(0) # removendo a transação validada
                else: 
                    conn.sendall(n_transacao.to_bytes(2, byteorder='big') + b'R')
    except Exception as e: 
        print(f'Ocorreu um erro ao extrair a transação do cliente: {e}')
    
        print(f'Cliente {name} desconectado')
    conn.close()

def serv_config():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((IP, PORTA))
        server.listen(5)
        print(f'Servidor ouvindo na porta {PORTA}.....')

        while True:
            conn, addr = server.accept()
            threading.Thread(target=atender_cliente, args=(conn, addr)).start() # Inicia uma Thread ao cliente

def add_transacao():
    try:
        while True: 
            comando = input('Comando: ')   
            if comando.startswith('/newtrans'):
                transacao, bits = comando.split()
                clientes_pendentes.append((transacao, int(bits))) # Add nova transação
            elif comando == '/validtrans':
                print(f'Transações validadas: {clientes_pendentes}')
            elif comando == '/pendtrans':
                print(f'Transações pendentes: {clientes_pendentes} ')
    except Exception as e:
        print(f'Ocorreu um erro na solicitação do comando desejado: {e}')


def mensagens_telegram_terminal():
    offset = 0  
    try:
        while True:
            resposta = requests.get(f'{API_URL}getUpdates?offset={offset}').json()
            mensagens = resposta.get('result', [])
            for msg in mensagens:
                chat_id = msg['message']['chat']['id']
                user_name = msg['message']['chat']['first_name']
                text = msg['message']['text']
                clientes_telegram.add(chat_id)
                text = f"{user_name, chat_id} no Telegram digitou: " + text
                comandos_telegram(chat_id, text)
                offset = msg['update_id'] + 1   
            time.sleep(5)
    except Exception as e:
        print(f'Ocorreu um erro ao tentar obter a mensagem do cliente {user_name, chat_id}: {e}')

def enviar_mensagem_telegram(texto):
    for chat_id in clientes_telegram:
        requests.get(f'{API_URL}sendMessage', params={'chat_id': chat_id, 'text': texto})
    
def comandos_telegram(chat_id, comando):
    if comando == '/validtrans':
        resposta = ('Transações validadas com êxito: ',clientes_pendentes)
    elif comando == '/pendTrans':
        resposta = ('Transações pendentes: ',clientes_pendentes)
    elif comando == '/clients':
        resposta = (f'Clientes conectados: {list(clientes.keys())}')
    else:
        resposta = ('O comando digitado está errado!')
    
    enviar_mensagem_telegram(resposta)


t= threading.Thread(target=serv_config)
t.start()
add_transacao()



