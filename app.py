from fastapi import FastAPI


APP_VERSION = "1.0.2"


app = FastAPI(
    title="Jenkins FastAPI Demo",
    version=APP_VERSION,
)


@app.get("/")
def root():

    return {
        "service": "jenkins-fastapi-demo",
        "version": APP_VERSION,
    }


@app.get("/health")
def health():

    return {
        "status": "ok",
    }


@app.get("/api/v1/add")
def add(a: int, b: int):

    return {
        "a": a,
        "b": b,
        "result": a + b,
    }
