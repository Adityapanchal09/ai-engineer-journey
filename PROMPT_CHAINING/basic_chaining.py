from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client=Groq()


def ask(system,user_msg):
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"system","content":system},
            {"role":"user","content":user_msg}
        ]
    )

    return response.choices[0].message.content


#The Chain ----
Raw_notes="""PHOTOSYNTHESIS

6CO2 + 6H2O -> C6H12O6 + 6O2 (wrote it wrong 2 times)
happens in chloroplasts
2 stages:
light dep reactions -> makes ATP, NADPH, O2 (from water)
calvin cycle -> uses CO2, ATP, NADPH -> makes G3P (sugar)
key terms: chlorophyll, thylakoid, stroma
eq: 6CO2 + 6H2O -> C6H12O6 + 6O2
remember: light -> chemical energy
notes: dont confuse with respiration! respiration is opposite (sorta)
diagram: sun -> leaf -> chloroplast -> thylakoid stack (grana)
quiz: what is output of light dep? -> O2, ATP, NADPH
what is input for calvin? -> CO2, ATP, NADPH
G3P -> glucose
messy: C6H12O6 is glucose, not fructose! (checked)
also: NADP+ -> NADPH (reduction)
ATP -> ADP (hydrolysis)
dark reactions? no, calvin cycle is better term.
summary: plants make food using light, water, CO2. release O2.
end."""
#step1 clean Grammer ---
step1=ask("fix Grammer and clarity return only the corrected text",Raw_notes)

#step2 summmarized the clean version---
step2=ask("summarize the clean version in two sentences",step1)

#step3 Generate a question from summary---
step3=ask("generate one exam based question on this",step2)

print("Cleaned:",step1)
print("Summary:",step2)
print("Question:",step3)
