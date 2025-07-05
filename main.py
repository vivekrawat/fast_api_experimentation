from fastapi import FastAPI
from enum import Enum

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