# Graph-Theoretic Cryptographic Transform

A cryptographic algorithm based on graph theory, tree structures, and traversal-dependent encoding.

## Foundation

### Definition
Let *P* = password string, *K* = (*p*, *b*, *s*) where *p*, *b* ∈ ℙ (primes), *p* > *b*, *s* ∈ ℤ (seed).

### Algorithm Steps

**1. Input Mapping**
- *D* = UTF-8(*P*) → {0,1,...,255}ⁿ where *n* = |*D*|
- If *n* < 4: *D* ← *D* || 0^(4-n) (padding to minimum length)

**2. Initialization Vector**
- *IV* ← PRNG(*s*) generates 6 random bytes
- *h* = djb2_hash(*IV*)

**3. Graph Construction G = (V, E)**
- *V* = {0, 1, ..., *n*-1} (vertex set)
- Ring edges: *E*₁ = {(*i*, (*i*+1) mod *n*) : *i* ∈ *V*} (ensures connectivity)
- Random edges: *E*₂ = {(*i*, *j*) : *i* < *j*, PRNG(*s* ⊕ *h*) < 0.7} (Erdős-Rényi model)
- *E* = *E*₁ ∪ *E*₂

**4. Starting Vertex Selection**
- *m* ← PRNG(*s* ⊕ *h*) mod *n*
- *v₀* = ((2^(*p*-1) · *m* + *h*) - *b*) mod *n*

**5. BFS Tree Construction**
- *T* = BFS(*G*, *v₀*) → spanning tree of *G*
- parent: *V* → *V* ∪ {⊥}, where parent(*v₀*) = ⊥
- children(*v*) = {*u* ∈ *V* : parent(*u*) = *v*}

**6. Node Encoding Function**
For each vertex *v* ∈ *V*:
- *N*(*v*) = children(*v*) ∪ {parent(*v*)} \ {⊥} (neighborhood in spanning tree)
- *κ*(*v*) = djb2_hash([*v*] || *IV* || *N*(*v*)[0:3]) ∧ 0xFF (key derivation)
- *E*(*v*) = *D*[*v*] ⊕ *κ*(*v*) (XOR encoding)
- Character mapping: 
  - If *E*(*v*) ≥ 32: chr(*E*(*v*))
  - Else: chr(*E*(*v*) + 256) (extended ASCII range)

**7. Output Generation**
- *σ* = postorder traversal of *T* starting from *v₀*
- *C* = *IV* || [char(*E*(*σ*(1))), char(*E*(*σ*(2))), ..., char(*E*(*σ*(*n*)))]

### Decryption Transform

**Inverse Mapping**: *D̂* = *E*⁻¹(*C*) where:
1. Parse *IV* (first 6 bytes) and encrypted sequence from *C*
2. Reconstruct identical graph *G* and tree *T* using same parameters (*p*, *b*, *s*, *IV*)
3. For each *v* in postorder sequence:
   - Reverse character mapping: 
     - If ord(char) ≥ 256: *encoded* = ord(char) - 256
     - Else: *encoded* = ord(char)
   - *D̂*[*v*] = *encoded* ⊕ *κ*(*v*)
4. Remove padding: trim trailing zeros

## Implementation Details

### Key Components
- **Graph Builder**: Creates Erdős-Rényi random graph with ring connectivity
- **Tree Traversal**: BFS for spanning tree, postorder for encoding sequence
- **Hash Function**: DJB2 for deterministic key derivation
- **Encoder**: XOR-based with extended ASCII mapping

### Security Features
- **Semantic Security**: Different *IV* for each encryption ensures different ciphertexts
- **Key-Dependent Structure**: Graph topology varies with (*p*, *b*, *s*)
- **Context-Dependent Encoding**: Each byte's encoding depends on its tree position and neighbors
- **Non-Linear Transform**: Graph structure introduces non-linearity

## Complexity Analysis

- **Space Complexity**: *O*(*n*²) for adjacency list representation
- **Time Complexity**: 
  - Graph construction: *O*(*n*²)
  - BFS traversal: *O*(*n* + *|E|*) = *O*(*n*²)
  - Encoding/Decoding: *O*(*n*)
  - **Total**: *O*(*n*²)
- **Key Size**: 2 primes + 1 seed integer


### Example Input/Output

```
Original:  My name is Zak, and I am a computer scientist
Encrypted: "ú#}WÈY\x82íąC'\x81\x8aÑč&¿Ö³=W¸øēNt\x84°\x83÷/B\x92)ā.t×\x991kć<»¹\x90uß2øÝ"
Decrypted: My name is Zak, and I am a computer scientist
Match: True
```

## Theoretical Basis
- **Graph Theory**: Erdős-Rényi random graphs for structural diversity
- **Tree Algorithms**: BFS spanning trees and postorder traversal
- **Cryptographic Primitives**: XOR operations, hash functions, PRNGs
- **Information Theory**: Context-dependent encoding based on graph topology

## Security Considerations

**Strengths:**
- Novel approach resistant to traditional cryptanalysis
- Key-dependent graph structure provides confusion
- Context-sensitive encoding provides diffusion
- Semantic security through randomized IV

## License

MIT License - see LICENSE file for details.

## Contributing

This is an experimental cryptographic algorithm.Do not use for production security applications. Contributions, security analysis, and peer review are welcome.

