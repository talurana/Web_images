from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.mount("/about", StaticFiles(directory="templates"), name="about.html")

@app.get("/")
async def root():
    data = 'Hello basic page'
    return RedirectResponse("/hello/{name}")


@app.get("/hello/{name}")
async def say_hello(name: str):
    data = "That's new page for something"
    return Response(content=data, media_type='text/html')
