''' Módulo responsável por inicializar a aplicação. '''

from src.basedados import bd
from src.modelos import FeiraLivre
from flask import Flask, request, jsonify
from sqlalchemy import and_


app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
bd.init_app(app)


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
