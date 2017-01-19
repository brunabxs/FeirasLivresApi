''' Módulo responsável por inicializar a aplicação. '''

import re
from src.basedados import bd
from src.excecoes import ViolacaoIndiceUnico
from src.modelos import buscar_ou_criar
from src.modelos import FeiraLivre, Endereco, Logradouro, Bairro
from src.modelos import Regiao8, Regiao5, Distrito, Subprefeitura
from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
bd.init_app(app)


@app.route('/feira', methods=['POST'])
def adicionar():
    '''
    Insere uma feira livre.

    Retorno
    =======
    str -- json contendo a feira inserida ou mensagem de erro.
    '''
    json = request.get_json(force=True)
    resposta = None
    campos_obrigatorios = verificar_campos_obrigatorios(json)
    if len(campos_obrigatorios) > 0:
        resposta = jsonify({'mensagem': 'Campo(s) obrigatório(s) não '
                                        'encontrado(s): {0}.'
                                        .format(', '.join(campos_obrigatorios)),
                            'erro': 400})
        resposta.status_code = 400
        return resposta
    feira_livre = FeiraLivre.query.filter_by(registro=json['registro']).first()
    if feira_livre is not None:
        resposta = jsonify({'mensagem': 'Feira livre com registro {0} '
                                        'já existe.'.format(json['registro']),
                            'erro': 400})
        resposta.status_code = 400
        return resposta
    try:
        feira_livre = criar_ou_atualizar(json)
        resposta = jsonify({'feira': feira_livre.dict})
        resposta.status_code = 200
    except ViolacaoIndiceUnico as erro:
        resposta = jsonify({'mensagem': str(erro), 'erro': 400})
        resposta.status_code = 400
    return resposta


@app.route('/feira', methods=['PUT'])
def alterar():
    '''
    Altera as informações de uma feira livre dado seu registro.

    Retorno
    =======
    str -- json contendo a feira atualizada ou mensagem de erro.
    '''
    json = request.get_json(force=True)
    resposta = None
    campos_obrigatorios = verificar_campos_obrigatorios(json)
    if len(campos_obrigatorios) > 0:
        resposta = jsonify({'mensagem': 'Campo(s) obrigatório(s) não '
                                        'encontrado(s): {0}.'
                                        .format(', '.join(campos_obrigatorios)),
                            'erro': 400})
        resposta.status_code = 400
        return resposta
    feira_livre = FeiraLivre.query.filter_by(registro=json['registro']).first()
    if feira_livre is None:
        resposta = jsonify({'mensagem': 'Feira livre com registro {0} '
                                        'não existe.'.format(json['registro']),
                            'erro': 404})
        resposta.status_code = 404
        return resposta
    try:
        feira_livre = criar_ou_atualizar(json, feira_livre)
        resposta = jsonify({'feira': feira_livre.dict})
        resposta.status_code = 200
    except ViolacaoIndiceUnico as erro:
        resposta = jsonify({'mensagem': str(erro), 'erro': 400})
        resposta.status_code = 400
    return resposta


@app.route('/feira', methods=['DELETE'])
def remover():
    '''
    Remove uma feira livre dado seu registro.
    Se a feira não existir na base de dados, retorna código 404.

    Retorno
    =======
    str -- json contendo a feira removida ou mensagem de erro.
    '''
    registro = request.args.get('registro')
    feira_livre = FeiraLivre.query.filter(FeiraLivre.registro == registro) \
                                  .first()
    if feira_livre is None:
        resposta = jsonify({'mensagem': 'Feira livre com registro {0} '
                                        'não existe.'.format(registro),
                            'erro': 404})
        resposta.status_code = 404
    else:
        bd.session.delete(feira_livre)
        bd.session.commit()
        resposta = jsonify({'feira': feira_livre.dict})
        resposta.status_code = 200
    return resposta


@app.route('/feiras', methods=['GET'])
def buscar():
    '''
    Busca feira(s) livre(s) por região e/ou distrito e/ou bairro e/ou nome.

    Retorno
    =======
    str -- json contendo o resultado da busca.
    '''
    regiao5 = request.args.get('regiao5')
    distrito = request.args.get('distrito')
    bairro = request.args.get('bairro')
    nome = request.args.get('nome')
    consulta = criar_consulta_busca(regiao5, distrito, bairro, nome)
    resultado = consulta.all()
    return jsonify({'feiras': [i.dict for i in resultado]})


def criar_ou_atualizar(json, feira_livre=None):
    '''
    Cria uma feira livre a partir do json ou atualiza utilizando esses dados.

    Parâmetros
    ==========
    json [Dict] -- json contendo as informações da feira livre.

    Retorno
    =======
    FeiraLivre -- feira livre criada/alterada.

    Exceções/Erros
    ==============
    ViolacaoIndiceUnico
    '''
    try:
        subprefeitura = buscar_ou_criar(bd.session, Subprefeitura,
                                        codigo=json['cod_subpref'],
                                        nome=json['subprefeitura'])
        distrito = buscar_ou_criar(bd.session, Distrito,
                                   codigo=json['cod_distrito'],
                                   nome=json['distrito'],
                                   subprefeitura_id=subprefeitura.id)
        regiao5 = buscar_ou_criar(bd.session, Regiao5,
                                  nome=json['regiao5'])
        regiao8 = buscar_ou_criar(bd.session, Regiao8,
                                  nome=json['regiao8'])
        bairro = buscar_ou_criar(bd.session, Bairro,
                                 nome=json['bairro'],
                                 distrito_id=distrito.id)
        logradouro = buscar_ou_criar(bd.session, Logradouro,
                                     nome=json['logradouro'])
        endereco = buscar_ou_criar(bd.session, Endereco,
                                   logradouro_id=logradouro.id,
                                   numero=json['numero'],
                                   referencia=json['referencia'],
                                   bairro_id=bairro.id,
                                   regiao5_id=regiao5.id,
                                   regiao8_id=regiao8.id,
                                   latitude=json['latitude'],
                                   longitude=json['longitude'],
                                   setor_censitario=json['setor_censitario'],
                                   area_ponderacao=json['area_ponderacao'])
        if feira_livre is None:
            feira_livre = buscar_ou_criar(bd.session, FeiraLivre,
                                          identificador=json['identificador'],
                                          nome=json['nome'],
                                          registro=json['registro'],
                                          endereco_id=endereco.id)
        else:
            feira_livre.identificador = json['identificador']
            feira_livre.nome = json['nome']
            feira_livre.endereco = endereco
        bd.session.commit()
        return feira_livre
    except ViolacaoIndiceUnico as erro:
        bd.session.rollback()
        raise erro
    except Exception as e:
        bd.session.rollback()
        raise e


def verificar_campos_obrigatorios(json):
    '''
    Verifica se existem campos obrigatórios que não estão presentes no json.
    Caso existam campos faltando, retorna quais são esses campos.
    Se não existem campos faltando no json, retorna uma lista vazia.

    Parâmetros
    ==========
    json [Dict] -- json a ser verificado.

    Retorno
    =======
    List -- campos obrigatórios no json que não estão presentes no json.
    '''
    campos_obrigatorios = {'cod_subpref', 'subprefeitura', 'cod_distrito',
                           'distrito', 'regiao5', 'regiao8', 'bairro',
                           'logradouro', 'numero', 'referencia', 'latitude',
                           'longitude', 'setor_censitario', 'area_ponderacao',
                           'identificador', 'nome', 'registro'}
    campos_nao_existentes = campos_obrigatorios.difference(json.keys())
    campos_nao_existentes = list(campos_nao_existentes)
    campos_nao_existentes.sort()
    return campos_nao_existentes


def identificar_entidade_colunas(mensagem):
    '''
    Identifica qual a entidade (e suas colunas) que gerou um erro de \
    índice único.

    Parâmetros
    ==========
    mensagem [str] -- mensagem de erro de índice único.

    Retorno
    =======
    Tuple(str, Tuple) -- contém a entidade e as colunas respectivamente.
    '''
    resultado = re.findall('[^.]*:? ([^.]*).([a-z0-9A-Z_][a-z0-9A-Z_]*),?', mensagem)
    colunas = list()
    for entidade, coluna in resultado:
        colunas.append(coluna)
    return (entidade, tuple(colunas))


def criar_consulta_busca(regiao5, distrito, bairro, nome):
    '''
    Cria a consulta a ser utilizada na busca de feiras livres.

    Parâmetros
    ==========
    regiao5 [str] -- regiao5 da localização da feira livre.
    distrito [str] -- distrito da localização da feira livre.
    bairro [str] -- bairro da localização da feira livre.
    nome [str] -- nome da feira livre.

    Retorno
    =======
    Query -- consulta a ser executada para encontrar feiras livres.
    '''
    filtros = list()
    relacoes = list()
    if nome is not None:
        filtros.append(FeiraLivre.nome.like('%' + nome + '%'))
    if regiao5 is not None:
        relacoes.append(FeiraLivre.endereco)
        relacoes.append(Endereco.regiao5)
        filtros.append(Regiao5.nome == regiao5)
    if distrito is not None:
        relacoes.append(FeiraLivre.endereco)
        relacoes.append(Endereco.bairro)
        relacoes.append(Bairro.distrito)
        filtros.append(Distrito.nome == distrito)
    if bairro is not None:
        relacoes.append(FeiraLivre.endereco)
        relacoes.append(Endereco.bairro)
        filtros.append(Bairro.nome == bairro)
    consulta = FeiraLivre.query
    # Adiciona na consulta relações únicas
    relacoes_utilizadas = set()
    for relacao in relacoes:
        if relacao not in relacoes_utilizadas:
            consulta = consulta.join(relacao)
            relacoes_utilizadas.add(relacao)
    # Adiciona os filtros à consulta
    for filtro in filtros:
        consulta = consulta.filter(*filtros)
    return consulta


if __name__ == '__main__':
    app.run()
