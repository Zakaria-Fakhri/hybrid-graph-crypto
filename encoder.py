from Func import djb2_hash

def encode_byte(byte_val, node_id, neighbors, key_data):
    key_input = bytes([node_id]) + key_data + bytes(neighbors[:3])
    key = djb2_hash(key_input) & 0xFF
    # Simple XOR without modulo - use the full range
    encoded = byte_val ^ key
    # Map to extended ASCII range to avoid issues with control characters
    return chr(encoded if encoded >= 32 else encoded + 256)

def decode_byte(char_val, node_id, neighbors, key_data):
    key_input = bytes([node_id]) + key_data + bytes(neighbors[:3])
    key = djb2_hash(key_input) & 0xFF
    # Reverse the mapping
    encoded = ord(char_val)
    if encoded >= 256:
        encoded -= 256
    # Simple XOR to get back the original
    return encoded ^ key

def pad_data(data, min_len):
    if len(data) < min_len:
        data += b'\x00' * (min_len - len(data))
    return data

def unpad_data(data):
    while data and data[-1] == 0:
        data.pop()
    return data
