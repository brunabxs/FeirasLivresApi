''' Módulo responsável por inicializar a aplicação. '''

from src.basedados import bd
from src.modelos import FeiraLivre
from flask import Flask, request, jsonify


app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
bd.init_app(app)


@app.route('/busca')
def buscar():
    '''
    Busca feira(s) livre(s) por região.

    Argumentos
    ==========
    regiao [str] -- região à qual deve pertencer a feira.

    Retorno
    =======
    str -- json contendo o resultado da busca.
    '''
    regiao = request.args.get('regiao')
    resultado = FeiraLivre.query.filter_by(regiao=regiao).all()
    return jsonify({'feiras': [i.dict for i in resultado]})

if __name__ == '__main__':
    app.run()
