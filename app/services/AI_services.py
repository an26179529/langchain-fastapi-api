from app.config.config import OPENAI_API_KEY
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class AIService:
    def __init__(self):
        self.model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=OPENAI_API_KEY
        )

    def get_model(self):
        return self.model

    def generate_query(self, user_input):

        template = """
        You are a helpful assistant. 
        Provide a concise and informative response to the user's query.
        User's query: {user_input}
        """

        prompt = ChatPromptTemplate.from_template(
            input_variables=["user_input"],
            template=template,
            output_key="query"
        )
    
        chain = prompt | self.model

        response = chain.invoke({"user_input": user_input})
        return response['query']