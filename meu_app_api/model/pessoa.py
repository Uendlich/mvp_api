from sqlalchemy import Column, String, Integer, DateTime
from model import Base
from logger import logger

class PessoaModel(Base):
    __tablename__ = 'pessoa'
    
    id_pessoa = Column(Integer, primary_key = True)
    nome =  Column(String(255), nullable=False) 
    tipo_pessoa  =  Column(String(1), nullable=False) 
    cpf_cnpj = Column(String(20), unique=True) 
    estado_civil =  Column(String(1)) 
    endereco =  Column(String(2000)) 
    telefone = Column(String(20)) 
    email  = Column(String(255)) 

    def __init__(self, nome:str,tipo_pessoa :str,cpf_cnpj:str,
                 estado_civil:str,endereco:str,telefone:str,email:str):
        """
        Cria uma Pessoa

        Arguments:
            nome =  Nome Completo da Pessoa
            tp_pessoa =  Tipo de Pessoa (F=Física J=Jurídica )
            cpf_cnpj =  CPF ou CNPJ da Pessoa
            estado_civil = Estado Civil (S=Solteiro,C=Casado,D=Divorsiado,V=Viuvo,N=Não informar)
            edereco =  Edereço da Pessoa
            telefone = Telefone da Pessoa
            email  = E-mail da pessoa         
        """
        self.nome = nome 
        self.tipo_pessoa  = tipo_pessoa  
        self.cpf_cnpj = cpf_cnpj 
        self.estado_civil = estado_civil 
        self.endereco = endereco 
        self.telefone = telefone 
        self.email = email 
        
        
    


