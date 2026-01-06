import functools
import json
import re
import time
from datetime import datetime
from json import JSONDecodeError


# Implement a simple decorator for logging
def log_decorator(func):
    # *args: собирает позиционные аргументы в кортеж.
    # **kwargs: собирает именованные аргументы в словарь.
    @functools.wraps(func)
    #  Декоратор @functools.wraps(func) используется для сохранения метаданных исходной функции (func) после её декорирования.
    def wrapper(*args, **kwargs):
        try:
            start_time = time.time()
            print(f"[{datetime.now()}] Starting func: {func.__name__}...")
            print(f"Arguments: args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            print(f"[{datetime.now()}] Finishing func: {func.__name__} during ({time.time()-start_time:.5f}). Rusultat: {result}")
            return result
        except Exception as e:
            print(f"[{datetime.now()}] Failed func: {func.__name__} with error: {e}")
            raise
    return wrapper

# Write a function to find duplicates in a list
@log_decorator
def search4duplicate(MyList: list):
    MyDic={}
    for lstitem in MyList:
        if lstitem in MyDic:
            MyDic[lstitem] = MyDic[lstitem] +1
        else:
            MyDic[lstitem] = 1
    # print(f"MyDic {MyDic}")
    return MyDic

# Write a function to find duplicates in a list
@log_decorator
def find_duplicates_v2(lst):
    from collections import Counter
    counter = Counter(lst)
    print(f"Counter: {counter}")
    # print(f"find_duplicates_v2 {[item for item, count in counter.items() if count > 1]}")
    return [item for item, count in counter.items() if count > 1]

# Write a function to find duplicates in a list
@log_decorator
def find_duplicates(lst):
    seen = set()
    duplicates = set()

    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    # print(f"find_duplicates {list(duplicates)}")
    return list(duplicates)

def open_json_file(path: str):
    try:
        with open(path,'r')  as file:
            my_json = json.load(file)
        return my_json
    except (TypeError, ValueError) as json_error:
        print(f"❌ Failed to serialize content from JSON: {json_error}")
    except FileNotFoundError as json_error:
        print(f"❌ Failed to serialize content from JSON: {json_error}")
    except JSONDecodeError as json_error:
        print(f"❌ Failed to serialize content from JSON: {json_error}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    return None

def save_json_file(path: str, content: str) -> bool:
    try:
        json.dumps(content)
        with open(path , 'w') as file:
            json.dump(content, file )
        return True
    except (TypeError, ValueError) as json_error:
        print(f"❌ Failed to serialize content to JSON: {json_error}")
    except OSError as file_error:
        print(f"❌ File I/O error: {file_error}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    return False


class TextUtils:
    @staticmethod
    def count_words(text):
        return len(text.split())
    @staticmethod
    def count_words2(text):
        words = re.split(r'[ ,;.]+', text)
        words = [word for word in words if word]
        return len(words)
    @log_decorator
    @staticmethod
    def to_snake_case(list):
        list2=[]
        for text in list:
            text = re.sub(r'([a-z])([A-Z])', r'\1_\2', text)
            text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1_\2', text)
            text = re.sub(r'[^a-zA-Z0-9_]', '_', text)
            text = re.sub(r'__+', '_', text)
            # text.strip('_').lower()
            list2.append(text.lower())
        return list2
    @staticmethod
    def remove_punctuation_re(text):
        return re.sub(r'[^\w\s]', '', text)

if __name__ == "__main__":
# 1. Write a function to find duplicates in a list
    my_list = ["shalom","privet","hello","shalom","hello"]
    search4duplicate(my_list)
    find_duplicates(my_list)
    find_duplicates_v2(my_list)
# 3. Work with JSON files - parsing and validation
    path=r"E:\Git_Projects\Amdocs\Python_tutorials\output\example_test.txt"
    path=r"E:\Git_Projects\Amdocs\Python_tutorials\output\ProductOrder_416885050005696512.json"
    my_json = open_json_file(path)
    print(f"FILE: opened")
    path=r"E:\Git_Projects\Amdocs\Python_tutorials\output\416885050005696512.json"
    data = {"name": "Evgeny", "tools": ["pytest", "selenium"], "experience": 3}
    save_json_file(path, data)
    #print(f"FILE: saved")
    #bad_data = {"name": "Evgeny", "joined": datetime.datetime.now()}
    #save_json_file(path, bad_data)
    #print(f"FILE: saved")
# 4. Goal 4: Class for working with strings
    print(f"word count: {TextUtils.count_words('aa bbbb   sss, rrrrr,gg')}")
    print(f"word count: {TextUtils.count_words2('Привет, мир! Это; тестовая строка.')}")
    print(f"snake_case: {TextUtils.to_snake_case(["HTMLParser","kebab-case-string","camelCaseString","PascalCaseString","This is a simple phrase","USER_NAME"])}")
