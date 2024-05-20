import os 

##add upper directory to sys.path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from uix import T
from uix.elements import button, row, page, header, text, input, col,div
from uix_components import basic_table
from algorithm.hamming_code import Bit, HammingCode  # Assuming these are in a module named algorithm
import uix
from .digit_area import DigitArea

from uix_components import basic_alert
import random    
def decode_data(encoded_input):
    encoded = [Bit(int(bit)) for bit in encoded_input]
    decoded = HammingCode.decode(encoded)
    if isinstance(decoded, int):
        return f"Error at position {decoded}"
    return [bit.get() for bit in decoded]  # Return list of bit values

def is_data_binary(data:str):
    return all(bit in ['0', '1'] for bit in data)
def filter_binary_data(data: str) -> str:
    return ''.join([bit for bit in data if bit in ['0', '1']])


def find_parity_indices(data_length):
    parity_indices = []
    r = 0
    while 2**r < data_length + r + 1:
        parity_indices.append(2**r - 1)
        r += 1
    return parity_indices

def create_tags(data_length):
    parity_indices = find_parity_indices(data_length)
    parity_count = len(parity_indices)
    table_data = [None] * (data_length + parity_count)
    
    # Insert parity bits
    for parity_index in parity_indices:
        table_data[parity_index] = "P"+ str(parity_index)
    
    # Insert data bits
    data_index = 0
    for i in range(len(table_data)):
        if table_data[i] is None:
            table_data[i] = "D" + str(data_index)
            data_index += 1
    
    return table_data


class HammingCodeUI(uix.Element):

    def __init__(self, id=None):
        self.input_table_header = []
        self.input_table_data = []
        self.input_table_visibility = "hidden"

        self.encoded_table_header = []
        self.encoded_table_data = []
        self.encoded_table_visibility = "hidden"
        
        self.decoded_table_header = []
        self.decoded_table_data = []
        self.decoded_table_visibility = "hidden"
        self.parity_count = -1
        self.data_length = -1
        self.toggle_index = -1
        self.alert_message = ""
        self.information_div = None
        super().__init__(id=id)
        with page("").style("background-color: #1e1e1e; color: #ffffff; font-family: Arial, sans-serif;"):
            with div().style("padding: 10px; box-sizing: border-box; background-color: #333333; color: #ffffff; border-bottom: 1px solid #444444;") as alert:
                self.alert = alert

            with header("").style("padding: 10px; box-sizing: border-box; background-color: #333333; color: #ffffff; border-bottom: 1px solid #444444;"):
                text("Hamming Code Simulator").style("font-size: 24px; font-weight: bold; margin: 0; padding: 0;")
            
            with col().cls("ui-content").style("gap: 20px; padding: 20px;"):
                with row().cls("ui-nav border").style("align-items: center;"):
                    with row().style("flex: 1;").style("gap: 20px;"):
                        text("Input Data").style("font-size: 18px; font-weight: bold;")
                        self.input_field = input("data_input", type="number").style("width: 25%; ")
                        self.input_field.set_value("")
                        self.input_field.set_attr("pattern", "[01]+")
                        self.input_field.on("input", self.set_value)
                    with row().style("flex: 1;").style("gap: 20px;"):
                        with div() as x:
                            self.information_div = x
                            text("Information").style("font-size: 18px; font-weight: bold;")
                            
                    with row().style("flex: 1;").style("gap: 20px;"):
                        self.random_toggle = button("Random Toggle").style("width:%25; padding: 10px 20px; font-size: 16px; background-color: #007bff; color: #ffffff; border: none; border-radius: 4px; cursor: pointer; width: auto;")
                        self.random_toggle.on("click", self.info_change)
                        self.text = text("").style("font-size: 18px; margin-top: 10px;")
                        self.random_toggle_output = text("").style("font-size: 18px; margin-top: 10px;")
                        
            with col().cls("ui-content").style("gap: 20px; padding: 20px;"):
                text("Outputs").style("font-size: 18px; font-weight: bold;")
                            
                with row().style("flex: 1;").style("gap: 20px;"):
                    with div(id = "input_table_div").style("display: flex; gap: 20px; align-items: center;") as x:
                        with text("Input Data").style("font-size: 5px;").style("visibility: hidden;") as t:
                            self.input_text = t
                        self.input_table_div = x
                        self.create_input_table()

                with row().style("flex: 1;").style("gap: 20px;"):
                    with div(id = "encoded_table_div").style("display: flex; gap: 20px; align-items: center;") as x:
                        with text("Encoded Data").style("font-size: 5px;").style("visibility: hidden;") as t:
                            self.encoded_text = t
                        self.encoded_table_div = x
                        self.create_encoded_table()
                with row().style("flex: 1;").style("gap: 20px;"):
                    with div(id = "decoded_table_div").style("display: flex; gap: 20px; align-items: center;") as x:
                        with text("Decoded Data").style("font-size: 5px;").style("visibility: hidden;") as t:
                            self.decoded_text = t
                        self.decoded_table_div = x
                        self.create_decoded_table()
                    
            with col().cls("ui-content").style("gap: 20px; padding: 20px;"):
                with row().style("flex: 1;").style("gap: 20px;"):
                    self.encode_button = button("Encode Data").style("width:%25; margin-top: 10px; padding: 10px 20px; font-size: 16px; background-color: #28a745; color: #ffffff; border: none; border-radius: 4px; cursor: pointer; width: auto;")
                    self.encode_button.on("click", self.encode_data)
                    self.encode_output = text("").style("font-size: 18px; margin-top: 10px;")
                    self.decode_button = button("Decode Data").style("width:%25;margin-top: 10px; padding: 10px 20px; font-size: 16px; background-color: #007bff; color: #ffffff; border: none; border-radius: 4px; cursor: pointer; width: auto;")
                    self.decode_button.on("click", self.decode_data)
                    self.decode_output = text("").style("font-size: 18px; margin-top: 10px;")
                    self.reset_button = button("Reset").style("width:%25;margin-top: 10px; padding: 10px 20px; font-size: 16px; background-color: #007bff; color: #ffffff; border: none; border-radius: 4px; cursor: pointer; width: auto;")
                    self.reset_button.on("click", self.clear)
                    self.reset_button = text("").style("font-size: 18px; margin-top: 10px;")

    def create_information(self):
        print("Random Toggle goes here")
        with div() as x:
            if self.parity_count> -1:
                text("Parity Count: "+str(self.parity_count)).style("font-size: 18px; font-weight: bold;").style("visibility: visible;")
            if self.data_length > -1:
                text("Data Length: "+str(self.data_length)).style("font-size: 18px; font-weight: bold;").style("visibility: visible;")
            if self.toggle_index > -1:
                text("Random Toggle Index").style("font-size: 18px; font-weight: bold;").style("visibility: visible;")
        return x

    def set_random_toggle(self):
        if self.data_length > -1:
            self.toggle_index = random.randint(0, self.data_length-1)
            
    def create_input_table(self):
        with div() as x:
            text("Input Data").style("font-size: 5px;").style("visibility: "+self.input_table_visibility+";")
            basic_table(headers=self.input_table_header, data=[self.input_table_data]).style("visibility: "+self.input_table_visibility+";")
        return x

    def create_encoded_table(self):
        with div() as x:
            text("Encoded Data").style("font-size: 5px;").style("visibility: "+self.encoded_table_visibility+";")
            basic_table(headers=self.encoded_table_header, data=[self.encoded_table_data]).style("visibility: "+self.encoded_table_visibility+";")
        return x
    def create_decoded_table(self):
        with div() as x:
            text("Decoded Data").style("font-size: 5px;").style("visibility: "+self.decoded_table_visibility+";")
            basic_table(headers=self.decoded_table_header, data=[self.decoded_table_data]).style("visibility: "+self.decoded_table_visibility+";")
        return x

    def create_alert(self):
        with div() as x:
            alert = basic_alert("", id ="comp_alert").style("display: block;")
            alert.set_value(self.alert_message)
            if self.alert_message == "":
                alert.style("display: none;")
        return alert


    def set_value(self, ctx, id, value):
        
        filtered_value = filter_binary_data(value)
        self.input_field.set_value(filtered_value)
        self.input_table_header = []
        self.input_table_data = []
        self.input_table_visibility = "hidden"
        self.input_table_div.update(self.create_input_table)
        for i in range(len(filtered_value)):
            self.input_table_header.append("D"+str(i))
            self.input_table_data.append(filtered_value[i])
        self.input_text.style("visibility: visible;")
        self.input_table_visibility = "visible"
        self.parity_count = len(find_parity_indices(len(filtered_value)))
        self.data_length = len(filtered_value)
        print(self.parity_count)
        print(self.data_length)
       
        self.input_table_div.update(self.create_input_table)
        self.information_div.update(self.create_information)
 
    def info_change(self, ctx, id, value):
        print("Random Toggle")
        self.information_div.update(self.create_information)


    def clear(self, ctx, id, value):
        self.input_table_header = []
        self.input_table_data = []
        self.input_table_visibility = "hidden"
        self.input_table_div.update(self.create_input_table)
        self.encoded_table_header = []
        self.encoded_table_data = []
        self.encoded_table_visibility = "hidden"
        self.encoded_table_div.update(self.create_encoded_table)
        self.decoded_table_header = []
        self.decoded_table_data = []
        self.decoded_table_visibility = "hidden"
        self.decoded_table_div.update(self.create_decoded_table)
        self.alert_message = "ahaatae"
        self.alert.update(self.create_alert)
        self.input_field.set_value("")
        

    def encode_data(self, ctx, id, value):
        print(self.input_field.value)
        bits = [Bit(int(bit)) for bit in self.input_field.value]
        encoded = HammingCode.encode(bits)
        encoded_list = [str(bit.value) for bit in encoded]
        created_tags = create_tags(len(bits))

        self.encoded_table_header = created_tags
        self.encoded_table_data = encoded_list
        self.encoded_table_visibility = "visible"
        self.encoded_table_div.update(self.create_encoded_table)


    def decode_data(self, ctx, id, value):
        if self.encoded_table_data:
            decoded = decode_data(self.encoded_table_data)
            decoced_list = [str(bit) for bit in decoded]
            if isinstance(decoded, int):
                self.alert_message = f"Error at position {decoded}"
                self.alert.update(self.create_alert)
            decoded_tags = []
            for i in range(len(decoded)):
                decoded_tags.append("D"+str(i))
            self.decoded_table_header = decoded_tags
            self.decoded_table_data = decoced_list
            self.decoded_table_visibility = "visible"
            self.decoded_table_div.update(self.create_decoded_table)
    
    

