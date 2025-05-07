# 学习List GOGOGO

list1 = ['Google', 'Runoob', 1997, 2000]
list2 = [1, 2, 3, 4, 5 ]
list3 = ["a", "b", "c", "d","e","f","g","h"]
list4 = ['red', 'green', 'blue', 'yellow', 'white', 'black']

print(list1[0]) #顺着数，从0开始
print(list2[-2]) #倒着数，从-1开始
print(list3[0:5]) # 取前六个
print(list3[2:-2]) # 第三个数到倒数第二个

list3.append('i') # 加一个字母i
print(list3) # 输出新的列表3

del list1[1] #删除列表第一个
print(list1) #输出新的列表1

print(len(list3)) #输出列表长度
print(max(list2)) #输出列表最大
print(list2+list3) #两个列表相加
print(list4*2) #输出两次
if 'red' in list1:
    print('red')
for x in list3:print(x)

