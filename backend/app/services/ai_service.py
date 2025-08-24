from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from app.core.config import settings
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger

class AIService:
    def __init__(self):
        self.model_name = settings.GROQ_MODEL_NAME
        self.api_key = settings.GROQ_API_KEY
        self.llm = self._initialize_llm()
        
    def _initialize_llm(self):
        try:
            return ChatGroq(
                groq_api_key=self.api_key,
                model_name=self.model_name,
                temperature=0.7,
                max_tokens=4096
            )
        except Exception as e:
            logger.error(f"Error initializing Groq LLM: {e}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def generate_response(self, messages):
        """Generate a response from the AI model based on conversation history"""
        try:
            # Format messages for LangChain
            formatted_messages = []
            for msg in messages:
                formatted_messages.append({"role": msg.role, "content": msg.content})
            
            # Create memory and conversation chain
            memory = ConversationBufferMemory(return_messages=True)
            for msg in formatted_messages[:-1]:  # Add all but the last message to memory
                if msg["role"] == "user":
                    memory.chat_memory.add_user_message(msg["content"])
                else:
                    memory.chat_memory.add_ai_message(msg["content"])
            
            # Create conversation chain
            conversation = ConversationChain(
                llm=self.llm,
                memory=memory,
                verbose=True
            )
            
            # Get response for the last user message
            last_message = formatted_messages[-1]["content"]
            response = conversation.predict(input=last_message)
            
            return response
        
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def generate_mental_health_insights(self, conversation_history):
        """Generate mental health insights based on conversation history"""
        try:
            # Create a specialized prompt for mental health insights
            prompt = PromptTemplate(
                input_variables=["history"],
                template="""You are a mental health assistant. Based on the following conversation history, 
                provide insights about the user's mental state, potential concerns, and helpful suggestions. 
                Be empathetic, supportive, and professional. Do not diagnose but offer thoughtful observations.
                
                Conversation history:
                {history}
                
                Insights:"""
            )
            
            # Format conversation history
            history_text = ""
            for msg in conversation_history:
                history_text += f"{msg.role}: {msg.content}\n"
            
            # Create chain with the specialized prompt
            chain = prompt | self.llm
            
            # Generate insights
            insights = chain.invoke({"history": history_text})
            
            return insights
        
        except Exception as e:
            logger.error(f"Error generating mental health insights: {e}")
            raise

# Create a singleton instance
ai_service = AIService()