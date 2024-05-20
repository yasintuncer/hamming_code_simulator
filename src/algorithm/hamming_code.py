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
        r = 0
        while 2**r < m + r + 1:
            r += 1
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
    def check_parity(received: List[Bit], parity_index: int):
        start_points = []
        for i in range( 2**parity_index - 1, len(received),  2**(parity_index+1)):
            start_points.append(i)

        all_points = []
        for start in start_points:
            for i in range(2**(parity_index)):
                if start + i < len(received):
                    all_points.append(start + i)
        parity = received[all_points[1]]
        for point in all_points[2:]:
            parity = parity ^ received[point]
        return parity

    
    @staticmethod
    def decode(received: List[Bit]):
        m_plus_r = len(received)
        r = 0
        while 2**r < m_plus_r + 1:
            r += 1
        c = []
        for i in range(r):
            parity = HammingCode.check_parity(received, i)
            c.append(received[2**i - 1] ^ parity)	
        err_check = sum([2**i * c[i].value for i in range(r)])
        if err_check != 0:
            return err_check -1
        data = []
        for i in range(len(received)):
            if i not in [2**i - 1 for i in range(r)]:
                data.append(received[i])
        return data

            
    
if __name__ == '__main__':
    data = [Bit(1), Bit(1), Bit(0), Bit(0), Bit(0), Bit(1), Bit(0), Bit(0)]
    print('Data:', data)
    encoded = HammingCode.encode(data)
    print('Encoded:', encoded)
    encoded[0].toggle()
    #print("Error set at index 3" , encoded)
    decoded = HammingCode.decode(encoded)
    print('Decoded:', decoded)