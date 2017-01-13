# FeirasLivresApi

[![Build Status](https://travis-ci.org/brunabxs/FeirasLivresApi.svg?branch=master)](https://travis-ci.org/brunabxs/FeirasLivresApi)

A Prefeitura de São Paulo disponibiliza um arquivo CSV contendo informações sobre a localização de feiras livres que ocorrem no Estado.
Para que aplicações possam ser desenvolvidas utilizando essas informações, criamos uma API REST para facilitar o acesso a essas informações.

## Backlog
Como ainda se encontra em desenvolvimento, você encontra o progresso no [Trello](https://trello.com/b/t0Aew7m8/feiraslivresapi)

## O que utilizamos?
- [Python (v3.6)](https://www.python.org/): Linguagem de programação escolhida.
- [Flask (v0.12)](http://flask.pocoo.org/): Microframework para construir aplicações web.
- [Flask-SQLAlchemy (v2.1)](http://flask-sqlalchemy.pocoo.org/2.1/): Extensão do Flask com suporte para o SQLAlchemy, que por sua vez, dá suporte ao SQLite.
- [SQLite (v3.16.2)](https://sqlite.org/): Banco de dados escolhido para armazenamento dos dados fornecidos pela Prefeitura de São Paulo.
- [unittest](https://docs.python.org/3/library/unittest.html): Framework de teste unitário nativo.
- [Coverage (v4.3.1)](https://pypi.python.org/pypi/coverage): Ferramenta de cobertura.
- [Travis CI](https://travis-ci.org/): Ferramenta de integração contínua.
