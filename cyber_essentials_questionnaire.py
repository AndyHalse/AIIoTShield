# Import required libraries
import json

# Read the CyberEssentialsOfficialQuestions.txt file and store the questions
with open("CyberEssentialsOfficialQuestions.txt", "r") as file:
    questions = file.readlines()

# Extract questions and create a list of dictionaries
formatted_questions = [{"question": q.strip()} for q in questions if q.startswith("Q")]

# Function to administer the Cyber Essentials questionnaire
def take_questionnaire(questionnaire_data):
    responses = []
    
    for q in questionnaire_data:
        print(q["question"])
        user_answer = input("Answer (Yes/No): ").lower()
        
        while user_answer not in ["yes", "no"]:
            user_answer = input("Invalid response. Please answer with Yes or No: ").lower()
        
        responses.append({"question": q["question"], "answer": user_answer})
    
    # Save the responses as a JSON file
    with open("questionnaire_responses.json", "w") as outfile:
        json.dump(responses, outfile)

    print("Questionnaire completed. Responses saved to questionnaire_responses.json")

# Run the Cyber Essentials questionnaire
take_questionnaire(formatted_questions)
