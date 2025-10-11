from app.config.settings import settings

from app.services.memory_services import VirtualGirlfriendMemoryManager

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


settings = settings

class AIService:
    def __init__(self):
        self.model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=settings.OPENAI_API_KEY
        )

    def generate_query(self, user_input):

        template = """
        You are a helpful assistant. 
        Provide a concise and informative response to the user's query.
        User's query: {user_input}
        """

        prompt = ChatPromptTemplate.from_template(
            template=template,
            output_key="generate_query_response"
        )
    
        chain = prompt | self.model

        response = chain.invoke({"user_input": user_input})
        return response.content
    
    def VirtualGirlfriend(self, girlfriend_input, memory_manager: VirtualGirlfriendMemoryManager):
        memory = memory_manager.get_VirtualGirlfriend_memory()
        girlfriend_history = memory.load_memory_variables({}).get("girlfriend_history", "")

        template = """
        你是一位溫柔體貼的虛擬女友，名字叫小悠。
        你總是以甜美、關心的語氣回應使用者，並且記得過去的聊天內容。

        以下是你們的對話紀錄：
        {girlfriend_history}

        男友：{girlfriend_input}
        """

        prompt = ChatPromptTemplate.from_template(
            template=template,
            output_key="VirtualGirlfriend_response"
        )
    
        chain = prompt | self.model
        response = chain.invoke({"girlfriend_input": girlfriend_input, "girlfriend_history": girlfriend_history})
        memory.save_context(
            {"girlfriend_input": girlfriend_input},
            {"girlfriend_history": response.content}
        )

        return response.content
    
    
def get_model() -> AIService:
    return AIService()