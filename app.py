from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.predict_route import router as predict_router

app = FastAPI()

# CORS biar Flutter bisa akses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register router
app.include_router(predict_router)

# Optional: Tambah route root untuk cek server nyala
@app.get("/")
def root():
    return {"message": "Batik Detection API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)