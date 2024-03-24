import tkinter as tk
from tkinter import messagebox

def cipher_table(key):
    playfair_table = [['' for _ in range(5)] for _ in range(5)]
    key_string = key + "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    for i in range(5):
        for j in range(5):
            playfair_table[i][j] = ""

    for k in range(len(key_string)):
        repeat = False
        used = False
        for i in range(5):
            for j in range(5):
                if playfair_table[i][j] == key_string[k]:
                    repeat = True
                elif playfair_table[i][j] == "" and not repeat and not used:
                    playfair_table[i][j] = key_string[k]
                    used = True

    return playfair_table

def parse_string(s):
    parse = s.upper().replace(" ", "")
    parse = parse.replace("J", "I")
    return parse

def find_position(playfair_table, letter):
    for i in range(5):
        for j in range(5):
            if playfair_table[i][j] == letter:
                return i, j

def encrypt_pair(playfair_table, a, b):
    r1, c1 = find_position(playfair_table, a)
    r2, c2 = find_position(playfair_table, b)

    if r1 == r2:
        c1 = (c1 + 1) % 5
        c2 = (c2 + 1) % 5
    elif c1 == c2:
        r1 = (r1 + 1) % 5
        r2 = (r2 + 1) % 5
    else:
        c1, c2 = c2, c1

    return playfair_table[r1][c1] + playfair_table[r2][c2]

def decrypt_pair(playfair_table, a, b):
    r1, c1 = find_position(playfair_table, a)
    r2, c2 = find_position(playfair_table, b)

    if r1 == r2:
        c1 = (c1 - 1) % 5
        c2 = (c2 - 1) % 5
    elif c1 == c2:
        r1 = (r1 - 1) % 5
        r2 = (r2 - 1) % 5
    else:
        c1, c2 = c2, c1

    return playfair_table[r1][c1] + playfair_table[r2][c2]

def cipher(plaintext, playfair_table):
    output = ""
    plaintext = plaintext.replace(" ", "").upper().replace("J", "I")

    if len(plaintext) % 2 != 0:
        plaintext += 'X'

    for i in range(0, len(plaintext), 2):
        a = plaintext[i]
        if i + 1 < len(plaintext):
            b = plaintext[i + 1]
        else:
            b = 'X'
        if a == b:
            b = 'X'
            i -= 1
        output += encrypt_pair(playfair_table, a, b)
    return output

def decipher(ciphertext, playfair_table):
    output = ""
    ciphertext = ciphertext.upper().replace(" ", "")
    
    for i in range(0, len(ciphertext), 2):
        a = ciphertext[i]
        if i + 1 < len(ciphertext):
            b = ciphertext[i + 1]
        else:
            b = 'X'
        if a == b:
            b = 'X'
            i -= 1
        output += decrypt_pair(playfair_table, a, b)
    return output
    

def display_table(playfair_table):
    table_str = "Playfair Table:\n"
    for row in playfair_table:
        table_str += " ".join(row) + "\n"
    return table_str

def encrypt():
    key = key_entry.get()
    plaintext = plaintext_entry.get()
    key = parse_string(key)
    plaintext = parse_string(plaintext)
    
    playfair_table = cipher_table(key)
    
    table_text.config(state="normal")
    table_text.delete(1.0, tk.END)
    table_text.insert(tk.END, display_table(playfair_table))
    table_text.config(state="disabled")
    
    ciphertext = cipher(plaintext, playfair_table)
    ciphertext_entry.delete(0, tk.END)
    ciphertext_entry.insert(0, ciphertext)

def decrypt():
    key = key_entry.get()
    ciphertext = ciphertext_entry.get()
    key = parse_string(key)
    ciphertext = parse_string(ciphertext)
    
    playfair_table = cipher_table(key)
    
    table_text.config(state="normal")
    table_text.delete(1.0, tk.END)
    table_text.insert(tk.END, display_table(playfair_table))
    table_text.config(state="disabled")
    
    decrypted_text = decipher(ciphertext, playfair_table)
    plaintext_entry.delete(0, tk.END)
    plaintext_entry.insert(0, decrypted_text)

root = tk.Tk()
root.title("Playfair Cipher")

key_label = tk.Label(root, text="Key:")
key_label.grid(row=0, column=0, padx=10, pady=10)

key_entry = tk.Entry(root, width=30)
key_entry.grid(row=0, column=1, padx=10, pady=10)

plaintext_label = tk.Label(root, text="Plaintext:")
plaintext_label.grid(row=1, column=0, padx=10, pady=10)

plaintext_entry = tk.Entry(root, width=30)
plaintext_entry.grid(row=1, column=1, padx=10, pady=10)

ciphertext_label = tk.Label(root, text="Ciphertext:")
ciphertext_label.grid(row=2, column=0, padx=10, pady=10)

ciphertext_entry = tk.Entry(root, width=30)
ciphertext_entry.grid(row=2, column=1, padx=10, pady=10)

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt)
encrypt_button.grid(row=3, column=0, padx=10, pady=10)

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt)
decrypt_button.grid(row=3, column=1, padx=10, pady=10)
    
table_text = tk.Text(root, height=8, width=30)
table_text.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
table_text.config(state="disabled")
root.mainloop()
