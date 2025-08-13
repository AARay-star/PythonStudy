"""
Try/Except 学习示例

内容涵盖：
- 基本 try/except
- 捕获多个特定异常与异常对象
- except 顺序与通用异常捕获
- try/except/else
- try/except/finally
- raise 主动抛出异常
- 自定义异常
"""

from typing import Any

#  title: str：参数类型标注，提示 title 应该是字符串
#  -> None：小箭头表示“返回类型”，这里表示函数不返回值（返回 None）
def print_header(title: str) -> None:

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def demo_basic() -> None:
    """最基础的 try/except：捕获指定异常类型。"""
    print_header("1) 基本 try/except")
    text = "42a"
    try:
        number = int(text)  # 这里会触发 ValueError
        print("转换成功:", number)
    except ValueError as error:
        print("捕获到 ValueError:", error)


def demo_multiple_excepts() -> None:
    """按类型分别处理不同异常，也可用元组合并。"""
    print_header("2) 多个 except")
    values: list[Any] = ["100", None, "abc"]
    for value in values:
        try:
            result = int(value)
            print(f"int({value!r}) => {result}")
        except TypeError as error:
            print("TypeError: 传入了不能转换的类型:", error)
        except ValueError as error:
            print("ValueError: 字符串内容不合法:", error)

    # 合并捕获多个类型到一个分支
    print("-- 合并捕获 --")
    for value in values:
        try:
            result = int(value)
            print(f"int({value!r}) => {result}")
        except (TypeError, ValueError) as error:
            print("捕获到 TypeError/ValueError:", error)


def demo_general_exception() -> None:
    """一般性兜底：放在最后，避免吞掉更具体的异常。"""
    print_header("3) 通用异常捕获 (Exception)")
    try:
        # 故意触发 ZeroDivisionError
        print(10 / 0)
    except ZeroDivisionError as error:
        print("更具体地处理 ZeroDivisionError:", error)
    except Exception as error:
        # 放在最后：兜底未知错误
        print("兜底捕获 Exception:", repr(error))


def demo_else() -> None:
    """else 仅在 try 块没有抛异常时执行。"""
    print_header("4) try/except/else")
    try:
        value = int("123")  # 不会抛异常
    except ValueError:
        print("except: 出错了")
    else:
        print("else: 无异常，结果是", value)


def demo_finally() -> None:
    """finally 总会执行：无论是否发生异常。"""
    print_header("5) try/except/finally")
    try:
        value = 10 / 0  # 触发 ZeroDivisionError
        print("结果:", value)
    except ZeroDivisionError as error:
        print("except: 捕获到:", error)
    finally:
        print("finally: 总会执行 (用于清理/释放资源)")


class AgeError(Exception):
    """演示自定义异常类型。"""


def validate_age(age: int) -> None:
    """演示 raise 主动抛出异常。"""
    if age < 0:
        raise AgeError(f"年龄不能为负数: {age}")
    if age > 150:
        raise AgeError(f"年龄过大: {age}")


def demo_raise_and_custom() -> None:
    print_header("6) raise 与自定义异常")
    for age in [18, -5, 200]:
        try:
            print("校验年龄:", age)
            validate_age(age)
        except AgeError as error:
            print("捕获到 AgeError:", error)
        else:
            print("通过校验")
#else：只有当 try 代码块“没有抛出异常”时才执行。适合“只有校验成功才做”的逻辑。
#finally：无论是否抛异常都会执行（包括异常未被捕获、甚至函数提前 return）。适合“清理/收尾”的逻辑。




#放“示例代码、命令行入口、快速测试”。
#只有在这个文件运行的时候才会执行下面的代码，如果是另外一个文件import这个文件，则不会执行下面的代码
if __name__ == "__main__":
    demo_basic()
    demo_multiple_excepts()
    demo_general_exception()
    demo_else()
    demo_finally()
    demo_raise_and_custom()
    
    
    
