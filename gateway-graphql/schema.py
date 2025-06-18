import graphene

class TelefoneInput(graphene.InputObjectType):
    numero = graphene.String(required=True)

class TelefoneType(graphene.ObjectType):
    numero = graphene.String()

class Contato(graphene.ObjectType):
    nome = graphene.String()
    categoria = graphene.String()
    telefones = graphene.List(TelefoneType)

class Query(graphene.ObjectType):
    contatos = graphene.List(Contato)

    def resolve_contatos(root, info):
        # Exemplo: retornar contatos com telefones
        return [
            Contato(
                nome="Fulano",
                categoria="Amigo",
                telefones=[TelefoneType(numero="9999-9999")]
            )
        ]

class AdicionarContato(graphene.Mutation):
    class Arguments:
        nome = graphene.String(required=True)
        categoria = graphene.String(required=True)
        telefones = graphene.List(TelefoneInput)

    ok = graphene.Boolean()
    contato = graphene.Field(lambda: Contato)

    def mutate(root, info, nome, categoria, telefones=None):
        # Lógica para adicionar contato e telefones
        novo_contato = Contato(
            nome=nome,
            categoria=categoria,
            telefones=[TelefoneType(numero=t.numero) for t in telefones] if telefones else []
        )
        ok = True
        return AdicionarContato(contato=novo_contato, ok=ok)

class Mutation(graphene.ObjectType):
    adicionar_contato = AdicionarContato.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)