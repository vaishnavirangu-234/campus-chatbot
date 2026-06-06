# src/llm_handler.py
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import List, Dict, Tuple
from config import Config

class LLMHandler:
    def __init__(self, model: str = None, temperature: float = 0.7):
        self.model = model or Config.LLM_MODEL
        self.temperature = temperature
        self.llm = ChatGroq(
            model_name=self.model,
            temperature=temperature,
            api_key=Config.GROQ_API_KEY
        )
        self.conversation_history = []
    
    def create_system_prompt(self, context: str = "") -> str:
        """Create system prompt for campus chatbot"""
        base_prompt = Config.SYSTEM_PROMPT
        
        if context:
            base_prompt += f"\n\nRelevant Context:\n{context}"
        
        return base_prompt
    
    def get_response(self, user_message: str, context: str = "", 
                    chat_history: List[Dict] = None) -> Tuple[str, List]:
        """Get response from LLM"""
        
        # Build message history
        messages = [
            SystemMessage(content=self.create_system_prompt(context))
        ]
        
        # Add chat history
        if chat_history:
            for msg in chat_history[-5:]:  # Keep last 5 messages
                if msg['role'] == 'user':
                    messages.append(HumanMessage(content=msg['content']))
                else:
                    messages.append(AIMessage(content=msg['content']))
        
        # Add current message
        messages.append(HumanMessage(content=user_message))
        
        try:
            response = self.llm.invoke(messages)
            return response.content, messages
        except Exception as e:
         
    
            print("LLM ERROR:", e)
            raise e
    
    def extract_query_intent(self, user_message: str) -> Dict:
        """Extract intent and entities from user message"""
        intent_prompt = f"""
        Analyze this campus-related question and extract the intent and key entities.
        Return a JSON response with 'intent' and 'entities'.
        
        Question: {user_message}
        
        Possible intents: location, event, club, facility, rule, procedure, contact, admission, placement
        """
        
        response = self.get_response(intent_prompt)[0]
        
        try:
            import json
            result = json.loads(response)
            return result
        except:
            return {
                'intent': 'general',
                'entities': [user_message]
            }