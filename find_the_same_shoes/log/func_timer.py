import time
import psutil
import functools


def performance_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_resources = psutil.Process().cpu_times()
        start_memory = psutil.Process().memory_info().rss
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        end_resources = psutil.Process().cpu_times()
        end_memory = psutil.Process().memory_info().rss
        
        print(f"函数 {func.__name__} 调用开始时间：{start_time}")
        print(f"函数 {func.__name__} 调用结束时间：{end_time}")
        print(f"函数 {func.__name__} 执行耗时：{end_time - start_time}")
        print(f"函数 {func.__name__} 消耗的系统资源：")
        print(f"  用户CPU时间：{end_resources.user - start_resources.user} 秒")
        print(f"  系统CPU时间：{end_resources.system - start_resources.system} 秒")
        print(f"  最大使用内存：{end_memory - start_memory} 字节")
        
        return result
    return wrapper

""" # 示例使用
@performance_decorator
def example_function(n):
    result = 0
    for i in range(n):
        result += i
    return result

example_function(1000000) """
