import sys

def getfile():
    try:
        file = open("/home/flash/Documents/SnowCrash/flag09/token", 'rb')
        s = file.read(100)
        print(s)
        return s

    except:
        print("error opening token file")

def forward(s, count):
#    s = "f4kmm6p|=�p�n��DB�Du{��"
   if isinstance(s, str):
       bstr = bytearray(s.encode('utf8', errors='replace'))
   else:
       bstr = bytearray(s)
   for i in range(count):
       for j in range(len(bstr) - 1):
           bstr[j] = (bstr[j] + j) % 256
       try:
           decoded = bstr.decode('ascii')
           print(f"Iteration {i}: {decoded}")
       except UnicodeDecodeError:
           pass
   return bstr

def backward(s, count):
#    s = "f4kmm6p|=�p�n��DB�Du{��"
   if isinstance(s, str):
       bstr = bytearray(s.encode('utf8', errors='replace'))
   else:
       bstr = bytearray(s)
   for i in range(count):
       for j in range(len(bstr) - 1):
           bstr[j] = (bstr[j] - j) % 256
       try:
           decoded = bstr.decode('ascii')
           print(f"Iteration {i}: {decoded}")
       except UnicodeDecodeError:
           pass
   return bstr


if __name__ == "__main__":
    s = getfile()
    print("forward\n___________________________________________________________________________________")
    forward(s, 1000)
    print("reverse\n___________________________________________________________________________________")
    backward(s, 1000)