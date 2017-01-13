'''
Módulo responsável por manter/executar os testes unitários e \
funcionais da aplicação.
'''

import unittest
import json
from app import app
from flask import jsonify
from src.basedados import bd
from src.modelos import FeiraLivre


class TestApp(unittest.TestCase):
    ''' Mantém os testes relacionados à aplicação. '''
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        bd.create_all()

    def tearDown(self):
        bd.session.remove()
        bd.drop_all()
        self.app_context.pop()

    def test_buscar1(self):
        '''
        Dada uma feira livre na região 'regiao1'
        Quando o busco por regiao='regiao1'
        Então devo receber um JSON contendo a feira livre na lista de feiras.
        '''
        # Arrange
        regiao = 'regiao1'
        feira_livre = FeiraLivre(regiao)
        bd.session.add(feira_livre)
        bd.session.commit()
        esperado = {'feiras': [{'regiao': regiao}]}
        # Act
        resposta = self.app.get('/busca?regiao=' + regiao)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar2(self):
        '''
        Dada uma feira livre na região 'regiao1'
        Quando o busco por regiao='regiao2'
        Então devo receber um JSON contendo uma lista vazia de feiras.
        '''
        # Arrange
        regiao = 'regiao1'
        outra_regiao = 'regiao2'
        feira_livre = FeiraLivre(regiao)
        bd.session.add(feira_livre)
        bd.session.commit()
        esperado = {'feiras': []}
        # Act
        resposta = self.app.get('/busca?regiao=' + outra_regiao)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar3(self):
        '''
        Dadas duas feiras livres na região 'regiao1'
        Quando o busco por regiao='regiao1'
        Então devo receber um JSON contendo ambas as feiras livres na lista \
        de feiras.
        '''
        # Arrange
        regiao = 'regiao1'
        feira_livre1 = FeiraLivre(regiao)
        feira_livre2 = FeiraLivre(regiao)
        bd.session.add(feira_livre1)
        bd.session.add(feira_livre2)
        bd.session.commit()
        esperado = {'feiras': [{'regiao': regiao}, {'regiao': regiao}]}
        # Act
        resposta = self.app.get('/busca?regiao=' + regiao)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

if __name__ == '__main__':
    unittest.main()
