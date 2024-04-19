#!/usr/bin/python3.5

import getopt
import sys

# Caesar Cipher

# Symbol alphabet
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hm:t:k:", ["encdec=", "stext=", "offset="])

    except getopt.getoptError:
        sys.exit(1)

    if len(sys.argv[1:]) < 6:
        print('Usage: ./caesar.py -m <encrypt/decrypt> -t <plain/cipher text> -k <offset>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: ./caesar.py -m <mode> -t <plain/cipher text> -k <offset>')
            sys.exit()
        elif opt in ("-m", "--encdec"):
            mode = arg
        elif opt in ("-t", "--stext"):
            message = arg
        elif opt in ("-k", "--offset"):
            key = int(arg)

    # convert chars to lower case and call the crypto function
    message = message.lower()
    Enc_Dec(message, key, mode)


def Enc_Dec(message, key, mode):
    # Initialize the plain/cipher text variable
    translated = ''

    # run the encryption/decryption code on each symbol in the message string
    for symbol in message:
        if symbol in ALPHABET:
            # get the encrypted (or decrypted) index value for this symbol
            num = ALPHABET.find(symbol)

            if mode == 'encrypt':
                num += key  # shift the symbol index up using the offset

            elif mode == 'decrypt':
                num -= key  # shift the symbol index down using the offset

            # Wrap-around if num is larger than the length of the symbol alphabet or less than 0
            if num >= len(ALPHABET):
                num -= len(ALPHABET)
            elif num < 0:
                num += len(ALPHABET)

            # add encrypted/decrypted symbol to the end of translated string
            translated += ALPHABET[num]

        else:
            # character is not part of the symbol alphabet
            translated += symbol

    return translated


if __name__ == "__main__":
    main(sys.argv[1:])
