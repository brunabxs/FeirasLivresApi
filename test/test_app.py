'''
Módulo responsável por manter/executar os testes unitários e \
funcionais da aplicação.
'''

import unittest
import unittest.mock as mock
import json
import logging
from copy import copy
from app import app
from app import verificar_campos_obrigatorios, identificar_entidade_colunas
from src.basedados import bd
from test.helpers import *

logger = logging.getLogger('app')
logger.setLevel(logging.CRITICAL)


class TestVerificarCamposObrigatorios(unittest.TestCase):
    ''' Mantém os testes unitários relacionados à função \
    verificar_campos_obrigatorios. '''
    JSON = {
        'identificador': 1,
        'latitude': -123,
        'longitude': 456,
        'setor_censitario': 'setor',
        'area_ponderacao': 'area',
        'cod_distrito': 'codd',
        'distrito': 'dist',
        'cod_subpref': 'cods',
        'subprefeitura': 'subpref',
        'regiao5': 'reg1',
        'regiao8': 'reg2',
        'nome': 'nome',
        'registro': 'reg',
        'logradouro': 'logradouro',
        'numero': 'num',
        'bairro': 'bairro',
        'referencia': 'referencia'
    }

    def test_todos_presentes(self):
        '''
        Dado um json contendo todos os campos obrigatórios \
        presentes
        Quando o verifico se todos estão presentes
        Então devo receber uma lista vazia.
        '''
        # Arrange
        json = copy(self.JSON)
        valor_esperado = []
        # Act
        valor_atual = verificar_campos_obrigatorios(json)
        # Assert
        self.assertEqual(valor_atual, valor_esperado)

    def test_ao_menos_um_faltando(self):
        '''
        Dado um json contendo ao menos um dos campos obrigatórios \
        faltando
        Quando o verifico se todos estão presentes
        Então devo receber uma lista contendo o campo que está \
        faltando.
        '''
        # Arrange
        json = copy(self.JSON)
        json.pop('identificador', None)
        valor_esperado = ['identificador']
        # Act
        valor_atual = verificar_campos_obrigatorios(json)
        # Assert
        self.assertEqual(valor_atual, valor_esperado)


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
        mensagem = '(sqlite3.IntegrityError) UNIQUE constraint failed: ' \
                   'Distrito.codigo'
        valor_esperado = ('Distrito', ('codigo',))
        # Act
        valor_atual = identificar_entidade_colunas(mensagem)
        # Assert
        self.assertEqual(valor_atual, valor_esperado)

    def test_varias_colunas(self):
        '''
        Dada uma mensagem de violação de índice único em que o \
        índice é composto por apenas mais de uma coluna da tabela
        Quando o identifico a entidade e as colunas
        Então devo receber uma tupla contendo o nome da entidade \
        e os nomes das colunas, respectivamente.
        '''
        # Arrange
        mensagem = '(sqlite3.IntegrityError) UNIQUE constraint failed: ' \
                   'Distrito.codigo, Distrito.nome'
        valor_esperado = ('Distrito', ('codigo', 'nome'))
        # Act
        valor_atual = identificar_entidade_colunas(mensagem)
        # Assert
        self.assertEqual(valor_atual, valor_esperado)


class TestBuscar(unittest.TestCase):
    ''' Mantém os testes relacionados à busca de uma feira. '''
    COD1, COD2 = 'cod1', 'cod2'
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

    def test_regiao(self):
        '''
        Dada uma feira livre na região 'regiao1'
        Quando o busco por regiao5='regiao1'
        Então devo receber um JSON contendo a feira livre na lista de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_regiao5(self.REGIAO1).build()
        valor_esperado = {'feiras': [feira_livre.dict]}
        # Act
        valor_atual = self.app.get('/feiras?regiao5=' + self.REGIAO1)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_regiao_diferente(self):
        '''
        Dada uma feira livre na região 'regiao1'
        Quando o busco por regiao5='regiao2'
        Então devo receber um JSON contendo uma lista vazia de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_regiao5(self.REGIAO1).build()
        valor_esperado = {'feiras': []}
        # Act
        valor_atual = self.app.get('/feiras?regiao5=' + self.REGIAO2)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_regiao_varias_feiras(self):
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
        valor_esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        valor_atual = self.app.get('/feiras?regiao5=' + self.REGIAO1)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_distrito(self):
        '''
        Dada uma feira livre no distrito 'distrito1'
        Quando o busco por distrito='distrito1'
        Então devo receber um JSON contendo a feira livre na lista de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_cod_distrito(self.COD1) \
                                           .with_distrito(self.DISTRITO1) \
                                           .build()
        valor_esperado = {'feiras': [feira_livre.dict]}
        # Act
        valor_atual = self.app.get('/feiras?distrito=' + self.DISTRITO1)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_distrito_diferente(self):
        '''
        Dada uma feira livre no distrito 'distrito1'
        Quando o busco por distrito='distrito2'
        Então devo receber um JSON contendo uma lista vazia de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_cod_distrito(self.COD1) \
                                           .with_distrito(self.DISTRITO1) \
                                           .build()
        valor_esperado = {'feiras': []}
        # Act
        valor_atual = self.app.get('/feiras?distrito=' + self.DISTRITO2)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_distrito_varias_feiras(self):
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
        valor_esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        valor_atual = self.app.get('/feiras?distrito=' + self.DISTRITO1)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_nome(self):
        '''
        Dada uma feira livre com nome 'nome1'
        Quando o busco por nome='nome1'
        Então devo receber um JSON contendo a feira livre na lista de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_nome(self.NOME1).build()
        valor_esperado = {'feiras': [feira_livre.dict]}
        # Act
        valor_atual = self.app.get('/feiras?nome=' + self.NOME1)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_nome_diferente(self):
        '''
        Dada uma feira livre com nome 'nome1'
        Quando o busco por nome='nome2'
        Então devo receber um JSON contendo uma lista vazia de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_nome(self.NOME1).build()
        valor_esperado = {'feiras': []}
        # Act
        valor_atual = self.app.get('/feiras?nome=' + self.NOME2)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_nome_varias_feiras(self):
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
        valor_esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        valor_atual = self.app.get('/feiras?nome=' + self.NOME1)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_nome_semelhante(self):
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
        valor_esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        valor_atual = self.app.get('/feiras?nome=' + self.NOME1)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_bairro(self):
        '''
        Dada uma feira livre no bairro 'bairro1'
        Quando o busco por bairro='bairro1'
        Então devo receber um JSON contendo a feira livre na lista de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_bairro(self.BAIRRO1).build()
        valor_esperado = {'feiras': [feira_livre.dict]}
        # Act
        valor_atual = self.app.get('/feiras?bairro=' + self.BAIRRO1)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_bairro_diferente(self):
        '''
        Dada uma feira livre no bairro 'bairro1'
        Quando o busco por bairro='bairro2'
        Então devo receber um JSON contendo uma lista vazia de feiras.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_bairro(self.BAIRRO1).build()
        valor_esperado = {'feiras': []}
        # Act
        valor_atual = self.app.get('/feiras?bairro=' + self.BAIRRO2)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_bairro_varias_feiras(self):
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
        valor_esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        valor_atual = self.app.get('/feiras?bairro=' + self.BAIRRO1)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_regiao_multiplas_feiras(self):
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
        valor_esperado = {'feiras': [feira_livre1.dict, feira_livre3.dict]}
        # Act
        valor_atual = self.app.get('/feiras?regiao5=' + self.REGIAO1)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_distrito_multiplas_feiras(self):
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
        valor_esperado = {'feiras': [feira_livre2.dict, feira_livre3.dict]}
        # Act
        valor_atual = self.app.get('/feiras?distrito=' + self.DISTRITO2)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_nome_semelhante_multiplas_feiras(self):
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
        valor_esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        valor_atual = self.app.get('/feiras?nome=' + self.NOME1)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_bairro_multiplas_feiras(self):
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
        valor_esperado = {'feiras': [feira_livre2.dict, feira_livre3.dict]}
        # Act
        valor_atual = self.app.get('/feiras?bairro=' + self.BAIRRO2)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_regiao_distrito_nome_bairro_multiplas_feiras(self):
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
        valor_esperado = {'feiras': [feira_livre2.dict]}
        # Act
        valor_atual = self.app.get('/feiras?regiao5=' + self.REGIAO2 +
                                   '&distrito=' + self.DISTRITO2 +
                                   '&bairro=' + self.BAIRRO2 +
                                   '&nome=' + self.NOME1)
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)

    def test_sem_parametros(self):
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
        valor_esperado = {'feiras': [feira_livre1.dict, feira_livre2.dict]}
        # Act
        valor_atual = self.app.get('/feiras')
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)


class TestRemover(unittest.TestCase):
    ''' Mantém os testes relacionados à remoção de uma feira. '''
    REGISTRO1, REGISTRO2 = '123', '456'

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

    def test_sucesso(self):
        '''
        Dada uma feira livre com registro '123'
        Quando removo a feira com registro '123'
        Então a feira deve ser removida;
              devo receber um JSON contendo a feira livre removida.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                           .build()
        valor_esperado = {'feira': feira_livre.dict}
        # Act
        valor_atual = self.app.delete('/feira?registro=' + self.REGISTRO1)
        feira_livre = FeiraLivre.query \
                                .filter(FeiraLivre.registro == self.REGISTRO1)\
                                .first()
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)
        self.assertEqual(valor_atual.status_code, 200)
        self.assertIsNone(feira_livre)

    def test_registro_nao_existente(self):
        '''
        Dada uma feira livre com registro '123'
        Quando removo a feira com registro '456'
        Então a feira não deve ser removida;
              devo receber um JSON contendo a mensagem de erro.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder(bd).with_registro(self.REGISTRO1) \
                                           .build()
        valor_esperado = {'mensagem': 'Feira livre com registro {0} '
                                      'não existe.'.format(self.REGISTRO2),
                          'erro': 404}
        # Act
        valor_atual = self.app.delete('/feira?registro=' + self.REGISTRO2)
        feira_livre = FeiraLivre.query \
                                .filter(FeiraLivre.registro == self.REGISTRO1)\
                                .first()
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)
        self.assertEqual(valor_atual.status_code, 404)
        self.assertIsNotNone(feira_livre)


class TestAdicionar(unittest.TestCase):
    ''' Mantém os testes relacionados à inclusão de nova feira. '''
    JSON = {
        'identificador': 1,
        'latitude': -123,
        'longitude': 456,
        'setor_censitario': 'setor',
        'area_ponderacao': 'area',
        'cod_distrito': 'codd',
        'distrito': 'dist',
        'cod_subpref': 'cods',
        'subprefeitura': 'subpref',
        'regiao5': 'reg1',
        'regiao8': 'reg2',
        'nome': 'nome',
        'registro': 'reg',
        'logradouro': 'logradouro',
        'numero': 'num',
        'bairro': 'bairro',
        'referencia': 'referencia'
    }

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

    @mock.patch('src.basedados.bd.session.commit')
    def test_sucesso(self, mock_commit):
        '''
        Dado um json com todos os dados necessários para o cadastro \
        de uma feira livre
        Quando adiciono a feira
        Então devo receber um JSON contendo a feira inserida.
        '''
        # Arrange
        dado = copy(self.JSON)
        feira_livre = FeiraLivreBuilder().from_dict(dado).build()
        valor_esperado = {'feira': feira_livre.dict}
        # Act
        valor_atual = self.app.post('/feira', data=json.dumps(dado))
        # Assert
        mock_commit.assert_called_once()
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)
        self.assertEqual(valor_atual.status_code, 200)
        self.assertEqual(FeiraLivre.query.count(), 1)

    @mock.patch('src.basedados.bd.session.rollback')
    def test_violacao_indice_unico(self, mock_rollback):
        '''
        Dados uma feira livre cadastrada
              um json para cadastro de nova feira em que há violação de \
        índice único.
        Quando adiciono a feira
        Então devo receber um JSON contendo a identificação do(s) campo(s) \
        incorreto(s).
        '''
        # Arrange
        dado = copy(self.JSON)
        FeiraLivreBuilder(bd).from_dict(dado).build()
        dado['registro'] += 'x'  # novo registro
        dado['distrito'] += 'x'  # quebra do índice de Distrito
        FeiraLivreBuilder().from_dict(dado).build()
        valor_esperado = {'mensagem': 'Um(a) novo(a) Distrito deve conter '
                                      'valores diferentes em codigo.',
                          'erro': 400}
        # Act
        valor_atual = self.app.post('/feira', data=json.dumps(dado))
        # Assert
        mock_rollback.assert_called_once()
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)
        self.assertEqual(valor_atual.status_code, 400)

    def test_dado_obrigatorio_nao_existente(self):
        '''
        Dado um json com alguns dados faltando para o cadastro \
        de uma feira livre
        Quando adiciono a feira
        Então devo receber um JSON contendo a identificação do(s) campo(s) \
        que estão faltando.
        '''
        # Arrange
        # Arrange
        dado = copy(self.JSON)
        dado.pop('identificador', None)
        dado.pop('distrito', None)
        valor_esperado = {'mensagem': 'Campo(s) obrigatório(s) não '
                                      'encontrado(s): distrito, '
                                      'identificador.',
                          'erro': 400}
        # Act
        valor_atual = self.app.post('/feira', data=json.dumps(dado))
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)
        self.assertEqual(valor_atual.status_code, 400)

    def test_registro_existente(self):
        '''
        Dados uma feira livre cadastrada
              um json com todos os dados necessários para o cadastro \
        da feira livre com mesmo registro da cadastrada
        Quando adiciono a feira
        Então devo receber um JSON contendo a a mensagem de que \
        a feira já existe.
        '''
        # Arrange
        dado = copy(self.JSON)
        FeiraLivreBuilder(bd).from_dict(dado).build()
        FeiraLivreBuilder().from_dict(dado).build()
        valor_esperado = {'mensagem': 'Feira livre com registro {0} já existe.'
                                      .format(dado['registro']),
                          'erro': 400}
        # Act
        valor_atual = self.app.post('/feira', data=json.dumps(dado))
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)
        self.assertEqual(valor_atual.status_code, 400)


class TestAlterar(unittest.TestCase):
    ''' Mantém os testes relacionados à alteração de uma feira. '''
    JSON = {
        'identificador': 1,
        'latitude': -123,
        'longitude': 456,
        'setor_censitario': 'setor',
        'area_ponderacao': 'area',
        'cod_distrito': 'codd',
        'distrito': 'dist',
        'cod_subpref': 'cods',
        'subprefeitura': 'subpref',
        'regiao5': 'reg1',
        'regiao8': 'reg2',
        'nome': 'nome',
        'registro': 'reg',
        'logradouro': 'logradouro',
        'numero': 'num',
        'bairro': 'bairro',
        'referencia': 'referencia'
    }

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

    @mock.patch('src.basedados.bd.session.commit')
    def test_sucesso(self, mock_commit):
        '''
        Dados uma feira livre cadastrada
              um json com todos os dados necessários para a \
        alteração da feira livre
        Quando altero a feira
        Então devo receber um JSON contendo a feira alterada.
        '''
        # Arrange
        dado = copy(self.JSON)
        FeiraLivreBuilder(bd).from_dict(dado).build()
        dado['regiao5'] += 'x'  #  alteração
        feira_livre = FeiraLivreBuilder().from_dict(dado).build()
        valor_esperado = {'feira': feira_livre.dict}
        # Act
        valor_atual = self.app.put('/feira', data=json.dumps(dado))
        # Assert
        mock_commit.assert_called()
        self.assertEqual(mock_commit.call_count, 2)
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)
        self.assertEqual(valor_atual.status_code, 200)
        self.assertEqual(FeiraLivre.query.count(), 1)

    @mock.patch('src.basedados.bd.session.rollback')
    def test_violacao_indice_unico(self, mock_rollback):
        '''
        Dados uma feira livre cadastrada
              um json para alteração da feira em que há violação de \
        índice único.
        Quando altero a feira
        Então devo receber um JSON contendo a identificação do(s) campo(s) \
        incorreto(s).
        '''
        # Arrange
        dado = copy(self.JSON)
        FeiraLivreBuilder(bd).from_dict(dado).build()
        dado['distrito'] += 'x'  # quebra do índice de Distrito
        FeiraLivreBuilder().from_dict(dado).build()
        valor_esperado = {'mensagem': 'Um(a) novo(a) Distrito deve conter '
                                      'valores diferentes em codigo.',
                          'erro': 400}
        # Act
        valor_atual = self.app.put('/feira', data=json.dumps(dado))
        # Assert
        mock_rollback.assert_called_once()
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)
        self.assertEqual(valor_atual.status_code, 400)

    def test_dado_obrigatorio_nao_existente(self):
        '''
        Dado um json com alguns dados faltando para a alteração \
        de uma feira livre
        Quando altero a feira
        Então devo receber um JSON contendo a identificação do(s) campo(s) \
        que estão faltando.
        '''
        # Arrange
        dado = copy(self.JSON)
        dado.pop('identificador', None)
        dado.pop('distrito', None)
        valor_esperado = {'mensagem': 'Campo(s) obrigatório(s) não '
                                      'encontrado(s): distrito, '
                                      'identificador.',
                          'erro': 400}
        # Act
        valor_atual = self.app.put('/feira', data=json.dumps(dado))
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)
        self.assertEqual(valor_atual.status_code, 400)

    def test_registro_nao_existente(self):
        '''
        Dados um json com todos os dados necessários para a alteração \
        da feira livre
        Quando altero a feira
        Então devo receber um JSON contendo a mensagem de que \
        a feira não existe.
        '''
        # Arrange
        dado = copy(self.JSON)
        feira_livre = FeiraLivreBuilder().from_dict(dado).build()
        # Act
        valor_esperado = {'mensagem': 'Feira livre com registro {0} '
                                      'não existe.'.format(dado['registro']),
                          'erro': 404}
        # Act
        valor_atual = self.app.put('/feira', data=json.dumps(dado))
        # Assert
        self.assertEqual(json.loads(valor_atual.data), valor_esperado)
        self.assertEqual(valor_atual.status_code, 404)


if __name__ == '__main__':
    unittest.main()
