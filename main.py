import ijson

import random

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# with open("questions.json", "r") as f:
#     # Stream items one by one from the top-level array
#     for question in ijson.items(f, "math.item"):
#         print(f"ID: {question['id']}")
#         print(f"Domain: {question['domain']}")
#         print(f"Question: {question['question']['question']}\n")

qset="english"


for i in range(2):
    total=0

    with open("questions.json","r",encoding="utf-8") as f:

        for question in ijson.items(f,qset+".item"):
            total+=1

    loop=True
    print(total)
    qset="math"

streak=0

def random_question(category):

    global streak

    selected_q=random.randint(0,0)
    current_q=0

    with open("questions.json","r",encoding="utf-8") as f:

        for question in ijson.items(f,category+".item"):
            if(current_q==selected_q):
                print()

                print(f"\nQuestion {selected_q}: {question['question']['question']}")
                if streak>=3:
                    print(f"{color.YELLOW}{color.BOLD}You have a {color.RED}{streak}{color.YELLOW} answer streak!{color.END}")
                print(f"\n{color.RED}A: {question['question']['choices']['A']}")
                print(f"{color.BLUE}B: {question['question']['choices']['B']}")
                print(f"{color.YELLOW}C: {question['question']['choices']['C']}")
                print(f"{color.GREEN}D: {question['question']['choices']['D']}{color.END}")

                user_answer=input("Your answer:")
                
                if(user_answer=="quit"): 
                    quit()

                correct=False
                correct_str=color.RED+color.BOLD+"Incorrect."+color.END
                if(user_answer.lower()==question['question']['correct_answer'].lower()):
                    correct=True
                    correct_str=color.GREEN+color.BOLD+"Correct!"+color.END
                    streak+=1
                    
                
                print(f"{correct_str} {question['question']['explanation']}")
                if not correct: print(f"{color.YELLOW} The correct answer was {color.BOLD}{question['question']['correct_answer']}{color.END}")

                if not correct:
                    streak=0

            current_q+=1



while loop:
    random_question(qset)
