from fastapi import APIRouter, Depends, HTTPException

from app.services.AI_services import AIService, get_model  # 透過依賴注入模型
from app.services.memory_services import VirtualGirlfriendMemoryManager, get_memory_manager
from app.services.auth_service import get_current_user

from app.models.request_model import QueryRequest, VirtualGirlfriendRequest
from app.models.user_model import TokenData

text_router = APIRouter(prefix="/api",tags=["LangChain"])
auth_router = APIRouter(prefix="/api",tags=["authentication"])

services = AIService()

"""
狀態路由
"""

@auth_router.get("/protected")
async def protected_route(current_user: TokenData = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}


"""
text相關路由
"""

@text_router.post("/query")
async def query(
    request: QueryRequest,
    model: AIService = Depends(get_model)):
    """
    接收用戶輸入並返回模型生成的回應

    Parameters:
        - user_input (str): 用戶的查詢輸入

    Returns:
        - query (str): 模型生成的回應
    """
    try:
        if not request.user_input:
            raise HTTPException(status_code=400, detail="User input is required")

        response = model.generate_query(request.user_input)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"伺服器錯誤：{str(e)}")
    
@text_router.post("/VirtualGirlfriend")
async def VirtualGirlfriend(
    request: VirtualGirlfriendRequest,
    model: AIService = Depends(get_model),
    memory_manager: VirtualGirlfriendMemoryManager = Depends(get_memory_manager)
    ):
    """
    處理與虛擬女友聊天的請求

    Parameters:
        - girlfriend_input (str): 用戶的聊天輸入

    Returns:
        - response (str): 模型生成的聊天回應
    """
    try:
        if not request.girlfriend_input :
            raise HTTPException(status_code=400, detail="Girlfriend Input are required")

        response = model.VirtualGirlfriend(request.girlfriend_input, memory_manager)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"伺服器錯誤：{str(e)}")