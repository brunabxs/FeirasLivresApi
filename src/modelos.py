''' Módulo responsável por definir os modelos que representam a base de dados. '''

from src.basedados import bd


class FeiraLivre(bd.Model):
    '''
    Representa a feira livre.
    Atributos
    ==========
    regiao [str] -- região à qual pertence a feira livre.
    '''
    __tablename__ = 'FeiraLivre'
    id = bd.Column(bd.Integer, primary_key=True)
    regiao = bd.Column(bd.String(255))

    def __init__(self, regiao):
        '''
        Construtor.

        Parâmetros
        ==========
        regiao [str] -- região à qual pertence a feira livre.
        '''
        self.regiao = regiao

    @property
    def dict(self):
        '''
        Retorna a representação do objeto como um dict.

        Retorno
        =======
        Dict -- representação do objeto como um dict.
        '''
        return {'regiao': self.regiao}
