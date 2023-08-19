from fastapi import FastAPI,Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiohttp
import pickle
from code import predictcar
import os
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_methods=["*"],
    allow_headers=["*"],
)
class Item(BaseModel):
    img: str 

PATH_HOG = 'http://localhost:8080/api/genhog'

HOG_API_URL_DEFAULT = 'http://localhost:8080/api/genhog'
HOG_API_URL_ALTERNATE = 'http://172.17.0.1:80/api/genhog'
HEADERS = {"Content-Type": "application/json"}

model = pickle.load(open(r'..\\model\\ImageFeatureModel.pk', 'rb'))

# pwd == work

@app.get("/")
def root():
    return {"message": "This is my api imageCAR"}    

@app.post("/api/carbrand")
async def genhog(request: Request):
    try:
        data = await request.json()
        jsons = {"img": data['img']}

        async with aiohttp.ClientSession() as session:
            async with session.get(PATH_HOG, json=jsons, headers=HEADERS) as response:
                hog_result = await response.json()

        res = predictcar(model,[hog_result['Hog']])
        return {"predict":res}
    except:
        raise HTTPException(status_code=500, detail="invalid value")