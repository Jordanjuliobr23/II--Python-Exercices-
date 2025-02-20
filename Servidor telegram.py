import socket
import threading
import sys
import requests
import time 

API_TOKEN ='/pr20242-Jordan'  
API_URL = f'https://api.telegram.org/bot{API_TOKEN}/getUpdates'

conec_totais = []
def mensagens_telegram():
    offset = 0
    while True:
        print("procurando novas mensagens")
        resposta = requests.get(f'{API_URL}getUpdates?offset={offset}')
        mensagens = resposta.json().get('result', [])
        for mensagem in mensagens:
            chat_id = mensagem['message']['chat']['id']
            user_name = mensagem['message']['chat']['first_name']
            text = mensagem['message']['text']
            clientes_telegram = set()
            clientes_telegram.add(chat_id)
            lista_clientes_telegram = list(clientes_telegram)
            print(lista_clientes_telegram[0])
            
            print(f"Nova mensagem de {user_name} ({chat_id}): {text}")
            offset = mensagem['update_id'] + 1
        time.sleep(2)

print("ligado")
t = threading.Thread(target=mensagens_telegram)
t.start()
    
def clientes(conn,adrr): #adrr ip e porta conn = concexao atual
    print(f'Novo cliente conectado: {addr}')
    conec_totais.append(conn)

    try:
        while True:
            tam_mensagem = conn.recv(2) #2 bytes do tamanho
            if not tam_mensagem: #sem o if quando o cliente desconecta buga o while
                break

            tam_mensagem = int.from_bytes(tam_mensagem,'big')
            mensagem = conn.recv(tam_mensagem).decode('utf-8')
            print(f'cliente:{adrr}, enviou: {mensagem}')

            #envia mensagem recebida para clientes
            mensagem_recebida = mensagem
            mensagem_recebida = mensagem_recebida.encode('utf-8')

            for conexão in conec_totais:
                if conexão != conn: #nao manda a mensagem para o proprio cliente que esta enviando
                    try:
                        len_mensagem = len(mensagem_recebida).to_bytes(2, 'big') 
                        mensagem_completa = len_mensagem + mensagem_recebida
                        conexão.send(mensagem_completa)

                        print(f"Enviando: {mensagem_recebida.decode('utf-8')} na rede")
                    except:
                        conec_totais.remove(conexão)

    except Exception as e:
        print(f"Erro com o cliente {addr}: {e}")
    finally:
        if conn in conec_totais:  #quando o cliente fecha o terminal encerra a conexão
            conn.close()
            conec_totais.remove(conn)
        print(f"Cliente {addr} desconectado.") 

host = '127.0.0.1' 
porta = 8080
try:
    sock = socket.socket() #flexibilidade de endereço
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #definida em socket e reutiliza portas ja conectadas (1 true)
    sock.bind((host, porta))
    sock.listen()
    print("Aguardando conexões...")

except OSError:
    print("Erro, endereço em uso.") #tratamento para o erro de endereço do terminal

threads = []

try:
    while True:
        conn, addr = sock.accept()

        t = threading.Thread(target=clientes , args=(conn, addr)) #config das threads
        t.start()
        threads.append(t)

except KeyboardInterrupt:
    ('Parando programa.')

finally: 
    if sock:   # se depois da excessao continuar aberta fecha
        sock.close()
    for t in threads:
        t.join() #recolhe os processors antes de fecha  