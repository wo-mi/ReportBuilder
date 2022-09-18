import requests

def run(token):

    url = 'http://localhost:5000/api/users/2'
    headers = {'Authorization': f'Bearer {token}'}

    r = requests.delete(url, headers=headers)

    if r.status_code == 200:
        return True
    else:
        print(r.status_code)
        print(r.text)
        return False

if __name__ == "__main__":
    from test_auth import get_token
    print(run(get_token()))
