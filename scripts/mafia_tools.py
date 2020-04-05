import bs4
import re
import numpy as np
from bs4 import BeautifulSoup

def parse_chat(chat):

    def time2seconds(array_time):
        array_time = [array_time[0]] + array_time # Добавляем нулевое сообщение с которого идет отсчёт
        array_time = list(map(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]), array_time)) # Переводим mm:ss -> seconds
        return np.cumsum((np.diff(array_time) % 3600))
        
        
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

def parse_summary(log):

    def get_move(move):
        decrypte_color = {'red' : 'move-maf', '#d5c32d' : 'move-positive'}
        colors = 'red|#d5c32d'
        r = re.findall(colors, move['style'])
        if r:
            return decrypte_color[r[0]]
        return 'move-city'
        
        
    CONST_UPDATE_CHAT = 3798821
    new_chat = True if log['id'] > CONST_UPDATE_CHAT else False
    
    if new_chat:
        types_move = ['move move-city', 'move move-maf', 'move move-positive', 'move move-doc', 'move move-man', 'move move-kom']
        moves = BeautifulSoup(log['summary']).find_all('span', {'class' : types_move})
        parse_moves = []
        player_nicks = '|'.join(list(map(lambda player: player['nick'], log['players'])))
        for move in moves:
            msg = move.get_text()
            nick_1, nick_2 = re.findall(player_nicks, msg)
            parse_moves.append([move['class'][1], (nick_1, nick_2)])
            
            
    else:
        moves = BeautifulSoup(log['summary']).find_all('b', {'style' : True})
        parse_moves = []
        player_nicks = '|'.join(list(map(lambda player: player['nick'], log['players'])))
        for move in moves:
            msg = move.get_text()
            nicks = re.findall(player_nicks, msg)
            if len(nicks) == 2:
                nick_1, nick_2 = nicks
            parse_moves.append([get_move(move), (nick_1, nick_2)])

    return parse_moves