from fastapi.applications import FastAPI

app = FastAPI()

@app.get("/")
async def hello_word():
    return {
        "message": "Hello World"
    }
