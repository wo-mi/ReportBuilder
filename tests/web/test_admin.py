import requests

def run(token):

    url = 'http://localhost:5000/api/admin/'
    headers = {'Authorization': f'Bearer {token}'}

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        return True
    else:
        return False

if __name__ == "__main__":
    from test_auth import get_token
    print(run(get_token()))
