from google import genai
from hyperon.atoms import OperationAtom, S
from hyperon.ext import register_atoms
from datetime import datetime
import csv
import os
from dotenv import load_dotenv

load_dotenv()

# File setup
time_stamp = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
CSV_PATH = f"generated/results_{time_stamp}.csv"
TXT_PATH = f"generated/results_{time_stamp}.txt"

os.makedirs("generated", exist_ok=True)

with open(CSV_PATH, 'w', newline='') as f:
    csv.writer(f).writerow(["ID", "Summary"])

with open(TXT_PATH, 'w') as f:
    f.write("Summarized Text\n")

# Initialize Gemini client once
GEMINI_CLIENT = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Summary writer function
def write_summary(gene_id, data):
    prompt = (
        f"Please summarize the following gene-related data in one clear, concise paragraph for a general scientific audience:\n\n{data}"
    )
    
    response = GEMINI_CLIENT.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    summary = response.text.strip()

    with open(CSV_PATH, 'a', newline='') as f:
        csv.writer(f).writerow([gene_id, summary])

    with open(TXT_PATH, 'a') as f:
        f.write(f"{summary}\n")

    return [S(summary)]

# Register with Hyperon
@register_atoms(pass_metta=True)
def utils(metta):
    summarizer_atom = OperationAtom(
        "gene_summarizer",
        lambda gene_id, data: write_summary(gene_id, data),
        ["Atom", "Expression", "Expression"],
        unwrap=False
    )
    return {r"write_summary": summarizer_atom}
