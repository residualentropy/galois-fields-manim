import numpy as np
from tqdm import trange
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from shape import SHAPE

def encrypt_aes_ecb(arr: np.array):
    key = b"sometextSOMETEXTsometext"
    flat = arr.reshape((arr.size,))
    flat_out = np.empty((arr.size,), dtype= np.uint8)
    for i in trange(arr.size // 128):
        pos = i * 128
        enc = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
        in_block = flat[pos:pos+128]
        in_bytes = in_block.tobytes()
        in_bytes += b"\x00" * (128 - len(in_bytes))
        ct = enc.update(in_bytes) + enc.finalize()
        out_block = np.frombuffer(ct, dtype= np.uint8)
        flat_out[pos:pos+128] = out_block[:( min(pos+128, arr.size) - pos )]
    return flat_out.reshape(SHAPE)

def encrypt_aes_gcm(arr: np.array):
    key = b"sometextSOMETEXTsometext"
    iv = b"yooooooo"
    flat = arr.reshape((arr.size,))
    flat_out = np.empty((arr.size,), dtype= np.uint8)
    enc = Cipher(algorithms.AES(key), modes.GCM(iv)).encryptor()
    for i in trange(arr.size // 128):
        pos = i * 128
        in_block = flat[pos:pos+128]
        in_bytes = in_block.tobytes()
        in_bytes += b"\x00" * (128 - len(in_bytes))
        ct = enc.update(in_bytes)
        out_block = np.frombuffer(ct, dtype= np.uint8)
        flat_out[pos:pos+128] = out_block[:( min(pos+128, arr.size) - pos )]
    return flat_out.reshape(SHAPE)
