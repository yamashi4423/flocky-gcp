from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "動作確認"}
