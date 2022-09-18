import requests

def get_token():
    r = requests.get('http://localhost:5000/api/token/',auth=('admin', 'abc'))

    if r.status_code == 200:
        json = r.json()
        token = json["token"]
        return token
    else:
        return False

def run():
    return get_token()

if __name__ == "__main__":
    print(get_token())
    