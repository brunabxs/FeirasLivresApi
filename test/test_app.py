'''
Módulo responsável por manter/executar os testes unitários e \
funcionais da aplicação.
'''

import unittest
import json
from app import app
from src.basedados import bd
from test.helpers import *


class TestApp(unittest.TestCase):
    ''' Mantém os testes relacionados à aplicação. '''
    COD1, COD2 = 'cod1', 'cod2'
    IDENTIFICADOR1, IDENTIFICADOR2 = 1, 2
    REGISTRO1, REGISTRO2, REGISTRO3 = '123', '456', '789'
    REGIAO1, REGIAO2 = 'regiao1', 'regiao2'
    DISTRITO1, DISTRITO2 = 'distrito1', 'distrito2'
    BAIRRO1, BAIRRO2 = 'bairro1', 'bairro2'
    NOME1, NOME2, NOME3 = 'nome1', 'nome1a', 'nome2'

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
        Quando o busco por regiao5='regiao1'
        Então devo receber um JSON contendo a feira livre na lista de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_regiao5(self.REGIAO1).build()
        esperado = {'feiras': [feira_livre.dict]}
        # Act
        resposta = self.app.get('/busca?regiao5=' + self.REGIAO1)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar2(self):
        '''
        Dada uma feira livre na região 'regiao1'
        Quando o busco por regiao5='regiao2'
        Então devo receber um JSON contendo uma lista vazia de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_regiao5(self.REGIAO1).build()
        esperado = {'feiras': []}
        # Act
        resposta = self.app.get('/busca?regiao5=' + self.REGIAO2)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar3(self):
        '''
        Dadas duas feiras livres na região 'regiao1'
        Quando o busco por regiao5='regiao1'
        Então devo receber um JSON contendo ambas as feiras livres na lista \
        de feiras.
        '''
        # Arrange
        feira_livre1 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                            .with_regiao5(self.REGIAO1) \
                                            .build()
        feira_livre2 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO2) \
                                            .with_regiao5(self.REGIAO1) \
                                            .build()
        esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        resposta = self.app.get('/busca?regiao5=' + self.REGIAO1)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar4(self):
        '''
        Dada uma feira livre no distrito 'distrito1'
        Quando o busco por distrito='distrito1'
        Então devo receber um JSON contendo a feira livre na lista de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_cod_distrito(self.COD1) \
                                           .with_distrito(self.DISTRITO1) \
                                           .build()
        esperado = {'feiras': [feira_livre.dict]}
        # Act
        resposta = self.app.get('/busca?distrito=' + self.DISTRITO1)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar5(self):
        '''
        Dada uma feira livre no distrito 'distrito1'
        Quando o busco por distrito='distrito2'
        Então devo receber um JSON contendo uma lista vazia de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_cod_distrito(self.COD1) \
                                           .with_distrito(self.DISTRITO1) \
                                           .build()
        esperado = {'feiras': []}
        # Act
        resposta = self.app.get('/busca?distrito=' + self.DISTRITO2)
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
        feira_livre1 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                            .with_cod_distrito(self.COD1) \
                                            .with_distrito(self.DISTRITO1) \
                                            .build()
        feira_livre2 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO2) \
                                            .with_cod_distrito(self.COD1) \
                                            .with_distrito(self.DISTRITO1) \
                                            .build()
        esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        resposta = self.app.get('/busca?distrito=' + self.DISTRITO1)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar7(self):
        '''
        Dada uma feira livre com nome 'nome1'
        Quando o busco por nome='nome1'
        Então devo receber um JSON contendo a feira livre na lista de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_nome(self.NOME1).build()
        esperado = {'feiras': [feira_livre.dict]}
        # Act
        resposta = self.app.get('/busca?nome=' + self.NOME1)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar8(self):
        '''
        Dada uma feira livre com nome 'nome1'
        Quando o busco por nome='nome2'
        Então devo receber um JSON contendo uma lista vazia de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_nome(self.NOME1).build()
        esperado = {'feiras': []}
        # Act
        resposta = self.app.get('/busca?nome=' + self.NOME2)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar9(self):
        '''
        Dadas duas feiras livres com nome 'nome1'
        Quando o busco por nome='nome1'
        Então devo receber um JSON contendo ambas as feiras livres na lista \
        de feiras.
        '''
        # Arrange
        feira_livre1 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                            .with_nome(self.NOME1) \
                                            .build()
        feira_livre2 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO2) \
                                            .with_nome(self.NOME1) \
                                            .build()
        esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        resposta = self.app.get('/busca?nome=' + self.NOME1)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar10(self):
        '''
        Dadas uma feira livre com nome 'nome1' e
              uma feira livre com nome 'nome1a'
        Quando o busco por nome='nome1'
        Então devo receber um JSON contendo ambas as feiras livres na lista \
        de feiras.
        '''
        # Arrange
        feira_livre1 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                            .with_nome(self.NOME1) \
                                            .build()
        feira_livre2 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO2) \
                                            .with_nome(self.NOME2) \
                                            .build()
        esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        resposta = self.app.get('/busca?nome=' + self.NOME1)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar11(self):
        '''
        Dada uma feira livre no bairro 'bairro1'
        Quando o busco por bairro='bairro1'
        Então devo receber um JSON contendo a feira livre na lista de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_bairro(self.BAIRRO1).build()
        esperado = {'feiras': [feira_livre.dict]}
        # Act
        resposta = self.app.get('/busca?bairro=' + self.BAIRRO1)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar12(self):
        '''
        Dada uma feira livre no bairro 'bairro1'
        Quando o busco por bairro='bairro2'
        Então devo receber um JSON contendo uma lista vazia de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_bairro(self.BAIRRO1).build()
        esperado = {'feiras': []}
        # Act
        resposta = self.app.get('/busca?bairro=' + self.BAIRRO2)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar13(self):
        '''
        Dadas duas feiras livres no bairro 'bairro1'
        Quando o busco por bairro='bairro1'
        Então devo receber um JSON contendo ambas as feiras livres na lista \
        de feiras.
        '''
        # Arrange
        feira_livre1 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                            .with_bairro(self.BAIRRO1) \
                                            .build()
        feira_livre2 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO2) \
                                            .with_bairro(self.BAIRRO1) \
                                            .build()
        esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        resposta = self.app.get('/busca?bairro=' + self.BAIRRO1)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar20(self):
        '''
        Dadas uma feira livre na região 'regiao1', no distrito 'distrito1', \
        no bairro 'bairro1' e nome 'nome1';
              uma feira livre na região 'regiao2', no distrito 'distrito2', \
        no bairro 'bairro2' e nome 'nome1a' e
              uma feira livre na região 'regiao1', no distrito 'distrito2', \
        no bairro 'bairro2' e nome 'nome2'
        Quando o busco por regiao5='regiao1'
        Então devo receber um JSON contendo a primeira e a terceira feiras \
        livres (somente) na lista de feiras.
        '''
        # Arrange
        feira_livre1 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                            .with_regiao5(self.REGIAO1) \
                                            .with_cod_distrito(self.COD1) \
                                            .with_distrito(self.DISTRITO1) \
                                            .with_bairro(self.BAIRRO1) \
                                            .with_nome(self.NOME1) \
                                            .build()
        feira_livre2 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO2) \
                                            .with_regiao5(self.REGIAO2) \
                                            .with_cod_distrito(self.COD2) \
                                            .with_distrito(self.DISTRITO2) \
                                            .with_bairro(self.BAIRRO2) \
                                            .with_nome(self.NOME2) \
                                            .build()
        feira_livre3 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO3) \
                                            .with_regiao5(self.REGIAO1) \
                                            .with_cod_distrito(self.COD2) \
                                            .with_distrito(self.DISTRITO2) \
                                            .with_bairro(self.BAIRRO2) \
                                            .with_nome(self.NOME3) \
                                            .build()
        esperado = {'feiras': [feira_livre1.dict, feira_livre3.dict]}
        # Act
        resposta = self.app.get('/busca?regiao5=' + self.REGIAO1)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar21(self):
        '''
        Dadas uma feira livre na região 'regiao1', no distrito 'distrito1', \
        no bairro 'bairro1' e nome 'nome1';
              uma feira livre na região 'regiao2', no distrito 'distrito2', \
        no bairro 'bairro2' e nome 'nome1a' e
              uma feira livre na região 'regiao1', no distrito 'distrito2', \
        no bairro 'bairro2' e nome 'nome2'
        Quando o busco por distrito='distrito2'
        Então devo receber um JSON contendo a segunda e a terceira feiras \
        livres (somente) na lista de feiras.
        '''
        # Arrange
        feira_livre1 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                            .with_regiao5(self.REGIAO1) \
                                            .with_cod_distrito(self.COD1) \
                                            .with_distrito(self.DISTRITO1) \
                                            .with_bairro(self.BAIRRO1) \
                                            .with_nome(self.NOME1) \
                                            .build()
        feira_livre2 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO2) \
                                            .with_regiao5(self.REGIAO2) \
                                            .with_cod_distrito(self.COD2) \
                                            .with_distrito(self.DISTRITO2) \
                                            .with_bairro(self.BAIRRO2) \
                                            .with_nome(self.NOME2) \
                                            .build()
        feira_livre3 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO3) \
                                            .with_regiao5(self.REGIAO1) \
                                            .with_cod_distrito(self.COD2) \
                                            .with_distrito(self.DISTRITO2) \
                                            .with_bairro(self.BAIRRO2) \
                                            .with_nome(self.NOME3) \
                                            .build()
        esperado = {'feiras': [feira_livre2.dict, feira_livre3.dict]}
        # Act
        resposta = self.app.get('/busca?distrito=' + self.DISTRITO2)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar22(self):
        '''
        Dadas uma feira livre na região 'regiao1', no distrito 'distrito1', \
        no bairro 'bairro1' e nome 'nome1';
              uma feira livre na região 'regiao2', no distrito 'distrito2', \
        no bairro 'bairro2' e nome 'nome1a' e
              uma feira livre na região 'regiao1', no distrito 'distrito2', \
        no bairro 'bairro2' e nome 'nome2'
        Quando o busco por nome='nome1'
        Então devo receber um JSON contendo a primeira e a segunda feiras \
        livres (somente) na lista de feiras.
        '''
        # Arrange
        feira_livre1 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                            .with_regiao5(self.REGIAO1) \
                                            .with_cod_distrito(self.COD1) \
                                            .with_distrito(self.DISTRITO1) \
                                            .with_bairro(self.BAIRRO1) \
                                            .with_nome(self.NOME1) \
                                            .build()
        feira_livre2 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO2) \
                                            .with_regiao5(self.REGIAO2) \
                                            .with_cod_distrito(self.COD2) \
                                            .with_distrito(self.DISTRITO2) \
                                            .with_bairro(self.BAIRRO2) \
                                            .with_nome(self.NOME2) \
                                            .build()
        feira_livre3 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO3) \
                                            .with_regiao5(self.REGIAO1) \
                                            .with_cod_distrito(self.COD2) \
                                            .with_distrito(self.DISTRITO2) \
                                            .with_bairro(self.BAIRRO2) \
                                            .with_nome(self.NOME3) \
                                            .build()
        esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        resposta = self.app.get('/busca?nome=' + self.NOME1)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar23(self):
        '''
        Dadas uma feira livre na região 'regiao1', no distrito 'distrito1', \
        no bairro 'bairro1' e nome 'nome1';
              uma feira livre na região 'regiao2', no distrito 'distrito2', \
        no bairro 'bairro2' e nome 'nome1a' e
              uma feira livre na região 'regiao1', no distrito 'distrito2', \
        no bairro 'bairro2' e nome 'nome2'
        Quando o busco por bairro='bairro2'
        Então devo receber um JSON contendo a segunda e a terceira feiras \
        livres (somente) na lista de feiras.
        '''
        # Arrange
        feira_livre1 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                            .with_regiao5(self.REGIAO1) \
                                            .with_cod_distrito(self.COD1) \
                                            .with_distrito(self.DISTRITO1) \
                                            .with_bairro(self.BAIRRO1) \
                                            .with_nome(self.NOME1) \
                                            .build()
        feira_livre2 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO2) \
                                            .with_regiao5(self.REGIAO2) \
                                            .with_cod_distrito(self.COD2) \
                                            .with_distrito(self.DISTRITO2) \
                                            .with_bairro(self.BAIRRO2) \
                                            .with_nome(self.NOME2) \
                                            .build()
        feira_livre3 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO3) \
                                            .with_regiao5(self.REGIAO1) \
                                            .with_cod_distrito(self.COD2) \
                                            .with_distrito(self.DISTRITO2) \
                                            .with_bairro(self.BAIRRO2) \
                                            .with_nome(self.NOME3) \
                                            .build()
        esperado = {'feiras': [feira_livre2.dict, feira_livre3.dict]}
        # Act
        resposta = self.app.get('/busca?bairro=' + self.BAIRRO2)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar30(self):
        '''
        Dadas uma feira livre na região 'regiao1', no distrito 'distrito1', \
        no bairro 'bairro1' e nome 'nome1';
              uma feira livre na região 'regiao2', no distrito 'distrito2', \
        no bairro 'bairro2' e nome 'nome1a' e
              uma feira livre na região 'regiao1', no distrito 'distrito2', \
        no bairro 'bairro2' e nome 'nome2'
        Quando o busco por regiao5='regiao2' e distrito='distrito2' e \
        bairro='bairro2' e nome='nome1'
        Então devo receber um JSON contendo a segunda feira livre (somente) \
        na lista de feiras.
        '''
        # Arrange
        feira_livre1 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                            .with_regiao5(self.REGIAO1) \
                                            .with_cod_distrito(self.COD1) \
                                            .with_distrito(self.DISTRITO1) \
                                            .with_bairro(self.BAIRRO1) \
                                            .with_nome(self.NOME1) \
                                            .build()
        feira_livre2 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO2) \
                                            .with_regiao5(self.REGIAO2) \
                                            .with_cod_distrito(self.COD2) \
                                            .with_distrito(self.DISTRITO2) \
                                            .with_bairro(self.BAIRRO2) \
                                            .with_nome(self.NOME2) \
                                            .build()
        feira_livre3 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO3) \
                                            .with_regiao5(self.REGIAO1) \
                                            .with_cod_distrito(self.COD2) \
                                            .with_distrito(self.DISTRITO2) \
                                            .with_bairro(self.BAIRRO2) \
                                            .with_nome(self.NOME3) \
                                            .build()
        esperado = {'feiras': [feira_livre2.dict]}
        # Act
        resposta = self.app.get('/busca?regiao5=' + self.REGIAO2 +
                                '&distrito=' + self.DISTRITO2 +
                                '&bairro=' + self.BAIRRO2 +
                                '&nome=' + self.NOME1)
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_buscar31(self):
        '''
        Dadas duas feiras livres
        Quando busco por nenhum dado em particular
        Então devo receber um JSON contendo todas as feiras livres na \
        lista de feiras.
        '''
        # Arrange
        feira_livre1 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                            .build()
        feira_livre2 = FeiraLivreBuilder(bd).with_registro(self.REGISTRO2) \
                                            .build()
        esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        resposta = self.app.get('/busca')
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)

    def test_remover1(self):
        '''
        Dada uma feira livre com registro '123'
        Quando removo a feira com registro '123'
        Então a feira deve ser removida;
              devo receber um JSON contendo a feira livre removida.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                           .build()
        esperado = {'feira': feira_livre.dict}
        # Act
        resposta = self.app.delete('/feiras?registro=' + self.REGISTRO1)
        feira_livre = FeiraLivre.query \
                                .filter(FeiraLivre.registro == self.REGISTRO1)\
                                .first()
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)
        self.assertEqual(resposta.status_code, 200)
        self.assertIsNone(feira_livre)

    def test_remover2(self):
        '''
        Dada uma feira livre com registro '123'
        Quando removo a feira com registro '456'
        Então a feira não deve ser removida;
              devo receber um JSON contendo a mensagem de erro.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                           .build()
        esperado = {'mensagem': 'Feira livre com registro {0} não existe.'
                                .format(self.REGISTRO2),
                    'erro': 404}
        # Act
        resposta = self.app.delete('/feiras?registro=' + self.REGISTRO2)
        feira_livre = FeiraLivre.query \
                                .filter(FeiraLivre.registro == self.REGISTRO1)\
                                .first()
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)
        self.assertEqual(resposta.status_code, 404)
        self.assertIsNotNone(feira_livre)


if __name__ == '__main__':
    unittest.main()
