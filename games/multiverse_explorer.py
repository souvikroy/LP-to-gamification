import streamlit as st
from typing import Dict, Any, List
import random
from .base_game import BaseGame

class MultiverseExplorerGame(BaseGame):
    """
    A creative writing game about alternate universes and wormholes 
    where players create news reports and explore the concepts of 
    fact vs. fiction.
    """
    
    def __init__(self, game_info: Dict[str, Any]):
        """Initialize the Multiverse Explorer Game"""
        super().__init__(game_info)
        
        # Game-specific state
        if "game_phase" not in st.session_state:
            st.session_state.game_phase = "intro"
            
        if "creative_score" not in st.session_state:
            st.session_state.creative_score = 0
            
        # LLM chain for evaluating creative writing
        self.evaluator_chain = self.create_llm_chain(
            """You are evaluating a student's creative writing about alternate universes or wormholes.
            
            The student was asked to: {instruction}
            
            The student wrote:
            {student_text}
            
            Please evaluate this writing based on:
            1. Creativity (how imaginative and original is it?)
            2. Understanding of concepts (does it show understanding of alternate universes or wormholes?)
            3. Language use (grammar, vocabulary, structure)
            
            Give a score out of 10 and brief feedback (2-3 sentences). Format your response as:
            Score: [number]
            Feedback: [your feedback]
            """,
            "evaluation"
        )
    
    def render(self):
        """Render the game UI"""
        # Game phases
        if st.session_state.game_phase == "intro":
            self._render_intro()
        elif st.session_state.game_phase == "fact_fiction":
            self._render_fact_fiction()
        elif st.session_state.game_phase == "theory_learning":
            self._render_theory_learning()
        elif st.session_state.game_phase == "creative_writing":
            self._render_creative_writing()
        elif st.session_state.game_phase == "completion":
            self._render_completion()
    
    def _render_intro(self):
        """Render the game introduction"""
        st.markdown("## Welcome to Multiverse Explorer!")
        st.markdown("""In this adventure, you'll explore the fascinating concepts of alternate universes and wormholes.
        You'll learn to distinguish between fact and fiction, understand scientific theories, and create your own creative news report.
        
        Are you ready to begin your journey across dimensions?""")
        
        if st.button("Start Adventure"):
            st.session_state.game_phase = "fact_fiction"
            st.experimental_rerun()
    
    def _render_fact_fiction(self):
        """Fact vs. Fiction challenge"""
        st.markdown("## Fact or Fiction?")
        st.markdown("Can you tell which of these statements are fact and which are fiction?")
        
        # Statements for the challenge
        if "fact_fiction_statements" not in st.session_state:
            st.session_state.fact_fiction_statements = [
                {"statement": "A dragon roared and flew off into the sunset.", "is_fact": False},
                {"statement": "A dog is working as a head chef in a 5-star restaurant.", "is_fact": False},
                {"statement": "Galaxies are moving away from each other as the universe expands.", "is_fact": True},
                {"statement": "Scientists have theorized that wormholes could connect different points in spacetime.", "is_fact": True},
                {"statement": "An old woman clicked her heels and teleported to another realm.", "is_fact": False},
                {"statement": "Some theories suggest there could be parallel universes we cannot directly observe.", "is_fact": True}
            ]
            st.session_state.fact_fiction_index = 0
            st.session_state.fact_fiction_score = 0
        
        # Show current statement
        if st.session_state.fact_fiction_index < len(st.session_state.fact_fiction_statements):
            current = st.session_state.fact_fiction_statements[st.session_state.fact_fiction_index]
            
            st.markdown(f"### Statement {st.session_state.fact_fiction_index + 1}/{len(st.session_state.fact_fiction_statements)}")
            st.markdown(f"**\"{current['statement']}\"**")
            
            # User selection
            user_choice = st.radio("This statement is:", ["Fact", "Fiction"], index=None)
            
            if st.button("Submit Answer"):
                if (user_choice == "Fact" and current["is_fact"]) or (user_choice == "Fiction" and not current["is_fact"]):
                    self.display_feedback("Correct! 🎉", True)
                    st.session_state.fact_fiction_score += 1
                else:
                    correct = "Fact" if current["is_fact"] else "Fiction"
                    self.display_feedback(f"Incorrect. This statement is actually {correct}.", False)
                
                st.session_state.fact_fiction_index += 1
                st.experimental_rerun()
        else:
            # End of quiz
            st.markdown(f"### Quiz Complete!")
            st.markdown(f"You scored {st.session_state.fact_fiction_score}/{len(st.session_state.fact_fiction_statements)} on the Fact vs. Fiction challenge!")
            
            if st.button("Continue to Theories"):
                st.session_state.game_phase = "theory_learning"
                st.experimental_rerun()
    
    def _render_theory_learning(self):
        """Learning about wormholes and alternate universes"""
        st.markdown("## Enter the Wizarding World")
        st.markdown("""
        Imagine you're at King's Cross Station in London, standing between platforms 9 and 10. 
        There's a wall that some people seem to walk straight through, disappearing to Platform 9¾.
        
        How would you explain this phenomenon scientifically?
        """)
        
        # Images or illustrations would be added here in a real app
        
        st.markdown("### Scientific Theories")
        st.markdown("""
        There are two main scientific concepts that could potentially explain such phenomena in our world:
        
        **1. Wormholes**
        - Theoretical passages through spacetime
        - Could connect widely separated regions of the universe
        - Might allow travel between different points in time
        
        **2. Alternate Universes**
        - Parallel worlds that exist alongside our own
        - Might have different physical laws or histories
        - Could potentially be accessed through certain "gateways"
        """)
        
        # Video resources would be linked here in a real app
        
        # Quiz to check understanding
        st.markdown("### Quick Check")
        
        if "theory_question" not in st.session_state:
            st.session_state.theory_question = {
                "question": "Which theory suggests a shortcut through spacetime?",
                "options": ["Alternate Universe", "Wormhole", "Time Dilation", "Quantum Entanglement"],
                "correct": "Wormhole"
            }
        
        st.markdown(f"**{st.session_state.theory_question['question']}**")
        answer = st.radio("Select your answer:", st.session_state.theory_question["options"], index=None)
        
        if st.button("Check Answer"):
            if answer == st.session_state.theory_question["correct"]:
                self.display_feedback("That's correct! A wormhole is a theoretical passage through spacetime that could create shortcuts for long journeys across the universe.", True)
                st.session_state.creative_score += 5
            else:
                self.display_feedback(f"Not quite. The correct answer is {st.session_state.theory_question['correct']}.", False)
            
            # Show continue button
            if st.button("Continue to Creative Writing"):
                st.session_state.game_phase = "creative_writing"
                st.experimental_rerun()
        
    def _render_creative_writing(self):
        """Creative writing challenge - news report"""
        st.markdown("## NEWS Report Challenge")
        st.markdown("""
        You are a journalist who has just witnessed something extraordinary: 
        you saw someone walk straight through the wall between platforms 9 and 10 at King's Cross Station!
        
        Write a NEWS report about what you witnessed. Remember to include:
        
        1. A catchy headline
        2. What you observed
        3. Your scientific explanation (choose either wormhole or alternate universe theory)
        4. Quotes from "witnesses" or "experts"
        5. A conclusion about what this might mean for science
        """)
        
        # User writing area
        user_report = st.text_area("Write your NEWS report here:", height=300)
        
        # Theory selection
        selected_theory = st.radio(
            "Which scientific theory are you using to explain the phenomenon?",
            ["Wormhole Theory", "Alternate Universe Theory"]
        )
        
        if st.button("Submit Report") and user_report:
            # Use LLM to evaluate the report
            evaluation = self.evaluator_chain.invoke({
                "instruction": "Write a NEWS report about witnessing someone walk through a wall, using either wormhole or alternate universe theory as an explanation.",
                "student_text": user_report
            })["evaluation"]
            
            # Extract score and feedback
            score_line = evaluation.split("\n")[0].strip()
            feedback = "\n".join(evaluation.split("\n")[1:]).strip()
            
            try:
                # Extract numeric score
                score = int(score_line.replace("Score:", "").strip())
                st.session_state.creative_score += score
            except:
                # If parsing fails, give a default score
                score = 5
                st.session_state.creative_score += score
            
            # Display the feedback
            st.markdown("### Your Report Evaluation")
            st.markdown(f"**Score: {score}/10**")
            st.markdown(f"**Feedback:**\n{feedback}")
            
            # Store the report
            st.session_state.final_report = user_report
            st.session_state.selected_theory = selected_theory
            
            # Continue button
            if st.button("See Final Results"):
                st.session_state.game_phase = "completion"
                st.experimental_rerun()
    
    def _render_completion(self):
        """Completion screen with achievements and summary"""
        st.markdown("## 🎉 Multiverse Explorer: Mission Complete!")
        
        # Display final score
        st.markdown(f"### Your Interdimensional Explorer Score: {st.session_state.creative_score}")
        
        # Display achievements
        st.markdown("### Achievements Unlocked:")
        st.markdown("- **Fact Checker** - Distinguished fact from fiction")
        st.markdown("- **Theoretical Physicist** - Understood complex scientific concepts")
        st.markdown("- **Creative Reporter** - Crafted an imaginative news report")
        
        # Display summary of what they learned
        st.markdown("### Knowledge Gained:")
        for outcome in self.learning_outcomes:
            st.markdown(f"- {outcome}")
        
        # Display the user's final report
        if hasattr(st.session_state, 'final_report') and st.session_state.final_report:
            st.markdown("### Your NEWS Report")
            st.markdown(st.session_state.final_report)
        
        # Option to play again
        if st.button("Start New Adventure"):
            # Reset game state
            st.session_state.game_phase = "intro"
            st.session_state.creative_score = 0
            
            # Clear specific game state
            for key in ["fact_fiction_statements", "fact_fiction_index", "fact_fiction_score", 
                       "theory_question", "final_report", "selected_theory"]:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.experimental_rerun()
