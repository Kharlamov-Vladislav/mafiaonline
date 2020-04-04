import bs4
import re
import numpy as np
from bs4 import BeautifulSoup

def time2seconds(array_time):
    array_time = [array_time[0]] + array_time # ��������� ������� ��������� � �������� ���� ������
    array_time = list(map(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]), array_time)) # ��������� mm:ss -> seconds
    return np.cumsum((np.diff(array_time) % 3600))

def parse_chat(chat):
    curr_elem, prev_elem = '', ''
    array_messages, array_time = [], []
    
    for elem in BeautifulSoup(chat).body:
        prev_elem, curr_elem = curr_elem, elem # ����� ��������� � ���������, ���� ���������� ���
        if isinstance(curr_elem, bs4.element.Tag): # ��������, ��� ������ ������ ��� � ����������
            if len(prev_elem) == 6 and re.match('\d{2}:\d{2}\s', prev_elem): #��������, ��� ���������� ��� �������� �����
                array_time.append(prev_elem.rstrip())
                array_messages.append(curr_elem.get_text())
    array_time = time2seconds(array_time) #��������� ������ ������ ��������� ��� ������� ��������� �������������� �������
    return list(zip(array_time, array_messages))