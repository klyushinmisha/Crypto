from random import Random
import time


class _Crypto:
    """This is core of bytes <—> chunk conversion"""
    def __init__(self, size, bias):
        self._size = size
        self._bias = bias % (size*8)

    def gen_chunks(self, b_seq):
        """Generates chunks from byte sequence and specified chunk size"""
        chunks = []
        b_len = len(b_seq)
        end_z = tuple(0 for i in range(b_len % self._size))
        nseq = tuple(b_seq) + end_z
        for i in range(0, len(nseq), self._size):
            chunk = nseq[i: i + self._size]
            res = 0
            for b in chunk:
                res <<= 8
                res |= b
            chunks.append(res)
        return chunks

    def gen_bytes(self, chunks):
        """Generate bytes from chunk"""
        b_seq = []
        for c in chunks:
            b_seq += self._bytes_from_chunk(c)
        return bytes(b_seq)

    def _bytes_from_chunk(self, chunk):
        """Helper for gen_bytes"""
        b_seq = []
        for i in range(self._size):
            value = (chunk >> ((self._size-1)*8 - i*8)) & (2**8 - 1)
            b_seq.append(value)
        return b_seq


class Encrypter(_Crypto):
    """Used to encrypt some bytes. Generates random gamma"""
    @property
    def gamma(self):
        return self._gamma

    def __init__(self, size, bias):
        super().__init__(size, bias)
        self._gamma = Random(time.time()).randint(0, 2 ** (size * 8) - 1)

    def encrypt(self, b_seq):
        chunks = self.gen_chunks(b_seq)
        n_chunks = tuple(map(self._encrypt_chunk, chunks))
        return self.gen_bytes(n_chunks)

    def _encrypt_chunk(self, c):
        n_chunk = self._gamma ^ c
        mask = 2**(self._size*8 - self._bias) - 1
        chunk_mask = (2**(self._size*8) - 1)
        hn = ((n_chunk & mask) << self._bias) & chunk_mask
        ln = ((n_chunk & (~mask)) >> (self._size*8 - self._bias)) & chunk_mask
        return hn | ln


class Decrypter(_Crypto):
    """Used to decrypt some bytes, using input gamma"""
    def __init__(self, size, bias, gamma):
        super().__init__(size, bias)
        self._gamma = gamma

    def decrypt(self, b_seq, gamma):
        chunks = self.gen_chunks(b_seq)
        n_chunks = tuple(map(self._decrypt_chunk, chunks))
        return self.gen_bytes(n_chunks)

    def _decrypt_chunk(self, c):
        mask = 2 ** self._bias - 1
        chunk_mask = (2 ** (self._size * 8) - 1)
        hn = ((c & mask) << (self._size*8 - self._bias)) & chunk_mask
        ln = ((c & (~mask)) >> self._bias) & chunk_mask
        return self._gamma ^ (hn | ln)
