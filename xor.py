def bxor(b1, b2):
    l1 = len(b1)
    l2 = len(b2)
    result = bytearray(b1)
    for i, b in enumerate(b2[:min(l1, l2)]):
        result[i] ^= b
    return bytes(result)
