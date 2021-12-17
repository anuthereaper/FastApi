#FastAPI with body and multiple methods within 1 fastAPI
#Includes Azure SQL DB connection (insert and select)
#---------------------------------------------------------------------------------------------------------------------------#
# startup script in azure app : gunicorn -w 4 -k uvicorn.workers.UvicornWorker apiwithdb:app                                #
# execute locally : uvicorn apiwithdb:app --reload                                                                          #
# install with pip pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org gunicorn -vvv                  #
# Create virtual environment : python -m venv .venv                                                                         #
# Create requirements.txt : pip freeze > requirements.txt                                                                   #
# Change driver to {ODBC Driver 17 for SQL Server} for Azure and {ODBC Driver 13 for SQL Server} for local                  # 
#---------------------------------------------------------------------------------------------------------------------------#
from typing import Optional
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import BaseSettings
import os

import pyodbc
import collections
import json
from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

import os

def insert_row(conn,insert_sql):
    cursor = conn.cursor()
    cursor.execute(insert_sql)
    print("Record inserted succesfully")
    conn.commit()

def select_rows(conn,sql_stmt):
    with conn.cursor() as cursor:
        cursor.execute(sql_stmt)
        rows = cursor.fetchall()
    objects_list = []
    if len(rows) > 0:
        for row in rows:
            d = collections.OrderedDict()
            d["id"] = row[0]
            d["crust"] = row[1]
            d["topping"] = row[2]
            objects_list.append(d)
    j = json.dumps(objects_list)
    return j

def connect_db():
    #my_app_setting_value = os.environ.get("myDb")
    #print(my_app_setting_value)

    connectionstr = 'DRIVER=' + order_info.driver + ';Server=tcp:' + order_info.servername + '.database.windows.net,1433;Database=' + order_info.database + ';Uid=' + order_info.userid + ';Pwd=' + order_info.password + ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
    print(connectionstr)
    conn = pyodbc.connect(connectionstr)
    print("Connection sucessful")
    return conn

class Order_info(BaseSettings):
    #app_name: str = "Awesome API"
    order_id: int = 0
    servername = os.getenv('dbserver') 
    database = os.getenv('dbname') 
    userid = os.getenv('userid') 
    password = os.getenv('dbpassword') 
    driver= '{ODBC Driver 17 for SQL Server}'           

#uvicorn fastAPI1:app --reload
class orders(BaseModel):
    id: Optional[str] = None
    crust: str
    topping: str
    # EXAMPLE Body
    """
    {
    "crust": "thin",
    "topping": "cheese"
    }
    """

orders_list = []
order_info = Order_info() 
conn = connect_db()

app = FastAPI()

@app.post("/orders/")
async def create_item(order: orders):
    order_info.order_id = order_info.order_id + 1
    order_id = order_info.order_id
    order.id = order_id
    orders_list.append(order)
    insert_sql =  "INSERT INTO [dbo].[Orders] (id, crust, topping) VALUES ('" + str(order.id) + "','" + order.crust + "','" + order.topping + "')"
    insert_row(conn,insert_sql)
    return orders_list

@app.get("/orders/")
async def get_all_orders():
    sql_stmt = "SELECT * FROM [dbo].[Orders]"
    orders_str = select_rows(conn,sql_stmt)
    orders_json = json.loads(orders_str)
    return orders_json
    #return {"Order List" : orders_list}

@app.get("/orders/{option}")
async def get_orders(option : int):
    sql_stmt = "SELECT * FROM [dbo].[Orders] WHERE id = " + str(option)
    orders_str = select_rows(conn,sql_stmt)
    orders_json = json.loads(orders_str)
    #print(orders_json)
    if len(orders_json) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=orders_json)    
    else:
        return orders_json

#@app.post()
#@app.put()
#@app.delete()

#@app.get("/items/{item_id}")
#async def read_item(item_id : int):
#    return {"item_id": item_id}

#@app.get("/items/")        http://127.0.0.1:8000/items/?skip=0&limit=10
#async def read_item(skip: int = 0, limit: int = 10):
#    return fake_items_db[skip : skip + limit]
