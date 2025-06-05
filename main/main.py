from hyperon.ext import register_atoms
from hyperon.atoms import OperationAtom, S, ExpressionAtom, SymbolAtom
from datetime import datetime
from google import genai
from dotenv import load_dotenv
import os
import csv
load_dotenv()

PROMPT = "Summarize the following data in a human-readable format. based on the following data"



time = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
text_file_name = f"../generated/results_{time}.txt"
csv_file_name = f"../generated/results_{time}.csv"


with open(csv_file_name, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Summary"])

with open(text_file_name, 'w') as f:
    f.write(f"Summarized Text \n")


def write_summary(geneId, data):
    # Configure the Gemini client
    client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
    response = client.models.generate_content(
    model="gemini-2.0-flash", contents= PROMPT + f"{data}" )
    summary = response.text.strip()
    
    # Write to a text file
    with open(csv_file_name, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([geneId, summary])
    with open(text_file_name, 'a') as f:
        f.write(f'{summary}\n')
    return [S(summary)]

@register_atoms(pass_metta=True)
def utils(metta):
    writeSummary = OperationAtom(
        "write_summary",
        lambda geneId, data: write_summary(geneId, data),
        ["Atom","Expression", "Expression"],
        unwrap=False
    )
    return {
        r"write_summary": writeSummary
    }




"""
def call_gemini_api(summary: str) -> str:
    client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
    response = client.models.generate_content(
    model="gemini-2.0-flash", contents= PROMPT + summary)
    return response.text

def summarize_data():
    with open('../data/nodes.metta', 'r') as file:
        data = file.read().replace('\n', ' ').strip()
    summary = call_gemini_api(data)
    time = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
    file_name = f"txt/results_{time}.txt"
    with open(file_name, 'w') as f:
        f.write(summary)
    return
summarize_data()"""