from passlib.hash import des_crypt

hash_target = "42hDRfypTqqnw"

with open("top100k.txt", "r") as f:
    for line in f:
        password = line.strip()
        print(password)
        if des_crypt.verify(password, hash_target):
            print(f"\n!!!!!!!!!!!!!!!trouve: {password}")
            exit(0)
            
print("pas trouve")