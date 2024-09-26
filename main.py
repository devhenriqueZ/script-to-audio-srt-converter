import uvicorn
from fastapi import FastAPI
from api.routes import router as api_router
from config.settings import Settings

app = FastAPI(title="Script to Audio and SRT Subtitles Converter")
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Health - OK"}

if __name__ == "__main__":
    settings = Settings()
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)