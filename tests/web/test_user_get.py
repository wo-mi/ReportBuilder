import requests

#curl -X POST http://localhost:5000/api/projects/1 -H "Authorization: Bearer {token}"

def run(token):

    url = 'http://localhost:5000/api/users/1'

    headers = {'Authorization': f'Bearer {token}'}

    r = requests.get(url, headers=headers)

    print(r.status_code)
    print(r.text)

    if r.status_code == 200:
        return True
    else:
        return False

if __name__ == "__main__":
    from test_auth import get_token
    print(run(get_token()))
