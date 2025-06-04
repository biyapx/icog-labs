from hyperon.ext import register_atoms
from hyperon.atoms import OperationAtom, S, ExpressionAtom, SymbolAtom
from datetime import datetime
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

PROMPT = """Summarize the following data in a human-readable format. 
The data is a list of dictionaries, where each dictionary represents a single object with the following keys:
- timestamp: The timestamp of the object.
- pattern: The pattern of the object.
- sti: The sti value of the object.
- lti: The lti value of the object.
The data is provided as a list of dictionaries as: 
"""

def get_txt_file_name() -> list:
    time = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
    file_name = f"txt/results_{time}.txt"
    return [S(file_name)]

def write_summary(afatoms, name):
    data = []
    
    for atom in afatoms.get_children():
        (pattern, av) = atom.get_children()
        (_, sti, lti, _) = av.get_children()
        data.append({
            "timestamp": str(datetime.now()),
            "pattern": str(pattern),
            "sti": str(sti),
            "lti": str(lti)
        })

    # Convert the data list to a string
    data_string = PROMPT + "\n" + str(data)

    # Configure the Gemini client
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-pro"

    # Send data to Gemini
    response = model.generate_content(data_string)
    summary = response.text

    # Extract the file name from the Atom
    file_name = name[0].get_name() if isinstance(name, list) else name.get_name()

    # Write to file
    with open(file_name, 'a') as f:
        f.write(summary + '\n')

    return [S("wrote")]

@register_atoms(pass_metta=True)
def main(metta):
    getTextFileName = OperationAtom(
        "get_txt_file_name",
        lambda: get_txt_file_name(),
        ["Atom"],
        unwrap=False
    )
    writeSummary = OperationAtom(
        "write_summary",
        lambda afatoms, name: write_summary(afatoms, name),
        ["Expression", "Expression", "Atom"],
        unwrap=False
    )
    return {
        r"get_txt_file_name": getTextFileName,
        r"write_summary": writeSummary
    }

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
summarize_data()