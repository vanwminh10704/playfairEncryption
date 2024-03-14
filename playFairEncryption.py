import tkinter as tk
import tkinter.ttk as ttk

app = tk.Tk()
app.title("Playfair Cipher")

# Function to convert the string to lowercase
def toLowerCase(plain):
    return plain.lower()

# Function to remove all spaces in a string
def removeSpaces(plain):
    return plain.replace(" ", "")

# Function to generate the 5x5 key square
def generateKeyTable(key):
    key = key.lower().replace(' ', '').replace('j', 'i')
    key_square = ''
    for letter in key + 'abcdefghiklmnopqrstuvwxyz':
        if letter not in key_square:
            key_square += letter
    return key_square

# Function to search for the characters of a digraph in the key square and return their position (for encryption)
def search_encrypt(key_square, a, b):
    if a == 'j':
        a = 'i'
    elif b == 'j':
        b = 'i'

    try:
        row_a, col_a = divmod(key_square.index(a), 5)
        row_b, col_b = divmod(key_square.index(b), 5)
    except ValueError:
        # Handle the case when a or b is not found in the key_square
        return ''

    if row_a == row_b:
        col_a = (col_a + 1) % 5
        col_b = (col_b + 1) % 5
    elif col_a == col_b:
        row_a = (row_a + 1) % 5
        row_b = (row_b + 1) % 5
    else:
        col_a, col_b = col_b, col_a

    return key_square[row_a * 5 + col_a] + key_square[row_b * 5 + col_b]

# Function to search for the characters of a digraph in the key square and return their position (for decryption)
def search_decrypt(key_square, a, b):
    if a == 'j':
        a = 'i'
    elif b == 'j':
        b = 'i'

    try:
        row_a, col_a = divmod(key_square.index(a), 5)
        row_b, col_b = divmod(key_square.index(b), 5)
    except ValueError:
        # Handle the case when a or b is not found in the key_square
        return ''

    if row_a == row_b:
        col_a = (col_a - 1) % 5
        col_b = (col_b - 1) % 5
    elif col_a == col_b:
        row_a = (row_a - 1) % 5
        row_b = (row_b - 1) % 5
    else:
        col_a, col_b = col_b, col_a

    return key_square[row_a * 5 + col_a] + key_square[row_b * 5 + col_b]

# Function to handle the encryption
def encrypt(plaintext, key_square):
    plaintext = removeSpaces(toLowerCase(plaintext))
    encrypted = ''
    i = 0
    while i < len(plaintext):
        if i == len(plaintext) - 1 or plaintext[i] == plaintext[i + 1]:
            encrypted += plaintext[i] + 'x'
        else:
            encrypted += plaintext[i] + plaintext[i + 1]
            i += 1
        i += 1
    result = ''
    for i in range(0, len(encrypted), 2):
        result += search_encrypt(key_square, encrypted[i], encrypted[i + 1])
    return result.upper()

# Function to handle the decryption
def decrypt(ciphertext, key_square):
    # Remove spaces from the ciphertext
    ciphertext = ciphertext.replace(" ", "")

    decrypted = ''
    i = 0
    while i < len(ciphertext):
        a = ciphertext[i].lower()
        if i + 1 < len(ciphertext):
            b = ciphertext[i + 1].lower()
        else:
            # If there's only one character left in the ciphertext, add 'x' to form a digraph
            b = 'x'

        if a == b:  # Case where there's a pair of identical characters
            b = 'x'
            i -= 1  # Move back 1 position to handle the next character pair
        decrypted += search_decrypt(key_square, a, b)
        i += 2

    # Check if the decrypted string has odd length, if so, add 'x' at the end
    if len(decrypted) % 2 != 0:
        decrypted += 'x'

    return decrypted.upper()

# Function to handle the encryption/decryption process
def process(selected_option):
    plaintext = message_entry.get("1.0", tk.END)
    key = key_entry.get("1.0", tk.END)
    key = key.strip()  # Remove leading/trailing whitespace
    key_square = generateKeyTable(key)

    # Clear the result text box before displaying new result
    result_text.delete("1.0", tk.END)

    if selected_option == "Encrypt":
        result = encrypt(plaintext, key_square)
    else:
        result = decrypt(plaintext, key_square)

    result_text.insert("1.0", result)

# GUI elements
message_label = ttk.Label(app, text="Enter Message:")
message_label.place(x=30, y=10)
message_entry = tk.Text(app, height=3, width=20)
message_entry.place(x=30, y=30)

key_label = ttk.Label(app, text="Enter Key:")
key_label.place(x=30, y=80)
key_entry = tk.Text(app, height=3, width=20)
key_entry.place(x=30, y=100)

encrypt_button = ttk.Button(app, text="Encrypt", command=lambda: process("Encrypt"))
encrypt_button.place(x=30, y=155)

decrypt_button = ttk.Button(app, text="Decrypt", command=lambda: process("Decrypt"))
decrypt_button.place(x=140, y=155)

result_label = ttk.Label(app, text="Result:")
result_label.place(x=30, y=200)
result_text = tk.Text(app, height=3, width=20)
result_text.place(x=30, y=220)

# Set window size and start event loop
app.geometry("350x350")
app.mainloop()
