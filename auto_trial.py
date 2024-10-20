import datetime
import uuid
import os
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()

file_path = os.path.expanduser(os.getenv('LOG'))
prefs_path = os.path.expanduser(os.getenv('PREFS'))

def already_ran_today(path: str) -> bool:
    try:
        with open(path, 'r') as f:
            last_line = f.readlines()[-1]
            if (last_line == '20'):
                return True
            return False
    except FileNotFoundError:
        print(f'File {path} not found')

def write_day(path: str) -> None:
    mode = 'w' if os.path.exists(path) else 'x'

    with open(path, mode) as f:
            f.write(str(datetime.date.today().day))

def change_uuid(path: str) -> None:
    tree = ET.parse(prefs_path)
    root = tree.getroot()
    for entry in root.findall('entry'):
        if (entry.get('key') == 'user_id_on_machine'):
            entry.set('value', str(uuid.uuid4()))
            break
    tree.write(path, encoding='UTF-8', xml_declaration=True)

def execute(log_path: str, prefs: str) -> None:
    if not already_ran_today(log_path):
        change_uuid(prefs)
        write_day(log_path)
        print('changed uuid')
    else:
        print('already did that for month')


if __name__ == '__main__':
    execute(file_path, prefs_path)
