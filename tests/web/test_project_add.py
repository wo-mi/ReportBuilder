import requests
import json

#curl -X POST http://localhost:5000/api/projects/1 -H "Authorization: Bearer {token}"

def run(token):

    url = 'http://localhost:5000/api/projects/'

    headers = {'Authorization': f'Bearer {token}'}

    jsonData = '''
    {
        "name": "Test project4",
        "config": ""
    }
    '''
    r = requests.post(url, headers=headers, json=json.loads(jsonData))

    if r.status_code == 200:
        return True
    else:
        print(r.status_code)
        print(r.text)
        return False

if __name__ == "__main__":
    from test_auth import get_token
    print(run(get_token()))
