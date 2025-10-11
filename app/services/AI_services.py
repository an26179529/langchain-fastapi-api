from app.config.settings import settings
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
            output_key="query"
        )
    
        chain = prompt | self.model

        response = chain.invoke({"user_input": user_input})
        return response.content
    
    
    
def get_model() -> AIService:
    return AIService()