import psycopg
import subprocess
import pandas as pd
import os



def fetch_top_records(limit=100):
    conn = None
    try:
        conn = psycopg.connect(**DB_CONFIG)
        print('Connected to the PostgreSQL database')
        query = f"""
        SELECT objekt_id, habitat
        FROM objekte
        JOIN fundzeiten USING(fundzeit_id)
        JOIN fundorte USING(fundort_id)
        WHERE  sammlung_id IN (32, 34) AND habitat IS NOT NULL AND LENGTH(habitat) > 70
        ORDER BY LENGTH(habitat) DESC LIMIT {limit};
        """
        with conn.cursor() as cur:
            cur.execute(query)
            records = cur.fetchall()
        if len(records) > 0:
            save_records_to_excel(records)
        return records
    except Exception as e:
        print(f"Error fetching records: {e}")
        return []
    finally:
        if conn:
            conn.close()

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

def save_records_to_excel(data):

    df = pd.DataFrame(data, columns=['objekt_id', 'habitat'])
    if os.path.exists(EXCEL_RECORD_FILE):
        existing_df = pd.read_excel(EXCEL_RECORD_FILE)
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_excel(EXCEL_RECORD_FILE, index=False)
    print(f"Data saved to {EXCEL_RECORD_FILE}")


def main(template_path, limit):
    records = fetch_top_records(limit=limit)
    if not records:
        print("No records fetched. Exiting.")
        return

    processed_data = []
    for record in records:
        objekt_id, habitat = record
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

#Please provide the database details, limit to extract the number of rows from sesam database and template path

DB_CONFIG = {
    "dbname": "",
    "user": "",
    "password": "",
    "host": "localhost",
    "port": "5432",
}
EXCEL_RESULT_FILE = 'results.xlsx'
EXCEL_RECORD_FILE = 'habitat_records.xlsx'

if __name__ == "__main__":
    limit = 1000000
    template_path = 'src/ontogpt/templates/biodiversity_with_prompt_v2.yaml'
    main(template_path, limit)

