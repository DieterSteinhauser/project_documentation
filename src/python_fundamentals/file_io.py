# ---------------------------------------------------------
#                          NOTES
# ---------------------------------------------------------

# ---------------------------------------------------------
#                         INCLUDES
# ---------------------------------------------------------

import os

# ---------------------------------------------------------
#                         SETUP
# ---------------------------------------------------------

poem = """Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth;

Then took the other, as just as fair,
And having perhaps the better claim,
Because it was grassy and wanted wear;
Though as for that the passing there
Had worn them really about the same,

And both that morning equally lay
In leaves no step had trodden black.
Oh, I kept the first for another day!
Yet knowing how way leads on to way,
I doubted if I should ever come back.

I shall be telling this with a sigh
Somewhere ages and ages hence:
Two roads diverged in a wood, and I—
I took the one less traveled by,
And that has made all the difference."""

local_dir = os.path.abspath(os.path.dirname(__file__))
bin_file = os.path.join(local_dir, 'binary_file.txt')
readable_file = os.path.join(local_dir, 'readable_file.txt')


# encode data for the binary file
hex_list = []
for letter in poem:
    hex_list.append(hex(ord(letter)))

# write to the binary file
with open(bin_file, 'w') as f:
    for value in hex_list:
        f.write(value)


# ---------------------------------------------------------
#                         ASSIGNMENT
# ---------------------------------------------------------

local_dir = os.path.abspath(os.path.dirname(__file__))  # path to local directory
bin_file = os.path.join(local_dir, 'binary_file.txt')   # binary file in local directory
readable_file = os.path.join(local_dir, 'readable_file.txt')  # path to local directory

# Method 1: More lines but easier to understand for beginners.

# read the binary file
with open(bin_file, 'r') as f:
    read_data = f.read()

# parse byte data as letters
hex_values = read_data.split('0x')  # separate every value by their hex delimiter.
hex_values.remove('')  # remove the weird empty element at the beginning of the list.

# decode each letter in the list
final_string = ''
for value in hex_values:

    # This will cast the string hex number to an integer, reading the value in base 16 (hex)
    temp = int(value, 16)

    # interpret the hex value as an ascii/UTF-8 letter
    letter = chr(temp)

    # add/append the letter to the complete string.
    final_string = final_string + letter

# write to the binary file
with open(readable_file, 'w', encoding='UTF-8') as f:
    f.writelines(final_string)

# ---------------------------------------------------------

# Method 2: Less lines but more pythonic and efficient.

# read the binary file
with open(bin_file, 'r') as f:
    read_data = f.read()

# parse byte data as letters
hex_values = read_data.split('0x')
decoded_letters = [chr(int(val, 16)) for val in hex_values[1:]]

# compose a stirng
final_string = ''.join(decoded_letters)
print(final_string)

# write to the binary file
with open(readable_file, 'w', encoding='UTF-8') as f:
    f.writelines(final_string)

# ---------------------------------------------------------
