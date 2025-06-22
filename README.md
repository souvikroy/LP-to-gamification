# Educational Gamification Applications

This project contains a suite of gamification applications based on educational lesson plans. Each application is designed to make learning interactive and fun through different game mechanics that reinforce educational concepts.

## Applications Included

1. **Race Track Ordinals** - A racing game to learn ordinal numbers
2. **Multiverse Explorer** - Creative writing game about alternate universes and wormholes
3. **Indus Valley Adventure** - Exploration game about the Indus Valley Civilization
4. **DNA Detective** - Forensic science game about DNA and crime scene investigation

## Setup Instructions

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. Run the application:
   ```
   streamlit run app.py
   ```

## Application Structure

- `app.py`: Main application entry point
- `json_processor.py`: Utility to process the lesson plan JSON data
- `games/`: Directory containing individual game implementations
  - `ordinal_race.py`: Ordinal numbers racing game
  - `multiverse_explorer.py`: Alternate universe/wormhole creative writing game
  - `indus_valley.py`: Indus Valley Civilization exploration game
  - `dna_detective.py`: DNA forensics detective game
- `idea.json`: Source data containing lesson plans
