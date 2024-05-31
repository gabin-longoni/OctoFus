import os
import requests
import json

# URLs for the text files containing IDs
urls = {
    "metiers": "https://thefalcon.gitbooks.io/bot-dofus-cookie-bot/content/Files/IDS/metiers.txt",
    "monstres": "https://thefalcon.gitbooks.io/bot-dofus-cookie-bot/content/Files/IDS/monstres.txt",
    "ressources": "https://thefalcon.gitbooks.io/bot-dofus-cookie-bot/content/Files/IDS/ressources.txt",
    "objets": "https://thefalcon.gitbooks.io/bot-dofus-cookie-bot/content/Files/IDS/objets.txt"
}

# Directory to save JSON files
output_dir = os.path.join(os.path.dirname(__file__), '..', 'resources', 'game_resources')
os.makedirs(output_dir, exist_ok=True)

# Function to download and convert text files to JSON
def convert_txt_to_json(url, filename):
    response = requests.get(url)
    response.encoding = 'utf-8'  # Ensure the response is read as UTF-8
    data = response.text
    
    # Remove BOM if present
    if data.startswith('\ufeff'):
        data = data[1:]
    
    lines = data.splitlines()
    
    # Assuming each line is formatted as "ID - Name"
    items = {}
    for line in lines:
        if '-' in line:
            item_id, name = line.split('-', 1)
            items[item_id.strip()] = name.strip()
    
    # Write to JSON file
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(items, json_file, indent=4, ensure_ascii=False)

# Convert each text file to JSON
for name, url in urls.items():
    convert_txt_to_json(url, f"{name}.json")

print(f"Conversion complete. JSON files have been created in '{output_dir}'.")
