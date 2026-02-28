from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok", "message": "Hello from App Runner!"}


@app.get("/health")
def health():
    return {"status": "healthy"}
