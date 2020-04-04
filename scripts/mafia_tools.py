import bs4
import re
import numpy as np
from bs4 import BeautifulSoup

def time2seconds(array_time):
    array_time = [array_time[0]] + array_time # Добавляем нулевое сообщение с которого идет отсчёт
    array_time = list(map(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]), array_time)) # Переводим mm:ss -> seconds
    return np.cumsum((np.diff(array_time) % 3600))

def parse_chat(chat):
    curr_elem, prev_elem = '', ''
    array_messages, array_time = [], []
    
    for elem in BeautifulSoup(chat).body:
        prev_elem, curr_elem = curr_elem, elem # время сообщения и сообщение, если корректный тэг
        if isinstance(curr_elem, bs4.element.Tag): # Проверка, что пришел нужный тег с сообщением
            if len(prev_elem) == 6 and re.match('\d{2}:\d{2}\s', prev_elem): #Проверка, что предыдущий тэг означает время
                array_time.append(prev_elem.rstrip())
                array_messages.append(curr_elem.get_text())
    array_time = time2seconds(array_time) #Возращает список секунд прошедших для каждого сообщения относительного первого
    return list(zip(array_time, array_messages))