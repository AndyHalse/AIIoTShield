# Import required libraries
import random

# Define the quiz questions and answers
quiz_data = [
    {
        "question": "What are the five technical controls covered by Cyber Essentials?",
        "answer": "firewalls, secure configuration, access control, malware protection, patch management"
    },
    {
        "question": "Why is it important for an organization to be Cyber Essentials certified?",
        "answer": "to demonstrate a commitment to cybersecurity and protect against common cyber threats"
    },
    {
        "question": "What is the difference between Cyber Essentials and Cyber Essentials Plus?",
        "answer": "Cyber Essentials Plus includes a hands-on technical verification, while Cyber Essentials is self-assessment"
    },
    {
        "question": "How does patch management play a role in Cyber Essentials certification?",
        "answer": "it ensures that software and systems are up to date, reducing vulnerability to known security issues"
    },
    {
        "question": "What types of malware protection are recommended for Cyber Essentials compliance?",
        "answer": "antivirus software, anti-malware software, email filtering, web filtering"
    }
]

# Function to administer the quiz
def take_quiz(quiz_data):
    score = 0
    random.shuffle(quiz_data)
    
    for q in quiz_data:
        print(q["question"])
        user_answer = input().lower()
        
        if user_answer == q["answer"].lower():
            print("Correct!")
            score += 1
        else:
            print("Incorrect. The correct answer is:", q["answer"])
    
    print("Your final score is:", score, "out of", len(quiz_data))

# Run the quiz
take_quiz(quiz_data)
