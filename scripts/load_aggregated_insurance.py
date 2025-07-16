import os
import sqlite3
import json

# Path to JSON insurance files
insurance_path = "data/aggregated/insurance"

# Connect to SQLite
conn = sqlite3.connect("db/phonepe_data.db")
cursor = conn.cursor()

inserted_count = 0

# Walk through each file
for root, dirs, files in os.walk(insurance_path):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                try:
                    content = json.load(f)

                    if not isinstance(content, dict):
                        print(f"⚠️ Skipping file (not a dict): {file_path}")
                        continue

                    transaction_data = content.get("data", {}).get("transactionData", [])

                    if not isinstance(transaction_data, list):
                        print(f"⚠️ Skipping file (invalid structure): {file_path}")
                        continue

                    for entry in transaction_data:
                        name = entry.get("name", "")
                        for instrument in entry.get("paymentInstruments", []):
                            table = os.path.basename(file_path).replace(".json", "")
                            parts = table.split("_")
                            year = int(parts[-2])
                            quarter = int(parts[-1])
                            state = "_".join(parts[4:-2])

                            cursor.execute("""
                                INSERT INTO aggregated_insurance ("table", state, year, quarter, name, type, count, amount)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                table,
                                state,
                                year,
                                quarter,
                                name,
                                instrument.get("type", ""),
                                instrument.get("count", 0),
                                instrument.get("amount", 0.0)
                            ))
                            inserted_count += 1

                except Exception as e:
                    print(f"❌ Error in file {file_path}: {e}")

# Finalize
conn.commit()
conn.close()
print(f"✅ Insurance data loaded successfully. Total rows inserted: {inserted_count}")
