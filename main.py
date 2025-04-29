from fastapi import FastAPI,Query, Path
from typing import Union
from pydantic import BaseModel
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
    4: {"Nome": "Renesmee Cullen", "idade": 4}, 
    5: {"Nome": "Alice Cullen", "idade": 104},
    6: {"Nome": "Jasper Hale", "idade": 120},
    7: {"Nome": "Rosalie Hale", "idade": 90},
    8: {"Nome": "Esme Cullen", "idade": 100},
    9: {"Nome": "Emmett Cullen", "idade": 105},
    10: {"Nome": "Charlie Swan", "idade": 40}
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

#procurar atores e seus personagens
@app.get("/todos-atores/{item_id}")
async def read_item(item_id: int):
    chaves = crepusculo_personagens.keys()
    print(chaves)
    if item_id not in chaves:
        return {"mensagem": "Peronagem e ator não encontrado"}
    return f"Ator: {crepusculo_personagens[item_id]}"

#criei a class para editaaar no put que faz parte do crud - CREAT, READ, UPDATE, DELETE
class Editar(BaseModel):
    name: str
    idade: int
#é o upgreat
@app.put("/editar_Atores/{editar_id}")
async def update_item(editar_id: int, editar: Editar):
    return {"todos-atores": editar_id, **editar.dict()}


#corpo da requisição
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


"""@app.get("/items/")
async def read_items(
        q: Union[str, None] = Query(
            default=None, 
            max_length=50,
            min_length=3,
            pattern="^[^\W\d_]{3}$", #pattern de 3 caracteres
            title = "título do item",
            description= "descrição sobre o item deve ser STR!"
        )
    ):
        results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
        if q:
            results.update({"q": q})
        return results
    
    
    
    
@app.get("/items/")
async def read_items(q: list[str] | None= Query(default=None, title= "Valor de consulta padrão Nulo", description="Olá bom dia/boa tarde/boa noite amigos!")):
    query_items = {"q":q}
    return query_items

#annotated força em serve para escrever mais que um tipo de dado

@app.get("/testezinho/")
async def read_teste(q: list[str] = Query(default=["foo", "bar"])):
    query_items = {"q": q}
    return query_items

"""


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
"""
from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


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