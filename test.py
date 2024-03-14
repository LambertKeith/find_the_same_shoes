from find_the_same_shoes.log.log_decorator import log_exceptions_and_info, setup_logger

logger = setup_logger()

@log_exceptions_and_info(logger)
def example_func1(a, b):

    return a/b

def test_log():
    print(example_func1(1, 6))




if __name__ == '__main__':
    test_log()