import requests

def run(token):

    url = 'http://localhost:5000/api/projects/1/config/'

    headers = {'Authorization': f'Bearer {token}'}

    json = '''
    {
        "title": "Test project",
        "overlay_template": "default",
        "output_filename": "Test web project - output",
        "table_of_content" : {
            "title": "Table of contents",
            "position": 0,
            "template": "table_of_content",
            "overlay_template": "default"
        },
        "documents": [
            {
                "filename":"filename.pdf",
                "title":"First document",
                "overlay_template" : "default",
                "number_prefix" : "",
                "start_number" : 1
            }
        ]
    }
    '''

    r = requests.post(url, headers=headers, json=json)

    if r.status_code == 200:
        return True
    else:
        print(r.status_code)
        print(r.text)
        return False


if __name__ == "__main__":
    from test_auth import get_token
    print(run(get_token()))
