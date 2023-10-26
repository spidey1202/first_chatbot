import json
from difflib import get_close_matches #try to match the best response for the inputs that we give to our chatbot
from typing import List

#load the knowledge base from json file
def load_knowledge_base(file_path: str) -> dict:
    """
    Read the knowledge base from a JSON file.
    
    :param file_path: The path to the JSON file containing the knowledge base.
    :return: A dictionary with the knowledge base data. 
    """
    with open(file_path, 'r') as file: #in read mode 
        data: dict = json.load(file)
    return data


#save the updated knowledge base to the JSON file
#function to save the dictionary to the knowledge base so that the next time we start the program, we will have the old responses also in the memory

def save_knowledge_base(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2) #insert that data into the json

def find_best_match(user_question: str, questions: List[str]) -> str | None: #function to find the best match from the dictionary
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6) #60% similar/accurate
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('You: ')
        if user_input.lower() == 'quit':
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str | None = get_answer_for_question(best_match, knowledge_base)
            if answer:
                print(f'Bot: {answer}')
            else:
                print("Bot: I'm not sure. Can you teach me?")
                new_answer: str = input('Type the answer or "skip" to skip: ')

                if new_answer.lower() != 'skip':
                    knowledge_base["questions"].append({"question": best_match, "answer": new_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print('Bot: Thank you! I learned a new response!')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    chat_bot()
