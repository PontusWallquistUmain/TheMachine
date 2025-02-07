from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    return {"First page"}


@app.post("/queue/{id}")
def add_to_queue(id):
    return {"Queue created"}