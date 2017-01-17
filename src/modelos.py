''' Módulo responsável por definir os modelos que representam a base de dados. '''

from src.basedados import bd


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
    id = bd.Column(bd.Integer, primary_key=True)
    codigo = bd.Column(bd.String(5))
    nome = bd.Column(bd.String(80))

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
    id = bd.Column(bd.Integer, primary_key=True)
    codigo = bd.Column(bd.String(5))
    nome = bd.Column(bd.String(80))
    subprefeitura_id = bd.Column(bd.Integer, bd.ForeignKey('Subprefeitura.id'))
    subprefeitura = bd.relationship('Subprefeitura')

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
    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String(80))

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
    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String(80))

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
    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String(80))
    distrito_id = bd.Column(bd.Integer, bd.ForeignKey('Distrito.id'))
    distrito = bd.relationship('Distrito')

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
    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String(80))

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
    latitude [real] -- latitude da localização do endereço no território do Município.
    longitude [real] -- longitude da localização do endereço no território do Município.
    setor_censitario [str] -- setor censitário do endereço.
    area_ponderacao [str] -- área de ponderação (agrupamento de setores censitários) do endereço.
    '''
    __tablename__ = 'Endereco'
    id = bd.Column(bd.Integer, primary_key=True)
    logradouro_id = bd.Column(bd.Integer, bd.ForeignKey('Logradouro.id'))
    logradouro = bd.relationship('Logradouro')
    numero = bd.Column(bd.String(10))
    referencia = bd.Column(bd.String(255))
    bairro_id = bd.Column(bd.Integer, bd.ForeignKey('Bairro.id'))
    bairro = bd.relationship('Bairro')
    regiao5_id = bd.Column(bd.Integer, bd.ForeignKey('Regiao5.id'))
    regiao5 = bd.relationship('Regiao5')
    regiao8_id = bd.Column(bd.Integer, bd.ForeignKey('Regiao8.id'))
    regiao8 = bd.relationship('Regiao8')
    latitude = bd.Column(bd.Numeric)
    longitude = bd.Column(bd.Numeric)
    setor_censitario = bd.Column(bd.String(50))
    area_ponderacao = bd.Column(bd.String(50))

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
    identificador [int] -- número de identificação do estabelecimento georreferenciado.
    nome [str] -- nome da feira livre.
    registro [str] -- registro da feira livre.
    endereco_id [int] -- id do endereço onde se localiza a feira livre.
    endereco [Endereco] -- endereço onde se localiza a feira livre.
    '''
    __tablename__ = 'FeiraLivre'
    id = bd.Column(bd.Integer, primary_key=True)
    identificador = bd.Column(bd.Integer)
    nome = bd.Column(bd.String(80))
    registro = bd.Column(bd.String(50))
    endereco_id = bd.Column(bd.Integer, bd.ForeignKey('Endereco.id'))
    endereco = bd.relationship('Endereco')

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
