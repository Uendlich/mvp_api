from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, redirect
from urllib.parse import unquote
from flask import request, jsonify

from sqlalchemy.exc import IntegrityError

from model import Session
from model.pessoa import PessoaModel
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
pessoa_tag = Tag(name="Pessoa", description="Adição, visualização e remoção de Pessoas à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/pessoa', tags=[pessoa_tag],
          responses={"200": PessoaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def criar_pessoa():
    # obtém os dados da nova pessoa a partir do corpo da requisição
    dados = request.json
    nome = dados.get('nome')
    tipo_pessoa = dados.get('tipo_pessoa')
    cpf_cnpj = dados.get('cpf_cnpj')
    estado_civil = dados.get('estado_civil')
    endereco = dados.get('endereco')
    telefone = dados.get('telefone')
    email = dados.get('email')

    # cria um objeto da classe Pessoa com os dados recebidos
    nova_pessoa = PessoaModel(nome=nome, tipo_pessoa=tipo_pessoa, cpf_cnpj=cpf_cnpj, estado_civil=estado_civil, endereco=endereco, telefone=telefone, email=email)
    logger.debug(f"Adicionando a pessoa de nome: '{nova_pessoa.nome}'") 
    try: 
        session = Session() 
        # adiciona a nova pessoa ao banco de dados
        session.add(nova_pessoa)
        session.commit()
        logger.debug(f"Adicionado a pessoa de nome: '{nova_pessoa.nome}'")
        # retorna os dados da nova pessoa criada como resposta da requisição
        return jsonify({
            'id_pessoa': nova_pessoa.id_pessoa,
            'nome': nova_pessoa.nome,
            'tipo_pessoa': nova_pessoa.tipo_pessoa,
            'cpf_cnpj': nova_pessoa.cpf_cnpj,
            'estado_civil': nova_pessoa.estado_civil,
            'endereco': nova_pessoa.endereco,
            'telefone': nova_pessoa.telefone,
            'email': nova_pessoa.email
        }), 200
    except IntegrityError as e:
            # como a duplicidade de CPF ou CNPJ(Documento) é a provável razão do IntegrityError
            error_msg = "Pessoa de mesmo documento já salvo na base :/"
            logger.warning(f"Erro ao adicionar Pessoa com o documento '{nova_pessoa.nome,nova_pessoa.cpf_cnpj}', {error_msg}")
            return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar uma nova pessoa :/"
        logger.warning(f"Erro ao adicionar Pessoa '{nova_pessoa.nome}', {error_msg}")
        return {"mesage": error_msg}, 400

# Método GET
@app.get('/pessoas', tags=[pessoa_tag],
         responses={"200": ListagemPessoasschema, "404": ErrorSchema})
def get_pessoas():
    """Faz a busca por todas as Pessoas cadastrados
        Retorna uma representação da listagem de Pessoas.
    """
    logger.debug(f"Coletando Pessoas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pessoa = session.query(PessoaModel).all()
    
    if not pessoa:
        # se não há Pessoa cadastrada
        return {"pessoa": []}, 200
    else:
        logger.debug(f"%d pessoas econtrados" % len(pessoa))
        # retorna a representação de Pessoa
        print(pessoa)
        return apresenta_pessoas(pessoa), 200
    
# Método GET    
@app.get('/pessoa', tags=[pessoa_tag],
         responses={"200": PessoaViewSchema, "404": ErrorSchema})    
def get_pessoa(query:PessoaBuscaSchema):
    print("aqui")
    """Faz a busca por uma pessoa a partir do ID
    Retorna uma representação de Pessoas.
    """
    # busca a pessoa com o ID especificado no banco de dados
    id_pessoa = query.id_pessoa
    logger.debug(f"Coletando dados sobre Pessoa #{id_pessoa}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pessoa =  session.query(PessoaModel).filter(PessoaModel.id_pessoa == id_pessoa).first()
    if not pessoa:
        # se a Pessoa não foi encontrada
        error_msg = "Pessoa não encontrada na base :/"
        logger.warning(f"  Erro ao buscar Pessoa com ID '{id_pessoa}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Pessoa econtrada: '{pessoa.nome}'")
        # retorna a representação de Pessoa
        return apresenta_pessoa(pessoa), 200         
    
# Método DELETE
@app.delete('/pessoa', tags=[pessoa_tag],
            responses={"200": PessoaDelSchema, "404": ErrorSchema})
def del_pessoa(query:PessoaBuscaSchema):
    """Deleta ums Pessoa a partir do id informado
       Retorna uma mensagem de confirmação da remoção.
    """
    id_pessoa = query.id_pessoa
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pessoa =  session.query(PessoaModel).filter(PessoaModel.id_pessoa == id_pessoa).first()
    #busca o nome da pessoa 
    pessoa_nome = apresenta_nome_pessoa(pessoa)

    logger.debug(f"Deletando dados sobre a Pessoa #{pessoa_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(PessoaModel).filter(PessoaModel.id_pessoa == id_pessoa).delete()
    session.commit()
    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado Pessoa #{pessoa_nome}")
        return {"mesage": "Pessoa Removida", "Nome": pessoa_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Pessoa não encontrada na base :/"
        logger.warning(f"Erro ao deletar a Pessoa #'{pessoa_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    
    
    
@app.put('/pessoa', tags=[pessoa_tag],
          responses={"200": PessoaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def atualizar_pessoa():
    # obtém os dados da nova pessoa a partir do corpo da requisição
    dados = request.json    
    nome = dados.get('nome')
    #tipo_pessoa = dados.get('tipo_pessoa')
    cpf_cnpj = dados.get('cpf_cnpj')
    #estado_civil = dados.get('estado_civil')
    #endereco = dados.get('endereco')
    #telefone = dados.get('telefone')
    #email = dados.get('email')
    
     # criando conexão com a base
    session = Session()
    # Atualiza pessoa
    for e in dados:
        coluna = e
        valor = dados[e]                    
        session.query(PessoaModel).filter(PessoaModel.cpf_cnpj == cpf_cnpj).update({coluna: valor}) 
        session.commit()
    pessoa =  session.query(PessoaModel).filter(PessoaModel.cpf_cnpj == cpf_cnpj).first()
    logger.debug(f"Atualizando a pessoa de nome: '{nome}'") 
    try: 
        if pessoa:
           # retorna os dados da nova pessoa criada como resposta da requisição
           return jsonify({
                'id_pessoa': pessoa.id_pessoa,
                'nome': pessoa.nome,
                'tipo_pessoa': pessoa.tipo_pessoa,
                'cpf_cnpj': pessoa.cpf_cnpj,
                'estado_civil': pessoa.estado_civil,
                'endereco': pessoa.endereco,
                'telefone': pessoa.telefone,
                'email': pessoa.email
           }), 200
        else:
           # se o produto não foi encontrado
           error_msg = "Pessoa não encontrada na base :/"
           logger.warning(f"Não foi possivel atualizar a Pessoa #'{pessoa.nome}', {error_msg}")
           return {"mesage": error_msg}, 404

    except Exception as e:
        # Caso erro 
        error_msg = "Não foi possível atualizar pessoa :/"
        logger.warning(f"Erro ao atualizar Pessoa '{pessoa.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
