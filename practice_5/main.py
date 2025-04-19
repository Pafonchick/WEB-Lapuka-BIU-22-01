# Лапука Павел БИУ-22-01
import os
from io import BytesIO
import uvicorn
import base64
from PIL import Image, ImageOps
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from keras.models import load_model
import numpy as np
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

model = load_model("mnist_cnn_model.h5")

class ImageData(BaseModel):
    image: str
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)
@app.options("/{path:path}")
async def options_handler(path: str):
    return {"status": "ok"}

@app.options("/recognize")
async def recognize(img_data: ImageData):
    return {"status": "ok"}

def process_image(img: Image.Image) -> Image.Image:
    img = img.resize((28, 28))
    img = img.convert("L")
    img = ImageOps.invert(img)
    img.save("processed_image.png")
    return img

def predict(img: Image.Image) -> int:
    img = process_image(img)
    img_arr = np.array(img) / 255.0
    img_arr = img_arr.reshape(1, 28, 28, 1)
    res = model.predict(img_arr)[0]
    return int(np.argmax(res))

@app.post("/recognize")
async def recognize(img_data: ImageData):
    try:
        if img_data.image.startswith("data:image/png;base64,"):
            img_str = img_data.image.replace("data:image/png;base64,", "")
        else:
            img_str = img_data.image

        img_bytes = base64.b64decode(img_str)
        img = Image.open(BytesIO(img_bytes))

        img.save("original_image.png")

        pred = predict(img)
        logger.info(f"Predicted digit: {pred}")
        return {
            "status": "ok",
            "variant": pred,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        }

    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(
            status_code=400,
            detail="Invalid image data",
            headers={"Access-Control-Allow-Origin": "*"}
        )

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        reload=True,
        headers=[
            ("Access-Control-Allow-Origin", "*"),
            ("Access-Control-Allow-Methods", "POST, OPTIONS"),
            ("Access-Control-Allow-Headers", "Content-Type")
        ]
    )