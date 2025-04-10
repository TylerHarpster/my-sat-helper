import ijson

import random

# with open("questions.json", "r") as f:
#     # Stream items one by one from the top-level array
#     for question in ijson.items(f, "math.item"):
#         print(f"ID: {question['id']}")
#         print(f"Domain: {question['domain']}")
#         print(f"Question: {question['question']['question']}\n")

total=0

with open("questions.json","r",encoding="utf-8") as f:

    for question in ijson.items(f,"math.item"):
        total+=1

loop=True

def random_question(category):

    selected_q=random.randint(0,total)
    current_q=0

    with open("questions.json","r",encoding="utf-8") as f:

        for question in ijson.items(f,category+".item"):
            if(current_q==selected_q):
                print(f"\n\n\nQuestion {selected_q}: {question['question']['question']}\n")
                print(f"A: {question['question']['choices']['A']}")
                print(f"B: {question['question']['choices']['B']}")
                print(f"C: {question['question']['choices']['C']}")
                print(f"D: {question['question']['choices']['D']}")

                user_answer=input("Your answer:")
                
                if(user_answer=="quit"): 
                    loop=False
                    quit()

                correct="Incorrect."
                if(user_answer.lower()==question['question']['correct_answer'].lower()):
                    correct="Correct!"
                    if(random.randint(0,100)==15): correct="Good boy ;)"
                
                print(f"{correct} {question['question']['explanation']}")
                print(f"The correct answer was {question['question']['correct_answer']}")

            current_q+=1



while loop:
    random_question("math")
