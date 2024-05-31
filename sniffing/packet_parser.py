import json
import os
from datetime import datetime

# Function to load JSON files
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Directory where the JSON files are located
json_dir = os.path.join(os.path.dirname(__file__), '..', 'resources', 'game_resources')

# Load the JSON files
item_names = load_json(os.path.join(json_dir, 'objets.json'))
# If you need to load other JSON files (e.g., metiers, monstres, ressources), do it similarly
# metiers_names = load_json(os.path.join(json_dir, 'metiers.json'))
# monstres_names = load_json(os.path.join(json_dir, 'monstres.json'))
# ressources_names = load_json(os.path.join(json_dir, 'ressources.json'))

def convert_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

def handle_chat_server_message(packet):
    sender_name = packet['senderName']
    message = packet['content']
    timestamp = convert_timestamp(packet['timestamp'])
    channel = packet.get('channel', -1)

    if channel == 0:
        channel_name = "Général"
    elif channel == 5:
        channel_name = "Commerce"
    elif channel == 6:
        channel_name = "Recrutement"
    elif channel == 9:
        channel_name = "Privé"
    elif channel == 14:
        channel_name = "Communauté"
    else:
        channel_name = f"Canal {channel}"

    print(f"[{timestamp}] [{channel_name}] {sender_name}: {message}")

def handle_character_selected_success_message(packet):
    character_info = packet['infos']
    character_name = character_info['name']
    
    print(f"Character selected: {character_name}")

def handle_inventory_content_message(packet):
    objects = packet['objects']
    kamas = packet['kamas']
    
    print(f"Kamas: {kamas}")
    print("Inventory items:")
    for obj in objects:
        item_id = obj['objectGID']
        item_name = item_names.get(str(item_id), f"Unknown Item (ID: {item_id})")
        quantity = obj['quantity']
        position = obj.get('position', 63)
        if position == 63:  # Position 63 indicates the item is in inventory
            print(f"Item: {item_name}, Quantity: {quantity} (In inventory)")
        else:
            print(f"Item: {item_name}, Quantity: {quantity} (Equipped)")

def handle_kamas_update_message(packet):
    kamas_total = packet['kamasTotal']
    print(f"Total Kamas: {kamas_total}")

def handle_storage_inventory_content_message(packet):
    objects = packet['objects']
    kamas = packet['kamas']
    
    print(f"Kamas in storage: {kamas}")
    print("Storage inventory items:")
    for obj in objects:
        item_id = obj['objectGID']
        item_name = item_names.get(str(item_id), f"Unknown Item (ID: {item_id})")
        quantity = obj['quantity']
        print(f"Item: {item_name}, Quantity: {quantity} (In storage inventory)")

def handle_unknown_packet(packet):
    pass

def parse_packet(packet):
    packet_type = packet.get('__type__')
    
    # Dictionary to emulate switch/case
    handlers = {
        'ChatServerMessage': handle_chat_server_message,
        'CharacterSelectedSuccessMessage': handle_character_selected_success_message,
        'InventoryContentMessage': handle_inventory_content_message,
        'KamasUpdateMessage': handle_kamas_update_message,
        'StorageInventoryContentMessage': handle_storage_inventory_content_message
    }

    # Get the handler from the dictionary and call it, or call the unknown handler if not found
    handler = handlers.get(packet_type, handle_unknown_packet)
    handler(packet)
