from fastapi import FastAPI, Query, Path
from enum import Enum
from schema.item import Item
from typing import Annotated
from schema.FilterParams import FilterParams

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/item/{item_id}")
async def get_item(item_id: int):
    return item_id

# order matters the path for /users/{user_id} would match also for /users/me, "thinking" that it's receiving a parameter user_id with a value of "me".
# so it is important to user /users/me before users/{user_id}


class EnumSample(str,Enum):
    enum1= 'blacksheep'
    enum2="blackhorse"
    enum3="darkk"

@app.get("/enum/{item}")
async def get_item(item: EnumSample):
    if item is EnumSample.enum1:
        return "black sheep"
    if item == EnumSample.enum2:
        return "black horse"
    if(item == EnumSample.enum3):
        return "dark"
    return item

@app.get("/files/{file_path}/{path_2}")
async def read_file(file_path: str, path2: str):
    return {"file_path": file_path + path2}

# if parameter contains a path
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


## query parameters


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
# optional parameters
@app.get("/queryitems/")
async def read_item(skip: int=0, limit : int|None = None):
    if limit:
        return fake_items_db[skip: skip+limit]
    else:
        return fake_items_db[skip:]
    
@app.get("/querybol/")
async def  read_item(q: bool = False):
    if q:
        return "the query parameter was true" # will run on q=1,yes,true, True
    else:
        return "query paramet was false" # q=0,no,false,False
    

@app.post("/item")
async def create_item(item: Item):
    # initialy the item has a type of Item
    items_dict = item.dict()# converting it to dict so it is serializable

    if item.tax is None:
        items_dict["tax"] = 12.43
    return items_dict
    # return item this return can also serialize it automatically

# below is an example of a body with query parameters and path parameters . Fast api is able to automatically recognize them
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, q: str | None = None):


# adding extra vlaidations to the query

@app.get("/item1/")
async def det_items(desc: Annotated[str|None, Query(max_length=20)]=None):
    if desc:
        return desc
    else:
        return "some text"

# q: str | None = None 3.10+
# q: Union[str, None] = None 3.8+

# q: Annotated[str | None] = None 3.10+
# q: Annotated[Union[str, None]] = None 3.8+

# async def read_items(q: str | None = Query(default=None, max_length=50)):  this is the old code without using annotated

# other attributes like max length
# min_length
# pattern="^fixedquery$
# regex="^fixedquery$
# regex is depricated and was used in previous versions now pattern is used


# async def read_items(q: Annotated[str, Query(min_length=3)] = "fixedquery"): default values

# in the following example the value is require but it can be none
# async def read_items(q: Annotated[str | None, Query(min_length=3)]):

#query parameter with list with multiple values
@app.get("/items3/")
async def get_items(q: Annotated[list[str]|None , Query(
    alias="item-query",
      title="Query string",
      description="Query string for the items to search in the database that have a good match ha ha ah a",#this stuff is displayed in the openapi docs
      min_length=3,
      max_length=50,
      pattern="^fixedquery$",
      deprecated=True,
)]):
    if q:
        return q
    else :
        return "some value"
# items3/?q=yaara&q=ff&q=string this is how the url will look



@app.get("/items4/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# example od path parameter using annotated
# async def read_items(
#     q: str, item_id: Annotated[int, Path(title="The ID of the item to get")]
# ):

# greater than and less than can also for the float values
# async def read_items(
#     *,
#     item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
#     q: str,
#     size: Annotated[float, Query(gt=0, lt=10.5)],
# ):
# gt: greater th
# an
# ge: greater than or equal
# lt: less than
# le: less than or equal


############# QUERY PARAMETERS WITH A PYDENTIC MODEL


@app.get("/filter/")
async def read_items(filter: Annotated[FilterParams, Query()]):
    # print(fil)
    return filter
