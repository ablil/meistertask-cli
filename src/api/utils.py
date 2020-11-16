import requests

RED = "\33[31m"
END = "\33[0m"


def catch_http_errors(func):
    def wrapper(*args):
        try:
            return func(*args)
        except requests.exceptions.ConnectionError as e:
            print(f'{RED}It seems there is not internet connection{END}')
            exit()
        except Exception as e:
            print(e)
            exit()
    return wrapper
