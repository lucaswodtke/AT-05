from enum import Enum
import uuid

class TipoTelefone(Enum):
    MOVEL = "móvel"
    FIXO = "fixo"
    COMERCIAL = "comercial"

class CategoriaContato(Enum):
    FAMILIAR = "familiar"
    PESSOAL = "pessoal"
    COMERCIAL = "comercial"

class Telefone:
    def __init__(self, numero: str, tipo: TipoTelefone):
        if not isinstance(tipo, TipoTelefone):
            raise ValueError("Tipo de telefone inválido")
        self.numero = numero
        self.tipo = tipo

    def to_dict(self):
        return {
            "numero": self.numero,
            "tipo": self.tipo.name
        }

class Contato:
    def __init__(self, nome: str, categoria: CategoriaContato):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.telefones = []
        if not isinstance(categoria, CategoriaContato):
            raise ValueError("Categoria de contato inválida")
        self.categoria = categoria

    def adicionar_telefone(self, telefone: Telefone):
        if isinstance(telefone, Telefone):
            self.telefones.append(telefone)
        else:
            raise ValueError("Objeto Telefone inválido")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "telefones": [telefone.to_dict() for telefone in self.telefones],
            "categoria": self.categoria.name
        }

banco_de_dados_contatos = {}
