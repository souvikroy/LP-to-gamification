import streamlit as st
from typing import Dict, Any
from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

class BaseGame(ABC):
    """
    Abstract base class for all educational gamification applications.
    Provides common functionality for game implementation.
    """
    
    def __init__(self, game_info: Dict[str, Any]):
        """
        Initialize the game with the provided game information.
        
        Args:
            game_info: Dictionary containing game metadata
        """
        self.title = game_info["name"]
        self.description = game_info["description"]
        self.learning_outcomes = game_info["learning_outcomes"]
        self.content_structure = game_info["content_structure"]
        self.game_type = game_info["type"]
        
        # Initialize the language model
        self.llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-3.5-turbo"
        )
    
    @abstractmethod
    def render(self):
        """
        Render the game UI using Streamlit.
        This method must be implemented by all derived classes.
        """
        pass
    
    def create_llm_chain(self, template: str, output_key: str = "result"):
        """
        Create a LangChain LLM chain with the specified prompt template.
        
        Args:
            template: String template for the prompt
            output_key: The key to use for the output in the chain
            
        Returns:
            An initialized LLMChain object
        """
        prompt = ChatPromptTemplate.from_template(template)
        return LLMChain(
            llm=self.llm,
            prompt=prompt,
            output_key=output_key,
            verbose=False
        )
    
    def display_progress(self, progress: float):
        """
        Display a progress bar for the game.
        
        Args:
            progress: Float between 0.0 and 1.0 representing progress
        """
        st.progress(progress)
    
    def display_feedback(self, feedback: str, is_correct: bool = None):
        """
        Display feedback to the user.
        
        Args:
            feedback: Feedback text to display
            is_correct: If the feedback is for a correct or incorrect answer
        """
        if is_correct is None:
            st.info(feedback)
        elif is_correct:
            st.success(feedback)
        else:
            st.error(feedback)
    
    def display_completion(self, message: str):
        """
        Display a completion message for the game.
        
        Args:
            message: Completion message to display
        """
        st.balloons()
        st.success(message)
