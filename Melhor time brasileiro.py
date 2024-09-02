import json
FILENAME = 'C:\\Users\\20241014050014\\Downloads\\Time\\mercado.json'
try:
    fd = open ( FILENAME,'r',encoding='latin1') 
    dados= fd.read()
    fd.close()
    mercado = json.loads(dados)
    clubes= mercado['clubes']
    for posicao in range (1, 7):
        selecao= []
        for atleta in mercado ['atletas']:
            if atleta['posicao_id'] == posicao:
                a_clube_id = atleta['clube_id']
                a_clube= clubes[str(a_clube_id)]
                selecao.append(
                    (atleta['apelido'],
                    atleta['media_num'],
                    a_clube['nome']))
        selecao.sort(key=lambda a: a[1], reverse=True)
        print(selecao[0:3])
except Exception as e:
    print(f'O erro é: {e}')
