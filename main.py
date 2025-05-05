from fastapi import FastAPI,Query, Path, Body,  HTTPException
from pydantic import BaseModel,Field
from typing import Annotated, Literal

#->>>>>>>>>>>>>>>>>>>>> ORGANIZAR O CODIGO E PERGUNTAR PARA O CLEBINHO O QUE TEM QUE FAZER E SE ESTOU NO CAMINHO CERTO
app = FastAPI()

# inicial no fastapi
@app.get('/')
async def root():
    return{'message':'Hello World'}


#personagens e idades de cada um deles
crepusculo_idade = {
    1: {"Nome": "Edward Cullen", "idade": 104}, 
    2: {"Nome": "Isabella Swanaria", "idade": 18},
    3: {"Nome": "Jacob Black", "idade": 16},
    4: {"Nome": "Renesmee Cullen", "idade": 104}, 
    5: {"Nome": "Alice Cullen", "idade": 104},
    6: {"Nome": "Jasper Hale", "idade": 120},
    7: {"Nome": "Rosalie Hale", "idade": 90},
    8: {"Nome": "Esme Cullen", "idade": 100},
    9: {"Nome": "Emmett Cullen", "idade": 105},
    10: {"Nome": "Charlie Swan", "idade": 40}
}

# exemplo de quest parameters
crepusculo_personagens = {
    1 : {"personagem": "Edward Cullen",     "ator": "Robert Pattinson"},
    2 : {"personagem": "Isabella Swan",     "ator": "Kristen Stewart"},
    3 : {"personagem": "Jacob Black",       "ator": "Taylor Lautner"},
    4 : {"personagem": "Renesmee Cullen",   "ator": "Mackenzie Foy"},
    5 : {"personagem": "Alice Cullen",      "ator": "Ashley Greene"},
    6 : {"personagem": "Jasper Hale",       "ator": "Jackson Rathbone"},
    7 : {"personagem": "Rosalie Hale",      "ator": "Nikki Reed"},
    8 : {"personagem": "Esme Cullen",       "ator": "Elizabeth Reaser"},
    9 : {"personagem": "Emmett Cullen",     "ator": "Kellan Lutz"},
    10 : {"personagem": "Charlie Swan",      "ator": "Billy Byrke"}
}


#selecionar todos os personagens
@app.get("/todos/")
async def root():
    return {"Todos os personagens":list(crepusculo_idade.values())}

#procurar por id
@app.get("/personagem/{item_id}")
async def read_item(item_id: int):
    chaves = crepusculo_idade.keys()
    print(chaves)
    if item_id not in chaves:
        return {"mensagem": "Idade e personagem não encontrado"}
    return f"Personagem: {crepusculo_idade[item_id]}"
#procurar atores e seus personagens
@app.get("/todos-atores/{item_id}")
async def read_item(item_id: int):
    chaves = crepusculo_personagens.keys()
    print(chaves)
    if item_id not in chaves:
        return {"mensagem": "Peronagem e ator não encontrado"}
    return f"Ator: {crepusculo_personagens[item_id]}"

#criei a class para editaar no put que faz parte do crud - CREAT, READ, UPDATE, DELETE
class Editar(BaseModel):
    name: str
    idade: int
#esse de baixo é o o upgreatM -> UPDATE
@app.put("/editar_Atores/{editar_id}")
async def update_item(editar_id: int, editar: Editar):
    return {"todos-atores": editar_id, **editar.dict()}


#corpo da requisição - POST CREAT
class Perso(BaseModel):
    name: str
    ator: str
    idade: int
@app.post("/perso/")
async def create_item(perso: Perso):
    print(perso.model_dump())
    return perso


#Parâmetros de rota da URL
@app.get("/pesquisa/")
async def filmes_item(skip: int = 0, limit: int = 5):
    crepusculo_lancamento = [
       {"Crepúsculo": "2008"},
       {"Lua Nova": "2009"},
       {"Eclipse": "2010"},
       {"Amanhecer Parte 1": "2011"},
       {"Amanhecer Parte 2": "2012"},
    ]
    return crepusculo_lancamento[skip : skip + limit]


crepusculo_personagens_str = [
    "Edward Cullen",
    "Isabella Swan",
    "Renesmee Cullen",
    "Jacob Black",
    "Alice Cullen",
    "Jasper Hale",
    "Rosalie Hale",
    "Esme Cullen",
    "Emmett Cullen",
    "Charlie Swan"
]


#Parâmetros de consulta e validações de texto -> Lista de parâmetros de consulta / múltiplos valores
@app.get("/consulta-por-nome/")
async def read_items(nome: str | None = Query(default=None, title="Valor de consulta padrão Nulo", description="Se não for str ele será como nulo, e se ele for nulo, ele entrega tudo")):
    if nome:
        personagem_encontrado = [personagem for personagem in crepusculo_personagens_str if personagem.lower().startswith(nome.lower())]
        
        if personagem_encontrado:
            return {"Mensagem": f"O personagem encontrado foi: {', '.join(personagem_encontrado)}. :D"}
        else:
            return {"Mensagem": "Querido usuário, infelizmente nenhum personagem foi encontrado."}
    else:
        return {"Mensagem": "Pesquisa alguma coisa uai :/"}


#Parâmetros de rota e validações numéricas -> não consegui fazer pesquisar por str, ele pesquisa por id
@app.get("/pesquisar-atoreszin/{item_id}")
async def read_items_miaor_igual(
    *, item_id: int = Path( title="The ID of the item to get", ge=1, le=10), q: str=None):#se eu for procurar o 11 não será possivel, visto que só tem de 1 até 10 e não menos que isso
    results = {"ID": item_id}
    
    perso = crepusculo_idade.get(item_id)
    if perso:
        results.update({"Nome do Personagem": perso['Nome'], "Idade":perso["idade"]})
    if q:
        results.update({"Consulta Adicional": q})
    return results


#Modelos de parâmetro de Consulta
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/personagenzin-crep/")
async def read_items(filter_query: FilterParams = Query()):
    comeco = filter_query.offset
    final = comeco + filter_query.limit
    
    chamandoo_itens = list(crepusculo_idade.items())[comeco:final]
    
    results = {
        "total": len(crepusculo_idade),
        "limit": filter_query.limit,
        "offset": filter_query.offset,
        "items": [{"ID": item[0], "O personagem é": item[1]["Nome"], "Sua idade é": item[1]["idade"]} for item in chamandoo_itens]
    }
    return results



#Deletar personagem / DELETE
@app.delete("/deletar/{item_id}", status_code= 200)
async def delete_personagem(item_id:int):
    if item_id in crepusculo_personagens:
        del crepusculo_personagens [item_id]
        return[""{"Personagem apagado"}]
    raise HTTPException(status_code=404, detail="O personagem não foi encontrado ;(")





##FALTA ESSES --------------------------------------------------------------------------

#também do Modelos de parâmetro de Consulta (apenas modelo)
class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query




# esse é do corpo - multiplos parametros
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

#esse é do corpo - multiplos parâmetros
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]=0):
    results = {
        "item_id": item_id,
        "item": item,
        "user": user,
        #a variavel importance nesse caso vai ser enviada no corpo da requisição
        "importance": importance
    }
    return results


#esse é do corpo - campos
class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results

#Esse é o corpo - modelos aninhados
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set() #ele não permite repetir valores iguais tipo: "tags": ["dollas", "dollar", "dollar"]

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    print(results) #essa linha foi adicionada pelo clebinho
    return results


#Esse é corpo modelos aninhados -> defina o sub-modelo
#é basicamente um dicionario dentro do outro
class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

#-> primeiro dicionario :)
{ 
    "name": "string",
    "description": "string",
    "price": 0,
    "tax": 0,
    "tags": [],
    #-> segundo dicionario, ele está dentro do primeiro:
    "image": { 
        "url": "string",
        "name": "string"
    }
}







'''
#annotated força em serve para escrever mais que um tipo de dado

@app.get("/testezinho/")
async def read_teste(q: list[str] = Query(default=["foo", "bar"])):
    query_items = {"q": q}
    return query_items
'''



"""
ge = maior ou igual
gt = maior que
le = menor ou igual
lt = menor que
"""



"""
@app.get("/items/{item_id}")
async def read_items_miaor_igual(
    *, item_id: int = Path(title="The ID of the item to get", ge=1, le=16), q: str):#se eu for procurar o 17 não será possivel, visto que só tem de 1 até 16 e não menos que isso
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
"""


#esse é o modelo de pârametros de consulta -> Parâmetros de Consulta com um Modelo Pydantic
"""
from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

-- ESSE É O MODELO DE PAÂMETROS DE CONSULTA

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
"""





"""from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query"""
    



#esse é o corpo - múltiplos parâmetros -> Misture Path, Query e parâmetros de corpo¶

"""from typing import Annotated

from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results"""
    
    
    

#esse é o corpo - campos -> Importe Field¶

"""from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]=0):
    results = {
        "item_id": item_id,
        "item": item,
        "user": user,
        #a variavel importance nesse caso vai ser enviada no corpo da requisição
        "importance": importance
    }
    return results"""
#-----------------------------------------------------

"""from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results"""
    
    
    
    
#esse é o corpo modelos aninhados -> Campos do tipo Lista
"""from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set() #ele não permite repetir valores iguais tipo: "tags": ["dollas", "dollar", "dollar"]

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    print(results) #essa linha foi adicionada pelo clebinho
    return results"""
    
#----------------------------------------------------------------------------------------------------------#
    
"""from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#é basicamente um dicionario dentro do outro
class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results"""




"""
{ -> primeiro dicionario :)
  "name": "string",
  "description": "string",
  "price": 0,
  "tax": 0,
  "tags": [],
  "image": { -> segundo dicionario, ele está dentro do primeiro
    "url": "string",
    "name": "string"
  }
}
"""