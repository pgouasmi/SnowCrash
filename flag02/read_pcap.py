from scapy.all import rdpcap, IP, TCP

packets = rdpcap("level02.pcap")
password_chars = []
password_mode = False

for packet in packets:
    if IP in packet and TCP in packet:
        tcp = packet[TCP]
        
        if tcp.payload and tcp.sport == 39247:
            # print(tcp.payload)
            data = bytes(tcp.payload)
            # print(data)``
            
            if not password_mode:
                continue
                
            for byte in data:
                if byte == 0x7f:
                    if password_chars:
                        password_chars.pop()
                elif 32 <= byte <= 126:
                    password_chars.append(chr(byte))
                elif byte in [13, 10]:
                    password_mode = False
                    break
        
        elif tcp.payload and tcp.dport == 39247:
            try:
                text = bytes(tcp.payload).decode('utf-8', errors='ignore')
                print(text)
                if "Password:" in text:
                    password_mode = True
                    password_chars = []
            except:
                pass

password = ''.join(password_chars)
print(f"Mot de passe: {password}")