
import requests
import sys
import datetime
import json
import os
import matplotlib.pyplot as plt

# Função para obter as moedas disponíveis na API do Banco Central
def obter_moedas():
    strURL = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$top=100&$format=json'
    try:
        resposta = requests.get(strURL).json()
        codigomoeda = [moeda['simbolo'] for moeda in resposta['value']]
        nomemoeda = [nome['nomeFormatado'] for nome in resposta['value']]
        anoatual = datetime.date.today().year
        return codigomoeda, nomemoeda, anoatual
    except requests.exceptions.RequestException as e:
        sys.exit(f'ERRO! Falha na requisição das moedas!: {e}')
    except KeyError:
        sys.exit('ERRO! Falha no acesso das chaves de dictMoedas!')
    except Exception as e:
        sys.exit(f'ERRO! Falha inesperada no programa!: {e}')


def solicitar_dados(codigomoeda, nomemoeda, anoatual):
    while True:
        print('=-'*100)
        print('Moedas disponíveis para escolha: ')
        print('=-'*100)
        for i in range(len(codigomoeda)):
            print(f'{codigomoeda[i]} - {nomemoeda[i]}')
        print('ATENÇÃO! Para encerrar o programa, apenas digite 0')

        moeda = input('Por favor, digite a sigla da moeda desejada: ').upper()
        if moeda == '0':
            return None, None  # Indica que o usuário deseja sair
        if moeda not in codigomoeda or len(moeda) > 3:
            print('ERRO! Moeda não validada pelo programa!')
            continue

        try:
            ano = int(input(f'Informe o ano desejado (até {anoatual}): '))
            if ano <= anoatual:
                return moeda, ano
            else:
                print(f'ERRO! O ano {ano} é superior ao ano atual!')
        except ValueError:
            print('ERRO! O valor apresentado não é válido, tente novamente!')

def obter_cotacoes(moeda, ano):
    strURL = f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?'
    strURL += f'@moeda=%27{moeda}%27&@dataInicial=%2701-01-{ano}%27&@dataFinalCotacao=%2712-31-{ano}%27&$format=json'

    try:
        dictCotacoes = requests.get(strURL).json()
        return dictCotacoes['value']
    except requests.exceptions.RequestException as e:
        sys.exit(f'ERRO! Houve falha ao tentar obter as cotações: {e}')
    except KeyError:
        sys.exit('ERRO! Houve falha no acesso às chaves de dictCotacoes!')
    except Exception as e:
        sys.exit(f'ERRO! Houve uma falha inesperada no programa!{e}')

def calcular_medias(dictCotacoes):
    medias = {}
    for cotacao in dictCotacoes:
        data = cotacao['dataHoraCotacao'].split('T')[0]
        mes = data[5:7]
        if mes not in medias:
            medias[mes] = {'mediaCompra': [], 'mediaVenda': []}
        if cotacao['cotacaoCompra'] is not None and cotacao['cotacaoVenda'] is not None:
            medias[mes]['mediaCompra'].append(cotacao['cotacaoCompra'])
            medias[mes]['mediaVenda'].append(cotacao['cotacaoVenda'])

    medias_calculadas = {}
    for mes in medias:
        if medias[mes]['mediaCompra'] and medias[mes]['mediaVenda']:
            mediaCompra = sum(medias[mes]['mediaCompra']) / len(medias[mes]['mediaCompra'])
            mediaVenda = sum(medias[mes]['mediaVenda']) / len(medias[mes]['mediaVenda'])
            medias_calculadas[mes] = {'mediaCompra': round(mediaCompra, 5), 'mediaVenda': round(mediaVenda, 5)}

    return medias_calculadas

def salvar_arquivos(moeda, ano, medias_calculadas):
    nome_arquivo_json = f'medias_cotacoes_{moeda}_{ano}.json'
    nome_arquivo_csv = f'medias_cotacoes_{moeda}_{ano}.csv'

    if os.path.exists(nome_arquivo_json):
        print(f'O arquivo {nome_arquivo_json} já existe e será sobrescrito.')
    if os.path.exists(nome_arquivo_csv):
        print(f'O arquivo {nome_arquivo_csv} já existe e será sobrescrito.')

    try:
        with open(nome_arquivo_json, 'w') as json_file:
            json.dump(medias_calculadas, json_file, indent=4)
    except IOError as e:
        sys.exit(f'ERRO! Falha ao tentar salvar o arquivo JSON: {e}')

    try:
        with open(nome_arquivo_csv, 'w') as csv_file:
            csv_file.write('moeda;mes;mediaCompra;mediaVenda\n')
            for mes in medias_calculadas:
                csv_file.write(f'{moeda};{mes};{medias_calculadas[mes]["mediaCompra"]};{medias_calculadas[mes]["mediaVenda"]}\n')
        print('Processo encerrado com sucesso!')
    except IOError as e:
        sys.exit(f'ERRO! Falha ao tentar salvar o arquivo CSV: {e}')


def gerar_grafico(moeda, ano, medias_calculadas):
    meses = sorted(medias_calculadas.keys())
    mediaCompra = [medias_calculadas[mes]['mediaCompra'] for mes in meses]
    mediaVenda = [medias_calculadas[mes]['mediaVenda'] for mes in meses]

    plt.figure(figsize=(20, 10))
    plt.plot(meses, mediaCompra, label='Média Compra', marker='o')
    plt.plot(meses, mediaVenda, label='Média Venda', marker='o')
    plt.title(f'Média Cotações {moeda} - Ano {ano}')
    plt.xlabel('Mês')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    codigomoeda, nomemoeda, anoatual = obter_moedas()
    while True:
        moeda, ano = solicitar_dados(codigomoeda, nomemoeda, anoatual)
        if moeda is None:  # Verifica se o usuário deseja sair
            print('PROGRAMA ENCERRADO!')
            break
        
        dictCotacoes = obter_cotacoes(moeda, ano)

        if dictCotacoes:
            medias_calculadas = calcular_medias(dictCotacoes)
            salvar_arquivos(moeda, ano, medias_calculadas)
            gerar_grafico(moeda, ano, medias_calculadas)
        else:
            print(f'Não foi possível encontrar cotações para {moeda} no ano {ano}.')

if __name__ == "__main__":
    main()

# Aaron Goldberg - 20241014050033
# Jordan Julio - 20241014050014
