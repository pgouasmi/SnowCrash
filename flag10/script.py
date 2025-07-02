#!/usr/bin/env python3
import socket
import threading
import datetime
import sys

def handle_client(client_socket, address):
    """Gère une connexion client"""
    print(f"[{datetime.datetime.now()}] Nouvelle connexion de {address[0]}:{address[1]}")
    
    try:
        while True:
            # Recevoir les données
            data = client_socket.recv(4096)
            if not data:
                break
            
            # Afficher les données reçues
            print(f"[{datetime.datetime.now()}] Reçu de {address[0]}:{address[1]}:")
            print(f"  Données brutes (hex): {data.hex()}")
            
            # Essayer d'afficher en texte
            try:
                text = data.decode('utf-8')
                print(f"  Texte: {repr(text)}")
            except UnicodeDecodeError:
                print(f"  Texte: [données binaires non-UTF8]")
            
            # Optionnel: renvoyer une réponse
            # client_socket.send(b"Message recu\n")
            
    except ConnectionResetError:
        print(f"[{datetime.datetime.now()}] Connexion fermée par {address[0]}:{address[1]}")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] Erreur avec {address[0]}:{address[1]}: {e}")
    finally:
        client_socket.close()
        print(f"[{datetime.datetime.now()}] Connexion terminée avec {address[0]}:{address[1]}")

def main():
    # Configuration
    HOST = '0.0.0.0'  # Écouter sur toutes les interfaces
    PORT = 6969
    
    # Créer le socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind et listen
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"[{datetime.datetime.now()}] Serveur en écoute sur {HOST}:{PORT}")
        print("Appuyez sur Ctrl+C pour arrêter")
        
        while True:
            # Accepter les connexions
            client_socket, address = server_socket.accept()
            
            # Créer un thread pour chaque client
            client_thread = threading.Thread(
                target=handle_client, 
                args=(client_socket, address)
            )
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print(f"\n[{datetime.datetime.now()}] Arrêt du serveur...")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] Erreur serveur: {e}")
    finally:
        server_socket.close()
        print(f"[{datetime.datetime.now()}] Serveur arrêté")

if __name__ == "__main__":
    main()