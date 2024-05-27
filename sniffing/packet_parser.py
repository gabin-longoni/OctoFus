import json
from datetime import datetime

def convert_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

def handle_chat_server_message(packet):
    sender_name = packet['senderName']
    message = packet['content']
    timestamp = convert_timestamp(packet['timestamp'])
    channel = packet.get('channel', -1)  # Utilisation d'un canal par défaut (-1) si non présent

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

def parse_packet(packet):
    packet_type = packet.get('__type__')
    
    if packet_type == 'ChatServerMessage':
        handle_chat_server_message(packet)
    else:
        print(f"Unknown packet type: {packet_type}")
