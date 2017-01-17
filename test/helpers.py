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
        self.feira_livre = FeiraLivre('qualquer', 'qualquer', 'qualquer', 'qualquer', 'qualquer')

    def with_registro(self, registro):
        '''
        Modifica o registro da feira livre.

        Parâmetros
        ==========
        registro [str] -- registro da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.registro = registro
        return self

    def with_regiao(self, regiao):
        '''
        Modifica a região à qual a feira livre pertence.

        Parâmetros
        ==========
        regiao [str] -- região à qual pertence a feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.regiao = regiao
        return self

    def with_distrito(self, distrito):
        '''
        Modifica o distrito ao qual a feira livre pertence.

        Parâmetros
        ==========
        distrito [str] -- distrito ao qual pertence a feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.distrito = distrito
        return self

    def with_nome(self, nome):
        '''
        Modifica o nome da feira livre.

        Parâmetros
        ==========
        nome [str] -- nome da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.nome = nome
        return self

    def with_bairro(self, bairro):
        '''
        Modifica o bairro ao qual a feira livre pertence.

        Parâmetros
        ==========
        bairro [str] -- bairro ao qual pertence a feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.bairro = bairro
        return self

    def build(self):
        '''
        Gera a feira livre.

        Retorno
        =======
        FeiraLivre -- instância da feira livre.
        '''
        return self.feira_livre
