import ijson # type: ignore
import pyautogui
import random
import time

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

qset="english"



def focus(window_name):
    vscode=pyautogui.getWindowsWithTitle(window_name)[0]
    pyautogui.hotkey('win','d')
    time.sleep(0.1)

    vscode.restore()
    vscode.activate()

total=0

def format(string):

    underline_keywords=["less","greater","not","sum","only","area","equation","value","value(s)","distributive property"]
    replace_keywords=[["frac",""],["}{","}/{"],["\\pi","π"]]
            
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
time_budget=1
spending_time=False
time_using=0
globaldiff="any"


def random_question(category,*args):

    global streak
    global time_budget
    global spending_time
    global time_using
    global globaldiff

    diff="any"

    if len(args)==1:
        diff=args[0]

    selected_q=random.randint(0,total)
    current_q=0

    with open("questions.json","r",encoding="utf-8") as f:

        for question in ijson.items(f,category+".item"):
            if(current_q==selected_q):
                
                if diff!="any" and question['difficulty']!=diff:
                    return 0

                difficulty=question['difficulty']
                print(style.BOLD)
                if difficulty=="Easy": print(color.GREEN)
                if difficulty=="Medium": print(color.YELLOW)
                if difficulty=="Hard": print(color.RED)
                print(f"\nDifficulty: {difficulty}"+style.END)


                print(f"Question {selected_q}: {format(question['question']['question'])}")
                if streak>=3:
                    print(f"{color.YELLOW}{color.BOLD}You have a {color.RED}{streak}{color.YELLOW} answer streak!{color.END}")
                if category=="english":
                    print(f"\n{question['question']['paragraph']}")

                print(f"\n{color.RED}A: {format(question['question']['choices']['A'])}")
                print(f"{color.BLUE}B: {format(question['question']['choices']['B'])}")
                print(f"{color.YELLOW}C: {format(question['question']['choices']['C'])}")
                print(f"{color.GREEN}D: {format(question['question']['choices']['D'])}")


                valid_answers=["a","b","c","d","quit"]

                user_answer=""
                valid_answer=False
                while not valid_answer:
                    user_answer=input("Your answer:")
                    try:
                        valid_answers.index(user_answer)
                        valid_answer=True
                    except ValueError:
                        if user_answer=="viewtime":
                            print(f"You have {time_budget} minutes available")
                        elif user_answer[0:9]=="spendtime":

                            try:
                                user_answer=user_answer[10:len(user_answer)]
                                user_answer=int(user_answer)
                                if user_answer>time_budget:
                                    print(color.RED+style.BOLD+"Not enough time!"+style.END)
                                else:
                                    time_budget-=user_answer
                                    time_using=user_answer*60
                                    spending_time=True
                                    return 0
                            except ValueError: 
                                print(color.RED+style.BOLD+"Invalid parameter!"+style.END)
                        elif user_answer[0:6]=="gimmie":
                            try:
                                user_answer=user_answer[7:len(user_answer)]
                                if user_answer.lower()=="easy":
                                    print(f"Difficulty is now {color.GREEN+style.BOLD} Easy. {style.END}")
                                    globaldiff="Easy"
                                if user_answer.lower()=="medium":
                                    print(f"Difficulty is now {color.YELLOW + style.BOLD} Medium. {style.END}")
                                    globaldiff="Medium"
                                if user_answer.lower()=="hard":
                                    print(f"Difficulty is now {color.RED + style.BOLD} Hard. {style.END}")
                                    globaldiff="Hard"
                                if user_answer.lower()=="any":
                                    print(f"Difficulty is now {color.BLUE + style.BOLD} Any. {style.END}")
                                    globaldiff="any"
                            except ValueError: 
                                print(color.RED+style.BOLD+"Invalid parameter!"+style.END)

                        else:
                            print(color.RED+style.BOLD+"Invalid answer!"+style.END)

                
                if(user_answer=="quit"): 
                    quit()
                

                correct=False
                correct_str=color.RED+color.BOLD+"Incorrect."+color.END
                if(user_answer.lower()==question['question']['correct_answer'].lower()):
                    correct=True
                    correct_str=color.GREEN+color.BOLD+"Correct!"+color.END
                    streak+=1
                    time_budget+=5
                    if streak>5:
                        time_budget+=(streak-5)

                    
                
                print(f"{correct_str} {format(question['question']['explanation'])}")
                if not correct: print(f"{color.YELLOW} The correct answer was {color.BOLD}{question['question']['correct_answer']}{color.END}")

                if not correct:
                    streak=0

            current_q+=1



while True:
    if not spending_time:
        random_question(qset,globaldiff)
    
    while spending_time:
        if time_using>0:
            time.sleep(1)
            time_using-=1
        else:
            focus("Visual Studio Code")
            spending_time=False