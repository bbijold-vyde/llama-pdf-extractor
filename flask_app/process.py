import openai 
import re
import fitz  # PyMuPDF PDF READ
import os
import time
import json
import pandas as pd
from langchain_community.llms import Ollama

#API KEY
openai.api_key = "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"

#PDF READ
def read_pdf(file_path):
    try:
        # Open the PDF
        doc = fitz.open(file_path)

        # Extract text from the first page
        first_page_text = doc[0].get_text()

        # Close the document
        doc.close()

        return  first_page_text # Return the first page
    except Exception as e:
        print("Error opening PDF: " + str(e) + file_path)
        return "Error opening PDF: " + str(e) + file_path

def extract_data_with_gpt(textOfCV):
    # Replace this with an appropriate prompt for the GPT model based on your data
    prompt = (
    "A következő szöveg alapján kérlek, gyűjtsd ki a jelentkező adatait, és formázd őket JSON formátumba. "
    "Az adatok között szerepelnie kell a névnek, email címnek, telefonszámnak, középiskola nevének, középiskolai szaknak, "
    "egyetem nevének, egyetemi szaknak, idegen nyelvnek és annak szintjének. Ha valamelyik adat nem áll rendelkezésre, "
    "az arra vonatkozó mezőt hagyd üresen. A szöveg a következő: \"" + textOfCV + "\"\n"
    "A JSON formátum a következő legyen:\n"
    "{\n"
    "    \"nev\": \"<NÉV>\",\n"
    "    \"email\": \"<EMAIL>\",\n"
    "    \"telefonszam\": \"<TELEFONSZÁM>\",\n"
    "    \"kozepiskola\": \"<KÖZÉPISKOLA>\",\n"
    "    \"kozep_szak\": \"<KÖZÉPISKOLAI SZAK>\",\n"
    "    \"egyetem\": \"<EGYETEM>\",\n"
    "    \"egyetem_szak\": \"<EGYETEMI SZAK>\",\n"
    "    \"nyelvvizsga\": \"<NYELVVIZSGA>\",\n"
    "    \"nyelv_szintje\": \"<NYELV SZINTJE>\"\n"
    "}"
    )

    response = openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=1024)
    return response.choices[0].text.strip()

def extract_data_with_llama(textOfCV):
    llm = Ollama(model="llama3", format="json")
    prompt = (
    "A következő szöveg alapján kérlek, gyűjtsd ki a jelentkező adatait, és formázd őket JSON formátumba. "
    "Az adatok között szerepelnie kell a névnek, email címnek, telefonszámnak, középiskola nevének, középiskolai szaknak, "
    "egyetem nevének, egyetemi szaknak, idegen nyelvnek és annak szintjének. Ha valamelyik adat nem áll rendelkezésre, "
    "az arra vonatkozó mezőt hagyd üresen. A szöveg a következő: \"" + textOfCV + "\"\n"
    "A formátum a következő legyen:\n"
    "{\n"
    "    \"nev\": \"<NÉV>\",\n"
    "    \"email\": \"<EMAIL>\",\n"
    "    \"telefonszam\": \"<TELEFONSZÁM>\",\n"
    "    \"kozepiskola\": \"<KÖZÉPISKOLA>\",\n"
    "    \"kozep_szak\": \"<KÖZÉPISKOLAI SZAK>\",\n"
    "    \"egyetem\": \"<EGYETEM>\",\n"
    "    \"egyetem_szak\": \"<EGYETEMI SZAK>\",\n"
    "    \"nyelvvizsga\": \"<NYELVVIZSGA>\",\n"
    "    \"nyelv_szintje\": \"<NYELV SZINTJE>\"\n"
    "}"
    "A válasz csak a JSON struktúrát tartalmazza"
    )
    result = llm.invoke(prompt)
    #print(result)
    return result

def post_process(response_text):
    # Parse the response text into a dictionary
    data_dict = json.loads(response_text)

    # Define the desired keys and their default values
    keys = ["nev", "email", "telefonszam", "kozepiskola", "kozep_szak", "egyetem", "egyetem_szak", "nyelvvizsga", "nyelv_szintje"]
    default_value = ""

    # Create a new dictionary with the desired structure
    structured_data = {key: data_dict.get(key, default_value) for key in keys}

    # Convert the structured data back into a JSON string
    structured_json = json.dumps(structured_data)

    return structured_json

def process_document(file_path):
    try:
        print(f"Processing {file_path}")
        textOfCV = read_pdf(file_path)
        response = extract_data_with_llama(textOfCV)
        data = json.loads(response)
        df = pd.DataFrame([data])
        if not os.path.isfile('output.csv'):
            df.to_csv('output.csv', mode='w', header=True, index=False)
        else:
            df.to_csv('output.csv', mode='a', header=False, index=False)
    except Exception as e:
        print(f"An error occurred: {e}")
