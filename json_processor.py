import json
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
                return json.load(file)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return {}
    
    def get_lesson_titles(self) -> List[str]:
        """
        Get a list of all lesson titles.
        
        Returns:
            List of lesson titles
        """
        return list(self.lesson_data.keys())
    
    def get_lesson_by_title(self, title: str) -> Dict[str, Any]:
        """
        Get lesson data by its title.
        
        Args:
            title: The title of the lesson
            
        Returns:
            Dict containing the lesson data
        """
        return self.lesson_data.get(title, {})
    
    def extract_game_info(self) -> List[Dict[str, Any]]:
        """
        Extract information for creating gamification applications.
        
        Returns:
            List of dictionaries with game information
        """
        game_info = []
        
        for title, data in self.lesson_data.items():
            # Extract key information from the lesson title
            lesson_code = title.split('_')[0]
            topic = title.split('_')[-1].replace('.pptx', '')
            
            # Determine game type based on content
            game_type = self._determine_game_type(data)
            
            # Create game metadata
            game = {
                "title": topic,
                "lesson_code": lesson_code,
                "full_title": title.replace('.pptx', ''),
                "learning_outcomes": data.get("learning_outcomes", []),
                "content_structure": data.get("content_structure", []),
                "type": game_type,
                "name": self._generate_game_name(topic, game_type),
                "description": self._generate_game_description(data, game_type, topic)
            }
            
            game_info.append(game)
            
        return game_info
    
    def _determine_game_type(self, lesson_data: Dict[str, Any]) -> str:
        """
        Determine the type of game based on lesson content.
        
        Args:
            lesson_data: Dictionary containing lesson data
            
        Returns:
            String representing the game type
        """
        outcomes = " ".join(lesson_data.get("learning_outcomes", []))
        content = str(lesson_data.get("content_structure", []))
        
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
            return f"{topic} Quiz Challenge"
    
    def _generate_game_description(self, data: Dict[str, Any], game_type: str, topic: str) -> str:
        """
        Generate a description for the game based on learning outcomes and game type.
        
        Args:
            data: Dictionary containing lesson data
            game_type: The type of game
            topic: The topic of the lesson
            
        Returns:
            String representing the game description
        """
        outcomes = data.get("learning_outcomes", ["Learn about " + topic])
        
        if game_type == "racing_game":
            return f"A racing game where players learn ordinal numbers (1st to 10th) by competing on a virtual race track. The game teaches the context and application of ordinal numbers in real-life scenarios through interactive racing challenges."
        elif game_type == "creative_writing":
            return f"An imaginative game where players explore the concepts of wormholes and alternate universes. Players write creative news reports about fictional scenarios, learning to differentiate between fact and fiction."
        elif game_type == "exploration_game":
            return f"An adventure game where players explore the ancient Indus Valley Civilization. Discover key features of Harappan cities, learn about the significance of the Indus River, and understand the social structure of this ancient civilization."
        elif game_type == "detective_game":
            return f"A forensic science game where players solve crimes using DNA evidence. Learn about DNA profiling, evidence collection, and proper procedures for handling samples while solving exciting mysteries."
        else:
            return f"An interactive quiz game to help you learn about {topic}. " + " ".join(outcomes[:2])
