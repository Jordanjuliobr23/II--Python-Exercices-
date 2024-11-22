import json

try:
    ano=int(input(f'Escolha entre o ano de 2021 e 2022: '))
except ValueError:
    print('ERRO! O ano digitado NÃO corresponde a um número inteiro!')
    exit()

# Carregamento dos dados conforme o ano solicitado
try:
    if ano == 2021: 
        with open('cartola_fc_2021.txt', 'r', encoding='utf-8') as file:
            dictCartola= json.load(file)
    elif ano == 2022:
        with open('cartola_fc_2022.txt', 'r', encoding='utf-8') as file:
            dictCartola= json.load(file)
    else: 
        print(f'ERRO! O ano de {ano} não é válido!')
except FileNotFoundError:
    print(f'ERRO! O arquivo não foi encontrado pelo programa!')


# Escalações disponíveis

lineup= { 
    1: '3-4-3',
    2: '3-5-2',
    3: '4-3-3',
    4: '4-4-2',
    5: '4-5-1',
    6: '5-3-2',
    7: '5-4-1'
}


for key, value in lineup.items():
    print(f'{key}: {value}')
try:
    esquema_escolhido=int(input('Escolha um desses esquemas táticos disponíveis (1-7): '))
    if esquema_escolhido > 7 or esquema_escolhido < 1:
        print(f'O não existe um esquema com a numeração {esquema_escolhido}')
except ValueError:
    print('ERRO! O número digitado não corresponde a um número inteiro!')

escala = {
    '3-4-3': {'Goleiro': 1, 'Zagueiro': 3, 'Lateral': 0, 'Meia': 4, 'Atacante': 3, 'Tecnico': 1},
    '3-5-2': {'Goleiro': 1, 'Zagueiro': 3, 'Lateral': 0, 'Meia': 5, 'Atacante': 2, 'Tecnico': 1},
    '4-3-3': {'Goleiro': 1, 'Zagueiro': 2, 'Lateral': 2, 'Meia': 3, 'Atacante': 3, 'Tecnico': 1},
    '4-4-2': {'Goleiro': 1, 'Zagueiro': 2, 'Lateral': 2, 'Meia': 4, 'Atacante': 2, 'Tecnico': 1},
    '4-5-1': {'Goleiro': 1, 'Zagueiro': 2, 'Lateral': 2, 'Meia': 5, 'Atacante': 1, 'Tecnico': 1},
    '5-3-2': {'Goleiro': 1, 'Zagueiro': 3, 'Lateral': 2, 'Meia': 3, 'Atacante': 2, 'Tecnico': 1},
    '5-4-1': {'Goleiro': 1, 'Zagueiro': 3, 'Lateral': 2, 'Meia': 4, 'Atacante': 1, 'Tecnico': 1},
}

# Esquema tático escolhido pelo usuário
esquema_final = lineup[esquema_escolhido]
qtd_posições = escala[esquema_final]

# Selecionando os jogadores com as maiores pontuações em cada posição
selecionados= {}

for posicao, qtd in qtd_posições.items():
    posicao_id = {
        'Goleiro': 1,
        'Zagueiro': 3,
        'Lateral': 2,
        'Meia': 4,
        'Atacante': 5,
        'Tecnico': 6
    }[posicao]

# Selecionando jogadores da posição específica
jogadores = []
for atleta in dictCartola['atletas']:
    if atleta['posicao_id'] == posicao_id:
        jogadores.append(atleta)

# Pontuação total do jogador (Médias do jogador X Partidas jogadas)
for atleta in jogadores: 
    if 'media_num' in atleta and 'jogos_num' in atleta:
        atleta['pontuacao_total'] = atleta['media_num'] * atleta ['jogos_num']
    else: 
        atleta['pontuacao_total'] = 0

# Ordena os jogadores a partir de sua pontuação total e selecionando os melhores em um dicionário
melhores_jogadores = []
while len(melhores_jogadores) < qtd:
        melhor = None
        for atleta in jogadores:
            if melhor is None or atleta['pontuacao_total'] > melhor['pontuacao_total']:
                melhor = atleta
        melhores_jogadores.append(melhor)
        jogadores.remove(melhor)

selecionados[posicao] = melhores_jogadores


#Construindo o dicionário final e ajustando a URL das fotos

final = {}

for posicao, atletas in selecionados.items():
    for atleta in atletas: 
        atleta_id = atleta['atleta_id']
        foto_url = atleta.get('foto', '')
        foto_url = foto_url.replace('_FORMATO_', '_220x220_')
        
        # Verificando se o clube existe no dicionário de clubes
        clube_id= atleta['clube_id']
        clube_nome= dictCartola['clubes'].get(clube_id,{}).get('nome', 'Clube Desconhecido')
        escudo_url = dictCartola['clubes'].get(clube_id, {}).get('escudos', {}).get('60x60', '')

        # Selecionando cada um dos números do jogador e adicionando no dicionário final
        final[atleta_id] = {
            'id': atleta_id,
            'nome': atleta.get('nome', 'Desconhecido'),
            'apelido': atleta.get('apelido', 'Sem Apelido'),
            'url_foto': foto_url,
            'clube': clube_nome,
            'escudo': escudo_url,
            'id_posicao': atleta['posicao_id'],
            'nome_posicao': posicao,
            'pontuacao': atleta.get('pontuacao_total', 0)
        }

# Salvamento do arquivo de saída em JSON
try: 
    Fd_out = f'selecao_cartola_fc_{ano}.txt'
    with open(Fd_out, 'w', encoding='utf-8') as outfile:
         json.dump(dictCartola, outfile, indent=4, ensure_ascii=False)
         print(f"Arquivo salvo como '{Fd_out}' com sucesso!'.")
except IOError:
    print('ERRO! Houve uma falha na tentativa de salvamento do arquivo JSON')
    exit()

# Exibição no console


    