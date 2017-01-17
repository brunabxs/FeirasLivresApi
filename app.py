''' Módulo responsável por inicializar a aplicação. '''

from src.basedados import bd
from src.modelos import FeiraLivre, Endereco, Regiao5, Bairro, Distrito
from flask import Flask, request, jsonify


app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
bd.init_app(app)


@app.route('/feiras', methods=['DELETE'])
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
        resposta = jsonify({'mensagem': 'Feira livre com registro {0} não existe.'
                                        .format(registro),
                            'erro': 404})
        resposta.status_code = 404
    else:
        bd.session.delete(feira_livre)
        bd.session.commit()
        resposta = jsonify({'feira': feira_livre.dict})
        resposta.status_code = 200
    return resposta


@app.route('/busca')
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