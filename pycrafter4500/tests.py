from pycrafter4500 import conv_len, bits_to_bytes

flagstring = 0x40  # 0b01000000 / mode
sequence_byte = 0x00  # -> 0
data = [0x01]
cmd2 = 0x1A
cmd3 = 0x07

data_len = conv_len(len(data) + 2, 16)
data_len = bits_to_bytes(data_len)
