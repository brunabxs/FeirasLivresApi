''' Módulo responsável por definir os modelos que representam a base de \
dados. '''

from src.basedados import bd
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


def converter_dict(elemento):
    '''
    Retorna a representação do elemento como Dict.
    Se o elemento for None, retorna None.

    Parâmetro
    =========
    elemento [object] -- instância que possui propriedade dict.

    Retorno
    =======
    Dict -- representação do elemento como Dict ou None.
    '''
    if elemento is None:
        return None
    return elemento.dict


def buscar_ou_criar(sessao, modelo, commit=False, **kwargs):
    '''
    Recupera um elemento dadas suas informações.
    Caso não seja encontrado, cria.

    Parâmetros
    ==========
    sessao [Session] -- sessão.
    modelo [Model] -- modelo.
    commit [bool] -- informa se faz ou não commit na sessão.
    kwargs -- informações pelas qual a entidade será \
    procurada ou criada.

    Retorno
    =======
    instância do modelo que foi encontrada ou criada.
    '''
    consulta = sessao.query(modelo).filter_by(**kwargs)
    instancia = consulta.first()
    if instancia:
        return instancia
    else:
        instancia = modelo(**kwargs)
        sessao.add(instancia)
        if commit:
            sessao.commit()
        sessao.flush()
        return instancia


class Subprefeitura(bd.Model):
    '''
    Representa a subprefeitura.

    Atributos
    ==========
    id [int] -- id da subprefeitura.
    codigo [str] -- código da subprefeitura.
    nome [str] -- nome da subprefeitura.
    '''
    __tablename__ = 'Subprefeitura'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(5), unique=True)
    nome = Column(String(80))

    @property
    def dict(self):
        '''
        Retorna a representação do objeto como um dict.

        Retorno
        =======
        Dict -- representação do objeto como um dict.
        '''
        return {'codigo': self.codigo,
                'nome': self.nome}


class Distrito(bd.Model):
    '''
    Representa o distrito municipal.

    Atributos
    ==========
    id [int] -- id do distrito municipal.
    codigo [str] -- código do distrito municipal.
    nome [str] -- nome do distrito municipal.
    subprefeitura_id [int] -- id da subprefeitura à qual pertence o distrito.
    subprefeitura [Subprefeitura] -- subprefeitura à qual pertence o distrito.
    '''
    __tablename__ = 'Distrito'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(5), unique=True)
    nome = Column(String(80))
    subprefeitura_id = Column(Integer, ForeignKey('Subprefeitura.id'))
    subprefeitura = relationship('Subprefeitura', lazy='subquery')

    @property
    def dict(self):
        '''
        Retorna a representação do objeto como um dict.

        Retorno
        =======
        Dict -- representação do objeto como um dict.
        '''
        return {'codigo': self.codigo,
                'nome': self.nome,
                'subprefeitura': converter_dict(self.subprefeitura)}


class Regiao5(bd.Model):
    '''
    Representa a região conforme divisão do Município em cinco áreas.

    Atributos
    ==========
    id [int] -- id da região.
    nome [str] -- nome da região.
    '''
    __tablename__ = 'Regiao5'
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), unique=True)

    @property
    def dict(self):
        '''
        Retorna a representação do objeto como um dict.

        Retorno
        =======
        Dict -- representação do objeto como um dict.
        '''
        return {'nome': self.nome}


class Regiao8(bd.Model):
    '''
    Representa a região conforme divisão do Município em oito áreas.

    Atributos
    ==========
    id [int] -- id da região.
    nome [str] -- nome da região.
    '''
    __tablename__ = 'Regiao8'
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), unique=True)

    @property
    def dict(self):
        '''
        Retorna a representação do objeto como um dict.

        Retorno
        =======
        Dict -- representação do objeto como um dict.
        '''
        return {'nome': self.nome}


class Bairro(bd.Model):
    '''
    Representa o bairro.

    Atributos
    ==========
    id [int] -- id do bairro.
    nome [str] -- nome do bairro.
    distrito_id [int] -- id do distrito municipal ao qual pertence o bairro.
    distrito [Distrito] -- distrito municipal ao qual pertence o bairro.
    '''
    __tablename__ = 'Bairro'
    id = Column(Integer, primary_key=True)
    nome = Column(String(80))
    distrito_id = Column(Integer, ForeignKey('Distrito.id'))
    distrito = relationship('Distrito', lazy='subquery')
    __table_args__ = (UniqueConstraint('nome', 'distrito_id', name='bairro_UK'),)

    @property
    def dict(self):
        '''
        Retorna a representação do objeto como um dict.

        Retorno
        =======
        Dict -- representação do objeto como um dict.
        '''
        return {'nome': self.nome,
                'distrito': converter_dict(self.distrito)}


class Logradouro(bd.Model):
    '''
    Representa o logradouro.

    Atributos
    ==========
    id [int] -- id do logradouro.
    nome [str] -- nome do logradouro.
    '''
    __tablename__ = 'Logradouro'
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), unique=True)

    @property
    def dict(self):
        '''
        Retorna a representação do objeto como um dict.

        Retorno
        =======
        Dict -- representação do objeto como um dict.
        '''
        return {'nome': self.nome}


class Endereco(bd.Model):
    '''
    Representa o endereço.

    Atributos
    ==========
    id [int] -- id do endereço.
    logradouro_id [int] -- id do logradouro do endereço.
    logradouro [Logradouro] -- logradouro do endereço.
    numero [str] -- número do logradouro do endereço.
    referencia [str] -- ponto de referência da localização do endereço.
    bairro_id [int] -- id do bairro do endereço.
    bairro [Bairro] -- bairro do endereço.
    regiao5_id [int] -- id da regiao5 do endereço.
    regiao5 [regiao5] -- regiao5 do endereço.
    regiao8_id [int] -- id da regiao8 do endereço.
    regiao8 [regiao8] -- regiao8 do endereço.
    latitude [float] -- latitude da localização do endereço no território \
    do Município.
    longitude [float] -- longitude da localização do endereço no território \
    do Município.
    setor_censitario [str] -- setor censitário do endereço.
    area_ponderacao [str] -- área de ponderação (agrupamento de setores \
    censitários) do endereço.
    '''
    __tablename__ = 'Endereco'
    id = Column(Integer, primary_key=True)
    logradouro_id = Column(Integer, ForeignKey('Logradouro.id'))
    logradouro = relationship('Logradouro', lazy='subquery')
    numero = Column(String(10))
    referencia = Column(String(255))
    bairro_id = Column(Integer, ForeignKey('Bairro.id'))
    bairro = relationship('Bairro', lazy='subquery')
    regiao5_id = Column(Integer, ForeignKey('Regiao5.id'))
    regiao5 = relationship('Regiao5', lazy='subquery')
    regiao8_id = Column(Integer, ForeignKey('Regiao8.id'))
    regiao8 = relationship('Regiao8', lazy='subquery')
    latitude = Column(Float)
    longitude = Column(Float)
    setor_censitario = Column(String(50))
    area_ponderacao = Column(String(50))
    __table_args__ = (UniqueConstraint('logradouro_id', 'bairro_id',
                                       'regiao5_id', 'regiao8_id',
                                       'numero', 'latitude', 'longitude',
                                       name='endereco_UK'),)

    @property
    def dict(self):
        '''
        Retorna a representação do objeto como um dict.

        Retorno
        =======
        Dict -- representação do objeto como um dict.
        '''
        return {'logradouro': converter_dict(self.logradouro),
                'numero': self.numero,
                'referencia': self.referencia,
                'bairro': converter_dict(self.bairro),
                'regiao5': converter_dict(self.regiao5),
                'regiao8': converter_dict(self.regiao8),
                'latitude': self.latitude,
                'longitude': self.longitude,
                'setor_censitario': self.setor_censitario,
                'area_ponderacao': self.area_ponderacao}


class FeiraLivre(bd.Model):
    '''
    Representa a feira livre.

    Atributos
    ==========
    id [int] -- id da feira livre.
    identificador [int] -- número de identificação do estabelecimento \
    georreferenciado.
    nome [str] -- nome da feira livre.
    registro [str] -- registro da feira livre.
    endereco_id [int] -- id do endereço onde se localiza a feira livre.
    endereco [Endereco] -- endereço onde se localiza a feira livre.
    '''
    __tablename__ = 'FeiraLivre'
    id = Column(Integer, primary_key=True)
    identificador = Column(Integer)
    nome = Column(String(80))
    registro = Column(String(50), unique=True)
    endereco_id = Column(Integer, ForeignKey('Endereco.id'))
    endereco = relationship('Endereco', lazy='subquery')

    @property
    def dict(self):
        '''
        Retorna a representação do objeto como um dict.

        Retorno
        =======
        Dict -- representação do objeto como um dict.
        '''
        return {'identificador': self.identificador,
                'nome': self.nome,
                'registro': self.registro,
                'endereco': converter_dict(self.endereco)}
