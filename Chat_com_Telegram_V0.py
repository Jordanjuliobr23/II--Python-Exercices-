import socket
import threading
import sys
import requests
import time 

API_TOKEN ='7359699123:AAH43iixaUcoYnsL5f_KiaK0jKDtFZ0n_K4'  
API_URL = f'https://api.telegram.org/bot{API_TOKEN}/'

conec_totais = []
clientes_telegram = set()
telegram_mensagem = ""
text = None
ultimo_enviado = None
mensagem = None
lock = threading.Lock()

def mensagens_telegram():
    global ultimo_enviado, text
    offset = 0  
    while True:
        print("procurando novas mensagens")
        resposta = requests.get(f'{API_URL}getUpdates?offset={offset}')
        mensagens = resposta.json().get('result', [])
        for msg in mensagens:
            chat_id = msg['message']['chat']['id']
            user_name = msg['message']['chat']['first_name']
            text = msg['message']['text']
            clientes_telegram.add(chat_id)

            if chat_id != ultimo_enviado:
                clientes_telegram.add(chat_id)

            ultimo_enviado = chat_id

            print(f"Nova mensagem de {user_name} ({chat_id}): {text}")
            offset = msg['update_id'] + 1   
        time.sleep(2)

def enviar_mensagem_telegram(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    response = requests.post(f"{API_URL}sendMessage", data=payload)

    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    
    
def enviar_para_todos(clientes_telegram):
    global text, ultimo_enviado
    with lock:
        if text:
            for chat_id in clientes_telegram:
                if chat_id != ultimo_enviado:
                    enviar_mensagem_telegram(chat_id, text)

thread_telegram = threading.Thread(target=enviar_para_todos, args=(clientes_telegram,))
thread_telegram.start()

def enviar_para_todos2(clientes_telegram):
    global mensagem
    while True:
        with lock:
            if mensagem != None:
                for chat_id in clientes_telegram:
                        enviar_mensagem_telegram(chat_id, mensagem)
            mensagem = None

thread_telegram2 = threading.Thread(target=enviar_para_todos2, args=(clientes_telegram,))
thread_telegram2.start()



print("ligado")
t = threading.Thread(target=mensagens_telegram)
t.start()
    
def clientes(conn,adrr): #adrr ip e porta conn = concexao atual
    global mensagem
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

def enviar_mensagem_global():
    global text
    while True:
        if text != None:
            print(f"Enviando texto global: {text}")
            with lock:
                mensagem_global = text.encode('utf-8')  # Codifica o texto para bytes
                for conexão in conec_totais:
                    try:
                        len_mensagem_global = len(mensagem_global).to_bytes(2, 'big')  # Tamanho da mensagem
                        mensagem_completa_global = len_mensagem_global + mensagem_global  # Junta o tamanho e a mensagem
                        conexão.send(mensagem_completa_global)  # Envia a mensagem
                        print(f"Mensagem global enviada para {conexão.getpeername()}: {text}")
                    except Exception as e:
                        print(f"Erro ao enviar mensagem global para {conexão.getpeername()}: {e}")
                        conec_totais.remove(conexão)  # Remove a conexão se houver erro
                text = None

outra_thread = threading.Thread(target=enviar_mensagem_global)
outra_thread.start()




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