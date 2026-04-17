# Question 1 - Part 1
# Member 1: Encryption functions

def encrypt_char(c, shift1, shift2):
    """Encrypt a single character using the assignment rules."""
    if c.islower():
        base = ord('a')
        if 'a' <= c <= 'm':
            shift = shift1 * shift2
        else:
            shift = -(shift1 + shift2)
        return chr((ord(c) - base + shift) % 26 + base)

    elif c.isupper():
        base = ord('A')
        if 'A' <= c <= 'M':
            shift = -shift1
        else:
            shift = shift2 ** 2
        return chr((ord(c) - base + shift) % 26 + base)

    else:
        return c


def encrypt_text(text, shift1, shift2):
    """Encrypt full text character by character."""
    return "".join(encrypt_char(c, shift1, shift2) for c in text)


def encrypt_file(shift1, shift2):
    """Read raw_text.txt, encrypt it, write to encrypted_text.txt."""
    try:
        with open("raw_text.txt", "r") as f:
            data = f.read()
    except FileNotFoundError:
        print("Error: raw_text.txt not found.")
        return False

    encrypted = encrypt_text(data, shift1, shift2)

    with open("encrypted_text.txt", "w") as f:
        f.write(encrypted)

    print("Encryption complete -> encrypted_text.txt")
    return True
