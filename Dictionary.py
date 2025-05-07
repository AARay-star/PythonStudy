# 字典的使用 GOGOGO

information = {'name': '丁真', 'likes': '雪豹', 'url': 'www.baidu.com','id':369} #创建一个关于information的字典

print(information)
print("Length:",len(information))
print(type(information))
print ("tinydict['Name']: ", information['name']) #访问字典里面的信息
print ("tinydict['ID']: ", information['id'])

information['id'] = 123456789 #修改字典
print(information)



emptyDict1 = {} #创建一个新的空字典
emptyDict2 = dict() # 使用内建函数dict()来创建字典

# 打印字典
print(emptyDict2)

# 查看字典的数量
print("Length:", len(emptyDict2))

# 查看类型
print(type(emptyDict2))

