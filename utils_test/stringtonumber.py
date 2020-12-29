
input = "@Cyberlink"
input = input.lower()
output = ""
for character in input:
   number = ord(character) - 96
   output += str(number)
print (output)