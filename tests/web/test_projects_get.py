import requests

#curl -X POST http://localhost:5000/api/projects/1 -H "Authorization: Bearer {token}"

def run(token):

    url = 'http://localhost:5000/api/projects/'

    headers = {'Authorization': f'Bearer {token}'}


    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        print(r.text)
        return True
    else:
        print(r.status_code)
        print(r.text)
        return False

if __name__ == "__main__":
    from test_auth import get_token
    print(run(get_token()))
