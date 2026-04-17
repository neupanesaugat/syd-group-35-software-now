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

def decrypt_char(c, shift1, shift2):
    """Decrypt a single character by reversing the encryption shifts."""
    if c.islower():
        base = ord('a')
        cand_am = chr((ord(c) - base - (shift1 * shift2)) % 26 + base)
        cand_nz = chr((ord(c) - base + (shift1 + shift2)) % 26 + base)
        return cand_am if 'a' <= cand_am <= 'm' else cand_nz
 
    elif c.isupper():
        base = ord('A')
        cand_am = chr((ord(c) - base + shift1) % 26 + base)
        cand_nz = chr((ord(c) - base - (shift2 ** 2)) % 26 + base)
        return cand_am if 'A' <= cand_am <= 'M' else cand_nz
 
    else:
        return c
 
 
def decrypt_text(text, shift1, shift2):
    """Decrypt full text character by character."""
    return "".join(decrypt_char(c, shift1, shift2) for c in text)
 
 
def decrypt_file(shift1, shift2):
    """Read encrypted_text.txt, decrypt it, write to decrypted_text.txt."""
    try:
        with open("encrypted_text.txt", "r") as f:
            data = f.read()
    except FileNotFoundError:
        print("Error: encrypted_text.txt not found.")
        return False
 
    decrypted = decrypt_text(data, shift1, shift2)
 
    with open("decrypted_text.txt", "w") as f:
        f.write(decrypted)
 
    print("Decryption complete -> decrypted_text.txt")
    return True
 
 
def verify():
    """Compare raw_text.txt with decrypted_text.txt and report result."""
    try:
        with open("raw_text.txt", "r") as f:
            original = f.read()
        with open("decrypted_text.txt", "r") as f:
            decrypted = f.read()
    except FileNotFoundError as e:
        print(f"Error during verification: {e}")
        return
 
    if original == decrypted:
        print("Verification successful: decrypted text matches original.")
    else:
        print("Verification failed: decrypted text does not match original.")
        for i, (a, b) in enumerate(zip(original, decrypted)):
            if a != b:
                print(f"  First difference at position {i}: "
                      f"original='{a}' decrypted='{b}'")
                break
 
 
def main():
    try:
        shift1 = int(input("Enter shift1: "))
        shift2 = int(input("Enter shift2: "))
    except ValueError:
        print("Error: shift1 and shift2 must be integers.")
        return
 
    if encrypt_file(shift1, shift2):
        if decrypt_file(shift1, shift2):
            verify()
 
 
if __name__ == "__main__":
    main()
