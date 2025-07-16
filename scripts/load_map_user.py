import os
import sqlite3
import json

# Path to map/user JSON files
map_user_path = "data/map/user"

# Connect to SQLite database
conn = sqlite3.connect("db/phonepe_data.db")
cursor = conn.cursor()

inserted_count = 0

for root, dirs, files in os.walk(map_user_path):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                try:
                    content = json.load(f)
                    districts = content.get("data", {}).get("districts", [])

                    if not districts:
                        print(f"⚠️ Skipping empty or null districts: {file_path}")
                        continue

                    table = os.path.basename(file_path).replace(".json", "")
                    parts = table.split("_")
                    year = int(parts[-2])
                    quarter = int(parts[-1])
                    state = "_".join(parts[4:-2])

                    for district in districts:
                        name = district.get("name", "")
                        registered_users = district.get("registeredUsers", 0)
                        app_opens = district.get("appOpens", 0)

                        cursor.execute("""
                            INSERT INTO map_user (
                                state, year, quarter, district, registered_users, app_opens
                            ) VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            state,
                            year,
                            quarter,
                            name,
                            registered_users,
                            app_opens
                        ))
                        inserted_count += 1

                except Exception as e:
                    print(f"❌ Error in file {file_path}: {e}")

conn.commit()
conn.close()

print(f"✅ Map user data loaded successfully. Total rows inserted: {inserted_count}")
