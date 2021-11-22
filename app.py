from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Text
from datetime import date, datetime

from starlette.status import HTTP_204_NO_CONTENT

# Instanciado la app

app = FastAPI(
    title="REST API with FastAPI and MongoDB",
    description="Simple REST API using fastapi and mongodb",
    version="0.0.1"
)

# Arrego (lista) donde se almacenan los objetos o JSON

postdb = []

# Post model (pydantic)

class Post(BaseModel):
  id: int
  title: str
  author: str
  content: Text
  created_at: datetime = datetime.now()
  published_at: datetime
  published: Optional[bool] = False

# Routes

@app.get("/", tags=["POST"])
def read_root():
    return {"home": "Home page"}

@app.get("/posts", response_model=list[Post], tags=["POST"])
def get_posts():
    return postdb

@app.post("/posts", response_model=Post, tags=["POST"])
def add_post(post: Post):
    postdb.append(post.dict())    # Se agrega al arreglo (postdb) como un dicccionario
    return postdb[-1]   # Retornar el ultimo id recibido.

@app.get("/posts/{post_id}", response_model=Post, tags=["POST"])
def get_post(post_id: int):
    for post in postdb:   # Se recorre el arreglo donde se almacenan
        if post["id"] == post_id:   # Si el id del post es igual al que estas consultando
            return post   # Retorna el post
    #post = post_id - 1
    #return postdb[post]
    raise HTTPException(status_code=404, detail="Post Not Found")   # Error controlado si el ID no existe

@app.put("/posts/{post_id}", response_model=Post, tags=["POST"])
def update_post(post_id: int, post: Post):
    postdb[post_id] = post
    return {"message": "Post has been updated succesfully"}

@app.delete("/posts/{post_id}", status_code=HTTP_204_NO_CONTENT, tags=["POST"])
def delete_post(post_id: int):
    for index, post in enumerate(postdb):   # las listas empiezan en 0 por eso enumerate para eliminar por indice y no id
      if post["id"] == post_id:
        postdb.pop(index)
        return {"message": "Post has been deleted succesfully"}
    raise HTTPException(status_code=404, detail="Post Not Found")
    #postdb.pop(post_id -1)
    #return {"message": "Post has been deleted succesfully"}