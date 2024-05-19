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
    def __init__(self, data:List[Bit]):
        self.data = data
        self.m = len(data)
        self.r = 0
        while 2**self.r < self.m + self.r + 1:
            self.r += 1
        
    def encode(self):
        encoded = List[Bit](self.m + self.r)
        
        parity_indices = [2**i - 1 for i in range(self.r)]
        data_indexes = [i for i in range(self.m + self.r) if i not in parity_indices]
        
        for data_index in data_indexes:
            encoded[data_index] = self.data[data_index]
        
        for parity_index in parity_indices:
            parity_check_indices = [i for i in range(self.m + self.r) if i & (1 << parity_index)]
            
                
        
        