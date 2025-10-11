from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.services.AI_services import AIService  # 透過依賴注入模型
from app.models.request_model import QueryRequest
from app.services.auth_service import get_current_user
from app.models.user_model import TokenData

text_router = APIRouter(prefix="/api",tags=["LangChain"])
auth_router = APIRouter(prefix="/api",tags=["authentication"])

services = AIService()

@auth_router.get("/protected")
async def protected_route(current_user: TokenData = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}

@text_router.post("/query")
async def query(
    request: QueryRequest,
    model=Depends(services.get_model)):
    """
    接收用戶輸入並返回模型生成的回應

    Parameters:
        - user_input (str): 用戶的查詢輸入

    Returns:
        - query (str): 模型生成的回應
    """

    if not request.user_input:
        raise HTTPException(status_code=400, detail="User input is required")

    response = model.generate_query(request.user_input)
    return {"response": response}