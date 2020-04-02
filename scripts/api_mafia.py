import requests
import json
def get_log(id_game):
    """Возращает полную информацию о партии:
    ----------------------------------------------------
    ВХОДНЫЕ ПАРАМЕТРЫ:
    id_game :: Целочисленное значение уникального индификатора партии
    
    ВОЗРАЩАЕТ:
    Полный лог партии в формате словаря
    """
    
    url = f'https://www.mafiaonline.ru/api/api.php?action=log&param=log&id={id_game}'
    r = requests.get(url)
    status_code = r.status_code
    r = json.loads(r.text)
    if status_code == 200 and r['r'] == 'ok':
        return r['log']