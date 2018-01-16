import json
import requests
import os
import sys


def publish(html_file, title, labels, post_id):
    access_token_file = '~/.medium-access-token'
    expanded_path = os.path.expanduser(access_token_file)
    print(expanded_path)
    if not os.path.exists(expanded_path):
        print(
            f'File {access_token_file} does not exist. Create that file and add your medium access token in that file')
        sys.exit()
    else:
        with open(expanded_path) as file:
            access_token = file.read().strip()

    # print(access_token)
    headers = get_headers(access_token)
    # print(headers)

    user_url = get_user_url(headers)

    if not user_url:
        sys.exit()

    # Publish new post
    posts_url = user_url + 'posts/'
    # print(posts_url)

    payload = generate_payload(title, labels, html_file, post_id)
    # print(payload)
    response = requests.request('POST', posts_url, data=payload, headers=headers)
    json_res = json.loads(response.text)
    print(json.dumps(json_res))


def generate_payload(title, labels, html_file, post_id):
    return {
        'title': title,
        'contentFormat': 'html',
        'tags': labels,
        'publishStatus': 'draft',
        'content': open(html_file).read()
    }


def get_headers(access_token):
    return {
        'Authorization': "Bearer " + access_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84'
    }


def get_user_url(headers):
    base_url = "https://api.medium.com/v1/"
    me_url = base_url + 'me/'

    # Validate access token by making a call to https://api.medium.com/v1/me
    try:
        me_response = requests.request("GET", me_url, headers=headers).text
    except:
        print('Unable to validate the access token in ~/.medium-access-token file. '
              'Check the access token and your internet connectivity')
        return

    json_me_response = json.loads(me_response)
    # print(json_me_response)
    user_id = json_me_response['data']['id']
    return base_url + 'users/' + user_id + '/'


if __name__ == '__main__':
    publish()
