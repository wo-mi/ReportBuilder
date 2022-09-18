import os
import requests

def run(token):

    path = os.path.join( os.path.dirname(__file__), 'filename.pdf')

    files = {'file': open(path, 'rb')}

    url = 'http://localhost:5000/api/projects/1/files/'
    headers = {'Authorization': f'Bearer {token}'}

    r = requests.post(url, headers=headers, files=files)

    if r.status_code == 200:
        return True
    else:
        print(r.status_code)
        print(r.text)
        return False

if __name__ == "__main__":
    from test_auth import get_token
    print(run(get_token()))
