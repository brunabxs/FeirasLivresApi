''' Módulo responsável por definir alguns helpers para os testes. '''

from src.modelos import FeiraLivre


def persistir(bd, *objetos):
    '''
    Persiste objetos no banco de dados.

    Parâmetros
    ==========
    bd [SQLAlchemy] -- instância do banco de dados onde objetos devem ser persistidos.
    objetos -- objetos a serem persistidos
    '''
    for objeto in objetos:
        bd.session.add(objeto)
    bd.session.commit()


class FeiraLivreBuilder:
    '''
    Constrói uma FeiraLivre para auxiliar os testes.

    Atributos
    ==========
    feira_livre [FeiraLivre] -- feira livre a ser construída.
    '''
    def __init__(self):
        ''' Construtor. '''
        self.feira_livre = FeiraLivre('qualquer', 'qualquer')

    def with_regiao(self, regiao):
        '''
        Modifica a região à qual a feira livre pertence.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.regiao = regiao
        return self

    def with_distrito(self, distrito):
        '''
        Modifica o distrito ao qual a feira livre pertence.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.distrito = distrito
        return self

    def build(self):
        '''
        Gera a feira livre.

        Retorno
        =======
        FeiraLivre -- instância da feira livre.
        '''
        return self.feira_livre
