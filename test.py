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
    preprecer.resize_image('2.png', '1.jpg')

if __name__ == '__main__':
    test1()