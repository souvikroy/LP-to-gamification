import streamlit as st
from typing import Dict, Any, List
import random
from .base_game import BaseGame

class IndusValleyAdventureGame(BaseGame):
    """
    An exploration game about the Indus Valley Civilization where players
    learn about key features, cities, and cultural aspects through interactive
    adventures.
    """
    
    def __init__(self, game_info: Dict[str, Any]):
        """Initialize the Indus Valley Adventure Game"""
        super().__init__(game_info)
        
        # Game-specific state
        if "game_stage" not in st.session_state:
            st.session_state.game_stage = "intro"
            
        if "knowledge_points" not in st.session_state:
            st.session_state.knowledge_points = 0
            
        if "artifacts_collected" not in st.session_state:
            st.session_state.artifacts_collected = []
            
        # Create the AI guide using LangChain
        self.guide_chain = self.create_llm_chain(
            """You are an archaeological expert named Dr. Sharma, guiding students through the ancient 
            Indus Valley Civilization. Answer the student's question about the Indus Valley.

            Student's Question: {question}
            
            Provide a helpful, educational response in 2-3 sentences. Be engaging but factually accurate.
            Focus on helping the student understand the Indus Valley Civilization better.
            """,
            "answer"
        )
    
    def render(self):
        """Render the game UI"""
        # Display header and sidebar info
        st.sidebar.markdown(f"### Explorer Stats")
        st.sidebar.markdown(f"Knowledge Points: {st.session_state.knowledge_points}")
        st.sidebar.markdown(f"Artifacts: {len(st.session_state.artifacts_collected)}/6")
        
        # Game stages
        if st.session_state.game_stage == "intro":
            self._render_intro()
        elif st.session_state.game_stage == "map":
            self._render_map()
        elif st.session_state.game_stage == "harappa":
            self._render_harappa()
        elif st.session_state.game_stage == "mohenjo_daro":
            self._render_mohenjo_daro()
        elif st.session_state.game_stage == "quiz":
            self._render_quiz()
        elif st.session_state.game_stage == "completion":
            self._render_completion()
    
    def _render_intro(self):
        """Introduction to the game"""
        st.markdown("## Journey to the Ancient Indus Valley")
        st.markdown("""
        Welcome, young archaeologist! You are about to embark on an exciting journey back in time to the 
        Indus Valley Civilization, one of the world's oldest urban civilizations.
        
        Your mission is to explore the ancient cities, learn about their remarkable achievements,
        collect valuable artifacts, and solve mysteries from the past.
        
        As you explore, you will:
        - Discover the geographical significance of the Indus River
        - Explore the advanced cities of Harappa and Mohenjo Daro
        - Learn about their sophisticated urban planning and sanitation systems
        - Uncover cultural artifacts and understand their significance
        """)
        
        st.markdown("### Meet Your Guide")
        st.markdown("""
        Dr. Sharma, an expert archaeologist, will be your guide on this journey.
        You can ask Dr. Sharma questions about the Indus Valley Civilization throughout your adventure.
        """)
        
        # Ask Dr. Sharma section
        with st.expander("Ask Dr. Sharma a question"):
            user_question = st.text_input("Your question:")
            if st.button("Ask") and user_question:
                guide_answer = self.guide_chain.invoke({"question": user_question})["answer"]
                st.markdown(f"**Dr. Sharma:** {guide_answer}")
        
        if st.button("Begin Your Adventure"):
            st.session_state.game_stage = "map"
            st.experimental_rerun()
    
    def _render_map(self):
        """Map view where player can select locations to visit"""
        st.markdown("## Indus Valley Map")
        st.markdown("""
        You are looking at a map of the Indus Valley region. The civilization flourished along 
        the Indus River, which was crucial for agriculture and transportation.
        
        Where would you like to explore first?
        """)
        
        # Location choices
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Harappa")
            st.markdown("One of the largest settlements of the Indus Valley Civilization")
            if st.button("Visit Harappa"):
                st.session_state.game_stage = "harappa"
                st.experimental_rerun()
        
        with col2:
            st.markdown("### Mohenjo Daro")
            st.markdown("The 'Mound of the Dead' - a remarkably well-preserved ancient city")
            if st.button("Visit Mohenjo Daro"):
                st.session_state.game_stage = "mohenjo_daro"
                st.experimental_rerun()
        
        # Ask Dr. Sharma section
        with st.expander("Ask Dr. Sharma a question"):
            user_question = st.text_input("Your question:")
            if st.button("Ask") and user_question:
                guide_answer = self.guide_chain.invoke({"question": user_question})["answer"]
                st.markdown(f"**Dr. Sharma:** {guide_answer}")
    
    def _render_harappa(self):
        """Harappa exploration"""
        st.markdown("## Exploring Harappa")
        st.markdown("""
        Welcome to Harappa, one of the most important cities of the Indus Valley Civilization.
        This city shows advanced urban planning with grid-like streets and sophisticated 
        construction techniques.
        """)
        
        # Areas to explore in Harappa
        st.markdown("### What would you like to explore?")
        
        tabs = st.tabs(["City Layout", "Construction", "Artifacts"])
        
        with tabs[0]:
            st.markdown("""
            ### City Layout
            
            Harappa had a well-planned layout with streets arranged in a grid pattern.
            The city was divided into distinct sections for different purposes.
            
            The citadel area was built on an elevated platform for protection against floods and enemies.
            """)
            
            if "harappa_layout_explored" not in st.session_state:
                st.session_state.knowledge_points += 5
                st.session_state.harappa_layout_explored = True
        
        with tabs[1]:
            st.markdown("""
            ### Construction Materials
            
            The buildings in Harappa were primarily made of mud bricks of standardized size.
            These bricks were baked in kilns, making them more durable.
            
            The standardization of bricks (ratio 4:2:1) across the civilization shows remarkable 
            planning and coordination.
            """)
            
            if "harappa_construction_explored" not in st.session_state:
                st.session_state.knowledge_points += 5
                st.session_state.harappa_construction_explored = True
        
        with tabs[2]:
            st.markdown("""
            ### Harappan Artifacts
            
            Explore the area to find important artifacts!
            """)
            
            if "harappa_seal" not in st.session_state.artifacts_collected:
                if st.button("Search for Artifacts"):
                    st.markdown("""
                    **You found a Harappan Seal!**
                    
                    This stone seal features an image of a unicorn-like animal and symbols 
                    from the undeciphered Indus script. These seals were likely used in trade 
                    to mark goods.
                    """)
                    st.session_state.artifacts_collected.append("harappa_seal")
                    st.session_state.knowledge_points += 10
            else:
                st.markdown("""
                **Harappan Seal**
                
                This stone seal features an image of a unicorn-like animal and symbols 
                from the undeciphered Indus script. These seals were likely used in trade 
                to mark goods.
                """)
        
        # Navigation buttons
        st.markdown("### Navigation")
        if st.button("Return to Map"):
            st.session_state.game_stage = "map"
            st.experimental_rerun()
    
    def _render_mohenjo_daro(self):
        """Mohenjo Daro exploration"""
        st.markdown("## Exploring Mohenjo Daro")
        st.markdown("""
        Welcome to Mohenjo Daro, the "Mound of the Dead." This remarkably well-preserved city 
        reveals the advanced nature of the Indus Valley Civilization, particularly its 
        sanitation systems and urban planning.
        """)
        
        # Areas to explore in Mohenjo Daro
        st.markdown("### What would you like to explore?")
        
        tabs = st.tabs(["Great Bath", "Sanitation", "Granary", "Artifacts"])
        
        with tabs[0]:
            st.markdown("""
            ### The Great Bath
            
            The Great Bath is one of the earliest public water tanks in the ancient world.
            This large basin is 12 meters long, 7 meters wide, and 2.4 meters deep.
            
            It was likely used for religious purification and rituals, showing the importance 
            of cleanliness in Indus culture.
            """)
            
            if "great_bath_explored" not in st.session_state:
                st.session_state.knowledge_points += 5
                st.session_state.great_bath_explored = True
        
        with tabs[1]:
            st.markdown("""
            ### Advanced Sanitation
            
            Mohenjo Daro had an advanced sanitation system that was ahead of its time.
            
            Houses had private bathrooms connected to a sophisticated drainage system.
            The drains were covered with bricks or stone slabs and were regularly cleaned.
            
            This level of sanitation wasn't seen again in South Asia until the modern era!
            """)
            
            if "sanitation_explored" not in st.session_state:
                st.session_state.knowledge_points += 5
                st.session_state.sanitation_explored = True
        
        with tabs[2]:
            st.markdown("""
            ### The Granary
            
            The large building identified as a granary shows how the civilization stored food.
            Its design included air ducts and platforms to protect grain from moisture and pests.
            
            This demonstrates the advanced agricultural practices and food management systems 
            of the Indus people.
            """)
            
            if "granary_explored" not in st.session_state:
                st.session_state.knowledge_points += 5
                st.session_state.granary_explored = True
        
        with tabs[3]:
            st.markdown("""
            ### Mohenjo Daro Artifacts
            
            Explore the area to find important artifacts!
            """)
            
            if "bronze_statuette" not in st.session_state.artifacts_collected:
                if st.button("Search Area 1"):
                    st.markdown("""
                    **You found the Dancing Girl Bronze Statuette!**
                    
                    This 4,500-year-old bronze figure of a dancing girl is one of the most famous 
                    artifacts from the civilization. Its creation shows the advanced metallurgical 
                    skills of the Indus people.
                    """)
                    st.session_state.artifacts_collected.append("bronze_statuette")
                    st.session_state.knowledge_points += 10
            
            if "priest_king" not in st.session_state.artifacts_collected:
                if st.button("Search Area 2"):
                    st.markdown("""
                    **You found the Priest King Sculpture!**
                    
                    This soapstone figure depicts a bearded man wearing an armband and cloak 
                    with trefoil patterns. It might represent a priest or ruler, though we 
                    don't know for certain who it portrays.
                    """)
                    st.session_state.artifacts_collected.append("priest_king")
                    st.session_state.knowledge_points += 10
        
        # Navigation buttons
        st.markdown("### Navigation")
        if st.button("Return to Map"):
            st.session_state.game_stage = "map"
            st.experimental_rerun()
        
        # After exploring both cities extensively, unlock the quiz
        explored_areas = 0
        for key in st.session_state.keys():
            if key.endswith("_explored"):
                explored_areas += 1
        
        if explored_areas >= 3 and len(st.session_state.artifacts_collected) >= 2:
            st.markdown("### Knowledge Test Available!")
            if st.button("Take Knowledge Test"):
                st.session_state.game_stage = "quiz"
                st.experimental_rerun()
    
    def _render_quiz(self):
        """Knowledge quiz about Indus Valley"""
        st.markdown("## Indus Valley Knowledge Test")
        st.markdown("""
        Now that you've explored the ancient cities of the Indus Valley, 
        let's test your knowledge about this remarkable civilization!
        """)
        
        if "quiz_questions" not in st.session_state:
            st.session_state.quiz_questions = [
                {
                    "question": "What material were most buildings in Harappa made from?",
                    "options": ["Stone blocks", "Wooden planks", "Standardized baked bricks", "Unbaked clay"],
                    "correct": "Standardized baked bricks"
                },
                {
                    "question": "What is the Great Bath in Mohenjo Daro thought to have been used for?",
                    "options": ["Swimming competitions", "Religious purification rituals", "Fish farming", "Drinking water storage"],
                    "correct": "Religious purification rituals"
                },
                {
                    "question": "Which feature of Indus Valley cities demonstrates their advanced engineering?",
                    "options": ["Electricity", "Covered drainage systems", "Elevators", "Concrete highways"],
                    "correct": "Covered drainage systems"
                },
                {
                    "question": "What was the importance of the Indus River to the civilization?",
                    "options": ["It provided hydroelectric power", "It was used for transportation and agriculture", "It was their only source of drinking water", "It was considered a deity"],
                    "correct": "It was used for transportation and agriculture"
                },
                {
                    "question": "What do the seals from the Indus Valley Civilization feature?",
                    "options": ["Photos of kings", "Animal images and undeciphered script", "Maps of cities", "Religious hymns"],
                    "correct": "Animal images and undeciphered script"
                }
            ]
            st.session_state.current_quiz_question = 0
            st.session_state.quiz_score = 0
        
        # Display the current question
        if st.session_state.current_quiz_question < len(st.session_state.quiz_questions):
            question = st.session_state.quiz_questions[st.session_state.current_quiz_question]
            st.markdown(f"### Question {st.session_state.current_quiz_question + 1}/{len(st.session_state.quiz_questions)}")
            st.markdown(question["question"])
            
            answer = st.radio("Select your answer:", question["options"], index=None)
            
            if st.button("Submit Answer"):
                if answer == question["correct"]:
                    self.display_feedback("Correct! Well done!", True)
                    st.session_state.quiz_score += 1
                    st.session_state.knowledge_points += 5
                else:
                    self.display_feedback(f"Not quite. The correct answer is: {question['correct']}", False)
                
                st.session_state.current_quiz_question += 1
                st.experimental_rerun()
        else:
            # Quiz complete
            st.markdown(f"### Quiz Complete!")
            st.markdown(f"You scored {st.session_state.quiz_score}/{len(st.session_state.quiz_questions)} on the Indus Valley Knowledge Test!")
            
            # Award bonus points for good performance
            if st.session_state.quiz_score >= 4:
                st.session_state.knowledge_points += 15
                st.markdown("**Outstanding knowledge!** You've earned 15 bonus Knowledge Points!")
            
            if st.button("Complete Your Journey"):
                st.session_state.game_stage = "completion"
                st.experimental_rerun()
    
    def _render_completion(self):
        """Completion screen with achievements"""
        st.markdown("## 🎉 Journey Complete: Indus Valley Adventure")
        st.markdown(f"""
        Congratulations, archaeologist! You've successfully explored the ancient Indus Valley Civilization 
        and discovered its remarkable achievements.
        
        **Final Knowledge Points: {st.session_state.knowledge_points}**
        
        **Artifacts Collected: {len(st.session_state.artifacts_collected)}/6**
        """)
        
        # Display artifacts collected
        st.markdown("### Your Artifact Collection:")
        
        if "harappa_seal" in st.session_state.artifacts_collected:
            st.markdown("- **Harappan Seal**: Used in trade and featuring the mysterious Indus script")
        
        if "bronze_statuette" in st.session_state.artifacts_collected:
            st.markdown("- **Dancing Girl Bronze Statuette**: Shows advanced metallurgical skills")
        
        if "priest_king" in st.session_state.artifacts_collected:
            st.markdown("- **Priest King Sculpture**: Possibly depicting a ruler or important figure")
        
        # Display knowledge gained
        st.markdown("### Knowledge Acquired:")
        for outcome in self.learning_outcomes:
            st.markdown(f"- {outcome}")
        
        # Option to play again
        if st.button("Start New Expedition"):
            # Reset game state
            for key in ["game_stage", "knowledge_points", "artifacts_collected", 
                      "quiz_questions", "current_quiz_question", "quiz_score"]:
                if key in st.session_state:
                    del st.session_state[key]
            
            # Clear exploration flags
            for key in list(st.session_state.keys()):
                if key.endswith("_explored"):
                    del st.session_state[key]
            
            # Initialize new game
            st.session_state.game_stage = "intro"
            st.session_state.knowledge_points = 0
            st.session_state.artifacts_collected = []
            
            st.experimental_rerun()
