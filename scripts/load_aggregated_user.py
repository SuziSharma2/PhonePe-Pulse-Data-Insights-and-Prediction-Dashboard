import os
import sqlite3
import json

# Path to your user JSON files
user_path = "data/aggregated/user"

# Connect to SQLite database
conn = sqlite3.connect("db/phonepe_data.db")
cursor = conn.cursor()

inserted_count = 0

# Walk through user data files
for root, dirs, files in os.walk(user_path):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                try:
                    content = json.load(f)
                    users = content.get("data", {}).get("usersByDevice", [])

                    if not users:
                        print(f"⚠️ Skipping empty or null usersByDevice: {file_path}")
                        continue

                    table = os.path.basename(file_path).replace(".json", "")
                    parts = table.split("_")
                    year = int(parts[-2])
                    quarter = int(parts[-1])
                    state = "_".join(parts[4:-2])

                    for device in users:
                        brand = device.get("brand", "")
                        count = device.get("count", 0)
                        percentage = device.get("percentage", 0.0)

                        cursor.execute("""
                            INSERT INTO aggregated_user (
                                state, year, quarter, brand, count, percentage
                            ) VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            state,
                            year,
                            quarter,
                            brand,
                            count,
                            percentage
                        ))
                        inserted_count += 1

                except Exception as e:
                    print(f"❌ Error in file {file_path}: {e}")

# Commit and close
conn.commit()
conn.close()

print(f"✅ User data loaded successfully. Total rows inserted: {inserted_count}")
