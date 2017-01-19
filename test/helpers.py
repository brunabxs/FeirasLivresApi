''' Módulo responsável por definir alguns helpers para os testes. '''

from src.modelos import FeiraLivre, Endereco, Logradouro, Bairro
from src.modelos import Regiao8, Regiao5, Distrito, Subprefeitura


class FeiraLivreBuilder:
    '''
    Constrói uma FeiraLivre para auxiliar os testes.

    Atributos
    ==========
    bd [SQLAlchemy] -- instância do banco de dados onde objetos devem \
    ser persistidos.
    feira_livre [FeiraLivre] -- feira livre a ser construída.
    '''
    def __init__(self, bd=None):
        '''
        Construtor.

        Parâmetros
        ==========
        bd [SQLAlchemy] -- instância do banco de dados onde objetos devem \
        ser persistidos. (default=None)
        '''
        self.bd = bd
        self.feira_livre = FeiraLivre()
        self.feira_livre.endereco = Endereco()
        self.feira_livre.endereco.logradouro = Logradouro()
        self.feira_livre.endereco.regiao5 = Regiao5()
        self.feira_livre.endereco.regiao8 = Regiao8()
        self.feira_livre.endereco.bairro = Bairro()
        self.feira_livre.endereco.bairro.distrito = Distrito()
        self.feira_livre.endereco.bairro.distrito.subprefeitura = Subprefeitura()

    def with_identificador(self, identificador):
        '''
        Modifica o identificador da feira livre.

        Parâmetros
        ==========
        identificador [str] -- identificador da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.identificador = identificador
        return self

    def with_latitude(self, latitude):
        '''
        Modifica a latitude da localização da feira livre.

        Parâmetros
        ==========
        latitude [real] -- latitude da localização da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.endereco.latitude = latitude
        return self

    def with_longitude(self, longitude):
        '''
        Modifica a longitude da localização da feira livre.

        Parâmetros
        ==========
        longitude [real] -- longitude da localização da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.endereco.longitude = longitude
        return self

    def with_setor_censitario(self, setor_censitario):
        '''
        Modifica o setor censitário da feira livre.

        Parâmetros
        ==========
        setor_censitario [str] -- setor censitário da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.endereco.setor_censitario = setor_censitario
        return self

    def with_area_ponderacao(self, area_ponderacao):
        '''
        Modifica a area de ponderação da feira livre.

        Parâmetros
        ==========
        area_ponderacao [str] -- area de ponderação da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.endereco.area_ponderacao = area_ponderacao
        return self

    def with_cod_distrito(self, cod_distrito):
        '''
        Modifica o código do distrito da feira livre.

        Parâmetros
        ==========
        cod_distrito [str] -- código do distrito da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.endereco.bairro.distrito.codigo = cod_distrito
        return self

    def with_distrito(self, distrito):
        '''
        Modifica o distrito da feira livre.

        Parâmetros
        ==========
        distrito [str] -- distrito da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.endereco.bairro.distrito.nome = distrito
        return self

    def with_cod_subpref(self, cod_subpref):
        '''
        Modifica o código da subprefeitura da feira livre.

        Parâmetros
        ==========
        cod_subpref [str] -- código da subprefeitura da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.endereco.bairro.distrito.subprefeitura.codigo = cod_subpref
        return self

    def with_subprefeitura(self, subprefeitura):
        '''
        Modifica a subprefeitura da feira livre.

        Parâmetros
        ==========
        subprefeitura [str] -- subprefeitura da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.endereco.bairro.distrito.subprefeitura.nome = subprefeitura
        return self

    def with_regiao5(self, regiao5):
        '''
        Modifica a região 5 da feira livre.

        Parâmetros
        ==========
        regiao5 [str] -- região 5 da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.endereco.regiao5.nome = regiao5
        return self

    def with_regiao8(self, regiao8):
        '''
        Modifica a região 8 da feira livre.

        Parâmetros
        ==========
        regiao8 [str] -- região 8 da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.endereco.regiao8.nome = regiao8
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

    def with_logradouro(self, logradouro):
        '''
        Modifica o logradouro da feira livre.

        Parâmetros
        ==========
        logradouro [str] -- logradouro da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.endereco.logradouro.nome = logradouro
        return self

    def with_numero(self, numero):
        '''
        Modifica o número da feira livre.

        Parâmetros
        ==========
        numero [str] -- número da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.endereco.numero = numero
        return self

    def with_bairro(self, bairro):
        '''
        Modifica o bairro da feira livre.

        Parâmetros
        ==========
        bairro [str] -- bairro da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.endereco.bairro.nome = bairro
        return self

    def with_referencia(self, referencia):
        '''
        Modifica a referência da feira livre.

        Parâmetros
        ==========
        referencia [str] -- referência da feira livre.

        Retorno
        =======
        FeiraLivreBuilder -- instância do builder.
        '''
        self.feira_livre.endereco.referencia = referencia
        return self

    def from_dict(self, dado):
        '''
        Constrói a feira livre a partir de um dict.

        Parâmetros
        ==========
        dado [Dict] -- contém todas as informações para construir \
        uma feira livre.

        Retorno
        =======
        FeiraLivre -- instância da feira livre.
        '''
        self.with_identificador(dado['identificador']) \
            .with_latitude(dado['latitude']) \
            .with_longitude(dado['longitude']) \
            .with_setor_censitario(dado['setor_censitario']) \
            .with_area_ponderacao(dado['area_ponderacao']) \
            .with_cod_distrito(dado['cod_distrito']) \
            .with_distrito(dado['distrito']) \
            .with_cod_subpref(dado['cod_subpref']) \
            .with_subprefeitura(dado['subprefeitura']) \
            .with_regiao5(dado['regiao5']) \
            .with_regiao8(dado['regiao8']) \
            .with_nome(dado['nome']) \
            .with_registro(dado['registro']) \
            .with_logradouro(dado['logradouro']) \
            .with_numero(dado['numero']) \
            .with_bairro(dado['bairro']) \
            .with_referencia(dado['referencia'])
        return self

    def build(self):
        '''
        Gera a feira livre e persiste na base de dados se estiver definida.

        Retorno
        =======
        FeiraLivre -- instância da feira livre.
        '''
        subprefeitura = Subprefeitura.query \
                                     .filter(Subprefeitura.codigo == self.feira_livre.endereco.bairro.distrito.subprefeitura.codigo) \
                                     .first()
        if subprefeitura is not None:
            self.feira_livre.endereco.bairro.distrito.subprefeitura = subprefeitura
        distrito = Distrito.query \
                           .filter(Distrito.codigo == self.feira_livre.endereco.bairro.distrito.codigo) \
                           .first()
        if distrito is not None:
            self.feira_livre.endereco.bairro.distrito = distrito
        regiao5 = Regiao5.query.filter(Regiao5.nome == self.feira_livre.endereco.regiao5.nome).first()
        if regiao5 is not None:
            self.feira_livre.endereco.regiao5 = regiao5
        regiao8 = Regiao8.query.filter(Regiao8.nome == self.feira_livre.endereco.regiao8.nome).first()
        if regiao8 is not None:
            self.feira_livre.endereco.regiao8 = regiao8
        bairro = Bairro.query.filter(Bairro.nome == self.feira_livre.endereco.bairro.nome).first()
        if bairro is not None:
            self.feira_livre.endereco.bairro = bairro
        logradouro = Logradouro.query.filter(Logradouro.nome == self.feira_livre.endereco.logradouro.nome).first()
        if logradouro is not None:
            self.feira_livre.endereco.logradouro = logradouro
        endereco = Endereco.query \
                           .join(Endereco.logradouro) \
                           .join(Endereco.bairro) \
                           .join(Endereco.regiao5) \
                           .join(Endereco.regiao8) \
                           .filter(Logradouro.nome == self.feira_livre.endereco.logradouro.nome) \
                           .filter(Bairro.nome == self.feira_livre.endereco.bairro.nome) \
                           .filter(Regiao5.nome == self.feira_livre.endereco.regiao5.nome) \
                           .filter(Regiao8.nome == self.feira_livre.endereco.regiao8.nome) \
                           .filter(Endereco.numero == self.feira_livre.endereco.numero) \
                           .first()
        if endereco is not None:
            self.feira_livre.endereco = endereco

        if self.bd is not None:
            self.bd.session.add(self.feira_livre)
            self.bd.session.commit()
            self.bd.session.flush()

        return self.feira_livre
