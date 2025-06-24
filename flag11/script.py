#!/usr/bin/env python3
import socket
import threading
import sys
import time

class SocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        
    def connect(self):
        """Établir la connexion"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # Timeout de 10 secondes
            
            print(f"🔌 Connexion à {self.host}:{self.port}...")
            self.socket.connect((self.host, self.port))
            self.connected = True
            print("✅ Connecté avec succès!")
            return True
            
        except socket.timeout:
            print("❌ Timeout de connexion")
            return False
        except ConnectionRefused:
            print("❌ Connexion refusée")
            return False
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            return False
    
    def listen_for_responses(self):
        """Thread pour écouter les réponses du serveur"""
        try:
            while self.connected:
                try:
                    data = self.socket.recv(4096)
                    if not data:
                        print("\n🔌 Serveur a fermé la connexion")
                        self.connected = False
                        break
                    
                    # Afficher les données reçues
                    try:
                        text = data.decode('utf-8')
                        print(f"\n📨 Reçu: {repr(text)}")
                        
                        # Afficher aussi en texte lisible si possible
                        if text.isprintable():
                            print(f"📝 Texte: {text}")
                        
                    except UnicodeDecodeError:
                        print(f"\n📨 Reçu (hex): {data.hex()}")
                        print(f"📨 Reçu (raw): {data}")
                    
                    print("💬 Votre message: ", end="", flush=True)
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"\n❌ Erreur de réception: {e}")
                    self.connected = False
                    break
                    
        except Exception as e:
            print(f"\n❌ Erreur dans le thread d'écoute: {e}")
            self.connected = False
    
    def send_message(self, message):
        """Envoyer un message au serveur"""
        try:
            if not self.connected:
                print("❌ Pas connecté")
                return False
            
            # Permettre d'envoyer des données brutes en hex
            if message.startswith("hex:"):
                hex_data = message[4:].replace(" ", "")
                data = bytes.fromhex(hex_data)
                print(f"📤 Envoi (hex): {data.hex()}")
            else:
                data = message.encode('utf-8')
                print(f"📤 Envoi: {repr(message)}")
            
            self.socket.send(data)
            return True
            
        except Exception as e:
            print(f"❌ Erreur d'envoi: {e}")
            self.connected = False
            return False
    
    def interactive_mode(self):
        """Mode interactif"""
        if not self.connect():
            return
        
        # Démarrer le thread d'écoute
        listen_thread = threading.Thread(target=self.listen_for_responses)
        listen_thread.daemon = True
        listen_thread.start()
        
        print("\n=== Mode Interactif ===")
        print("Commandes spéciales:")
        print("  'quit' ou 'exit' - Quitter")
        print("  'hex:414243' - Envoyer des données en hexadécimal")
        print("  'raw:Hello\\n' - Envoyer avec échappements (\\n, \\r, \\t)")
        print("  'file:path' - Envoyer le contenu d'un fichier")
        print("")
        
        try:
            while self.connected:
                try:
                    message = input("💬 Votre message: ").strip()
                    
                    if message.lower() in ['quit', 'exit', 'q']:
                        break
                    
                    if not message:
                        continue
                    
                    # Commandes spéciales
                    if message.startswith("raw:"):
                        # Permettre les échappements
                        raw_msg = message[4:].encode().decode('unicode_escape')
                        self.socket.send(raw_msg.encode('utf-8'))
                        print(f"📤 Envoi (raw): {repr(raw_msg)}")
                        
                    elif message.startswith("file:"):
                        # Envoyer un fichier
                        filename = message[5:]
                        try:
                            with open(filename, 'rb') as f:
                                file_data = f.read()
                            self.socket.send(file_data)
                            print(f"📤 Fichier envoyé: {filename} ({len(file_data)} bytes)")
                        except Exception as e:
                            print(f"❌ Erreur lecture fichier: {e}")
                            
                    else:
                        # Message normal ou hex
                        self.send_message(message)
                
                except KeyboardInterrupt:
                    print("\n🛑 Interruption détectée")
                    break
                except EOFError:
                    print("\n🛑 EOF détecté")
                    break
                    
        finally:
            self.disconnect()
    
    def disconnect(self):
        """Fermer la connexion"""
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
                print("🔌 Connexion fermée")
            except:
                pass

def main():
    # Configuration
    HOST = "10.0.2.16"
    PORT = 5151
    
    print("🚀 Client Socket Interactif")
    print(f"Cible: {HOST}:{PORT}")
    
    client = SocketClient(HOST, PORT)
    
    try:
        client.interactive_mode()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du client")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()