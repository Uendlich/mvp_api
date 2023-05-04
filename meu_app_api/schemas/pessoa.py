from pydantic import BaseModel
from typing import  List
from model.pessoa import PessoaModel


class PessoasSchema(BaseModel):
    """ Define como uma nova Pessoa a ser inserido deve ser representada
    """
    nome =  "Nome Sobrenome "
    tipo_pessoa = "F"
    cpf_cnpj = "XXX.XXX.XXX-XX"
    estado_civil = "S"
    endereco =  "Minha rua,numero  bairro - cidade -estado - Cep: xxxxx-xxx"
    telefone = "(XX) XXXXX-XXXX"
    email  = "meuemail@gmail.com"


class PessoaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no ID da Pessoa.
       ID = 0 
    """
    id_pessoa: int = 0

class ListagemPessoasschema(BaseModel):
    """ Define como uma listagem de Pessoa será retornada.
    """
    pessoa:List[PessoasSchema]    

def apresenta_pessoas(pessoa: List[PessoaModel]):
    """ Retorna uma representação do pessoa seguindo o schema definido em
        PessoaViewSchema.
    """
    result = []
    for pessoa in pessoa:
        result.append({
           'id_pessoa'  : pessoa.id_pessoa,
           'nome' : pessoa.nome,
           'tipo_pessoa' : pessoa.tipo_pessoa,
           'cpf_cnpj' : pessoa.cpf_cnpj,
           'estado_civil' : pessoa.estado_civil,
           'endereco' : pessoa.endereco,
           'telefone' : pessoa.telefone,
           'email' : pessoa.email
        })

    return {"Pessoas": result}

class PessoaViewSchema(BaseModel):
    """ Define como uma Pessoa será retornada: Pessoa 
    """
    id_pessoa = "0"
    nome =  "Nome Sobrenome "
    tipo_pessoa = "F"
    cpf_cnpj = "XXX.XXX.XXX-XX"
    estado_civil = "S"
    endereco =  "Minha rua,numero  bairro - cidade -estado - Cep: xxxxx-xxx"
    telefone = "(XX) XXXXX-XXXX"
    email  = "meuemail@gmail.com"

class PessoaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str    

def apresenta_pessoa(pessoa: PessoaModel):
    """ Retorna uma representação de uma Pessoa seguindo o schema definido em
        PessoaViewSchema.
    """
    return {
        'id_pessoa'  : pessoa.id_pessoa,
        'nome' : pessoa.nome,
        'tipo_pessoa' : pessoa.tipo_pessoa,
        'cpf_cnpj' : pessoa.cpf_cnpj,
        'estado_civil' : pessoa.estado_civil,
        'endereco' : pessoa.endereco,
        'telefone' : pessoa.telefone,
        'email' : pessoa.email
    }
def apresenta_nome_pessoa(pessoa: PessoaModel):
    """ Retorna uma representação de uma Pessoa seguindo o schema definido em
        PessoaViewSchema.
    """
    return {
           'nome' : pessoa.nome
    }
    
class PessoaSchema(BaseModel):
    """ Define como uma Pessoa a ser passada para Atualização
    """
    nome =  "Nome Sobrenome "
    tipo_pessoa = "F"
    cpf_cnpj = "XXX.XXX.XXX-XX"
    estado_civil = "S"
    endereco =  "Minha rua,numero  bairro - cidade -estado - Cep: xxxxx-xxx"
    telefone = "(XX) XXXXX-XXXX"
    email  = "meuemail@gmail.com"