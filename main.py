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
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# with open("questions.json", "r") as f:
#     # Stream items one by one from the top-level array
#     for question in ijson.items(f, "math.item"):
#         print(f"ID: {question['id']}")
#         print(f"Domain: {question['domain']}")
#         print(f"Question: {question['question']['question']}\n")

qset="math"

total=0

def format(string):

    underline_keywords=["less","greater","not","sum","only","area","equation","value","value(s)","distributive property"]
    replace_keywords=[["frac",""],["}{","}/{"]]
            
    newstring=""
    i = 0
    ending_dollar_sign=False
    while i<len(string):

        current_char=string[i]

        try:
            if current_char == "*" and string[i+1].isalnum():
                current_char = style.ITALIC

            if current_char == "*" and string[i-1]!=" ":
                current_char = style.END

            if current_char=="$":
                if ending_dollar_sign:
                    current_char=style.END
                else:
                    current_char=style.ITALIC
                ending_dollar_sign=not ending_dollar_sign
        finally: ""
        
        try:
            for keyword in underline_keywords:

                if string[i:i+len(keyword)].lower()==keyword:
                    current_char=color.UNDERLINE+current_char
                if string[i-len(keyword):i].lower()==keyword:
                    current_char=color.END+current_char
        finally: ""

        try:
            for keyword_pair in replace_keywords:

                if string[i:i+len(keyword_pair[0])].lower()==keyword_pair[0]:
                    current_char=keyword_pair[1]
                    i+=len(keyword_pair[0])-1
                
        finally: ""
    


        newstring+=current_char

        i+=1
    
    return newstring+style.END

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

                print(f"\nQuestion {selected_q}: {format(question['question']['question'])}")
                if streak>=3:
                    print(f"{color.YELLOW}{color.BOLD}You have a {color.RED}{streak}{color.YELLOW} answer streak!{color.END}")
                print(f"\n{color.RED}A: {format(question['question']['choices']['A'])}")
                print(f"{color.BLUE}B: {format(question['question']['choices']['B'])}")
                print(f"{color.YELLOW}C: {format(question['question']['choices']['C'])}")
                print(f"{color.GREEN}D: {format(question['question']['choices']['D'])}{color.END}")

                user_answer=input("Your answer:")
                
                if(user_answer=="quit"): 
                    quit()

                correct=False
                correct_str=color.RED+color.BOLD+"Incorrect."+color.END
                if(user_answer.lower()==question['question']['correct_answer'].lower()):
                    correct=True
                    correct_str=color.GREEN+color.BOLD+"Correct!"+color.END
                    streak+=1
                    
                
                print(f"{correct_str} {format(question['question']['explanation'])}")
                if not correct: print(f"{color.YELLOW} The correct answer was {color.BOLD}{question['question']['correct_answer']}{color.END}")

                if not correct:
                    streak=0

            current_q+=1



while True:
    random_question(qset)
    selected_q+=1