import os
import csv
import time
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# import openai

# # Set OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")



PROMPT = '''
You are an expert in predictive maintenance for industrial systems. Given the following abstract or summary of a research paper, classify it according to these fields:


1. Domain: examples of domain include but are not limited to: "HVAC systems", "Commercial buildings", "Pharmaceutical facilities", "Chip manufacturing". 
2. Input: types of input data including but not limited to: "Sensor data", "Time series", "Natural language text", "Structured data", "Unstructured data", "Images".
3. Output: type of predicted output including but not limited to: "Remaining Useful Life", "Fault prediction", "Root cause analysis".
4. Modeling category: one of ["Rules and/or logic based", "Physics based", "First principles", "Knowledge based", "Data driven", "Hybrid", "Neurosymbolic", "Physics informed", "Other"].
5. Modeling technique: specific techniques mentioned (e.g., "SVM", "GNN", "CNN", "PINN", etc.).
6. Explainability: whether it uses interpretable or explainable techniques ("Yes: <technique>" or "No").
7. Relevance score: integer from 0 (lowest) to 5 (highest), where relevance is defined as the study's applicability to predictive maintenance in HVAC systems for commercial buildings, pharmaceutical facilities, or chip manufacturing, using sensor data, combining rules and ML, and being interpretable.

When your answer is 'Other', think again. Analyse the text to see if you can figure out the domain.


Provide your answers in JSON format where the keys are the field names from the above list.

Abstract: """{text}"""
Answer:
'''


def classify_record(text):
    prompt = PROMPT.format(text=text)
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def main():
    input_csv = "Documents/literature review/bibtex/PdM-RUL-FDD-9006-scopus/data_missed.csv"
    output_csv = "Documents/literature review/bibtex/PdM-RUL-FDD-9006-scopus/data_extract_missed.csv"

    errors = []
    err_count = 0

    with open(input_csv, newline='', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)
        # Write header
        writer.writerow(["Domain", "Input", "Output", "Modeling category", "Modeling technique", "Explainability", "Relevance", "EID"])

        for i, row in enumerate(reader, 1):
            text = row['text']
            eid = row['EID']
            classification = classify_record(text)

            try:
                classification = json.loads(classification)
                classification['eid'] = eid

                # print(list(classification.values()))
                # print(classification)

                classification = classification.values()
                writer.writerow(classification)
            except:
                errors.append(eid)
                writer.writerow(['other','other','other','other','other','other','other',eid])
                print("parse error: ", eid, len(errors))



            # Rate-limit to avoid hitting rate limits
            time.sleep(0.5)
            if i % 100 == 0:
                print(f"Processed {i} records...")

    print("Classification complete. Output written to", output_csv, len(errors))
    
    with open("errors.txt", "a") as err_file:
        err_file.write(str(errors))



if __name__ == "__main__":
    main()
