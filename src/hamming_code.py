from typing import Any, List


class Bit:
    def __init__(self, value=0):
        if value not in (0, 1):
            raise ValueError('Bit value must be 0 or 1')
        self.value = value
        
    def __str__(self):
        return str(self.value)
    
    def set(self, value):
        if value not in (0, 1):
            raise ValueError('Bit value must be 0 or 1')
        self.value = value
    
    def toggle(self):
        self.value = 1 - self.value
        
    def get(self):
        return self.value

    def __and__(self, other):
        if isinstance(other, Bit):
            return Bit(self.value & other.value)
        return NotImplemented

    def __or__(self, other):
        if isinstance(other, Bit):
            return Bit(self.value | other.value)
        return NotImplemented

    def __xor__(self, other):
        if isinstance(other, Bit):
            return Bit(self.value ^ other.value)
        return NotImplemented
    

class HammingCode:
    
    @staticmethod
    def encode(data:List[Bit]):
        m = len(data)
        r = HammingCode.find_parity_length(m)
        
        encoded = List[Bit](m +r)
        
        # find parity bits locations
        parity_indices = [2**i - 1 for i in range(self.r)]
        # fill data bits in encoded array
        for i in range(len(encoded)):
            if i in parity_indices:
                continue
            encoded[i] = data[i]

        for i in range(r):
            parity = HammingCode.check_parity(encoded, i)
            encoded[2**i - 1] = parity

        return encoded
    
    
    @staticmethod
    def find_parity_length(m:int):
        r = 0
        while 2**r < m + r + 1:
            r += 1
        return r
    
    @staticmethod      
    def check_parity(received:List[Bit], parity_index:int):
        parity = Bit(0)
        for i in range(len(received)):
            if i & (1 << parity_index):
                parity = parity ^ received[i]
        return parity
    
    @staticmethod
    def check_error(received:List[Bit]):
        r = HammingCode.find_parity_length(len(received))
        error_index = 0
        for i in range(r):
            parity = HammingCode.check_parity(received, i)
            if parity.value:
                error_index += 2**i
        return error_index
    
    @staticmethod
    def decode(received:List[Bit]):
        r = HammingCode.find_parity_length(len(received))
        error_index = HammingCode.check_error(received)
        if error_index:
            return error_index
        decoded = List[Bit](len(received) - r)
        j = 0
        for i in range(len(received)):
            if i  == 2**j - 1:
                j += 1
                continue
            decoded.append(received[i])
        return decoded