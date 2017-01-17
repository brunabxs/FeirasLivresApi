'''
Módulo responsável por manter/executar os testes unitários dos \
modelos.
'''

import unittest
import unittest.mock as mock
from app import app
from src.basedados import bd
from src.modelos import converter_dict, buscar_ou_criar
from src.modelos import Subprefeitura, Distrito, Regiao5, Regiao8
from src.modelos import Bairro, Logradouro, Endereco, FeiraLivre


class TestConverterDict(unittest.TestCase):
    ''' Mantém os testes unitários relacionados à função converter_dict. '''

    def test_converter_dict1(self):
        '''
        Dado um elemento com valor None
        Quando é feita sua conversão para dict
        Então deve retornar None.
        '''
        # Arrange
        elemento = None
        esperado = None
        # Act
        resposta = converter_dict(elemento)
        # Assert
        self.assertEqual(resposta, esperado)

    def test_converter_dict2(self):
        '''
        Dado um elemento tem propriedade dict
        Quando é feita sua conversão para dict
        Então deve retornar a sua representação em dict.
        '''
        # Arrange
        elemento = FeiraLivre()
        esperado = {}
        with mock.patch('src.modelos.FeiraLivre.dict',
                        new_callable=mock.PropertyMock) as mock_dict:
            mock_dict.return_value = {}
            # Act
            resposta = converter_dict(elemento)
        # Assert
        self.assertEqual(resposta, esperado)


class TestBuscarOuCriar(unittest.TestCase):
    ''' Mantém os testes unitários relacionados à função buscar_ou_criar. '''

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

    def test_criar(self):
        '''
        Dado um elemento com atributo codigo
        Quando se procura pelo elemento de codigo='123'
        Então deve persistir o elemento (com código '123') e
              deve existir apenas um elemento no final.
        '''
        # Arrange
        # Act
        resposta = buscar_ou_criar(bd.session, Subprefeitura, codigo='123')
        # Assert
        self.assertEqual(resposta.codigo, '123')
        self.assertEqual(resposta.id, 1)
        total = Subprefeitura.query.count()
        self.assertEqual(total, 1)

    def test_buscar(self):
        '''
        Dado um elemento com atributo codigo='123'
        Quando se procura pelo elemento de codigo='123'
        Então não deve persistir outro elemento (com código '123') e
              deve existir apenas um elemento no final e
              deve retornar o elemento existente.
        '''
        # Arrange
        esperado = Subprefeitura(codigo='123')
        bd.session.add(esperado)
        bd.session.commit()
        bd.session.flush()
        # Act
        resposta = buscar_ou_criar(bd.session, Subprefeitura, codigo='123')
        # Assert
        self.assertEqual(resposta, esperado)
        total = Subprefeitura.query.count()
        self.assertEqual(total, 1)

    def test_commit1(self):
        '''
        Dado um elemento a ser inserido
        Quando a opção de commit está ligada (commit=True)
        Então a inserção não é desfeita num rollback (sqlalchemy inicia nova \
        sessão após commit).
        '''
        # Arrange
        esperado = 1
        # Act
        buscar_ou_criar(bd.session, Subprefeitura, True, codigo='123')
        bd.session.rollback()
        # Assert
        resposta = Subprefeitura.query.count()
        self.assertEqual(resposta, esperado)

    def test_commit2(self):
        '''
        Dado um elemento a ser inserido
        Quando a opção de commit está desligada (commit=False)
        Então a inserção é desfeita num rollback.
        '''
        # Arrange
        esperado = 0
        # Act
        buscar_ou_criar(bd.session, Subprefeitura, False, codigo='123')
        bd.session.rollback()
        # Assert
        resposta = Subprefeitura.query.count()
        self.assertEqual(resposta, esperado)


class TestSubprefeitura(unittest.TestCase):
    ''' Mantém os testes relacionados ao modelo Subprefeitura. '''
    CODIGO = '123'
    NOME = 'subpref'

    def test_dict(self):
        '''
        Dada uma subprefeitura com código '123' e nome 'subpref'
        Quando dict é chamado
        Então devo receber um dict com os dados da subprefeitura.
        '''
        # Arrange
        subprefeitura = Subprefeitura(codigo=self.CODIGO, nome=self.NOME)
        esperado = {'codigo': subprefeitura.codigo,
                    'nome': subprefeitura.nome}
        # Act
        resposta = subprefeitura.dict
        # Assert
        self.assertEqual(resposta, esperado)


class TestDistrito(unittest.TestCase):
    ''' Mantém os testes relacionados ao modelo Distrito. '''
    CODIGO = '123'
    NOME = 'distrito'

    @mock.patch('src.modelos.converter_dict', return_value='DICT')
    def test_dict(self, mock_converter_dict):
        '''
        Dado um distrito com código '123' e nome 'distrito'
        Quando dict é chamado
        Então devo receber um dict com os dados do distrito.
        '''
        # Arrange
        distrito = Distrito(codigo=self.CODIGO, nome=self.NOME)
        esperado = {'codigo': distrito.codigo,
                    'nome': distrito.nome,
                    'subprefeitura': 'DICT'}
        # Act
        resposta = distrito.dict
        # Assert
        self.assertEqual(resposta, esperado)
        mock_converter_dict.assert_called_once()


class TestRegiao5(unittest.TestCase):
    ''' Mantém os testes relacionados ao modelo Regiao5. '''
    NOME = 'regiao'

    def test_dict(self):
        '''
        Dado uma região 5 com nome 'regiao'
        Quando dict é chamado
        Então devo receber um dict com os dados da região.
        '''
        # Arrange
        regiao = Regiao5(nome=self.NOME)
        esperado = {'nome': regiao.nome}
        # Act
        resposta = regiao.dict
        # Assert
        self.assertEqual(resposta, esperado)


class TestRegiao8(unittest.TestCase):
    ''' Mantém os testes relacionados ao modelo Regiao8. '''
    NOME = 'regiao'

    def test_dict(self):
        '''
        Dado uma região 8 com nome 'regiao'
        Quando dict é chamado
        Então devo receber um dict com os dados da região.
        '''
        # Arrange
        regiao = Regiao8(nome=self.NOME)
        esperado = {'nome': regiao.nome}
        # Act
        resposta = regiao.dict
        # Assert
        self.assertEqual(resposta, esperado)


class TestBairro(unittest.TestCase):
    ''' Mantém os testes relacionados ao modelo Bairro. '''
    NOME = 'bairro'

    @mock.patch('src.modelos.converter_dict', return_value='DICT')
    def test_dict(self, mock_converter_dict):
        '''
        Dado um bairro nome 'bairro'
        Quando dict é chamado
        Então devo receber um dict com os dados do bairro.
        '''
        # Arrange
        bairro = Bairro(nome=self.NOME)
        esperado = {'nome': bairro.nome,
                    'distrito': 'DICT'}
        # Act
        resposta = bairro.dict
        # Assert
        self.assertEqual(resposta, esperado)
        mock_converter_dict.assert_called_once()


class TestLogradouro(unittest.TestCase):
    ''' Mantém os testes relacionados ao modelo Logradouro. '''
    NOME = 'logradouro'

    def test_dict(self):
        '''
        Dado um logradouro nome 'logradouro'
        Quando dict é chamado
        Então devo receber um dict com os dados do logradouro.
        '''
        # Arrange
        logradouro = Logradouro(nome=self.NOME)
        esperado = {'nome': logradouro.nome}
        # Act
        resposta = logradouro.dict
        # Assert
        self.assertEqual(resposta, esperado)


class TestEndereco(unittest.TestCase):
    ''' Mantém os testes relacionados ao modelo Endereco. '''
    NUMERO = 's/n'
    REFERENCIA = 'referencia'
    LAT = 123
    LONG = 456
    SETOR_CENS = 'setor'
    AREA_POND = 'area'

    @mock.patch('src.modelos.converter_dict', return_value='DICT')
    def test_dict(self, mock_converter_dict):
        '''
        Dado um endereço nome 'endereco'
        Quando dict é chamado
        Então devo receber um dict com os dados do endereço.
        '''
        # Arrange
        endereco = Endereco(numero=self.NUMERO,
                            referencia=self.REFERENCIA,
                            latitude=self.LAT,
                            longitude=self.LONG,
                            setor_censitario=self.SETOR_CENS,
                            area_ponderacao=self.AREA_POND)
        esperado = {'numero': endereco.numero,
                    'referencia': endereco.referencia,
                    'latitude': endereco.latitude,
                    'longitude': endereco.longitude,
                    'setor_censitario': endereco.setor_censitario,
                    'area_ponderacao': endereco.area_ponderacao,
                    'logradouro': 'DICT',
                    'bairro': 'DICT',
                    'regiao5': 'DICT',
                    'regiao8': 'DICT'}
        # Act
        resposta = endereco.dict
        # Assert
        self.assertEqual(resposta, esperado)
        mock_converter_dict.assert_called()
        self.assertEqual(mock_converter_dict.call_count, 4)


class TestFeiraLivre(unittest.TestCase):
    ''' Mantém os testes relacionados ao modelo FeiraLivre. '''
    IDENTIFICADOR = '1'
    REGISTRO = '123'
    NOME = 'nome'

    @mock.patch('src.modelos.converter_dict', return_value='DICT')
    def test_dict(self, mock_converter_dict):
        '''
        Dadas uma feira livre com identificador '1', registro '123' e \
        nome 'nome'
        Quando dict é chamado
        Então devo receber um dict com os dados da feira livre.
        '''
        # Arrange
        feira_livre = FeiraLivre(identificador=self.IDENTIFICADOR,
                                 registro=self.REGISTRO,
                                 nome=self.NOME)
        esperado = {'nome': feira_livre.nome,
                    'registro': feira_livre.registro,
                    'identificador': feira_livre.identificador,
                    'endereco': 'DICT'}
        # Act
        resposta = feira_livre.dict
        # Assert
        self.assertEqual(resposta, esperado)
        mock_converter_dict.assert_called_once()
