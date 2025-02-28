import socket
import time
import hashlib

nome = "" # Nome do cliente a receber pelo usuário.
pedido_rec = None

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORTA = 31471
IP = "127.0.0.1"
server.connect((IP, PORTA))

def pedir_trans():
    global pedido_rec
    try:
        while True:
            cod_pedido_g = "G"
            nome_bytes = nome.encode("utf-8")
            pedido_bytes = cod_pedido_g.encode("utf-8")
            server.sendall(pedido_bytes + nome_bytes)

            pedido_rec = server.recv(4096)

            if pedido_rec[0] == ord("W"):
                time.sleep(10)
                continue

            elif pedido_rec[0] == ord("T"):
                numTransacao = int.from_bytes(pedido_rec[1:3], byteorder='big')
                numCliente = int.from_bytes(pedido_rec[3:5], byteorder='big')
                tamJanela = int.from_bytes(pedido_rec[5:9], byteorder='big')
                bitZero = pedido_rec[9]
                tamTransacao = int.from_bytes(pedido_rec[10:14], byteorder='big')
                transacao = pedido_rec[14:14 + tamTransacao]
                break

            else:
                time.sleep(10)
                continue

    except Exception as e:
        print(f"Ocorreu um erro ao pedir transação ao servidor: {e}")

def calc_nonce(tamJanela, bitZero, transacao, numTransacao):
    fim_janela = tamJanela + 999999
    
    meta = bytearray(bitZero // 8)

    for jan in range(tamJanela, fim_janela + 1):
        nonce = meta + transacao.encode('utf-8') + str(jan).encode('utf-8')
        hash_nonce = hashlib.sha256(nonce).hexdigest()
        verificar_hash = '0' * (bitZero // 4)

        if hash_nonce.startswith(verificar_hash):
            nT = numTransacao.to_bytes(2, byteorder='big' )
            server.sendall(nT + nonce)
            validacao = server.recv(2)
            if validacao == ord('V'):
                print("Pedido validado")
                pedir_trans()

            elif validacao == ord('R'):
                print("Pedido rejeitado")
                pedir_trans()

    pedir_trans()
    