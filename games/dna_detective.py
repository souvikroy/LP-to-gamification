import streamlit as st
from typing import Dict, Any, List
import random
from .base_game import BaseGame

class DNADetectiveGame(BaseGame):
    """
    A forensic science game where players learn about DNA and crime scene
    investigation through interactive detective scenarios.
    """
    
    def __init__(self, game_info: Dict[str, Any]):
        """Initialize the DNA Detective Game"""
        super().__init__(game_info)
        
        # Game-specific state
        if "game_phase" not in st.session_state:
            st.session_state.game_phase = "intro"
            
        if "investigator_points" not in st.session_state:
            st.session_state.investigator_points = 0
            
        if "evidence_collected" not in st.session_state:
            st.session_state.evidence_collected = []
            
        # DNA analysis helper using LLM
        self.dna_analyzer = self.create_llm_chain(
            """You are a DNA analysis expert explaining forensic concepts to students.
            
            The student has asked: {question}
            
            Provide a simple, educational explanation suitable for grade 4 students.
            Your explanation should be 2-3 sentences maximum and focus on making the concept
            easy to understand while remaining scientifically accurate.
            """,
            "explanation"
        )
    
    def render(self):
        """Render the game UI"""
        # Display header and sidebar info
        st.sidebar.markdown(f"### Detective Stats")
        st.sidebar.markdown(f"Investigator Points: {st.session_state.investigator_points}")
        st.sidebar.markdown(f"Evidence Collected: {len(st.session_state.evidence_collected)}/5")
        
        # Game phases
        if st.session_state.game_phase == "intro":
            self._render_intro()
        elif st.session_state.game_phase == "dna_basics":
            self._render_dna_basics()
        elif st.session_state.game_phase == "crime_scene":
            self._render_crime_scene()
        elif st.session_state.game_phase == "completion":
            self._render_completion()
    
    def _render_intro(self):
        """Introduction to DNA Detective Game"""
        st.markdown("## DNA Detective: The Missing Museum Artifact")
        st.markdown("""
        Welcome, young detective! A valuable artifact has disappeared from the city museum, 
        and you've been called in to solve the case using forensic science.
        
        In this investigation, you'll learn about:
        - The basics of DNA and its importance in forensic science
        - How to collect and analyze evidence from a crime scene
        - Proper procedures for handling forensic samples
        - How DNA profiling helps solve crimes
        
        Are you ready to put your detective skills to the test?
        """)
        
        # Detective name input
        detective_name = st.text_input("Enter your detective name:", value="Detective")
        
        if st.button("Begin Investigation") and detective_name:
            st.session_state.detective_name = detective_name
            st.session_state.game_phase = "dna_basics"
            st.experimental_rerun()
    
    def _render_dna_basics(self):
        """Learn about DNA basics"""
        st.markdown("## DNA: The Blueprint of Life")
        st.markdown(f"""
        Hello, {st.session_state.detective_name}! Before we head to the crime scene,
        let's learn some basics about DNA and why it's so important for solving crimes.
        """)
        
        st.markdown("""
        ### What is DNA?
        
        DNA (Deoxyribonucleic Acid) is a special molecule found in every cell of our bodies.
        It contains all the information that makes you unique - like a blueprint or instruction manual
        for your body. Just like your fingerprints, your DNA is unique to you!
        
        ### Why is DNA important in forensic science?
        
        When people visit places, they often leave tiny bits of themselves behind - 
        skin cells, hair, saliva, or blood. These samples contain DNA that can be analyzed
        to identify who was at a scene. It's like having a signature that can't be faked!
        """)
        
        # DNA fact check quiz
        st.markdown("### Quick DNA Facts Check")
        
        if "dna_questions" not in st.session_state:
            st.session_state.dna_questions = [
                {
                    "question": "What does DNA stand for?",
                    "options": ["Digital Network Analysis", "Deoxyribonucleic Acid", "Detective Nature Assessment", "Dynamic Natural Algorithm"],
                    "correct": "Deoxyribonucleic Acid"
                },
                {
                    "question": "Which of these can contain DNA evidence?",
                    "options": ["A rock", "A plastic toy", "A strand of hair", "A shadow"],
                    "correct": "A strand of hair"
                }
            ]
            st.session_state.current_dna_question = 0
            st.session_state.dna_score = 0
        
        # Display the current question
        if st.session_state.current_dna_question < len(st.session_state.dna_questions):
            question = st.session_state.dna_questions[st.session_state.current_dna_question]
            st.markdown(f"**Question {st.session_state.current_dna_question + 1}:** {question['question']}")
            
            answer = st.radio("Select your answer:", question["options"], index=None)
            
            if st.button("Check Answer"):
                if answer == question["correct"]:
                    self.display_feedback("That's correct! Great job!", True)
                    st.session_state.dna_score += 1
                    st.session_state.investigator_points += 5
                else:
                    self.display_feedback(f"Not quite. The correct answer is: {question['correct']}", False)
                
                st.session_state.current_dna_question += 1
                st.experimental_rerun()
        else:
            # DNA basics complete
            st.markdown(f"### Basic Training Complete!")
            st.markdown(f"You answered {st.session_state.dna_score}/{len(st.session_state.dna_questions)} questions correctly.")
            
            # DNA expert Q&A
            st.markdown("### Ask the DNA Expert")
            st.markdown("Before heading to the crime scene, you can ask our DNA expert a question:")
            
            dna_question = st.text_input("Your question about DNA or forensics:")
            if st.button("Ask Expert") and dna_question:
                expert_answer = self.dna_analyzer.invoke({"question": dna_question})["explanation"]
                st.markdown(f"**Expert:** {expert_answer}")
            
            if st.button("Go to Crime Scene"):
                st.session_state.game_phase = "crime_scene"
                st.experimental_rerun()
    
    def _render_crime_scene(self):
        """Crime scene investigation"""
        st.markdown("## The Museum Crime Scene")
        st.markdown(f"""
        Welcome to the museum, {st.session_state.detective_name}! The valuable ancient DNA exhibit has been stolen.
        Your task is to collect evidence and solve the case.
        """)
        
        # Simple evidence collection activity
        st.markdown("### Collect Evidence")
        st.markdown("Search different areas of the museum to find clues:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Display Case")
            if "fingerprints" not in st.session_state.evidence_collected:
                if st.button("Search Display Case"):
                    st.markdown("You found fingerprints on the glass! This could contain DNA from the suspect.")
                    st.session_state.evidence_collected.append("fingerprints")
                    st.session_state.investigator_points += 10
                    st.experimental_rerun()
            else:
                st.markdown("✓ Fingerprints collected from the display case")
                
            if "hair_strand" not in st.session_state.evidence_collected:
                if st.button("Look Around Display Case"):
                    st.markdown("You found a hair strand near the display case! This is excellent DNA evidence.")
                    st.session_state.evidence_collected.append("hair_strand")
                    st.session_state.investigator_points += 10
                    st.experimental_rerun()
            else:
                st.markdown("✓ Hair strand collected from near the display case")
        
        with col2:
            st.markdown("#### Security Office")
            if "security_footage" not in st.session_state.evidence_collected:
                if st.button("Check Security Cameras"):
                    st.markdown("You found security camera footage showing someone suspicious!")
                    st.session_state.evidence_collected.append("security_footage")
                    st.session_state.investigator_points += 10
                    st.experimental_rerun()
            else:
                st.markdown("✓ Security footage collected")
            
            if "visitor_log" not in st.session_state.evidence_collected:
                if st.button("Check Visitor Log"):
                    st.markdown("You found the museum visitor log with names of everyone who visited today.")
                    st.session_state.evidence_collected.append("visitor_log")
                    st.session_state.investigator_points += 10
                    st.experimental_rerun()
            else:
                st.markdown("✓ Visitor log collected")
        
        # Evidence collected, ready to solve
        if len(st.session_state.evidence_collected) >= 3:
            st.markdown("### Evidence Analysis")
            st.markdown("You've collected enough evidence to analyze and solve the case!")
            
            if st.button("Analyze Evidence and Solve Case"):
                st.session_state.game_phase = "completion"
                st.experimental_rerun()
    
    def _render_completion(self):
        """Game completion"""
        st.markdown("## Case Solved!")
        st.markdown(f"""
        Congratulations, {st.session_state.detective_name}! You've successfully solved the case of the missing museum artifact.
        
        By analyzing the DNA evidence and other clues you collected, you identified the culprit!
        The stolen artifact has been recovered and returned to the museum.
        """)
        
        # Display final score
        st.markdown(f"### Final Score: {st.session_state.investigator_points} points")
        
        # Display evidence collected
        st.markdown("### Evidence Collected:")
        for evidence in st.session_state.evidence_collected:
            if evidence == "fingerprints":
                st.markdown("- Fingerprints from the display case")
            elif evidence == "hair_strand":
                st.markdown("- Hair strand with DNA evidence")
            elif evidence == "security_footage":
                st.markdown("- Security camera footage")
            elif evidence == "visitor_log":
                st.markdown("- Museum visitor log")
        
        # Knowledge gained
        st.markdown("### What You Learned:")
        for outcome in self.learning_outcomes:
            st.markdown(f"- {outcome}")
        
        # Play again button
        if st.button("Start New Investigation"):
            # Reset game state
            st.session_state.game_phase = "intro"
            st.session_state.investigator_points = 0
            st.session_state.evidence_collected = []
            
            # Reset quiz state
            if "dna_questions" in st.session_state:
                del st.session_state.dna_questions
            if "current_dna_question" in st.session_state:
                del st.session_state.current_dna_question
            if "dna_score" in st.session_state:
                del st.session_state.dna_score
            
            st.experimental_rerun()
