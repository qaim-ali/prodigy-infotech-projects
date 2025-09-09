message="hello, World!"
shift=7
LAST_CHAR_CODE= ord("Z")
FIRST_CHAR_CODE=ord("A")
CHAR_RANGE=26


def caesar_shift(message, shift,mode="encrypt"):
    #adjust mode for decryption
    if mode == "decrypt":
        shift=-shift
    # resut placeholder
    result = ""

    # go through each of the letters in the message
    for char in message.upper():
        if char.isalpha():
            # do something
            # convert this code in to the ASCII code.
            char_code = ord(char)
            new_char_code = char_code + shift

            if new_char_code > LAST_CHAR_CODE:
                new_char_code -= CHAR_RANGE
            if new_char_code< FIRST_CHAR_CODE:
                new_char_code += CHAR_RANGE

            new_char = chr(new_char_code)
            result = result + new_char
            #print(char, char_code, new_char_code, new_char)
        else:
            result = result + char
    print(result)
#caesar_shift("my name is qaim ali", 3)
#def main():
print("Caesar Cipher program")
print("1. encrypt a program")
print("2. decrypt a program")
choice=int(input("ENTER YOUR CHOICE(1 OR 2): "))
if choice == 1:
    user_message = input("KINLDY WRITE YOUR MESSAGE HERE: ")
    user_shift = int(input("KINLDY INPUT YOUR SHIFT KEY HERE(IN INTEGER FROM: "))
    caesar_shift(user_message, user_shift,"encrypt")
elif choice == 2:
    user_message = input("KINLDY WRITE YOUR MESSAGE HERE: ")
    user_shift = int(input("KINLDY INPUT YOUR SHIFT KEY HERE(IN INTEGER FROM: "))
    caesar_shift(user_message, user_shift,"decrypt")
else:
    print("invlaid Choice. please select 1 or 2")
#if __name__=="__main__":
 #   main()


"""user_message=input("KINLDY WRITE YOUR MESSAGE HERE: ")
user_shift=int(input("KINLDY INPUT YOUR SHIFT KEY HERE(IN INTEGER FROM): "))
caesar_shift(user_message,user_shift)"""

