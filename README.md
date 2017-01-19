# FeirasLivresApi

[![Build Status](https://travis-ci.org/brunabxs/FeirasLivresApi.svg?branch=master)](https://travis-ci.org/brunabxs/FeirasLivresApi)

A Prefeitura de São Paulo disponibiliza um arquivo CSV contendo informações sobre a localização de feiras livres que ocorrem no Estado.
Para que aplicações possam ser desenvolvidas utilizando essas informações, criamos uma API REST para facilitar o acesso a essas informações.

## O que utilizamos?
- [Python (v3.6)](https://www.python.org/): Linguagem de programação escolhida.
- [Flask (v0.12)](http://flask.pocoo.org/): Microframework para construir aplicações web.
- [Flask-SQLAlchemy (v2.1)](http://flask-sqlalchemy.pocoo.org/2.1/): Extensão do Flask com suporte para o SQLAlchemy, que por sua vez, dá suporte ao SQLite.
- [SQLite (v3.16.2)](https://sqlite.org/): Banco de dados escolhido para armazenamento dos dados fornecidos pela Prefeitura de São Paulo.
- [unittest](https://docs.python.org/3/library/unittest.html): Framework de teste unitário nativo.
- [Coverage (v4.3.1)](https://pypi.python.org/pypi/coverage): Ferramenta de cobertura.
- [Travis CI](https://travis-ci.org/): Ferramenta de integração contínua.

## Funcionalidades
### Cadastro de uma nova feira
#### Requisição HTTP 
```
POST /feira
```
#### Parâmetros de consulta
Não oferece.
#### Corpo da Requisição
Forneça todos os campos.

| Nome do parâmetro     | Valor    | Descrição                                                                  |
| --------------------- | -------- | -------------------------------------------------------------------------- |
| identificador         | int      | número de identificação do estabelecimento georreferenciado                |
| latitude              | float    | latitude da localização do endereço no território do Município.            |
| longitude             | float    | longitude da localização do endereço no território do Município.           |
| setor_censitario      | string   | setor censitário conforme IBGE                                             |
| area_ponderacao       | string   | área de ponderação (agrupamento de setores censitários) conforme IBGE 2010 |
| cod_distrito          | string   | código do Distrito Municipal conforme IBGE                                 |
| distrito              | string   | nome do Distrito Municipal                                                 |
| cod_subpref           | string   | código de cada uma das 31 Subprefeituras (2003 a 2012)                     |
| subprefeitura         | string   | nome da Subprefeitura (31 de 2003 até 2012)                                |
| regiao5               | string   | região conforme divisão do Município em cinco áreas                        |
| regiao8               | string   | região conforme divisão do Município em oito áreas                         |
| nome                  | string   | denominação da feira livre atribuída pela Supervisão de Abastecimento      |
| registro              | string   | número do registro da feira livre na PMSP                                  |
| logradouro            | string   | nome do logradouro onde se localiza a feira livre                          |
| numero                | string   | um número do logradouro onde se localiza a feira livre                     |
| bairro                | string   | bairro de localização da feira livre                                       |
| referencia            | string   | ponto de referência da localização da feira livre                          |

```
POST /feira
Content-Type: application/json

{
	"identificador": 1,
	"latitude": -46550164,
	"longitude": -23558733,
	"setor_censitario": "355030885000091",
	"area_ponderacao": "3550308005040",
	"cod_distrito": "87",
	"distrito": "VILA FORMOSA",
	"cod_subpref": "26",
	"subprefeitura": "ARICANDUVA-FORMOSA-CARRAO",
	"regiao5": "Leste",
	"regiao8": "Leste 1",
	"nome": "VILA FORMOSA",
	"registro": "4041-0",
	"logradouro": "RUA MARAGOJIPE",
	"numero": "S/N",
	"bairro": "VL FORMOSA",
	"referencia": "TV RUA PRETORIA"
}
```
#### Resposta HTTP
Se for um sucesso, o método retorna a feira livre no corpo da resposta.
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "feira": {
        "endereco": {
            "area_ponderacao": "3550308005040",
            "bairro": {
                "distrito": {
                    "codigo": "87",
                    "nome": "VILA FORMOSA",
                    "subprefeitura": {
                        "codigo": "26",
                        "nome": "ARICANDUVA-FORMOSA-CARRAO"
                    }
                },
                "nome": "VL FORMOSA"
            },
            "latitude": -46550164,
            "logradouro": {
                "nome": "RUA MARAGOJIPE"
            },
            "longitude": -23558733,
            "numero": "S/N",
            "referencia": "TV RUA PRETORIA",
            "regiao5": {
                "nome": "Leste"
            },
            "regiao8": {
                "nome": "Leste 1"
            },
            "setor_censitario": "355030885000091"
        },
        "identificador": 1,
        "nome": "VILA FORMOSA",
        "registro": "4041-0"
    }
}
```
#### Erros

| Código | Descrição                                                              |
| ------ | ---------------------------------------------------------------------- |
| 400    | Corpo da requisição não contém todos os parâmetros necessários         |
| 400    | Tentativa de cadastro de uma feira com mesmo registro de uma existente |
| 400    | Violação de índice único                                               |

### Busca de feiras
#### Requisição HTTP 
```
GET /feiras
```
#### Parâmetros de consulta
Ao menos um dos parâmetros é obrigatório.

| Nome do parâmetro     | Valor    | Descrição                                                   |
| --------------------- |:--------:| ----------------------------------------------------------- |
| nome                  | string   | nome da feira livre                                         |
| regiao5               | string   | nome da região conforme divisão do Município em cinco áreas |
| bairro                | string   | nome do bairro                                              |
| distrito              | string   | nome do distrito                                            |

#### Corpo da Requisição
Não oferece.
#### Resposta HTTP
Se for um sucesso, o método retorna as feiras livres no corpo da resposta.
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "feiras": [
        {
            "endereco": {
                "area_ponderacao": "3550308005044",
                "bairro": {
                    "distrito": {
                        "codigo": "27",
                        "nome": "CURSINO",
                        "subprefeitura": {
                            "codigo": "13",
                            "nome": "IPIRANGA"
                        }
                    },
                    "nome": "MOINHO VELHO"
                },
                "latitude": -23609187,
                "logradouro": {
                    "nome": "RUA LINO GUEDES"
                },
                "longitude": -46610849,
                "numero": "109.000000",
                "referencia": "ALTURA DA VERGUEIRO 7450",
                "regiao5": {
                    "nome": "Sul"
                },
                "regiao8": {
                    "nome": "Sul 1"
                },
                "setor_censitario": "355030827000078"
            },
            "identificador": 879,
            "nome": "CERRACAO",
            "registro": "4025-8"
        }
    ]
}
```
### Exclusão de feira
#### Requisição HTTP 
```
DELETE /feira
```
#### Parâmetros de consulta

| Nome do parâmetro     | Valor    | Descrição                                                   |
| --------------------- | -------- | ----------------------------------------------------------- |
| registro              | string   | registro da feira livre                                     |

#### Corpo da Requisição
Não oferece.
#### Resposta HTTP
Se for um sucesso, o método retorna a feira livre no corpo da resposta.
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "feira": {
        "endereco": {
            "area_ponderacao": "3550308005044",
            "bairro": {
                "distrito": {
                    "codigo": "27",
                    "nome": "CURSINO",
                    "subprefeitura": {
                        "codigo": "13",
                        "nome": "IPIRANGA"
                    }
                },
                "nome": "MOINHO VELHO"
            },
            "latitude": -23609187,
            "logradouro": {
                "nome": "RUA LINO GUEDES"
            },
            "longitude": -46610849,
            "numero": "109.000000",
            "referencia": "ALTURA DA VERGUEIRO 7450",
            "regiao5": {
                "nome": "Sul"
            },
            "regiao8": {
                "nome": "Sul 1"
            },
            "setor_censitario": "355030827000078"
        },
        "identificador": 879,
        "nome": "CERRACAO",
        "registro": "4025-8"
    }
}
```
#### Erros

| Código | Descrição                                                              |
| ------ | ---------------------------------------------------------------------- |
| 404    | Tentativa de exclusão de uma feira com registro inexistente            |

### Alteração de feira
#### Requisição HTTP 
```
PUT /feira
```
#### Parâmetros de consulta
Não oferece.
#### Corpo da Requisição
Forneça todos os campos.

| Nome do parâmetro     | Valor    | Descrição                                                                  |
| --------------------- | -------- | -------------------------------------------------------------------------- |
| identificador         | int      | número de identificação do estabelecimento georreferenciado                |
| latitude              | float    | latitude da localização do endereço no território do Município.            |
| longitude             | float    | longitude da localização do endereço no território do Município.           |
| setor_censitario      | string   | setor censitário conforme IBGE                                             |
| area_ponderacao       | string   | área de ponderação (agrupamento de setores censitários) conforme IBGE 2010 |
| cod_distrito          | string   | código do Distrito Municipal conforme IBGE                                 |
| distrito              | string   | nome do Distrito Municipal                                                 |
| cod_subpref           | string   | código de cada uma das 31 Subprefeituras (2003 a 2012)                     |
| subprefeitura         | string   | nome da Subprefeitura (31 de 2003 até 2012)                                |
| regiao5               | string   | região conforme divisão do Município em cinco áreas                        |
| regiao8               | string   | região conforme divisão do Município em oito áreas                         |
| nome                  | string   | denominação da feira livre atribuída pela Supervisão de Abastecimento      |
| registro              | string   | número do registro da feira livre na PMSP                                  |
| logradouro            | string   | nome do logradouro onde se localiza a feira livre                          |
| numero                | string   | um número do logradouro onde se localiza a feira livre                     |
| bairro                | string   | bairro de localização da feira livre                                       |
| referencia            | string   | ponto de referência da localização da feira livre                          |

```
PUT /feira
Content-Type: application/json

{
	"identificador": 1,
	"latitude": -46550164,
	"longitude": -23558733,
	"setor_censitario": "355030885000091",
	"area_ponderacao": "3550308005040",
	"cod_distrito": "87",
	"distrito": "VILA FORMOSA",
	"cod_subpref": "26",
	"subprefeitura": "ARICANDUVA-FORMOSA-CARRAO",
	"regiao5": "Leste",
	"regiao8": "Leste 1",
	"nome": "VILA FORMOSA",
	"registro": "4041-0",
	"logradouro": "RUA MARAGOJIPE",
	"numero": "S/N",
	"bairro": "VL FORMOSA",
	"referencia": "TV RUA PRETORIA"
}
```
#### Resposta HTTP
Se for um sucesso, o método retorna a feira livre no corpo da resposta.
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "feira": {
        "endereco": {
            "area_ponderacao": "3550308005040",
            "bairro": {
                "distrito": {
                    "codigo": "87",
                    "nome": "VILA FORMOSA",
                    "subprefeitura": {
                        "codigo": "26",
                        "nome": "ARICANDUVA-FORMOSA-CARRAO"
                    }
                },
                "nome": "VL FORMOSA"
            },
            "latitude": -46550164,
            "logradouro": {
                "nome": "RUA MARAGOJIPE"
            },
            "longitude": -23558733,
            "numero": "S/N",
            "referencia": "TV RUA PRETORIA",
            "regiao5": {
                "nome": "Leste"
            },
            "regiao8": {
                "nome": "Leste 1"
            },
            "setor_censitario": "355030885000091"
        },
        "identificador": 1,
        "nome": "VILA FORMOSA",
        "registro": "4041-0"
    }
}
```
#### Erros

| Código | Descrição                                                              |
| ------ | ---------------------------------------------------------------------- |
| 400    | Corpo da requisição não contém todos os parâmetros necessários         |
| 404    | Tentativa de alteração de uma feira com registro inexistente           |
| 400    | Violação de índice único                                               |

## Desenvolvimento
### Como importar os dados?
- Faça o download do arquivo (Pode ser encontrado em recursos/DEINFO_AB_FEIRASLIVRES_2014.csv)
- A partir do diretório raiz, instale as dependências
```
pip install -r requirements.txt
```
- Rode o script de criação/população do banco de dados
```
python script.py
```

### Como executar a aplicação?
- A partir do diretório raiz, instale as dependências
```
pip install -r requirements.txt
```
- Rode a aplicação
```
python app.py
```
- A aplicação sobe por padrão em [localhost:5000](localhost:5000)

### Como executar os testes?
- A partir do diretório raiz, instale as dependências
```
pip install -r requirements.txt
```
- Rode os testes
```
python -m unittest discover
```

### Como verificar a cobertura?
- A partir do diretório raiz, instale as dependências
```
pip install -r requirements.txt
```
- Rode o coverage
```
coverage run --branch --omit=test/* -m unittest discover
coverage html -d relatorios/coverage
```
- Abra o o arquivo relatorios/coverage/index.html gerado e veja o relatório de cobertura dos testes

### Como alterar o banco de dados utilizado?
Em config.py você encontra as configurações básicas da aplicação.

### Acompanhamento
Você pode acompanhar o desenvolvimento pelo [Trello](https://trello.com/b/t0Aew7m8/feiraslivresapi)
