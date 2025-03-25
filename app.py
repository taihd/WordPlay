import streamlit as st
import re
from collections import defaultdict

# Set up the page
st.set_page_config(page_title="WordPlay - Word Guessing Game", layout="wide")
st.title("WordPlay - Word Guessing Game")
st.write("Find possible words from a set of letters with optional constraints.")

# Load words from the file
@st.cache_data
def load_words():
    with open("words.txt", "r") as file:
        # Read all words and filter out very short words and words with special characters
        words = [word.strip().lower() for word in file if word.strip() and len(word.strip()) >= 2]
        # Remove words with special characters, keeping only alphabetic words
        words = [word for word in words if re.match(r'^[a-z]+$', word)]
    return words

# Group words by length for faster filtering
@st.cache_data
def group_words_by_length(words):
    word_groups = defaultdict(list)
    for word in words:
        word_groups[len(word)].append(word)
    return word_groups

# Check if a word can be formed from the given letters
def can_form_word(word, letters):
    letter_count = {}
    for letter in letters:
        letter_count[letter] = letter_count.get(letter, 0) + 1
    
    for letter in word:
        if letter not in letter_count or letter_count[letter] == 0:
            return False
        letter_count[letter] -= 1
    
    return True

# Find all possible words that can be formed with the given letters and constraints
def find_possible_words(letters, word_length, constraints):
    all_words = group_words_by_length(load_words()).get(word_length, [])
    possible_words = []
    
    for word in all_words:
        # Check if the word matches all constraints
        matches_constraints = True
        for position, letter in constraints.items():
            if position < len(word) and word[position] != letter:
                matches_constraints = False
                break
        
        # If word matches constraints and can be formed from the letters
        if matches_constraints and can_form_word(word, letters):
            possible_words.append(word)
    
    return possible_words

# Main app layout
st.subheader("Step 1: Enter Letters")
letter_input = st.text_input("Enter a list of letters (without spaces):", "abcdefghijklmnopqrstuvwxyz")
letters = [letter.lower() for letter in letter_input if letter.isalpha()]

if letters:
    st.write(f"You entered {len(letters)} letters: {', '.join(letters)}")
    
    st.subheader("Step 2: Select Word Length")
    max_length = min(15, len(letters))  # Limit max length to 15 or the number of letters
    word_length = st.slider("Select word length:", 2, max_length, 5)
    
    st.subheader("Step 3: Add Constraints (Optional)")
    st.write("Select letters for specific positions in the word:")
    
    # Create a grid of dropdowns for position constraints
    constraints = {}
    cols = st.columns(min(word_length, 8))  # Limit to 8 columns per row for better display
    
    for i in range(word_length):
        with cols[i % 8]:
            st.write(f"Position {i+1}")
            letter = st.selectbox(f"Letter #{i+1}", [''] + letters, key=f"pos_{i}")
            if letter:
                constraints[i] = letter.lower()
    
    # Button to find words
    st.subheader("Step 4: Find Possible Words")
    if st.button("Find Words"):
        with st.spinner("Searching for words..."):
            possible_words = find_possible_words(letters, word_length, constraints)
            
            if possible_words:
                st.success(f"Found {len(possible_words)} possible words!")
                st.write("Possible words:")
                
                # Display words in a nice format
                word_columns = st.columns(3)
                for i, word in enumerate(sorted(possible_words)):
                    word_columns[i % 3].write(f"• {word}")
            else:
                st.warning("No words found that match your criteria.")
else:
    st.warning("Please enter at least one letter to start.")

# Add footer with instructions
st.markdown("---")
st.write("### How to use this app:")
st.write("1. Enter a list of letters that you want to use to form words.")
st.write("2. Select the length of the word you want to find.")
st.write("3. Optionally, add constraints by selecting which letter should be at a specific position.")
st.write("4. Click 'Find Words' to see all possible words that can be formed with your letters and constraints.") 