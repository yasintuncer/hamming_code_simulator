from typing import Any, List


class Bit:
    def __init__(self, value=0):
        if value not in (0, 1):
            raise ValueError('Bit value must be 0 or 1')
        self.value = value
        
    def __str__(self):
        return str(self.value)
    def __repr__(self):
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
    def encode(data: List[Bit]):
        m = len(data)
        r = HammingCode.find_parity_length(m)
        
        encoded = [Bit(0) for _ in range(m + r)]
        
        # Find parity bits locations
        parity_indices = [2**i - 1 for i in range(r)]
        # Fill data bits in encoded array
        j = 0
        for i in range(len(encoded)):
            if i in parity_indices:
                continue
            encoded[i] = data[j]
            j += 1

        for i in range(r):
            parity = HammingCode.check_parity(encoded, i)
            encoded[2**i - 1] = parity

        return encoded
    
    
    @staticmethod
    def find_parity_length(m: int):
        r = 0
        while 2**r < m + r + 1:
            r += 1
        return r
    
    @staticmethod      
    def check_parity(received: List[Bit], parity_index: int):
        values_of_parity_index = []
        i = 0
        parity_block_size = parity_index + 1
        while(i<= len(received)):
            if i < 2**parity_index - 1:
                i += 1
                continue
            for j in range(parity_block_size):
                if i + j > len(received):
                    break
                values_of_parity_index.append(i + j)
            i += 2 * parity_block_size
        print('Values of parity index:', values_of_parity_index)
            
    
    @staticmethod
    def check_error(received: List[Bit]):
        r = HammingCode.find_parity_length(len(received))
        error_index = 0
        for i in range(r):
            
            parity = HammingCode.check_parity(received, i)
            if parity.value != 0:
                error_index += 2**i
        return error_index
    
    @staticmethod
    def decode(received: List[Bit]):
        r = HammingCode.find_parity_length(len(received))
        error_index = HammingCode.check_error(received)
        if error_index:
            return error_index
        decoded = []
        j = 0
        for i in range(len(received)):
            if i == 2**j - 1:
                j += 1
                continue
            decoded.append(received[i])
        return decoded
    
    
if __name__ == '__main__':
    data = [Bit(1), Bit(1), Bit(0), Bit(0), Bit(0), Bit(1), Bit(1), Bit(0)]
    
    encoded = HammingCode.encode(data)
    print('Encoded:', encoded)
