from find_the_same_shoes.log.log_decorator import log_exceptions_and_info, setup_logger
from find_the_same_shoes.log.func_timer import performance_decorator
from find_the_same_shoes.compare_servers import preprocessing
import time


def example_func1(a, b):
    time.sleep(3)
    return a/b

def test_log():
    print(example_func1(1, 6))


def test1():
    preprecer = preprocessing.ImagePreprocessor()
    preprecer.resize_image('2.jpg', '1.jpg')


def test2():
    preprecer = preprocessing.ImagePreprocessor()
    if preprecer.remove_background(r"D:\workspace\RMBG-1.4\source\1.jpg"):
        print("yes")
    else:
        print("no")
    pass


if __name__ == '__main__':
    test2()