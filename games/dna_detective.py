import streamlit as st
from typing import Dict, Any, List
import random
import base64
from PIL import Image
import requests
from io import BytesIO
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
        
        # Game visuals
        self.game_images = {
            "intro": "https://img.freepik.com/free-vector/detective-equipments-composition-flat-style_1284-60574.jpg",
            "dna_basics": "https://img.freepik.com/free-vector/dna-structure-design-biochemistry-concept_23-2148499811.jpg",
            "crime_scene": "https://img.freepik.com/free-vector/crime-scene-concept-illustration_114360-1214.jpg",
            "evidence": "https://img.freepik.com/free-vector/flat-design-fingerprint-detection-background_23-2148179688.jpg",
            "complete": "https://img.freepik.com/free-vector/detective-concept-illustration_114360-1687.jpg"
        }
        
        self.game_gifs = {
            "dna": "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif",
            "microscope": "https://media.giphy.com/media/xUPGcpMkMDcIQQbTa0/giphy.gif",
            "magnify": "https://media.giphy.com/media/fSvqyvXn1M3btN8sDh/giphy.gif"
        }
            
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
    
    def display_image(self, url, width=None):
        """Display an image from a URL with optional width"""
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            if width:
                st.image(img, width=width)
            else:
                st.image(img)
        except Exception as e:
            st.error(f"Could not load image: {e}")
    
    def _render_intro(self):
        """Introduction to DNA Detective Game"""
        st.markdown("## 🔍 DNA Detective: The Missing Museum Artifact")
        
        # Display game logo/intro image
        col1, col2 = st.columns([2, 1])
        
        with col1:
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
                
        with col2:
            self.display_image(self.game_images["intro"])
    
    def _render_dna_basics(self):
        """Learn about DNA basics"""
        st.markdown("## 🧬 DNA: The Blueprint of Life")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
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
        
        with col2:
            self.display_image(self.game_gifs["dna"])
            st.caption("DNA structure animation")  
        
        # DNA fact check quiz - add more questions to enhance the game
        st.markdown("### 📝 Quick DNA Facts Check")
        
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
                },
                {
                    "question": "Why is DNA unique to each person?",
                    "options": ["Because everyone eats different food", "Because of genetic variations from our parents", "Because we all use different shampoo", "Because of our different names"],
                    "correct": "Because of genetic variations from our parents"
                },
                {
                    "question": "Which of these is NOT a common source of DNA evidence?",
                    "options": ["Blood", "Saliva", "Metal", "Skin cells"],
                    "correct": "Metal"
                },
                {
                    "question": "What tool do forensic scientists use to see DNA better?",
                    "options": ["Telescope", "Microwave", "Microscope", "X-ray machine"],
                    "correct": "Microscope"
                }
            ]
            st.session_state.current_dna_question = 0
            st.session_state.dna_score = 0
        
        # Display the current question with a progress bar
        if st.session_state.current_dna_question < len(st.session_state.dna_questions):
            total_questions = len(st.session_state.dna_questions)
            progress = (st.session_state.current_dna_question / total_questions)
            st.progress(progress)
            st.caption(f"Question {st.session_state.current_dna_question + 1} of {total_questions}")
            
            question = st.session_state.dna_questions[st.session_state.current_dna_question]
            st.markdown(f"**Question {st.session_state.current_dna_question + 1}:** {question['question']}")
            
            answer = st.radio("Select your answer:", question["options"], index=None)
            
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("Check Answer"):
                    if answer == question["correct"]:
                        self.display_feedback("That's correct! Great job! +5 points", True)
                        st.session_state.dna_score += 1
                        st.session_state.investigator_points += 5
                    else:
                        self.display_feedback(f"Not quite. The correct answer is: {question['correct']}", False)
                    
                    st.session_state.current_dna_question += 1
                    st.experimental_rerun()
        else:
            # DNA basics complete with animated progress
            st.success(f"### 🎉 Basic Training Complete!")
            st.markdown(f"You answered {st.session_state.dna_score}/{len(st.session_state.dna_questions)} questions correctly.")
            
            # Add score meter
            score_percentage = (st.session_state.dna_score / len(st.session_state.dna_questions)) * 100
            st.progress(score_percentage / 100)
            
            # Display reward image based on score
            col1, col2 = st.columns([1, 1])
            with col1:
                # DNA expert Q&A
                st.markdown("### 👩‍🔬 Ask the DNA Expert")
                st.markdown("Before heading to the crime scene, you can ask our DNA expert a question:")
                
                dna_question = st.text_input("Your question about DNA or forensics:")
                if st.button("Ask Expert") and dna_question:
                    st.spinner("Analyzing your question...")
                    expert_answer = self.dna_analyzer.invoke({"question": dna_question})["explanation"]
                    st.info(f"**Expert:** {expert_answer}")
                
                if st.button("👉 Go to Crime Scene"):
                    st.session_state.game_phase = "crime_scene"
                    st.experimental_rerun()
            
            with col2:
                self.display_image(self.game_images["dna_basics"])
    
    def _render_crime_scene(self):
        """Crime scene investigation"""
        st.markdown("## 🕵️ The Museum Crime Scene")
        
        # Create two columns for layout
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown(f"""
            Welcome to the museum, {st.session_state.detective_name}! The valuable DNA artifact was stolen last night.
            We need to collect evidence from the scene to find out who did it.
            """)
            
            # Add some more context about DNA evidence collection
            st.info("""
            **Remember**: Good detectives know that DNA evidence can be found on objects people have touched,
            especially if they weren't wearing gloves. Look for surfaces where the thief might have left traces!
            """)
        
        with col2:
            self.display_image(self.game_images["crime_scene"])
        
        # Evidence collection mini-game with improved visuals
        st.markdown("### 🔍 Collect Evidence")
        st.markdown("Look around the museum and click on areas where you might find DNA evidence.")
        
        evidence_spots = [
            "Display Case", 
            "Door Handle",
            "Broken Glass",
            "Security Camera",
            "Visitor Log",
            "Coffee Cup"
        ]
        
        evidence_descriptions = {
            "Display Case": "You found fingerprints on the glass! This could contain DNA from the suspect.",
            "Door Handle": "You collected DNA samples from the door handle. The thief likely touched this!",
            "Broken Glass": "You found a small piece of cloth caught on the broken glass. It might have the thief's DNA!",
            "Security Camera": "You found security camera footage showing someone suspicious!",
            "Visitor Log": "You found the museum visitor log with names of everyone who visited today.",
            "Coffee Cup": "You found a discarded coffee cup with possible saliva DNA evidence!"
        }
        
        # Create a visual representation of the evidence spots
        # Use a 3x2 grid for better visualization
        col1, col2, col3 = st.columns(3)
        evidence_icons = ["💎", "🚪", "🔍", "📹", "📋", "☕"]
        
        # Display spots where evidence might be found with icons
        cols = [col1, col2, col3]  # Create a list of column objects
        for i, spot in enumerate(evidence_spots):
            with cols[i % 3]:
                spot_collected = spot in st.session_state.evidence_collected
                button_label = f"{evidence_icons[i]} {spot}" + (" ✓" if spot_collected else "")
                button_type = "success" if spot_collected else "primary" 
                
                if st.button(button_label, key=f"spot_{i}", type=button_type) and not spot_collected:
                    st.session_state.evidence_collected.append(spot)
                    st.success(evidence_descriptions[spot])
                    points = random.randint(5, 15)  # Variable points for more excitement
                    st.session_state.investigator_points += points
                    st.markdown(f"**+{points} points!**")
                    st.experimental_rerun()
        
        # Display collected evidence with nice formatting
        if st.session_state.evidence_collected:
            st.markdown("### 🧪 Evidence Collected")
            
            # Show progress towards goal
            evidence_count = len(st.session_state.evidence_collected)
            required_evidence = 3
            
            # Progress bar for evidence collection
            progress = min(1.0, evidence_count / required_evidence)
            st.progress(progress)
            st.caption(f"Evidence collected: {evidence_count}/{required_evidence} required samples")
            
            # Display evidence in a nice grid with images
            cols = st.columns(min(3, evidence_count))
            for i, evidence in enumerate(st.session_state.evidence_collected):
                with cols[i % min(3, evidence_count)]:
                    st.markdown(f"**Sample #{i+1}:**")
                    st.markdown(f"**Source:** {evidence}")
                    st.markdown(f"**Type:** DNA trace evidence")
                    # Show a small microscope image for each evidence
                    self.display_image(self.game_gifs["microscope"], width=100)
                
            # Quick analysis of one piece of evidence
            if evidence_count >= required_evidence:
                st.success("### You've collected enough evidence!")
                
                # Add a spinner and fancier button
                if st.button("🔬 Analyze Evidence in the Lab", type="primary"):
                    with st.spinner("Processing evidence samples..."):
                        # Simulate processing time
                        import time
                        time.sleep(1)
                    st.session_state.game_phase = "completion"
                    st.experimental_rerun()
    
    def _render_completion(self):
        """Game completion"""
        st.markdown("## 🏆 Case Solved!")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.success(f"""
            Congratulations, **{st.session_state.detective_name}**! You've successfully solved the case of the missing museum artifact.
            
            By analyzing the DNA evidence and other clues you collected, you identified the culprit!
            The stolen artifact has been recovered and returned to the museum.
            """)
            
            # Generate a more detailed summary of the investigation
            culprits = ["Professor Plum", "Colonel Mustard", "Miss Scarlet", "Dr. Green"]
            culprit = random.choice(culprits)
            
            st.markdown("### 📋 Case Summary")
            st.info(f"""
            **Case:** The Missing Museum Artifact
            **Lead Investigator:** {st.session_state.detective_name}
            **Evidence Analyzed:** {len(st.session_state.evidence_collected)} samples
            **Perpetrator:** {culprit}
            **Recovery:** Complete - Artifact returned to museum
            **Case Status:** Closed successfully
            """)
        
        with col2:
            self.display_image(self.game_images["complete"])
        
        # Display final score with animated meter
        st.markdown("### 🎮 Game Performance")
        score_col, badge_col = st.columns([3, 1])
        
        with score_col:
            st.markdown(f"**Final Score:** {st.session_state.investigator_points} points")
            
            # Determine rank based on points
            if st.session_state.investigator_points >= 50:
                rank = "Master Detective"
                emoji = "🔍🏆"
            elif st.session_state.investigator_points >= 35:
                rank = "Senior Investigator"
                emoji = "🕵️‍♀️⭐"
            elif st.session_state.investigator_points >= 20:
                rank = "Junior Detective"
                emoji = "🔎✅"
            else:
                rank = "Detective Trainee"
                emoji = "🔍"
                
            st.markdown(f"**Rank Achieved:** {emoji} {rank}")
            
            # Create a score meter
            max_possible = 60  # Maximum possible score
            score_percentage = min(1.0, st.session_state.investigator_points / max_possible)
            st.progress(score_percentage)
            st.caption(f"Score: {st.session_state.investigator_points}/{max_possible} possible points")
        
        # Display evidence collected in a nice format
        st.markdown("### 🧪 Evidence Collected")
        evidence_cols = st.columns(min(3, len(st.session_state.evidence_collected)))
        
        for i, evidence in enumerate(st.session_state.evidence_collected):
            with evidence_cols[i % len(evidence_cols)]:
                st.markdown(f"**Evidence #{i+1}:** {evidence}")
                st.markdown("**DNA Analysis:** Positive match")
                self.display_image(self.game_gifs["magnify"], width=100)
        
        # What you learned section
        st.markdown("### 📚 What You Learned")
        st.markdown("""
        In this DNA Detective game, you learned:
        - How DNA evidence is used in forensic science
        - Different sources of DNA evidence (fingerprints, hair, saliva)
        - The importance of careful evidence collection
        - How DNA analysis helps identify suspects
        - The scientific process of investigation
        """)
        
        # Play again button
        if st.button("🔄 Play Again", type="primary"):
            # Reset game state
            st.session_state.game_phase = "intro"
            st.session_state.investigator_points = 0
            st.session_state.evidence_collected = []
            if "dna_questions" in st.session_state:
                del st.session_state["dna_questions"]
            if "current_dna_question" in st.session_state:
                del st.session_state["current_dna_question"]
            if "dna_score" in st.session_state:
                del st.session_state["dna_score"]
            st.experimental_rerun()
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
