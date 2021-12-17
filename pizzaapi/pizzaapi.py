#fastAPI with body and multiple methods within 1 fastAPI
#---------------------------------------------------------------------------------------------------------------------------#
# startup script in azure app : gunicorn -w 4 -k uvicorn.workers.UvicornWorker pizzaapi:app                                 #
# execute locally : uvicorn pizzaapi:app --reload                                                                           #
# install with pip pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org gunicorn -vvv                  #
# Create virtual environment : python -m venv .venv                                                                         #
# Create requirements.txt : pip freeze > requirements.txt                                                                   # 
#---------------------------------------------------------------------------------------------------------------------------

from typing import Optional
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import BaseSettings

from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

class Order_info(BaseSettings):
    #app_name: str = "Awesome API"
    order_id: int = 0

#uvicorn fastAPI1:app --reload
class orders(BaseModel):
    id: Optional[str] = None
    crust: str
    toppings: List[str]
    # EXAMPLE Body
    """
    {
    "crust": "thin",
    "toppings": ["cheese","jalapenos"]
    }
    """

orders_list = []
last_order_id = 0
order_item = {
    "crust": "Thick",
    "toppings": ["cheese","jalapenos"]
    }

#orders_list.append(order_item)   
order_info = Order_info() 
app = FastAPI()

@app.post("/orders/")
async def create_item(order: orders):
    #print(order)
    #print(orders_list)
    #print(order_info.order_id)
    order_info.order_id = order_info.order_id + 1
    order_id = order_info.order_id
    order.id = order_id
    orders_list.append(order)
    return orders_list

@app.get("/orders/")
async def get_all_orders():
    return {"Order List" : orders_list}

@app.get("/orders/{option}")
async def get_orders(option : int):
    for i in orders_list:
        if i.id == option:
            print(i)
            return i

    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="")
    #return "Not found"
#@app.post()
#@app.put()
#@app.delete()

#@app.get("/items/{item_id}")
#async def read_item(item_id : int):
#    return {"item_id": item_id}

#@app.get("/items/")        http://127.0.0.1:8000/items/?skip=0&limit=10
#async def read_item(skip: int = 0, limit: int = 10):
#    return fake_items_db[skip : skip + limit]
