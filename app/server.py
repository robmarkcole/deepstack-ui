### Original -> https://github.com/render-examples/fastai-v3/blob/master/app/server.py
import aiohttp
import asyncio
import uvicorn
from pathlib import Path
import sys
from io import BytesIO
import deepstack.core as ds
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

## Depstack setup
DEEPSTACK_IP_ADDRESS = 'localhost'
DEEPSTACK_PORT = '5000'
DEEPSTACK_API_KEY = "Mysecretkey"
DEEPSTACK_TIMEOUT = 20 # Default is 10

dsobject = ds.DeepstackObject(DEEPSTACK_IP_ADDRESS, DEEPSTACK_PORT, DEEPSTACK_API_KEY, DEEPSTACK_TIMEOUT)

@app.route("/")
async def homepage(request):
    html_file = path / "view" / "index.html"
    return HTMLResponse(html_file.open().read())


@app.route("/analyze", methods=["POST"])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data["file"].read())

    try:
        dsobject.detect(img_bytes)
    except ds.DeepstackException as exc:
        print(exc)

    prediction = dsobject.predictions[0]
    return JSONResponse({"result": str(prediction)})


if __name__ == "__main__":
    if "serve" in sys.argv:
        uvicorn.run(app=app, host="0.0.0.0", port=8000, log_level="info")
