''' Módulo responsável por inicializar a aplicação. '''

from src.basedados import bd
from src.modelos import FeiraLivre
from flask import Flask, request, jsonify
from sqlalchemy import and_


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
    regiao = request.args.get('regiao')
    distrito = request.args.get('distrito')
    nome = request.args.get('nome')
    bairro = request.args.get('bairro')
    filtros = []
    if regiao is not None:
        filtros.append(FeiraLivre.regiao == regiao)
    if distrito is not None:
        filtros.append(FeiraLivre.distrito == distrito)
    if nome is not None:
        filtros.append(FeiraLivre.nome.like('%' + nome + '%'))
    if bairro is not None:
        filtros.append(FeiraLivre.bairro == bairro)
    if len(filtros) > 0:
        resultado = FeiraLivre.query.filter(and_(*filtros)).all()
    else:
        resultado = FeiraLivre.query.all()
    return jsonify({'feiras': [i.dict for i in resultado]})

if __name__ == '__main__':
    app.run()
