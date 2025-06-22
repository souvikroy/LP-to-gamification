import streamlit as st
from typing import Dict, Any, List
import random
from .base_game import BaseGame

class OrdinalRaceGame(BaseGame):
    """
    A racing game to teach ordinal numbers (1st through 10th)
    through interactive challenges and race simulations.
    """
    
    def __init__(self, game_info: Dict[str, Any]):
        """Initialize the Ordinal Race Game"""
        super().__init__(game_info)
        
        # Game-specific state
        if "race_positions" not in st.session_state:
            st.session_state.race_positions = []
            
        if "current_level" not in st.session_state:
            st.session_state.current_level = 1
            
        if "score" not in st.session_state:
            st.session_state.score = 0
            
        # Game levels
        self.levels = [
            "Identify the Position",
            "Complete the Race",
            "Traffic Rules Quiz",
            "Parking Challenge"
        ]
        
        # Create car racers
        self.racers = ["Red Car", "Blue Car", "Green Car", "Yellow Car", 
                      "Orange Car", "Purple Car", "White Car", "Black Car", 
                      "Silver Car", "Gold Car"]
        
        # Ordinal numbers
        self.ordinals = ["1st", "2nd", "3rd", "4th", "5th", 
                        "6th", "7th", "8th", "9th", "10th"]
    
    def render(self):
        """Render the game UI"""
        # Game description
        st.write("Welcome to Race Track Ordinals! In this game, you'll learn about ordinal numbers through exciting racing challenges.")
        
        # Display current level
        st.subheader(f"Level {st.session_state.current_level}: {self.levels[st.session_state.current_level-1]}")
        
        # Display score
        st.sidebar.metric("Score", st.session_state.score)
        
        # Render the appropriate level
        if st.session_state.current_level == 1:
            self._render_level_one()
        elif st.session_state.current_level == 2:
            self._render_level_two()
        elif st.session_state.current_level == 3:
            self._render_level_three()
        elif st.session_state.current_level == 4:
            self._render_level_four()
        else:
            self._render_completion()
    
    def _render_level_one(self):
        """Level 1: Identify the position of a specific car"""
        
        if not st.session_state.race_positions:
            # Generate random positions
            positions = list(range(10))
            random.shuffle(positions)
            st.session_state.race_positions = [self.racers[i] for i in positions]
            st.session_state.target_car = random.choice(st.session_state.race_positions)
            st.session_state.attempts = 0
        
        # Display the race positions
        st.markdown("### Race Positions")
        for idx, car in enumerate(st.session_state.race_positions):
            st.write(f"{self.ordinals[idx]}: {car}")
        
        # Ask the question
        st.markdown(f"### Question: What position did the {st.session_state.target_car} finish in?")
        
        # Get user input
        user_answer = st.radio("Select the correct position:", self.ordinals, index=None)
        
        if st.button("Submit Answer"):
            st.session_state.attempts += 1
            correct_position = self.ordinals[st.session_state.race_positions.index(st.session_state.target_car)]
            
            if user_answer == correct_position:
                self.display_feedback(f"Correct! The {st.session_state.target_car} finished in {correct_position} place!", True)
                st.session_state.score += max(10 - st.session_state.attempts + 1, 1)  # Score based on attempts
                st.session_state.current_level += 1
                st.session_state.race_positions = []  # Reset for next level
                st.experimental_rerun()
            else:
                self.display_feedback(f"That's not correct. Try again!", False)
    
    def _render_level_two(self):
        """Level 2: Complete the race by arranging cars in the correct order"""
        
        if "ordered_cars" not in st.session_state:
            available_cars = self.racers.copy()
            random.shuffle(available_cars)
            st.session_state.ordered_cars = []
            st.session_state.available_cars = available_cars[:6]  # Use 6 cars for simplicity
        
        st.markdown("### Complete the Race")
        st.write("Arrange the cars in the correct order from 1st to 6th place:")
        
        # Display current arrangement
        st.markdown("### Current Race Order:")
        for idx, car in enumerate(st.session_state.ordered_cars):
            st.write(f"{self.ordinals[idx]}: {car}")
        
        # Select cars to position
        if len(st.session_state.ordered_cars) < 6:
            selected = st.selectbox("Select a car to add to the race:", 
                                  ["Select a car..."] + st.session_state.available_cars)
            
            if st.button("Add Car") and selected != "Select a car...":
                if selected in st.session_state.available_cars:
                    st.session_state.ordered_cars.append(selected)
                    st.session_state.available_cars.remove(selected)
                    st.experimental_rerun()
        
        # Check if complete
        if len(st.session_state.ordered_cars) == 6:
            if st.button("Finish Race"):
                # The challenge is just to complete the ordering, so give points for completion
                self.display_feedback("You've successfully ordered all the cars!", True)
                st.session_state.score += 15
                st.session_state.current_level += 1
                
                # Reset for next level
                if "ordered_cars" in st.session_state:
                    del st.session_state.ordered_cars
                if "available_cars" in st.session_state:
                    del st.session_state.available_cars
                
                st.experimental_rerun()
    
    def _render_level_three(self):
        """Level 3: Traffic rules quiz related to ordinal numbers"""
        
        if "quiz_questions" not in st.session_state:
            # Questions related to traffic rules and ordinal numbers
            st.session_state.quiz_questions = [
                {
                    "question": "Which traffic light should you stop at?",
                    "options": ["1st red light", "2nd yellow light", "Any red light", "Only at stop signs"],
                    "correct": "Any red light"
                },
                {
                    "question": "In a line of cars at a stop sign, which car goes first?",
                    "options": ["1st car", "2nd car", "Last car", "Whoever honks first"],
                    "correct": "1st car"
                },
                {
                    "question": "At a 4-way intersection, if two cars arrive at the same time, which has the right of way?",
                    "options": ["1st car to arrive", "Car on the right", "Bigger car", "Neither car"],
                    "correct": "Car on the right"
                }
            ]
            st.session_state.current_question = 0
            st.session_state.quiz_score = 0
        
        # Display the current question
        if st.session_state.current_question < len(st.session_state.quiz_questions):
            question = st.session_state.quiz_questions[st.session_state.current_question]
            st.markdown(f"### Question: {question['question']}")
            
            answer = st.radio("Select your answer:", question["options"], index=None)
            
            if st.button("Submit Answer"):
                if answer == question["correct"]:
                    self.display_feedback("Correct answer!", True)
                    st.session_state.quiz_score += 1
                else:
                    self.display_feedback(f"Incorrect. The correct answer is: {question['correct']}", False)
                
                st.session_state.current_question += 1
                st.experimental_rerun()
        else:
            # Quiz completed
            st.session_state.score += st.session_state.quiz_score * 5
            st.markdown(f"### Quiz Complete!")
            st.write(f"You got {st.session_state.quiz_score} out of {len(st.session_state.quiz_questions)} questions correct!")
            
            if st.button("Continue to Next Level"):
                st.session_state.current_level += 1
                
                # Reset quiz state
                if "quiz_questions" in st.session_state:
                    del st.session_state.quiz_questions
                if "current_question" in st.session_state:
                    del st.session_state.current_question
                if "quiz_score" in st.session_state:
                    del st.session_state.quiz_score
                
                st.experimental_rerun()
    
    def _render_level_four(self):
        """Level 4: Parking challenge using ordinal numbers"""
        
        if "parking_spots" not in st.session_state:
            # Create parking scenario
            st.session_state.parking_spots = ["Empty" for _ in range(10)]
            
            # Fill some spots randomly
            filled_indices = random.sample(range(10), 5)
            for idx in filled_indices:
                car_color = random.choice(["Red", "Blue", "Green", "Yellow", "Purple"])
                st.session_state.parking_spots[idx] = f"{car_color} Car"
            
            # Set up the challenge
            st.session_state.target_spot = None
            for i in range(10):
                if st.session_state.parking_spots[i] == "Empty":
                    st.session_state.target_spot = i
                    break
        
        st.markdown("### Parking Challenge")
        st.write("Park your car in the correct parking spot based on the instructions.")
        
        # Display parking garage
        st.markdown("### Current Parking Garage:")
        cols = st.columns(5)
        for i in range(10):
            col_idx = i % 5
            with cols[col_idx]:
                st.write(f"Spot {i+1}: {st.session_state.parking_spots[i]}")
        
        if st.session_state.target_spot is not None:
            target_ordinal = self.ordinals[st.session_state.target_spot]
            st.markdown(f"### Instructions: Park your car in the {target_ordinal} parking spot.")
            
            # User selects a spot
            user_spot = st.number_input("Select a parking spot number (1-10):", 
                                      min_value=1, max_value=10, value=1)
            
            if st.button("Park Car"):
                if st.session_state.parking_spots[user_spot-1] != "Empty":
                    self.display_feedback("That spot is already taken! Try another spot.", False)
                elif user_spot - 1 == st.session_state.target_spot:
                    self.display_feedback(f"Perfect! You correctly parked in the {target_ordinal} spot!", True)
                    st.session_state.score += 20
                    st.session_state.current_level += 1
                    
                    # Reset for completion
                    if "parking_spots" in st.session_state:
                        del st.session_state.parking_spots
                    if "target_spot" in st.session_state:
                        del st.session_state.target_spot
                    
                    st.experimental_rerun()
                else:
                    self.display_feedback(f"That's not the {target_ordinal} spot. Try again!", False)
    
    def _render_completion(self):
        """Display completion screen with summary and rewards"""
        st.markdown("## 🎉 Congratulations! You've completed Race Track Ordinals!")
        st.write(f"Your final score is: {st.session_state.score}")
        
        # Display certificate with learned skills
        st.markdown("### Your Race Track Ordinals Certificate")
        st.markdown("You have successfully learned:")
        for outcome in self.learning_outcomes:
            st.markdown(f"- {outcome}")
        
        # Option to play again
        if st.button("Play Again"):
            # Reset game state
            st.session_state.current_level = 1
            st.session_state.score = 0
            st.session_state.race_positions = []
            
            # Clear any level-specific state
            for key in list(st.session_state.keys()):
                if key not in ["current_level", "score", "race_positions"]:
                    del st.session_state[key]
            
            st.experimental_rerun()
