# >> 和 & 的使用
# reg >> 8：把 reg 右移 8 位，相当于丢掉低 8 位，只留下高 8 位在最低位的位置上。
reg = 0x4142  # 高字节 0x41('A'=65), 低字节 0x42('B'=66)
high_byte = (reg >> 8) & 0xFF  # 0x41 -> 65
low_byte  = reg & 0xFF         # 0x42 -> 66

print(high_byte)
print(low_byte)


