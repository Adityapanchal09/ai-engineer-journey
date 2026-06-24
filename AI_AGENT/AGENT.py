from groq import Groq
from dotenv import load_dotenv
import json,math

load_dotenv()
client=Groq()

#---Define Tools Plain python functions----
def calculator(expression:str)->str:
    try:
        result=eval(expression)
        return f"result:{result}"
    except:
        return "Error: Invalid expression"
    

def word_counter(text:str)->str:
    words=len(text.split())
    chars=len(text)
    return f"words:{words},characters:{chars}"


def read_file(filepath:str)->str:
    try:
        with open(filepath,"r") as f:
            return f.read()[:500] #first 500 charcters
    except:
        return "Error:File not found!"


#---Tool Registery---
TOOLS={
    "calculator":calculator,
    "word_counter":word_counter,
    "file_reader":read_file
}            

#Tools Description sent to the AI---
TOOLS_DESCRIPTION="""
You Have access to these tools, to use them respond with only JSON object:
{"tool":"tool_name","input":"your input here"}

Availabe Tools:
-calculator: evaluates with expressions, Input:math expression "2+2" or "15*8"
-word_counter: counts word and characters. Input:any text string
-read_file:reads a text file. Input:file path

If you dont need a tool respond normally with your answer
"""

def run_agent(user_task):
    print(f"\n TASk:{user_task}")
    messages=[
        {"role":"system","content":TOOLS_DESCRIPTION},
        {"role":"user","content":user_task}
    ]

    #Agent loop max 5 iterations to prevent for infinite loops
    for i in range(5):
        response=client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )

        reply=response.choices[0].message.content.strip()


        # try to parse as tool call
        try:
            tool_call=json.loads(reply)
            tool_name=tool_call["tool"]
            tool_input=tool_call["input"]

            if tool_name in TOOLS:
                print(f"\n Using tool:{tool_name}")
                print(f"input:{tool_input}")
                tool_result=TOOLS[tool_name](tool_input)
                print(f"result:{tool_result}")

                #feed result back to agent
                messages.append({"role":"assistant","content":reply})
                messages.append({"role":"user","content":f"tool_result:{tool_result}"})
            else:
                print(f"\n Answer:{reply}")

        except json.JSONDecodeError:
            # not a tool call this is a final answer
            print(f"\nanswer:{reply}")
            break


#---test the agent----
run_agent("what is 1234 multiplied by 5678")
run_agent("count the words in:the quick brown fox runs over the lazy dog")
run_agent("What is the capital of France?") #no tool needed
#run_agent("C:\Users\ADITYA PANCHAL\ai_engineer\MINI_RAG\notes.txt")