import random
import os.path


# this funtion is used to read files
def read_text(file_path):
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            return file.read()
    else:
        print("There is no file you have entered.")
        input()
        exit()


private_keys = []


# this function is used to generate private keys and calculate public keys to get secret key
def generate_keys():
    if len(private_keys) == 2:
        del private_keys[:]

    y1 = random.randint(1, 2147483423)  # random y01
    y2 = random.randint(1, 2147483422)  # random y01
    m1 = 2147483642  # given m1
    m2 = 2147483423  # given m2
    a1 = 450  # given a1
    a2 = 234  # given a2
    alpha = 3  # given alpha
    prime = 353  # given prime

    for i in range(2):
        # Evaluate 2 LCGs
        y1 = (y1 * a1) % m1
        y2 = (y2 * a2) % m2
        # CLCG equation
        x = (y1 - y2) % m1
        # calculate private key using clcgs formula and cope range not to higer than 500 by modding 500
        if x > 0:
            private_keys.append((x / m1) % 500)
        elif x < 0:
            private_keys.append((x / (m1 + 1)) % 500)
        elif x == 0:
            private_keys.append(((m1 - 1) / m1) % 500)

    insec_secretA = (alpha ** private_keys[0]) % prime  # calculate insecure channel of user A
    insec_secretB = (alpha ** private_keys[1]) % prime  # calculate insecure channel of user B
    # calculate shared key for user A based on insecure channel of user B and private key of user A
    a_secret = ((insec_secretB ** private_keys[0]) % prime)
    # calculate shared key for user B based on insecure channel of user A and private key of user B
    b_secret = ((insec_secretA ** private_keys[1]) % prime)
    print("User A Private Key :", private_keys[0])
    print("User B Private Key :", private_keys[1])
    print("User A Public Key (insecure chanel):", insec_secretA)
    print("User B Public Key (insecure chanel):", insec_secretB)
    print("Secret key : ", (round(a_secret, 10) + round(b_secret, 10)) / 2)


# this function is to encrypt and decrypt message
def crypt(key, message):
    S = list(range(256))  # create list of 256 indexes
    j = 0

    for i in list(range(256)):  # loop to swap between key and store posible ascii code
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    j, y = 0, 0
    return_output = []

    for char in message:  # loop again to swap each message index and key table above
        j = (j + 1) % 256
        y = (y + S[j]) % 256
        S[j] = S[y]
        S[y] = S[j]
        return_output.append(chr(ord(char) ^ S[(S[j] + S[y]) % 256]))

    return "".join(return_output)


# this function is to match the function read text and crypt to encrypt the message (calculate last 64 bits block)
def send():
    plain = read_text(input(
        "Enter the message file you need to send(ex.plaintext.txt):"))  # read the text file and store it in to 'plain'
    plain = list(plain)  # turn every letter into array
    message = list(plain)
    len_message = len(plain)  # count the length of the array plain
    cal_bytes = len_message  # get the last byte of last block
    cal_last_block = (cal_bytes % 8)  # get the first byte of last block
    message = len_message - cal_last_block - 8
    message_last = len_message - cal_last_block
    list_plaintext = plain[
                     (len_message - cal_last_block) - 8:len_message - cal_last_block]  # store every bytes of last block
    list_message = plain[0:message]
    arr_mes_last = plain[len_message - cal_last_block:len_message]

    plain = ""  # 'plain' is = to new 'plain' which is string
    message = ""
    message_last = ""
    for i in list_plaintext:  # loop and add every byte into string 'plain'
        plain += i

    for i in list_message:
        message += i

    for i in arr_mes_last:
        message_last += i

    key = input("Enter key to encrypt message :")  # now get the secret key of user A and store it in 'key'
    encrypted = crypt(key,
                      plain)  # call 'crypt' function along with the 'key' and last 64bits block of the read plaintext from text file
    print("\nYou encrypted last 64bits block message is :", encrypted)
    print("Your message will be sent like this :", message, encrypted, message_last)


# selection menu
while True:
    print("\n1.Generate Keys")
    print("2.Encrypt Message")
    print("3.Decrypt Message")
    print("4.Exit")
    choice = input("Please select menu:")
    if choice == '1':
        generate_keys()
    if choice == '2':
        send()
    if choice == '3':
        encrypted = input("Enter encrypted message you need to decrypt :")
        user_input = input("Please enter key to decrypt the encrypted message :")  # get the secret key from user B
        print("Decrypted message :", crypt(user_input, encrypted))
    if choice == '4':
        break
input()
