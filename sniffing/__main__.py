from sniffing.sniffer import start_sniffing
from sniffing.data.msg import Msg
import argparse
import logging
from pprint import pprint
from sniffing.packet_parser import parse_packet  # Importer la fonction parse_packet de parser.py

def on_msg(msg):
    global m
    m = msg

    # # Affiche le type du message
    # print("\n--- New Packet Received ---")
    # print("Message type:")
    # pprint(msg.json()["__type__"])
    
    # # Affiche les données du message converties depuis JSON
    # print("Message JSON data:")
    # pprint(msg.json())

    # Appeler le parseur pour traiter le paquet
    packet = msg.json()
    parse_packet(packet)

def main():
    parser = argparse.ArgumentParser(description="Packet sniffer")
    parser.add_argument("--interface", type=str, help="Network interface to sniff on")
    args = parser.parse_args()

    # Configure le logging pour ne montrer que les erreurs
    logging.basicConfig(level=logging.ERROR)
    
    # Démarre le sniffer avec la fonction on_msg
    stop = start_sniffing(on_msg)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        stop()

if __name__ == "__main__":
    main()
