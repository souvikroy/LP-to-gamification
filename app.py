import os
import streamlit as st
from dotenv import load_dotenv
from json_processor import LessonPlanProcessor

# Create the games directory if it doesn't exist
os.makedirs("games", exist_ok=True)

# Import game modules
from games.ordinal_race import OrdinalRaceGame
from games.multiverse_explorer import MultiverseExplorerGame
from games.indus_valley import IndusValleyAdventureGame
from games.dna_detective import DNADetectiveGame

# Load environment variables
load_dotenv()

# Check if API key is set
if not os.getenv("OPENAI_API_KEY"):
    st.error("OpenAI API key not found. Please set it in the .env file.")
    st.stop()

# Set page configuration
st.set_page_config(
    page_title="Educational Gamification Apps",
    page_icon="🎮",
    layout="wide"
)

def main():
    """Main application entry point"""
    
    # Application header
    st.title("🎮 Educational Gamification Applications")
    st.subheader("Interactive Learning Games")
    
    # Process the lesson plan JSON data
    processor = LessonPlanProcessor("idea.json")
    games_info = processor.extract_game_info()
    
    # Create a sidebar for game selection
    st.sidebar.title("Game Selection")
    game_titles = [game["name"] for game in games_info]
    
    selected_game = st.sidebar.selectbox(
        "Choose a Game:",
        game_titles
    )
    
    # Find the selected game info
    selected_game_info = next((game for game in games_info if game["name"] == selected_game), None)
    
    if selected_game_info:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Game Info")
        st.sidebar.write(f"**Type:** {selected_game_info['type'].replace('_', ' ').title()}")
        st.sidebar.write(f"**Lesson:** {selected_game_info['full_title']}")
        
        # Display learning outcomes in the sidebar
        st.sidebar.markdown("### Learning Outcomes")
        for outcome in selected_game_info["learning_outcomes"]:
            st.sidebar.markdown(f"- {outcome}")
    
        # Display the selected game
        st.header(f"{selected_game}")
        st.markdown(selected_game_info["description"])
        
        # Launch the appropriate game based on type
        if selected_game_info["type"] == "racing_game":
            game = OrdinalRaceGame(selected_game_info)
            game.render()
        elif selected_game_info["type"] == "creative_writing":
            game = MultiverseExplorerGame(selected_game_info)
            game.render()
        elif selected_game_info["type"] == "exploration_game":
            game = IndusValleyAdventureGame(selected_game_info)
            game.render()
        elif selected_game_info["type"] == "detective_game":
            game = DNADetectiveGame(selected_game_info)
            game.render()
        else:
            st.write("Game type not implemented yet!")

if __name__ == "__main__":
    main()
