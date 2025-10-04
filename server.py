# server.py

from fastapi import FastAPI

# إنشاء تطبيق FastAPI
app = FastAPI()

# نقطة الدخول الرئيسية
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# مثال على نقطة أخرى
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}
