# >> 和 & 的使用
# reg >> 8：把 reg 右移 8 位，相当于丢掉低 8 位，只留下高 8 位在最低位的位置上。
reg = 0x4142  # 高字节 0x41('A'=65), 低字节 0x42('B'=66)
high_byte = (reg >> 8) & 0xFF  # 0x41 -> 65
low_byte  = reg & 0xFF         # 0x42 -> 66

print(high_byte)
print(low_byte)

#enumerate()
# enumerate(iterable, start=0) 会把可迭代对象包装成“(索引, 元素)”对的序列。
#for i, v in enumerate(['a', 'b']):  # 产生 (0,'a'), (1,'b')
#    ...
#for i, v in enumerate(['a', 'b'], start=1):  # 产生 (1,'a'), (2,'b')
#    ...

#range()
# 1) 基础遍历：0,1,2,3,4
for i in range(5):
    print(i, end=' ')
print()
# 2) 指定起止：1~10（不含11）
for i in range(1, 11):
    print(i, end=' ')
print()
# 3) 步长：偶数序列 0,2,4,6,8,10
for i in range(0, 11, 2):
    print(i, end=' ')
print()
# 4) 倒序与负步长：10,8,6,4,2
for i in range(10, 0, -2):
    print(i, end=' ')
print()
# 5) 重复执行 N 次（忽略循环变量）
for _ in range(3):
    print("Hello")
# 6) 求和与列表化
total = sum(range(1, 101))      # 1~100 的和
print("sum(1..100) =", total)
print("list(range(3)) =", list(range(3)))  # [0,1,2]
# 7) 通过下标遍历列表（需要下标时）
nums = [10, 20, 30, 40, 50]
for i in range(len(nums)):
    print(f"index={i}, value={nums[i]}")
# 8) 间隔取样：每隔3个元素取一个
for i in range(0, len(nums), 3):
    print(f"sample idx={i}, value={nums[i]}")
# 9) 推导式：生成列表/集合/字典
squares = [i * i for i in range(1, 6)]              # [1,4,9,16,25]
even_set = {i for i in range(0, 11, 2)}             # {0,2,4,6,8,10}
index_map = {i: nums[i] for i in range(len(nums))}  # {0:10,1:20,...}
print(squares, even_set, index_map)
# 10) 嵌套循环：简单九九乘法表（部分）
for i in range(1, 4):
    for j in range(1, i + 1):
        print(f"{i}*{j}={i*j}", end=' ')
    print()

