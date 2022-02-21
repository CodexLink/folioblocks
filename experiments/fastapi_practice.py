from fastapi import FastAPI

api_inst = FastAPI()

@api_inst.get("/")
async def root():
    return {"message": "Hello World"}

"""
Notes:
- As per described, parameter should be the same as the function argument. You cannot make this different!
- To assert typing, you need to invoke types! Without it, the API will access anything as a parameter argument.
"""
@api_inst.get("/items/{item_id}")
async def readItem(item_id: int):
    return {"item_id": item_id}


"""
Notes:
ORDER MATTERS.
According to the docs, by declaring `/users/me` before the `users/<argument>` will ensure that the first argument will not be automatically parsed as part of the `users/<argument>`.

See "https://fastapi.tiangolo.com/tutorial/path-params/#order-matters".
"""

@api_inst.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@api_inst.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# ! Enums (This example is different than the API docs.)
from enum import Enum

class RequestDocument(str, Enum): # First argument acknowledges that the argument will string for the API docs. And then we subclass Enum as the base of this class.
    pre_enrollment = "pre_reg"
    tor = "transcript_of_records"
    recognitions =  "recog"

@api_inst.get("/document/{user_address}/{doc_type}") # Should be UUID for the first argument, but this is just a test.
async def request_doc(user_address: str, doc_type: RequestDocument):
    return {
        "user": user_address,
        "doc_type": RequestDocument.pre_enrollment if doc_type is RequestDocument.pre_enrollment else RequestDocument.tor if doc_type is RequestDocument.tor else RequestDocument.recognitions
    }

# * Note, if ever we encountered the file path as a parameter. We can use the following.
@api_inst.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

"""
As per stated:
You could need the parameter to contain /home/johndoe/myfile.txt, with a leading slash (/).

In that case, the URL would be: /files//home/johndoe/myfile.txt, with a double slash (//) between files and home.
"""

# Query Parameters (Custom Example+ API docs.)
# This can be useful for gathering recent blocks or nodes.

# API Docs.
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@api_inst.get("/items/") # Evaluates to /items/?skip=0&limit=0.
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# Custom Example
from typing import Any, Dict, Final

# Typing Customization
AddressHexUUID = str
BlockchainJSON = Final[Dict[int, AddressHexUUID]]

blockchain_blocks: BlockchainJSON = [
    {1: "0x8701273091283"},
    {2: "0x8701273091284"},
    {3: "0x8701273091285"},
    {4: "0x8701273091287"},
    {5: "0x8701273091289"}
]

@api_inst.get("/blockchain/") # This function contains type operator of the Optional[type] equivalent.
async def list_blockchain(initial: int = 0, final: int = 0, done_by: str | None = None) -> tuple[BlockchainJSON, str]:
    return (blockchain_blocks[initial : final], done_by) # We use slice here, mind the gap.

# Required Parameters with one on the query

@api_inst.get("/items/{item_id}")
# This API will work with `/items/foo-item?needy=what_is_it`
# Not supplying needy here will throw an error.
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


# === Request Body. (Example is different than the API docs.)
# We are going to use Pydantic here to define the required fields for the POST operation of an endpoint.

from pydantic import BaseModel
from secrets import token_hex
BlockHash = str # For now.

class Block(BaseModel): # On instantiation, default values can be enforced.
    id: int
    auto_id = -1 # We cannot use final here. Since it's pretty much obvious. This is overrideable.
    nonce: int
    nonce_optional: int | None # This is just an example. Let's see if this is possible.
    prev: BlockHash
    next: BlockHash

@api_inst.post("/create_block/")
async def create_block(block_metadata: Block):
    # We have two ways to access the data. [1] Through the variable reference.
    # Or, we can use [2] .dict().

    # What to choose? For me, [1] is better since you are accessing the BaseModel along with the data.

    _metadata = block_metadata.dict() # [2]

    print(
        block_metadata.id,
        block_metadata.auto_id,
        # _metadata.id,
        # _metadata.auto_id,
        _metadata
    )

    if block_metadata.id == block_metadata.auto_id: # [1]
        return block_metadata
    else:
        block_metadata.prev = "folio:" + token_hex(16)
        block_metadata.next = "folio:" + token_hex(16)

        return block_metadata

# Body + Path (Custom Example)
BlockN = int

@api_inst.put("/blockchain/{id}") # THIS WAS NEVER INTENDED IN THE BLOCKCHAIN SYSTEM. May be used in Testng for Reliability.
async def modify_block(id: BlockN, content: Block):
    return {"id_ref": id, **content.dict()}

"""
* Note: I won't do Body + Path + Query since I may not use it later on. But I know how.

Also, keep in mind that:
- If the parameter is also declared in the path, it will be used as a path parameter.
- If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
- If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.
"""

# Additional Validation: Query
# This ensures that the input, specifically for the search functionality will be evaluated, even though it will be recognized as an query.

from fastapi import Query
@api_inst.get("/search")
async def search_explorer(
    context: str | None = Query(None, min_length=3, max_length=32), # Regex is allowed here.
    required_context: str = Query(..., min_length=3) # This asserts a required context with no default value.
): # We may even enforce the type of the data, but that is hassle.
    pass

# Note, there are some parameters such as title, description, etc. They are not covered here.
# Topics such as [1] Query parameter list / multiple values, [2] Query parameter list / multiple values with defaults, [3] Declare more metadata, etc. were not  covered. They may be useful during the development.

# Additional Validation: Path
# Every parameters that an endpoint can take, should have their own documentation, specifically for the path as well.
from fastapi import Path
@api_inst.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: str | None = Query(None, alias="item-query"), # alias is just an alternative keyword for external reference.
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Not sure how this one would work, since I'm not familiar with the * syntax in python. But I'm aware of its use, specifically for parameters.
@api_inst.get("/items/{item_id}")
async def read_items(
    *, item_id: int = Path(..., title="The ID of the item to get"), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Number Path Limitation: Greater than or Equal
@api_inst.get("/items/{item_id}")
async def read_items(
    *, item_id: int = Path(..., title="The ID of the item to get", ge=1), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# * There are two examples that demonstrates other number types and assertion / conditions.

# Assert that a singular field is not a query parameter but is included as a body parameter.
from fastapi import Body
from pydantic import Field

"""
New Version of this schema was added below.
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

"""
class User(BaseModel):
    username: str
    full_name: str | None = None

class Item(BaseModel):
    name: str
    description: str | None = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: float | None = None

"""
# Conflict with the new.
@api_inst.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

@api_inst.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: int = Body(...)
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results
"""

# BaseModel API Documenting with Field

@api_inst.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

# In the end, the documentation examples are so good that I don't need to type it anymore. Though, the risk of not remembering it is always there but the way how I was able to get its point shows that I can check the documentation without having problems on how-to.
