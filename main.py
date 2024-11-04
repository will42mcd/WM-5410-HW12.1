# Code taken from: https://rosettacode.org/wiki/LZW_compression#Python
# Author: unlisted
# License: Public domain
# Acessed on: 11/2/2024
# CHANGELOG
#   - Added driver code
#   - Added main function
#   - Modified decompress to decode pickle files and renamed to decode_pickle()
#   - Added saved_pickle()

import pickle
from io import StringIO


def compress(uncompressed):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dict_size = 256
    dictionary = dict((chr(i), i) for i in range(dict_size))
    # in Python 3: dictionary = {chr(i): i for i in range(dict_size)}

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result


def saved_pickle(data):
    with open("pickled_alice_oz.txt", 'wb') as file:
        pickle.dump(data, file)


def decode_pickle(fname):
    text = open (fname, "rb")
    compressed = pickle.load(text)
    # Build the dictionary.
    dict_size = 256
    dictionary = dict((i, chr(i)) for i in range(dict_size))
    # in Python 3: dictionary = {i: chr(i) for i in range(dict_size)}

    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry
    count = 0
    string = ""
    for i in result.getvalue():
        string = string + i
        count += 1
        if count == 45:
            break
    return string


def main():
    with open("alice_oz.txt", encoding='utf8') as f:
        text = f.read()
    compressed = compress(text)
    
    saved_pickle(compressed)
    
    print(decode_pickle("pickled_alice_oz.txt"))


if __name__ == "__main__":
    main()
    
    
    