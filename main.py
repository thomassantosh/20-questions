"""
Python text game around 20 questions
Idea attribution to Jaya Moore, https://github.com/jayascript
"""

import random
import pandas as pd

def add_question(df=None):
    """Add a new question"""
    new_question = str(input("What is the new question? (Should be 'yes'): "))
    df[new_question] = None
    df.loc[len(df.index)-1,new_question] = 'yes'
    return df


def update_or_create_animal(df=None, questions=None, responses=None):
    """Update existing animal or create new animal"""
    new_animal = str(input("What animal are you thinking of? (a/an): "))
    existing_animals = list( df['Animal'].unique() )
#     print(f"Existing animals: {existing_animals}")
    if new_animal in existing_animals:
        # Update existing row
        print("Animal already exists in database...updating new responses.")
        existing_animal_index = df.index [ df['Animal']==new_animal][0]
        # Update mechanics
        questions.append('Animal')
        responses.append(new_animal)
        df.loc[existing_animal_index,questions] = responses
    else:
        # Add new animal to the list
        print(f"The new animal TO BE added (a/an): {new_animal}")
        animal_dict = {'Animal':new_animal}
        for i,_ in enumerate(questions):
            animal_dict.update({questions[i]:responses[i]})
        print(animal_dict)
        df.loc[len(df.index)] = (animal_dict)
            
        # Add a new question, for a new animal which will be 'Yes'
        df = add_question(df=df)
    df.to_csv('./data/final_gamedata.csv', index=False, encoding='utf-8')


def make_guess(df=None, original_df=None):
    """Core game logic"""
    question_set = [x for x in df.columns if x != "Animal"]
    
    track_questions, track_responses = [], []
    
    for _ in range(20):
        if len(question_set) == 0:
            print('\033[96mRan out of questions.\033[00m')
            break
            
        random_question = random.choice(question_set)
        response = str(input(f'Question: {random_question} '))
        while response.lower() not in ('yes', 'no'):
            print('Please re-enter a yes/no answer')
            response = str(input(f'Question: {random_question} '))
            
        track_questions.append(random_question)
        track_responses.append(response)
        
        # Filter for answer
        df = df[ df[random_question] == response]
        
        # Show possible outcomes
        if len(df) != 0:
            print(f"Number of possible responses: {len(df)} and options: {list(df['Animal'].unique())}")
        
        # Failure condition
        if len(df) == 0:
            print("\033[96mNo more data.. Dataframe is empty. Computer loses. Player wins.\033[00m")
            update_or_create_animal(df=original_df, questions=track_questions, responses=track_responses)
            break
            
        # Win state
        if len(df) == 1:
            last_animal = list(df['Animal'].unique())[0]
            win_response = str(input(f"Is it {last_animal}? "))
            if win_response.lower() == 'yes':
                print("\033[92mYay! Computer wins. Player loses.\033[00m")
                break
            elif win_response.lower() == 'no':
                print('\033[96mNo guesses left. Computer loses. Player wins.\033[00m')
                
                # Remove the 'animal' line from the dataframe, since inaccurate
                df = df.drop( df.index[ df['Animal']== last_animal])
                
                # Show current state of tracking of questions and responses
                print("")
                print("-----------Tracked responses-------------")
                for i,_ in enumerate(track_questions):
                    print(f"Question: {track_questions[i]}, Answer: {track_responses[i]}")
                    
                update_or_create_animal(df=original_df, questions=track_questions, responses=track_responses)
                
                break
        
        # Take out question from list to avoid repetition
        question_set.remove(random_question)


def play_game():
    """Actual gameplay"""
    print("LET'S PLAY 20 QUESTIONS!")
    print("------------------------")
    df = pd.read_csv('./data/final_animals.csv')
    results = df.copy()
    make_guess(df=results, original_df=df)


if __name__ == "__main__":
    play_game()
