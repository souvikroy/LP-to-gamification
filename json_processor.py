import json
import base64
import os
from typing import Dict, List, Any, Optional

class LessonPlanProcessor:
    """
    A class to process lesson plan JSON data and extract relevant information
    for gamification applications.
    """
    
    def __init__(self, json_path: str):
        """
        Initialize the processor with the path to the JSON file.
        
        Args:
            json_path: Path to the lesson plan JSON file
        """
        self.json_path = json_path
        self.lesson_data = self._load_json()
        
    def _load_json(self) -> Dict[str, Any]:
        """
        Load the JSON data from the file.
        
        Returns:
            Dict containing the lesson plan data
        """
        try:
            with open(self.json_path, 'r') as file:
                data = json.load(file)
                # Return the lesson_gamification array from the JSON
                return data.get("lesson_gamification", [])
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return []
    
    def get_lesson_titles(self) -> List[str]:
        """
        Get a list of all lesson titles.
        
        Returns:
            List of lesson titles
        """
        return [lesson.get("title", "") for lesson in self.lesson_data]
    
    def get_lesson_by_title(self, title: str) -> Dict[str, Any]:
        """
        Get lesson data by its title.
        
        Args:
            title: The title of the lesson
            
        Returns:
            Dict containing the lesson data
        """
        for lesson in self.lesson_data:
            if lesson.get("title", "") == title:
                return lesson
        return {}
    
    def get_base64_image(self, image_path):
        """
        Convert an image to base64 for Streamlit display.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Base64 encoded image string
        """
        try:
            if not os.path.exists(image_path):
                return ""
                
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except Exception as e:
            print(f"Error encoding image: {e}")
            return ""
    
    def get_placeholder_image_url(self, game_type):
        """
        Get a placeholder image URL based on game type.
        
        Args:
            game_type: Type of the game
            
        Returns:
            URL to an appropriate placeholder image
        """
        if game_type == "racing_game":
            return "https://img.freepik.com/free-vector/racing-composition-with-flat-image-racing-cars-finish-line-with-checkered-flag-vector-illustration_1284-66262.jpg"
        elif game_type == "creative_writing":
            return "https://img.freepik.com/free-vector/space-background-with-planet-landscape_107791-6146.jpg"
        elif game_type == "exploration_game":
            return "https://img.freepik.com/free-vector/ancient-civilization-city-lost-desert_107791-18380.jpg"
        elif game_type == "detective_game":
            return "https://img.freepik.com/free-vector/detective-equipments-composition-flat-style_1284-60574.jpg"
        else:
            return "https://img.freepik.com/free-vector/quiz-background-with-items-flat-design_23-2147599082.jpg"
    
    def extract_game_info(self) -> List[Dict[str, Any]]:
        """
        Extract information for creating gamification applications.
        
        Returns:
            List of dictionaries with game information
        """
        game_info = []
        
        for lesson in self.lesson_data:
            # Extract key information from the lesson
            lesson_code = lesson.get("lesson_code", "")
            title = lesson.get("title", "")
            theme = lesson.get("theme", [])
            games = lesson.get("games", [])
            
            # Map each lesson to a specific game type
            if "Ordinal Numbers" in title:
                game_type = "racing_game"
            elif "Alternate Universe" in title or "Wormhole" in title:
                game_type = "creative_writing"
            elif "Indus Valley" in title:
                game_type = "exploration_game"
            elif "DNA" in title:
                game_type = "detective_game"
            else:
                game_type = "quiz_game"
            
            # Create learning outcomes from the game descriptions
            learning_outcomes = []
            for game in games:
                description = game.get("description", "")
                if description:
                    learning_outcomes.append(description)
            
            # Create game metadata
            game = {
                "title": title,
                "lesson_code": lesson_code,
                "full_title": title,
                "theme": theme,
                "learning_outcomes": learning_outcomes,
                "content_structure": games,
                "type": game_type,
                "name": self._generate_game_name(title, game_type),
                "description": self._generate_game_description(learning_outcomes, game_type, title),
                "image_url": self.get_placeholder_image_url(game_type)
            }
            
            game_info.append(game)
            
        return game_info
    
    def _determine_game_type(self, lesson_data: Any) -> str:
        """
        Determine the type of game based on lesson content.
        
        Args:
            lesson_data: Data containing lesson information (can be dict or list)
            
        Returns:
            String representing the game type
        """
        # Handle the case when lesson_data is a list
        if isinstance(lesson_data, list):
            # Convert list to string for searching keywords
            content_str = str(lesson_data)
            
            if "ordinal" in content_str.lower() or "race" in content_str.lower():
                return "racing_game"
            elif "universe" in content_str.lower() or "wormhole" in content_str.lower():
                return "creative_writing"
            elif "indus valley" in content_str.lower():
                return "exploration_game"
            elif "dna" in content_str.lower() or "forensic" in content_str.lower():
                return "detective_game"
            else:
                return "quiz_game"
        
        # Handle the case when lesson_data is a dictionary
        outcomes = " ".join(lesson_data.get("learning_outcomes", [])) if isinstance(lesson_data, dict) else ""
        content = str(lesson_data.get("content_structure", [])) if isinstance(lesson_data, dict) else ""
        
        if "ordinal" in outcomes.lower() or "race" in content.lower():
            return "racing_game"
        elif "universe" in outcomes.lower() or "wormhole" in content.lower():
            return "creative_writing"
        elif "indus valley" in outcomes.lower():
            return "exploration_game"
        elif "dna" in outcomes.lower() or "forensic" in outcomes.lower():
            return "detective_game"
        else:
            return "quiz_game"
    
    def _generate_game_name(self, topic: str, game_type: str) -> str:
        """
        Generate a catchy name for the game based on topic and game type.
        
        Args:
            topic: The topic of the lesson
            game_type: The type of game
            
        Returns:
            String representing the game name
        """
        if game_type == "racing_game":
            return f"Race Track Ordinals"
        elif game_type == "creative_writing":
            return f"Multiverse Explorer"
        elif game_type == "exploration_game":
            return f"Indus Valley Adventure"
        elif game_type == "detective_game":
            return f"DNA Detective"
        else:
            return f"{topic.split()[0]} Quiz Challenge"
    
    def _generate_game_description(self, data: Any, game_type: str, topic: str) -> str:
        """
        Generate a description for the game based on learning outcomes and game type.
        
        Args:
            data: Learning outcomes or descriptions (can be dict, list, or string)
            game_type: The type of game
            topic: The topic of the lesson
            
        Returns:
            String representing the game description
        """
        if game_type == "racing_game":
            return f"A racing game where players learn ordinal numbers (1st to 10th) by competing on a virtual race track. The game teaches the context and application of ordinal numbers in real-life scenarios through interactive racing challenges."
        elif game_type == "creative_writing":
            return f"An imaginative game where players explore the concepts of wormholes and alternate universes. Players write creative news reports about fictional scenarios, learning to differentiate between fact and fiction."
        elif game_type == "exploration_game":
            return f"An adventure game where players explore the ancient Indus Valley Civilization. Discover key features of Harappan cities, learn about the significance of the Indus River, and understand the social structure of this ancient civilization."
        elif game_type == "detective_game":
            return f"A forensic science game where players solve crimes using DNA evidence. Learn about DNA profiling, evidence collection, and proper procedures for handling samples while solving exciting mysteries."
        else:
            if isinstance(data, list) and len(data) > 0:
                return f"An interactive quiz game to help you learn about {topic}. " + data[0][:100] + "..."
            else:
                return f"An interactive quiz game to help you learn about {topic}."
                
    def get_game_gif(self, game_type: str) -> str:
        """
        Get a GIF URL for the game based on its type.
        
        Args:
            game_type: Type of the game
            
        Returns:
            URL to an appropriate GIF
        """
        if game_type == "racing_game":
            return "https://media.giphy.com/media/l0HlBQrcyc1TGwGJ2/giphy.gif"  # Racing cars
        elif game_type == "creative_writing":
            return "https://media.giphy.com/media/ule4vhcY1xEKQ/giphy.gif"  # Space/universe animation
        elif game_type == "exploration_game":
            return "https://media.giphy.com/media/3oKIPDjV0Oa2tiAmME/giphy.gif"  # Map/exploration
        elif game_type == "detective_game":
            return "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif"  # DNA animation
        else:
            return "https://media.giphy.com/media/3o7qDLkrYI7oNqB1ny/giphy.gif"  # Quiz animation
