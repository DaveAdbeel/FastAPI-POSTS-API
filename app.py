from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime 
from uuid import uuid4 as uuid


app = FastAPI()
posts = []

#Post Model 
class Post(BaseModel):
    id:Optional[str]
    title:str
    author:str
    content:Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    is_published: bool = False

@app.get("/")
def index() -> None:
    return {"hello":"world"}

@app.get("/posts")
def get_posts() -> None:
    return posts 

@app.get("/posts/{post_id}")
def get_posts(post_id:str) -> list:
    post = [post if str(post["id"]) == post_id else "Post not found" for post in posts]
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post

@app.post("/posts")
def save_post(post:Post) -> dict:
    post.id = uuid()
    posts.append(post.model_dump())
    
    return {"status": 200,
            "message": "Post Saved Succesfully"}
    
@app.delete("/posts/{post_id}")
def delete_post(post_id:str) -> dict:
    post = [post if str(post["id"]) == post_id else "Post not found" for post in posts]
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found, can't delete post")
    else:
        posts.remove(post[0])
        return {"status": 200,
                "message": "Post Deleted Succesfully"}

    
@app.put("/posts/{post_id}")
def update_post(post_id:str, newPost:Post) -> dict:
    post = [post if str(post["id"]) == post_id else "Post not found" for post in posts]
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found, can't update post")
    else:
        for oldPost in posts:
            if oldPost["id"] == post[0]["id"]:
                oldPost.update(newPost)
                
        return {"status": 200,
                "message": "Post Updated Succesfully"}
    