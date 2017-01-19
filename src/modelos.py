''' Módulo responsável por definir os modelos que representam a base de \
dados. '''

from src.basedados import bd
from src.excecoes import ViolacaoIndiceUnico
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
    modelo [Modelo] -- modelo.
    commit [bool] -- informa se faz ou não commit na sessão.
    kwargs -- informações pelas qual a entidade será \
    procurada ou criada.

    Retorno
    =======
    instância do modelo que foi encontrada ou criada.

    Exceções/Erros
    ==============
    ViolacaoIndiceUnico
    '''
    consulta = sessao.query(modelo).filter_by(**kwargs)
    instancia = consulta.first()
    if instancia:
        return instancia
    else:
        ocorreu_violacao, indices = verificar_violacao_indice_unico(sessao,
                                                                    modelo,
                                                                    **kwargs)
        if ocorreu_violacao:
            raise ViolacaoIndiceUnico('Um(a) novo(a) {0} deve conter valores '
                                      'diferentes em {1}.'
                                      .format(modelo.__table__.name,
                                              ', '.join(indices)))
        instancia = modelo(**kwargs)
        sessao.add(instancia)
        if commit:
            sessao.commit()
        sessao.flush()
        return instancia


def verificar_violacao_indice_unico(sessao, modelo, **kwargs):
    '''
    Verifica se existe violação da restrição de índice único e quais \
    as colunas que estão relacionadas com essa violação.

    Parâmetros
    ==========
    sessao [Session] -- sessão.
    modelo [Modelo] -- modelo.
    kwargs -- informações.

    Retorno
    =======
    [bool, List] -- True se as informações fornecidas geram uma instancia \
    que tem violação do índice único; False caso contrário. A lista contém \
    os nomes das colunas cujos valores violaram a restrição de índice.
    '''
    indices = modelo.recuperar_indices_chave_unica()
    dados_indice = dict()
    for i in indices:
        if isinstance(i, list):
            for indice in i:
                if indice in kwargs:
                    dados_indice[indice] = kwargs[indice]
                else:
                    dados_indice[indice] = None
        else:
            if i in kwargs:
                dados_indice[i] = kwargs[i]
            else:
                dados_indice[i] = None
        instancia = sessao.query(modelo).filter_by(**dados_indice).first()
        if instancia is not None and isinstance(i, list):
            return True, i
        if instancia is not None:
            return True, [i]
    return False, []


class Modelo(bd.Model):
    ''' Classe abstrata que deve ser estendida pelos modelos da aplicação. '''
    __abstract__ = True

    @classmethod
    def recuperar_indices_chave_unica(cls):
        '''
        Recupera as colunas que pertencem a um índice de chave única.

        Retorno
        =======
        List [str, tuple(str)] -- nomes das colunas que pertencem a um \
        índice de chave única.
        '''
        indices_chave_unica = list()
        for coluna in cls.__table__.columns:
            if coluna.unique:
                indices_chave_unica.append(coluna.name)
        if hasattr(cls, '__table_args__'):
            for arg in cls.__table_args__:
                if type(arg) is UniqueConstraint:
                    varias_colunas = list()
                    for coluna in arg.columns:
                        varias_colunas.append(coluna.name)
                    indices_chave_unica.append(varias_colunas)
        return indices_chave_unica


class Subprefeitura(Modelo):
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


class Distrito(Modelo):
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


class Regiao5(Modelo):
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


class Regiao8(Modelo):
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


class Bairro(Modelo):
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


class Logradouro(Modelo):
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


class Endereco(Modelo):
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


class FeiraLivre(Modelo):
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
