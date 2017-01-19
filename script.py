''' Módulo responsável pelo script de importação do arquivo csv. '''

import argparse
import csv
from app import app
from src.basedados import bd
from src.modelos import buscar_ou_criar
from src.modelos import FeiraLivre, Endereco, Logradouro, Bairro
from src.modelos import Regiao8, Regiao5, Distrito, Subprefeitura


def criar_entidades(caminho_arquivo_csv):
    ''' Cria as entidades a partir dos dados do arquivo csv

    Parâmetros
    ==========
    caminho_arquivo_csv [str] -- caminho para o arquivo csv
    '''
    arquivo = open(caminho_arquivo_csv, 'r')
    leitor = csv.DictReader(arquivo, delimiter=',')
    for linha in leitor:
        subprefeitura = buscar_ou_criar(bd.session, Subprefeitura,
                                        codigo=linha['CODSUBPREF'],
                                        nome=linha['SUBPREFE'])
        distrito = buscar_ou_criar(bd.session, Distrito,
                                   codigo=linha['CODDIST'],
                                   nome=linha['DISTRITO'],
                                   subprefeitura=subprefeitura)
        regiao5 = buscar_ou_criar(bd.session, Regiao5,
                                  nome=linha['REGIAO5'])
        regiao8 = buscar_ou_criar(bd.session, Regiao8,
                                  nome=linha['REGIAO8'])
        bairro = buscar_ou_criar(bd.session, Bairro,
                                 nome=linha['BAIRRO'],
                                 distrito=distrito)
        logradouro = buscar_ou_criar(bd.session, Logradouro,
                                     nome=linha['LOGRADOURO'])
        endereco = buscar_ou_criar(bd.session, Endereco,
                                   logradouro=logradouro,
                                   numero=linha['NUMERO'],
                                   referencia=linha['REFERENCIA'],
                                   bairro=bairro,
                                   regiao5=regiao5,
                                   regiao8=regiao8,
                                   latitude=linha['LAT'],
                                   longitude=linha['LONG'],
                                   setor_censitario=linha['SETCENS'],
                                   area_ponderacao=linha['AREAP'])
        feira_livre = buscar_ou_criar(bd.session, FeiraLivre,
                                      identificador=linha['ID'],
                                      nome=linha['NOME_FEIRA'],
                                      registro=linha['REGISTRO'],
                                      endereco=endereco)
        bd.session.commit()


def importar(arquivo_csv, conf):
    ''' Cria a base de dados e importa os dados do arquivo csv

    Parâmetros
    ==========
    csv [str] -- caminho para o arquivo csv.
    arquivo_csv [str] -- tipo de configuração.
    '''
    if conf == 'prod':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.TestingConfig')
    contexto = app.app_context()
    contexto.push()
    bd.drop_all()
    bd.create_all()
    criar_entidades(arquivo_csv)
    bd.session.remove()
    contexto.pop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cria a base de dados e '
                                                 'importa os dados do arquivo'
                                                 'csv.')
    parser.add_argument('--csv', required=True, type=str,
                        help='Caminho para o arquivo csv')
    parser.add_argument('--conf', default='prod', type=str,
                        choices=['prod', 'test'],
                        help='Tipo de configuração')
    args = parser.parse_args()

    importar(args.csv, args.conf)
