'''
Módulo responsável por manter/executar os testes unitários e \
funcionais da aplicação.
'''

import unittest
import json
from app import app
from flask import jsonify
from src.basedados import bd
from test.helpers import *


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
        feira_livre = FeiraLivreBuilder().with_regiao(regiao).build()
        persistir(bd, feira_livre)
        esperado = {'feiras': [feira_livre.dict]}
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
        feira_livre = FeiraLivreBuilder().with_regiao(regiao).build()
        persistir(bd, feira_livre)
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
        feira_livre1 = FeiraLivreBuilder().with_regiao(regiao).build()
        feira_livre2 = FeiraLivreBuilder().with_regiao(regiao).build()
        persistir(bd, feira_livre1, feira_livre2)
        esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        resposta = self.app.get('/busca?regiao=' + regiao)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar4(self):
        '''
        Dada uma feira livre no distrito 'distrito1'
        Quando o busco por distrito='distrito1'
        Então devo receber um JSON contendo a feira livre na lista de feiras.
        '''
        # Arrange
        distrito = 'distrito1'
        feira_livre = FeiraLivreBuilder().with_distrito(distrito).build()
        persistir(bd, feira_livre)
        esperado = {'feiras': [feira_livre.dict]}
        # Act
        resposta = self.app.get('/busca?distrito=' + distrito)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar5(self):
        '''
        Dada uma feira livre no distrito 'distrito1'
        Quando o busco por distrito='distrito2'
        Então devo receber um JSON contendo uma lista vazia de feiras.
        '''
        # Arrange
        distrito = 'distrito1'
        outro_distrito = 'distrito2'
        feira_livre = FeiraLivreBuilder().with_distrito(distrito).build()
        persistir(bd, feira_livre)
        esperado = {'feiras': []}
        # Act
        resposta = self.app.get('/busca?distrito=' + outro_distrito)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar6(self):
        '''
        Dadas duas feiras livres no distrito 'distrito1'
        Quando o busco por distrito='distrito1'
        Então devo receber um JSON contendo ambas as feiras livres na lista \
        de feiras.
        '''
        # Arrange
        distrito = 'distrito1'
        feira_livre1 = FeiraLivreBuilder().with_distrito(distrito).build()
        feira_livre2 = FeiraLivreBuilder().with_distrito(distrito).build()
        persistir(bd, feira_livre1, feira_livre2)
        esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        resposta = self.app.get('/busca?distrito=' + distrito)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar7(self):
        '''
        Dadas uma feira livre na região 'regiao1' e no distrito 'distrito1';
              uma feira livre na região 'regiao2' e no distrito 'distrito2' e
              uma feira livre na região 'regiao1' e no distrito 'distrito2'
        Quando o busco por regiao='regiao1'
        Então devo receber um JSON contendo a primeira e a terceira feiras \
        livres (somente) na lista de feiras.
        '''
        # Arrange
        regiao1, regiao2 = 'regiao1', 'regiao2'
        distrito1, distrito2 = 'distrito1', 'distrito2'
        feira_livre1 = FeiraLivreBuilder().with_regiao(regiao1).with_distrito(distrito1).build()
        feira_livre2 = FeiraLivreBuilder().with_regiao(regiao2).with_distrito(distrito2).build()
        feira_livre3 = FeiraLivreBuilder().with_regiao(regiao1).with_distrito(distrito2).build()
        persistir(bd, feira_livre1, feira_livre2, feira_livre3)
        esperado = {'feiras': [feira_livre1.dict, feira_livre3.dict]}
        # Act
        resposta = self.app.get('/busca?regiao=' + regiao1)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar8(self):
        '''
        Dadas uma feira livre na região 'regiao1' e no distrito 'distrito1';
              uma feira livre na região 'regiao2' e no distrito 'distrito2' e
              uma feira livre na região 'regiao1' e no distrito 'distrito2'
        Quando o busco por distrito='distrito2'
        Então devo receber um JSON contendo a segunda e a terceira feiras \
        livres (somente) na lista de feiras.
        '''
        # Arrange
        regiao1, regiao2 = 'regiao1', 'regiao2'
        distrito1, distrito2 = 'distrito1', 'distrito2'
        feira_livre1 = FeiraLivreBuilder().with_regiao(regiao1).with_distrito(distrito1).build()
        feira_livre2 = FeiraLivreBuilder().with_regiao(regiao2).with_distrito(distrito2).build()
        feira_livre3 = FeiraLivreBuilder().with_regiao(regiao1).with_distrito(distrito2).build()
        persistir(bd, feira_livre1, feira_livre2, feira_livre3)
        esperado = {'feiras': [feira_livre2.dict, feira_livre3.dict]}
        # Act
        resposta = self.app.get('/busca?distrito=' + distrito2)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar9(self):
        '''
        Dadas uma feira livre na região 'regiao1' e no distrito 'distrito1';
              uma feira livre na região 'regiao2' e no distrito 'distrito2' e
              uma feira livre na região 'regiao1' e no distrito 'distrito2'
        Quando o busco por regiao='regiao1' e distrito='distrito1'
        Então devo receber um JSON contendo a primeira feira livre (somente) \
        na lista de feiras.
        '''
        # Arrange
        regiao1, regiao2 = 'regiao1', 'regiao2'
        distrito1, distrito2 = 'distrito1', 'distrito2'
        feira_livre1 = FeiraLivreBuilder().with_regiao(regiao1).with_distrito(distrito1).build()
        feira_livre2 = FeiraLivreBuilder().with_regiao(regiao2).with_distrito(distrito2).build()
        feira_livre3 = FeiraLivreBuilder().with_regiao(regiao1).with_distrito(distrito2).build()
        persistir(bd, feira_livre1, feira_livre2, feira_livre3)
        esperado = {'feiras': [feira_livre1.dict]}
        # Act
        resposta = self.app.get('/busca?regiao=' + regiao1 + '&distrito=' + distrito1)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar10(self):
        '''
        Dadas uma feira livre na região 'regiao1' e no distrito 'distrito1' e
              uma feira livre na região 'regiao2' e no distrito 'distrito2'
        Quando busco por nenhum dado em particular
        Então devo receber um JSON contendo todas as feiras livres na lista de \
        feiras.
        '''
        # Arrange
        regiao1, regiao2 = 'regiao1', 'regiao2'
        distrito1, distrito2 = 'distrito1', 'distrito2'
        feira_livre1 = FeiraLivreBuilder().with_regiao(regiao1).with_distrito(distrito1).build()
        feira_livre2 = FeiraLivreBuilder().with_regiao(regiao2).with_distrito(distrito2).build()
        persistir(bd, feira_livre1, feira_livre2)
        esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        resposta = self.app.get('/busca')
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

if __name__ == '__main__':
    unittest.main()
