### Original -> https://github.com/render-examples/fastai-v3/blob/master/app/server.py
import aiohttp
import asyncio
import uvicorn
from pathlib import Path
import sys
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

path = Path(__file__).parent

app = Starlette()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["X-Requested-With", "Content-Type"],
)
app.mount("/static", StaticFiles(directory="app/static"))


@app.route("/")
async def homepage(request):
    html_file = path / "view" / "index.html"
    return HTMLResponse(html_file.open().read())


@app.route("/analyze", methods=["POST"])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data["file"].read())
    img = open_image(BytesIO(img_bytes))
    prediction = learn.predict(img)[0]
    return JSONResponse({"result": str(prediction)})


if __name__ == "__main__":
    if "serve" in sys.argv:
        uvicorn.run(app=app, host="0.0.0.0", port=8000, log_level="info")
