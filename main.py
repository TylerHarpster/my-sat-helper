import ijson # type: ignore

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

class style:
    ITALIC = "\033[3m"
    END = '\033[0m'

# with open("questions.json", "r") as f:
#     # Stream items one by one from the top-level array
#     for question in ijson.items(f, "math.item"):
#         print(f"ID: {question['id']}")
#         print(f"Domain: {question['domain']}")
#         print(f"Question: {question['question']['question']}\n")

qset="math"

total=0

def format():
    with open("questions.json","r",encoding="utf-8") as f:
        for question in ijson.items(f,qset+".item"):
            question = question["question"]
            q: str = question["question"]

            prev_c = ""
            i = 0
            for c in q:
                if c == "*" and q[i+1].isalnum():
                    c[i] = style.ITALIC
                if c == "*" and q[i-1].isalnum():
                    c[i] = style.END

# format() 

with open("questions.json","r",encoding="utf-8") as f:
    for question in ijson.items(f,qset+".item"):
        total+=1

streak=0
selected_q=0

def random_question(category):

    global streak

    global selected_q
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



while True:
    random_question(qset)
    selected_q+=1
