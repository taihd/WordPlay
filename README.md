# WordPlay - Word Guessing Game

This is a Streamlit app that helps you find possible words from a set of letters with optional constraints.

## Features

- Enter a list of letters to use for word formation
- Select a word length for guessing
- Add constraints for specific letter positions via dropdown menus
- Find all possible matching words from a dictionary

## How to Run

1. Make sure you have Python installed on your system
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```
4. The app will open in your default web browser

## How to Use

1. Enter a list of letters in the input field
2. Select the desired word length using the slider
3. Optionally, add constraints by selecting specific letters for positions in the word
4. Click "Find Words" to see all possible words that can be formed

## Requirements

- Python 3.7+
- Streamlit

## File Structure

- `app.py`: The main Streamlit application
- `words.txt`: The dictionary file containing words
- `requirements.txt`: Required Python packages 