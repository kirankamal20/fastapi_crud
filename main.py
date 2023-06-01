from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()
router = APIRouter()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="kiran"
)


class Item(BaseModel):
    name: str
    price: float


@app.post("/signup")
def create_item(item: Item):
    mycursor = mydb.cursor()
    sql = "INSERT INTO items (name, price) VALUES (%s, %s)"
    val = (item.name, item.price)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Item created successfully"}


@app.get("/read/{id}")
def read_item(id: int):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM items WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        return {"name": result[1], "price": result[2]}
    else:
        return {"message": "Item not found"}


@app.put("/update/{id}")
def update_item(id: int, item: Item):
    mycursor = mydb.cursor()
    sql = "UPDATE items SET name = %s, price = %s WHERE id = %s"
    val = (item.name, item.price, id)
    mycursor.execute(sql, val)
    mydb.commit()
    return

@app.delete("/delete/{id}")
def delete_item(id: int):
    try:
        mycursor = mydb.cursor()
        sql = "DELETE FROM items WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        mydb.commit()
        return {"message": "Item with ID {id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/getall")
def read_item():
    mycursor = mydb.cursor()
    sql = "SELECT * FROM items"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if result:
        items = []
        for row in result:
            items.append({"id": row[0], "name": row[1], "price": row[2]})

        return items
    else:
        return {"message": "No items found"}
    
 
@app.post("/login")
def login(userid: str, password: str):
    mycursor = mydb.cursor()

    sql = "SELECT * FROM login WHERE username = %s AND password = %s"
    val = (userid, password)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    if result:
        return{"d":{
            "Message": "Login successful",
            "userid": result[0]
        }}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
@app.post("/Signup")
def signup(userid: str, password: str):
    mycursor = mydb.cursor()
    
    # Check if username already exists
    check_username_sql = "SELECT username FROM login WHERE username = %s"
    check_username_val = (userid,)
    mycursor.execute(check_username_sql, check_username_val)
    existing_username = mycursor.fetchone()
    if existing_username:
         raise HTTPException(status_code=401, detail= "Username already exists")
    
    else:
         insert_user_sql = "INSERT INTO login (username, password) VALUES (%s, %s)"
         insert_user_val = (userid, password)
         mycursor.execute(insert_user_sql, insert_user_val)
         mydb.commit()
    
         return {"message": "Sign Up Success"}
@app.get("/getAllUsers")
def getAllUsers():
    mycursor = mydb.cursor()
    sql = "SELECT * FROM login"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if result:
        items = []
        for row in result:
            items.append({"id": row[0], "username": row[1], "password": row[2]})

        return items
    else:
        return {"message": "No items found"}
    

