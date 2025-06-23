import os
import streamlit as st
from dotenv import load_dotenv
from json_processor import LessonPlanProcessor
import requests
from PIL import Image
from io import BytesIO

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

def display_image(url, width=None):
    """Display an image from a URL with optional width"""
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        if width:
            st.image(img, width=width)
        else:
            st.image(img)
        return True
    except Exception as e:
        st.error(f"Could not load image: {e}")
        return False

def main():
    """Main application entry point"""
    
    # Application header
    st.title("🎮 Educational Gamification Applications")
    st.subheader("Interactive Learning Games")
    
    # Process the lesson plan JSON data
    processor = LessonPlanProcessor("idea.json")
    games_info = processor.extract_game_info()
    
    # Create a sidebar for game selection with improved visuals
    st.sidebar.title("🎲 Game Selection")
    
    # Group games by type for better organization
    game_types = {
        "racing_game": "🏁 Racing Games",
        "creative_writing": "📝 Creative Writing Games", 
        "exploration_game": "🌍 Exploration Games",
        "detective_game": "🕵️ Detective Games", 
        "quiz_game": "❓ Quiz Games"
    }
    
    # Organize games by type
    games_by_type = {}
    for game in games_info:
        game_type = game["type"]
        if game_type not in games_by_type:
            games_by_type[game_type] = []
        games_by_type[game_type].append(game)
    
    # Create a more visual game selector with images
    selected_game_info = None
    
    # Show a tab for each game type that has games
    if games_by_type:
        game_type_tabs = st.sidebar.tabs([game_types.get(t, t) for t in games_by_type.keys()])
        
        # For each tab, show the games of that type
        for i, (game_type, games) in enumerate(games_by_type.items()):
            with game_type_tabs[i]:
                for game in games:
                    # Create a card-like display for each game
                    st.sidebar.markdown(f"### {game['name']}")
                    # Show game image
                    if 'image_url' in game and game['image_url']:
                        display_image(game['image_url'], width=200)
                    
                    st.sidebar.markdown(f"**Topic:** {game['title']}")
                    st.sidebar.markdown(game['description'][:100] + "...")
                    
                    if st.sidebar.button(f"Play {game['name']}", key=f"play_{game['name']}"):
                        selected_game_info = game
    
    # If no game is selected via buttons, use the previously selected game or select the first one
    if not selected_game_info:
        if "selected_game" in st.session_state:
            selected_game_name = st.session_state.selected_game
            selected_game_info = next((g for g in games_info if g["name"] == selected_game_name), games_info[0] if games_info else None)
        else:
            selected_game_info = games_info[0] if games_info else None
            
    if selected_game_info:
        # Store the selected game name in session state
        st.session_state.selected_game = selected_game_info["name"]
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"## {selected_game_info['name']}")
            st.markdown(f"**Topic:** {selected_game_info['title']}")
            
            # If there are learning outcomes, show them
            if selected_game_info.get('learning_outcomes'):
                with st.expander("Learning Objectives"):
                    for outcome in selected_game_info['learning_outcomes'][:3]:  # Show first 3 for brevity
                        st.markdown(f"- {outcome}")
        
        with col2:
            # Display game image
            if 'image_url' in selected_game_info and selected_game_info['image_url']:
                display_image(selected_game_info['image_url'])
            
            # Show a gif related to the game type
            if hasattr(processor, 'get_game_gif'):
                gif_url = processor.get_game_gif(selected_game_info["type"])
                if gif_url:
                    display_image(gif_url)
        
        # Initialize and launch the appropriate game
        game_type = selected_game_info["type"]
        
        # Game launch section with improved visuals
        st.markdown("---")
        st.markdown("### Game Launch")
        
        # Start button
        if st.button("🔄 Start Game", type="primary", key="start_game"):
            # Initialize and launch the appropriate game
            if game_type == "racing_game":
                game = OrdinalRaceGame(selected_game_info)
            elif game_type == "creative_writing":
                game = MultiverseExplorerGame(selected_game_info)
            elif game_type == "exploration_game":
                game = IndusValleyAdventureGame(selected_game_info)
            elif game_type == "detective_game":
                game = DNADetectiveGame(selected_game_info)
            else:
                st.error("Unknown game type. Please select another game.")
                return
                
            # Render the game
            game.render()
    else:
        st.warning("No games found in the lesson plan. Please check your JSON data.")

if __name__ == "__main__":
    main()
