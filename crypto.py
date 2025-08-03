import random
from Func import is_prime, djb2_hash
from build_G import build_graph
from traversing import bfs, build_tree, postorder
from encoder import encode_byte, decode_byte, pad_data, unpad_data

def generate_iv(seed, length=6):
    random.seed(seed)
    result = []
    for _ in range(length):
        result.append(random.randint(0, 255))
    return bytes(result)


def calc_start_node(p, b, seed, iv, data_len):
    h = djb2_hash(iv)
    random.seed(seed ^ h)
    m = random.randint(0, data_len - 1)
    return ((2**(p-1) * m + h) - b) % data_len

def encrypt(password, p, b, seed):
    if not (is_prime(p) and is_prime(b) and p > b):
        raise ValueError("Invalid key parameters")
    
    data = password.encode('utf-8')
    data = pad_data(data, 4)
    n = len(data)
    
    iv = generate_iv(seed)
    start = calc_start_node(p, b, seed, iv, n)
    
    # build graph and tree
    graph = build_graph(n, 0.7, seed ^ djb2_hash(iv))
    parent = bfs(graph, start)
    children = build_tree(parent)
    
    # encode nodes
    encoded = {}
    for i in range(n):
        nbrs = children[i][:]
        if parent[i] != -1:
            nbrs.append(parent[i])
        encoded[i] = encode_byte(data[i], i, nbrs, iv)
    
    # build result
    order = postorder(children, start)
    result = ''
    for b in iv:
        result += chr(b)
    for node in order:
        result += encoded[node]

    return result

def decrypt(ciphertext, p, b, seed):
    if len(ciphertext) < 7:
        raise ValueError("Invalid ciphertext")
    
    iv_list = []
    for c in ciphertext[:6]:
        iv_list.append(ord(c))
    iv = bytes(iv_list)

    encrypted = ciphertext[6:]
    n = len(encrypted)
    
    start = calc_start_node(p, b, seed, iv, n)
    
    # rebuild same structures
    graph = build_graph(n, 0.7, seed ^ djb2_hash(iv))
    parent = bfs(graph, start)
    children = build_tree(parent)
    order = postorder(children, start)
    
    # decode
    decoded = [0] * n
    for i, node in enumerate(order):
        nbrs = children[node][:]
        if parent[node] != -1:
            nbrs.append(parent[node])
        decoded[node] = decode_byte(encrypted[i], node, nbrs, iv)
    
    decoded = unpad_data(decoded)
    return bytes(decoded).decode('utf-8', errors='ignore')
