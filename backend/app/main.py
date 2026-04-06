from fastapi import FastAPI, UploadFile, File
import pandas as pd
from app.services.profile_service import build_profile

app = FastAPI(title="DataSight API")

@app.get("/")
def read_root():
    return {"message":"DataSight backend is running"}

@app.post("/upload")
async def upload_file(file:UploadFile=File(...)):
    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(file.file)

        else:
            return {"error": "Unsupported file format"}
        
        return {
            "filename":file.filename,
            "summary":build_profile(df),
        }

    except Exception as e:
        return {"error":str(e)}