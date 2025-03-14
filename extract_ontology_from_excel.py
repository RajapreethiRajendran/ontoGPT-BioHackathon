import psycopg
import subprocess
import pandas as pd
import os
import pandas as pd


def process_record(objekt_id, habitat, template_path):
    try:
        process = subprocess.run(
            ['ontogpt', '-v', 'extract', '-t', template_path, '-m', 'ollama/llama3'],
            input=habitat,
            text=True,
            capture_output=True
        ) 
        if process.returncode == 0:
            result_text = process.stdout.strip()
            return result_text
        else:
            print(f"Error processing habitat for objekt_id {objekt_id}: {process.stderr}")
            return None
    except Exception as e:
        print(f"Error during ontogpt call for objekt_id {objekt_id}: {e}")
        return None

def save_result_to_excel(data):

    df = pd.DataFrame(data, columns=['objekt_id', 'habitat', 'result'])
    if os.path.exists(EXCEL_RESULT_FILE):
        existing_df = pd.read_excel(EXCEL_RESULT_FILE)
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_excel(EXCEL_RESULT_FILE, index=False)
    print(f"Data saved to {EXCEL_RESULT_FILE}")

def main(template_path, df):
    processed_data = []
    for row in df.iterrows():
        objekt_id = row['objekt_id']
        habitat = row['habitat']
        if len(habitat) > 10:
            print(f"Processing objekt_id: {objekt_id}, habitat: {habitat}")
            result = process_record(objekt_id, habitat, template_path)
            if result is None:
                print(f"Skipping objekt_id {objekt_id} due to processing error.")
                continue

            processed_data.append({'objekt_id': objekt_id, 'habitat': habitat, 'result': result})

    if processed_data:
        save_result_to_excel(processed_data)
    print("Processing complete.")

EXCEL_RESULT_FILE = 'results.xlsx'
EXCEL_RECORD_FILE = 'habitat_records.xlsx'

if __name__ == "__main__":
    template_path = 'src/ontogpt/templates/biodiversity_with_prompt_v2.yaml'
    df = pd.read_excel(EXCEL_RECORD_FILE)

    main(template_path, df)
