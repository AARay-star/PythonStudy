# 类对象的学习 GOGOGO

class Demo1:

    i = 12345  # 属性的定义
    # 方法的定义
    def func1(self):
        return '你好'

x = Demo1()

# 访问类的属性和方法
print(x.i)
print(x.func1())



class Complex:
    # 类的方法与普通的函数只有一个特别的区别——它们必须有一个额外的第一个参数名称, 按照惯例它的名称是 self。
    def __init__(self, realpart, imagpart):  #此为一个自动调用的方法
        self.r = realpart
        self.i = imagpart

x = Complex(3.0, -4.5)
print(x.r, x.i)  # 输出结果：3.0 -4.5



class MyClass:
    def __init__(self, value):
        self.value = value

    def display_value(self):
        print(self.value)

# 创建一个类的实例
obj = MyClass(42)
# 调用实例的方法
obj.display_value() # 输出 42


# 创建一个类定义
class people:
    #定义基本属性
    name = ''
    age = 0
    #定义私有属性
    _weight = 0
    def __init__(self, n, a , w):
        self.name = n
        self.age = a
        self._weight = w #私有属性
    def display(self):
        print(self.name, self.age, self._weight)
        print("%s说：我%d岁！" % (self.name, self.age))

#单继承
class person(people):
    province = ''
    def __init__(self,n,a,w,c):  #此处需要按照父类的顺序进行写入，除非使用关键字参数，不然会有问题
        people.__init__(self,n,a,w) # 调用父类
        self.province = c
    #覆写父类的方法
    def display(self):
        print("%s说：我今年%d岁了，我是%s的"%(self.name,self.age,self.province))


pep = people('丁真', 3, 20,)
pep.display()

per = person('丁真', 3, 20, '妈妈生')
per.display()

#另外一个类，多继承之前的准备
class member():
    pet = ''
    name = ''
    def __init__(self, n, p):
        self.name = n
        self.pet = p
    def speak(self):
        print("我是%s，%s闭嘴" % (self.name, self.pet))

#多继承
class sample(person, member):
    a = ''
    def __init__(self, n, a, w,c,p):
        person.__init__(self,n,a,w,c)
        member.__init__(self,n,p)

test = sample('丁真',3,100,'妈妈生','雪豹')
test.speak()   #若方法名同，默认调用的是在括号中参数位置排前父类的方法



class Parent:  # 定义父类
    def myMethod(self):
        print('调用父类方法')


class Child(Parent):  # 定义子类
    def myMethod(self):
        print('调用子类方法')


c = Child()  # 子类实例
c.myMethod()  # 子类调用重写方法
super(Child, c).myMethod()  # super函数实现的是：用子类对象调用父类已被覆盖的方法


#私有变量和公有变量输出
class JustCounter:
    __secretCount = 0  # 私有变量
    publicCount = 0  # 公开变量

    def count(self):
        self.__secretCount += 1
        self.publicCount += 1
        print(self.__secretCount)

counter = JustCounter()
counter.count()
counter.count()
print(counter.publicCount)
#print(counter.__secretCount)  # 报错，实例不能访问私有变量


#私有方法和公有方法
class Site:
    def __init__(self, name, url):
        self.name = name  # public
        self.__url = url  # private

    def who(self):
        print('name  : ', self.name)
        print('url : ', self.__url)

    def __foo(self):  # 私有方法
        print('这是私有方法')

    def foo(self):  # 公共方法
        print('这是公共方法')
        self.__foo()


x = Site('菜鸟教程', 'www.runoob.com')
x.who()  # 正常输出
x.foo()  # 正常输出
#x.__foo()  # 报错