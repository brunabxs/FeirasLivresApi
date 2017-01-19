'''
Módulo responsável por manter/executar os testes unitários e \
funcionais da aplicação.
'''

import unittest
import unittest.mock as mock
import json
from app import app, verificar_campos_obrigatorios, identificar_entidade_colunas
from src.basedados import bd
from test.helpers import *


class TestVerificarCamposObrigatorios(unittest.TestCase):
    ''' Mantém os testes unitários relacionados à função \
    verificar_campos_obrigatorios. '''

    def test_todos_presentes(self):
        '''
        Dado um json contendo todos os campos obrigatórios \
        presentes
        Quando o verifico se todos estão presentes
        Então devo receber uma lista vazia.
        '''
        # Arrange
        json = {
            'identificador': 1,
            'latitude': -123,
            'longitude': 456,
            'setor_censitario': 'setor',
            'area_ponderacao': 'area',
            'cod_distrito': 'coddist',
            'distrito': 'dist',
            'cod_subpref': 'codsubpref',
            'subprefeitura': 'subpref',
            'regiao5': 'reg',
            'regiao8': 'reg2',
            'nome': 'nome',
            'registro': 'registro',
            'logradouro': 'logradouro',
            'numero': 'num',
            'bairro': 'bairro',
            'referencia': 'referencia'
        }
        esperado = []
        # Act
        resposta = verificar_campos_obrigatorios(json)
        # Assert
        self.assertEqual(resposta, esperado)

    def test_ao_menos_um_faltando(self):
        '''
        Dado um json contendo ao menos um dos campos obrigatórios \
        faltando
        Quando o verifico se todos estão presentes
        Então devo receber uma lista contendo o campo que está \
        faltando.
        '''
        # Arrange
        json = {
            # 'identificador': 1,
            'latitude': -123,
            'longitude': 456,
            'setor_censitario': 'setor',
            'area_ponderacao': 'area',
            'cod_distrito': 'coddist',
            'distrito': 'dist',
            'cod_subpref': 'codsubpref',
            'subprefeitura': 'subpref',
            'regiao5': 'reg',
            'regiao8': 'reg2',
            'nome': 'nome',
            'registro': 'registro',
            'logradouro': 'logradouro',
            'numero': 'num',
            'bairro': 'bairro',
            'referencia': 'referencia'
        }
        esperado = ['identificador']
        # Act
        resposta = verificar_campos_obrigatorios(json)
        # Assert
        self.assertEqual(resposta, esperado)


class TestIdentificarEntidadeColunas(unittest.TestCase):
    ''' Mantém os testes unitários relacionados à função \
    identificar_entidade_colunas. '''

    def test_coluna_unica(self):
        '''
        Dada uma mensagem de violação de índice único em que o \
        índice é composto por apenas uma coluna da tabela
        Quando o identifico a entidade e a coluna
        Então devo receber uma tupla contendo o nome da entidade \
        e o nome da coluna, respectivamente.
        '''
        # Arrange
        mensagem = '(sqlite3.IntegrityError) UNIQUE constraint failed: Distrito.codigo'
        esperado = ('Distrito', ('codigo',))
        # Act
        resposta = identificar_entidade_colunas(mensagem)
        # Assert
        self.assertEqual(resposta, esperado)

    def test_varias_colunas(self):
        '''
        Dada uma mensagem de violação de índice único em que o \
        índice é composto por apenas mais de uma coluna da tabela
        Quando o identifico a entidade e as colunas
        Então devo receber uma tupla contendo o nome da entidade \
        e os nomes das colunas, respectivamente.
        '''
        # Arrange
        mensagem = '(sqlite3.IntegrityError) UNIQUE constraint failed: Distrito.codigo, Distrito.nome'
        esperado = ('Distrito', ('codigo', 'nome'))
        # Act
        resposta = identificar_entidade_colunas(mensagem)
        # Assert
        self.assertEqual(resposta, esperado)


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
        self.contexto = app.app_context()
        self.contexto.push()
        bd.create_all()

    def tearDown(self):
        bd.session.remove()
        bd.drop_all()
        self.contexto.pop()

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
        resposta = self.app.get('/feiras?regiao5=' + self.REGIAO1)
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
        resposta = self.app.get('/feiras?regiao5=' + self.REGIAO2)
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
        resposta = self.app.get('/feiras?regiao5=' + self.REGIAO1)
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
        resposta = self.app.get('/feiras?distrito=' + self.DISTRITO1)
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
        resposta = self.app.get('/feiras?distrito=' + self.DISTRITO2)
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
        resposta = self.app.get('/feiras?distrito=' + self.DISTRITO1)
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
        resposta = self.app.get('/feiras?nome=' + self.NOME1)
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
        resposta = self.app.get('/feiras?nome=' + self.NOME2)
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
        resposta = self.app.get('/feiras?nome=' + self.NOME1)
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
        resposta = self.app.get('/feiras?nome=' + self.NOME1)
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
        resposta = self.app.get('/feiras?bairro=' + self.BAIRRO1)
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
        resposta = self.app.get('/feiras?bairro=' + self.BAIRRO2)
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
        resposta = self.app.get('/feiras?bairro=' + self.BAIRRO1)
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
        resposta = self.app.get('/feiras?regiao5=' + self.REGIAO1)
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
        resposta = self.app.get('/feiras?distrito=' + self.DISTRITO2)
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
        resposta = self.app.get('/feiras?nome=' + self.NOME1)
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
        resposta = self.app.get('/feiras?bairro=' + self.BAIRRO2)
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
        resposta = self.app.get('/feiras?regiao5=' + self.REGIAO2 +
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
        resposta = self.app.get('/feiras')
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
        resposta = self.app.delete('/feira?registro=' + self.REGISTRO1)
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
        resposta = self.app.delete('/feira?registro=' + self.REGISTRO2)
        feira_livre = FeiraLivre.query \
                                .filter(FeiraLivre.registro == self.REGISTRO1)\
                                .first()
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)
        self.assertEqual(resposta.status_code, 404)
        self.assertIsNotNone(feira_livre)

    @mock.patch('src.basedados.bd.session.commit')
    def test_adicionar1(self, mock_commit):
        '''
        Dado um json com todos os dados necessários para o cadastro \
        de uma feira livre
        Quando adiciono a feira
        Então devo receber um JSON contendo a feira inserida.
        '''
        # Arrange
        dado = {
            'identificador': self.IDENTIFICADOR1,
            'latitude': -123,
            'longitude': 456,
            'setor_censitario': 'setor',
            'area_ponderacao': 'area',
            'cod_distrito': 'coddist',
            'distrito': self.DISTRITO1,
            'cod_subpref': 'codsubpref',
            'subprefeitura': 'subpref',
            'regiao5': self.REGIAO1,
            'regiao8': self.REGIAO2,
            'nome': self.NOME1,
            'registro': self.REGISTRO1,
            'logradouro': 'logradouro',
            'numero': 'num',
            'bairro': self.BAIRRO1,
            'referencia': 'referencia'
        }
        feira_livre = FeiraLivreBuilder().from_dict(dado).build()
        esperado = {'feira': feira_livre.dict}
        # Act
        resposta = self.app.post('/feira', data=json.dumps(dado))
        feira_livre = FeiraLivre.query \
                                .filter(FeiraLivre.registro == self.REGISTRO1)\
                                .first()
        # Assert
        mock_commit.assert_called_once()
        self.assertEqual(json.loads(resposta.data), esperado)
        self.assertEqual(resposta.status_code, 200)

    @mock.patch('src.basedados.bd.session.rollback')
    def test_adicionar2(self, mock_rollback):
        '''
        Dados uma feira livre cadastrada
              um json para cadastro de nova feira em que há \
        violação de índice unico.
        Quando adiciono a feira
        Então devo receber um JSON contendo a identificação do(s) campo(s) \
        incorreto(s).
        '''
        # Arrange
        dado = {
            'identificador': self.IDENTIFICADOR1,
            'latitude': -123,
            'longitude': 456,
            'setor_censitario': 'setor',
            'area_ponderacao': 'area',
            'cod_distrito': 'coddist',
            'distrito': self.DISTRITO1,
            'cod_subpref': 'codsubpref',
            'subprefeitura': 'subpref',
            'regiao5': self.REGIAO1,
            'regiao8': self.REGIAO2,
            'nome': self.NOME1,
            'registro': self.REGISTRO1,
            'logradouro': 'logradouro',
            'numero': 'num',
            'bairro': self.BAIRRO1,
            'referencia': 'referencia'
        }
        FeiraLivreBuilder(bd).from_dict(dado).build()
        dado['registro'] = self.REGISTRO2
        dado['distrito'] = self.DISTRITO2  # quebra do índice de Distrito
        FeiraLivreBuilder().from_dict(dado).build()
        esperado = {'mensagem': 'Um(a) novo(a) Distrito deve conter valores diferentes em codigo.',
                    'erro': 400}
        # Act
        resposta = self.app.post('/feira', data=json.dumps(dado))
        # Assert
        mock_rollback.assert_called_once()
        self.assertEqual(json.loads(resposta.data), esperado)
        self.assertEqual(resposta.status_code, 400)

    def test_adicionar3(self):
        '''
        Dado um json com alguns dados faltando para o cadastro \
        de uma feira livre
        Quando adiciono a feira
        Então devo receber um JSON contendo a identificação do(s) campo(s) \
        que estão faltando.
        '''
        # Arrange
        dado = {
            # 'identificador': self.IDENTIFICADOR1,
            'latitude': -123,
            'longitude': 456,
            'setor_censitario': 'setor',
            'area_ponderacao': 'area',
            'cod_distrito': 'coddist',
            # 'distrito': self.DISTRITO1,
            'cod_subpref': 'codsubpref',
            'subprefeitura': 'subpref',
            'regiao5': self.REGIAO1,
            'regiao8': self.REGIAO2,
            'nome': self.NOME1,
            'registro': self.REGISTRO1,
            'logradouro': 'logradouro',
            'numero': 'num',
            'bairro': self.BAIRRO1,
            'referencia': 'referencia'
        }
        esperado = {'mensagem': 'Campo(s) obrigatório(s) não encontrado(s): distrito, identificador.',
                    'erro': 400}
        # Act
        resposta = self.app.post('/feira', data=json.dumps(dado))
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)
        self.assertEqual(resposta.status_code, 400)

    def test_adicionar4(self):
        '''
        Dados uma feira livre cadastrada
              um json com todos os dados necessários para o \
        cadastro da feira livre com mesmo registro da cadastrada
        Quando adiciono a feira
        Então devo receber um JSON contendo a a mensagem de que \
        a feira já existe.
        '''
        # Arrange
        dado = {
            'identificador': self.IDENTIFICADOR1,
            'latitude': -123,
            'longitude': 456,
            'setor_censitario': 'setor',
            'area_ponderacao': 'area',
            'cod_distrito': 'coddist',
            'distrito': self.DISTRITO1,
            'cod_subpref': 'codsubpref',
            'subprefeitura': 'subpref',
            'regiao5': self.REGIAO1,
            'regiao8': self.REGIAO2,
            'nome': self.NOME1,
            'registro': self.REGISTRO1,
            'logradouro': 'logradouro',
            'numero': 'num',
            'bairro': self.BAIRRO1,
            'referencia': 'referencia'
        }
        FeiraLivreBuilder(bd).from_dict(dado).build()
        FeiraLivreBuilder().from_dict(dado).build()
        esperado = {'mensagem': 'Feira livre com registro {0} já existe.'
                                .format(self.REGISTRO1),
                    'erro': 400}
        # Act
        resposta = self.app.post('/feira', data=json.dumps(dado))
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)
        self.assertEqual(resposta.status_code, 400)

    @mock.patch('src.basedados.bd.session.commit')
    def test_alterar1(self, mock_commit):
        '''
        Dados uma feira livre cadastrada
              um json com todos os dados necessários para a \
        alteração da feira livre
        Quando altero a feira
        Então devo receber um JSON contendo a feira alterada.
        '''
        # Arrange
        dado = {
            'identificador': self.IDENTIFICADOR1,
            'latitude': -123,
            'longitude': 456,
            'setor_censitario': 'setor',
            'area_ponderacao': 'area',
            'cod_distrito': 'coddist',
            'distrito': self.DISTRITO1,
            'cod_subpref': 'codsubpref',
            'subprefeitura': 'subpref',
            'regiao5': self.REGIAO1,
            'regiao8': self.REGIAO2,
            'nome': self.NOME1,
            'registro': self.REGISTRO1,
            'logradouro': 'logradouro',
            'numero': 'num',
            'bairro': self.BAIRRO1,
            'referencia': 'referencia'
        }
        FeiraLivreBuilder(bd).from_dict(dado).build()
        dado['regiao5'] = self.REGIAO2  #  alteração
        feira_livre = FeiraLivreBuilder().from_dict(dado).build()
        esperado = {'feira': feira_livre.dict}
        # Act
        resposta = self.app.put('/feira', data=json.dumps(dado))
        # Assert
        mock_commit.assert_called()
        self.assertEqual(mock_commit.call_count, 2)
        self.assertEqual(json.loads(resposta.data), esperado)
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(FeiraLivre.query.count(), 1)

    @mock.patch('src.basedados.bd.session.rollback')
    def test_alterar2(self, mock_rollback):
        '''
        Dados uma feira livre cadastrada
              um json para alteração da feira em que há \
        violação de índice unico.
        Quando altero a feira
        Então devo receber um JSON contendo a identificação do(s) campo(s) \
        incorreto(s).
        '''
        # Arrange
        dado = {
            'identificador': self.IDENTIFICADOR1,
            'latitude': -123,
            'longitude': 456,
            'setor_censitario': 'setor',
            'area_ponderacao': 'area',
            'cod_distrito': 'coddist',
            'distrito': self.DISTRITO1,
            'cod_subpref': 'codsubpref',
            'subprefeitura': 'subpref',
            'regiao5': self.REGIAO1,
            'regiao8': self.REGIAO2,
            'nome': self.NOME1,
            'registro': self.REGISTRO1,
            'logradouro': 'logradouro',
            'numero': 'num',
            'bairro': self.BAIRRO1,
            'referencia': 'referencia'
        }
        FeiraLivreBuilder(bd).from_dict(dado).build()
        dado['distrito'] = self.DISTRITO2  # quebra do índice de Distrito
        FeiraLivreBuilder().from_dict(dado).build()
        esperado = {'mensagem': 'Um(a) novo(a) Distrito deve conter valores diferentes em codigo.',
                    'erro': 400}
        # Act
        resposta = self.app.put('/feira', data=json.dumps(dado))
        # Assert
        mock_rollback.assert_called_once()
        self.assertEqual(json.loads(resposta.data), esperado)
        self.assertEqual(resposta.status_code, 400)

    def test_alterar3(self):
        '''
        Dado um json com alguns dados faltando para a alteração \
        de uma feira livre
        Quando altero a feira
        Então devo receber um JSON contendo a identificação do(s) campo(s) \
        que estão faltando.
        '''
        # Arrange
        dado = {
            # 'identificador': self.IDENTIFICADOR1,
            'latitude': -123,
            'longitude': 456,
            'setor_censitario': 'setor',
            'area_ponderacao': 'area',
            'cod_distrito': 'coddist',
            # 'distrito': self.DISTRITO1,
            'cod_subpref': 'codsubpref',
            'subprefeitura': 'subpref',
            'regiao5': self.REGIAO1,
            'regiao8': self.REGIAO2,
            'nome': self.NOME1,
            'registro': self.REGISTRO1,
            'logradouro': 'logradouro',
            'numero': 'num',
            'bairro': self.BAIRRO1,
            'referencia': 'referencia'
        }
        esperado = {'mensagem': 'Campo(s) obrigatório(s) não encontrado(s): distrito, identificador.',
                    'erro': 400}
        # Act
        resposta = self.app.put('/feira', data=json.dumps(dado))
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)
        self.assertEqual(resposta.status_code, 400)

    def test_alterar4(self):
        '''
        Dados um json com todos os dados necessários para a \
        alteração da feira livre
        Quando altero a feira
        Então devo receber um JSON contendo a mensagem de que \
        a feira não existe.
        '''
        # Arrange
        dado = {
            'identificador': self.IDENTIFICADOR1,
            'latitude': -123,
            'longitude': 456,
            'setor_censitario': 'setor',
            'area_ponderacao': 'area',
            'cod_distrito': 'coddist',
            'distrito': self.DISTRITO1,
            'cod_subpref': 'codsubpref',
            'subprefeitura': 'subpref',
            'regiao5': self.REGIAO1,
            'regiao8': self.REGIAO2,
            'nome': self.NOME1,
            'registro': self.REGISTRO1,
            'logradouro': 'logradouro',
            'numero': 'num',
            'bairro': self.BAIRRO1,
            'referencia': 'referencia'
        }
        feira_livre = FeiraLivreBuilder().from_dict(dado).build()
        # Act
        esperado = {'mensagem': 'Feira livre com registro {0} não existe.'
                                .format(self.REGISTRO1),
                    'erro': 404}
        # Act
        resposta = self.app.put('/feira', data=json.dumps(dado))
        # Assert
        self.assertEqual(json.loads(resposta.data), esperado)
        self.assertEqual(resposta.status_code, 404)


if __name__ == '__main__':
    unittest.main()
