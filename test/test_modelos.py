'''
Módulo responsável por manter/executar os testes unitários dos \
modelos.
'''

import unittest
from test.helpers import FeiraLivreBuilder


class TestFeiraLivre(unittest.TestCase):
    ''' Mantém os testes relacionados ao modelo FeiraLivre. '''
    REGISTRO = '123'
    REGIAO = 'regiao'
    DISTRITO = 'distrito'
    BAIRRO = 'bairro'
    NOME = 'nome'

    def test_dict(self):
        '''
        Dadas uma feira livre com registro '123' na região 'regiao', \
        no distrito 'distrito', no bairro 'bairro' e nome 'nome'
        Quando dict é chamado
        Então devo receber um dict com os dados da feira livre.
        '''
        # Arrange
        feira_livre = FeiraLivreBuilder().with_registro(self.REGISTRO) \
                                         .with_regiao(self.REGIAO) \
                                         .with_distrito(self.DISTRITO) \
                                         .with_bairro(self.BAIRRO) \
                                         .with_nome(self.NOME) \
                                         .build()
        esperado = {'regiao': self.REGIAO,
                    'bairro': self.BAIRRO,
                    'nome': self.NOME,
                    'distrito': self.DISTRITO,
                    'registro': self.REGISTRO}
        # Act
        resposta = feira_livre.dict
        # Assert
        self.assertEqual(resposta, esperado)
