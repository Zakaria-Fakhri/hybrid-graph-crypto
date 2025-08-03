from crypto import encrypt, decrypt

def test_crypto():
    pwd = "My name is Zak, and I am a computer scientist"
    key_p=7
    key_b=3
    seed=54321
    
    encrypted = encrypt(pwd, key_p, key_b, seed)
    decrypted = decrypt(encrypted, key_p, key_b, seed)
    
    print(f"Original:  {pwd}")
    print(f"Encrypted: {encrypted!r}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {pwd == decrypted}")

if __name__ == "__main__":
    
    test_crypto()
