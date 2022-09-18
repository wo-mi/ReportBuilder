import os
import requests
import shutil
import re

#curl -X POST http://localhost:5000/api/projects/1 -H "Authorization: Bearer {token}"

basedir = os.path.dirname(os.path.abspath(__file__))

def run(token):

    url = 'http://localhost:5000/api/projects/1'

    headers = {'Authorization': f'Bearer {token}'}


    with requests.get(url, headers=headers, stream=True) as r:
        d = r.headers['content-disposition']
        filename = (re.findall("filename=(.+)", d)[0])
        if filename[0] == "\"" and filename[-1] == "\"":
            filename = filename[1:-1]

        with open(os.path.join(basedir,filename), 'wb') as f:
            shutil.copyfileobj(r.raw, f)

if __name__ == "__main__":
    from test_auth import get_token
    print(run(get_token()))
