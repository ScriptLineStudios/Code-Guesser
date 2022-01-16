from scripts.get_code import get_repo
import requests

def generate_round(): 
    desc, code = get_repo()
    r = requests.get(code, allow_redirects=True)
    file = open("data/script", 'wb').write(r.content)
    b_lines = []
    with open("data/script", 'rb') as f:
        for row in f:
            b_lines.append(row.decode('utf-8').rstrip())

    if b_lines == []:
        generate_round()
    else:
        return b_lines, desc