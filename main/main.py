from hyperon.ext import register_atoms
from hyperon.atoms import OperationAtom, S
import csv
from datetime import datetime
from google import genai
from dotenv import load_dotenv
import os
load_dotenv()

def get_csv_file_name() -> str:
    """Creates a name and file for the current instance of the controller."""
    time = datetime.now().strftime("%H:%M:%S-%d-%m-%Y")
    file_name = f"csv/results_{time}.csv"
    return [S(file_name)]

def write_to_csv(afatoms, name):
    data = []

    for atom in afatoms:

def read_csv(file_path: str):
    """Reads a CSV file and returns its content."""
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def summarize_data(data):
    """Summarizes the CSV data and returns a string summary."""
    summary = []
    for row in data:
        summary.append(f"Pattern: {row['pattern']}, STI: {row['sti']}, LTI: {row['lti']}")
    return "\n".join(summary)
    
PROMPT="Generate a human readable summary based on this csv data"
"""Calls the Gemini API to summarize the provided text and returns the response."""
def call_gemini_api(summary: str) -> str:
    client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
    response = client.models.generate_content(
    model="gemini-2.0-flash", contents=PROMPT)
    return response.text

@register_atoms(pass_metta=True)
def utils(metta):
    getCsvFileName = OperationAtom(
        "get_csv_file_name",
        lambda: get_csv_file_name(),
        ["Atom"],
        unwrap=False
    )

    writeToCsv = OperationAtom(
        "write_to_csv",
        lambda afatoms, name: write_to_csv(afatoms, name),
        ["Expression", "Expression", "Atom"],
        unwrap=False
    )

    summarizeCsv = OperationAtom(
        "summarize_csv",
        lambda file_path: call_gemini_api(summarize_data(read_csv(file_path.get_name()))),
        ["Expression"],
        unwrap=False
    )

    return {
        r"get_csv_file_name": getCsvFileName,
        r"write_to_csv": writeToCsv,
        r"summarize_csv": summarizeCsv
    }