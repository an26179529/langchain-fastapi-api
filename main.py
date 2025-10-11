from fastapi import FastAPI
import uvicorn

from app.api.routes import text_router, auth_router



app = FastAPI(
    title="AI Model API",
    description="使用 FastAPI 封裝 LangChain 功能的範例",
    version="1.0"
)

app.include_router(text_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



