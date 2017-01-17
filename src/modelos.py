''' Módulo responsável por definir os modelos que representam a base de dados. '''

from src.basedados import bd


class FeiraLivre(bd.Model):
    '''
    Representa a feira livre.

    Atributos
    ==========
    registro [str] -- registro da feira livre.
    regiao [str] -- região à qual pertence a feira livre.
    distrito [str] -- distrito ao qual pertence a feira livre.
    nome [str] -- nome da feira livre.
    bairro [str] -- bairro ao qual pertence a feira livre.
    '''
    __tablename__ = 'FeiraLivre'
    id = bd.Column(bd.Integer, primary_key=True)
    registro = bd.Column(bd.String(255))
    regiao = bd.Column(bd.String(255))
    distrito = bd.Column(bd.String(255))
    nome = bd.Column(bd.String(255))
    bairro = bd.Column(bd.String(255))

    def __init__(self, registro, regiao, distrito, nome, bairro):
        '''
        Construtor.

        Parâmetros
        ==========
        registro [str] -- registro da feira livre.
        regiao [str] -- região à qual pertence a feira livre.
        distrito [str] -- distrito ao qual pertence a feira livre.
        nome [str] -- nome da feira livre.
        bairro [str] -- bairro ao qual pertence a feira livre.
        '''
        self.registro = registro
        self.regiao = regiao
        self.distrito = distrito
        self.nome = nome
        self.bairro = bairro

    @property
    def dict(self):
        '''
        Retorna a representação do objeto como um dict.

        Retorno
        =======
        Dict -- representação do objeto como um dict.
        '''
        return {'registro': self.registro,
                'regiao': self.regiao,
                'distrito': self.distrito,
                'nome': self.nome,
                'bairro': self.bairro}
