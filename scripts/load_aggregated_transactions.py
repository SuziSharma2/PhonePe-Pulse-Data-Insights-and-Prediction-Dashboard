import os
import sqlite3
import json

# Path to your transaction JSON files
transaction_path = "data/aggregated/transaction"

# Connect to the SQLite database
conn = sqlite3.connect("db/phonepe_data.db")
cursor = conn.cursor()

inserted_count = 0

# Loop through all transaction JSON files
for root, dirs, files in os.walk(transaction_path):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                try:
                    content = json.load(f)
                    if isinstance(content, dict):
                        data = content.get("data", {}).get("transactionData", [])
                        for entry in data:
                            transaction_type = entry.get("name", "")
                            for instrument in entry.get("paymentInstruments", []):
                                table = os.path.basename(file_path).replace(".json", "")
                                parts = table.split("_")
                                year = int(parts[-2])
                                quarter = int(parts[-1])
                                state = "_".join(parts[4:-2])

                                cursor.execute("""
                                    INSERT INTO aggregated_transactions (
                                        state, year, quarter, transaction_type,
                                        transaction_count, transaction_amount
                                    ) VALUES (?, ?, ?, ?, ?, ?)
                                """, (
                                    state,
                                    year,
                                    quarter,
                                    transaction_type,
                                    instrument.get("count", 0),
                                    instrument.get("amount", 0.0)
                                ))
                                inserted_count += 1
                except Exception as e:
                    print(f"❌ Error in file {file_path}: {e}")

# Save changes and close
conn.commit()
conn.close()

print(f"✅ Transactions data loaded successfully. Total rows inserted: {inserted_count}")
