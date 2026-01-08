#Secure password generator
#python_project
#loop to ask for pswd length:
import random
while True:
    pswd_length = int(input("How many characters should your secure password have? "))
    
    if pswd_length < 10:
        print("Your password should have at least 10 characters")
        continue
    if pswd_length > 32:
        print("Your password should have a maximum of 32 characters")
        continue
    #asking about inclusion of characters:
        #else:
    include_uppercase = input("Include uppercase? (y/n): ").lower() == "y"

    include_nums = input("Include numbers? (y/n): ").lower() == "y"
                   
    include_symbols = input("Include symbols? (y/n): ").lower() == "y"
    break
    
    #now the character pool is being formed:

lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
symbols = "!@#$%^&*()_+-=[]{}|;:,.<>/?"

full_pool = ""
full_pool = lowercase_letters


if include_uppercase:
        full_pool += uppercase_letters
if include_nums:
        full_pool += numbers
if include_symbols:
        full_pool += symbols        

if full_pool == "":
      print("No characters to form the password from")
      exit()

      #now is the time to build the password

password = ""

for i in range(pswd_length):
      char = random.choice(full_pool)
      password += char
      
print("This is your new secure password: " + password)
      

    