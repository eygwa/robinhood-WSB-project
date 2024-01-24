# NOTE: Last comma must be manually removed from json

import requests
import json
import time
import os

def remove_first_last_line(s):
    lines = s.split('\n')
    lines = lines[1:-1]
    return '\n'.join(lines)
    
def add_json_boundaries(filename):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("{\n" + content)
        f.seek(0, 2)
        f.write("\n}")

current_date = 1640995200  # January 1st, 2022 at midnight UTC
end_date = 1672531200  # January 1st, 2023 at midnight UTC

url = 'https://api.pushshift.io/reddit/search/submission/'
subreddit = 'wallstreetbets'
query_token = 'BB'

post_count = 0
filename = f'wallstreetbets_posts_{current_date}.json'

try:
    os.remove(filename)
except:
    pass
while current_date < end_date:
    current_time = time.time()
    print(f"Retrieving posts for {time.ctime(current_date)}...")
    try:
        payload = {'subreddit': subreddit,
                   'q': query_token,
                   'size': 100,
                   'after': current_date,
                   'before': current_date + 86400}
        res = requests.get(url, params=payload)
        data = res.json()
        all_posts = data['data']
        print(f"Retrieved {len(all_posts)} posts. Total = {post_count} posts.")
    except Exception as e:
        # Too Many Requests, wait a minute
        print(f'ERROR: {e}')
        print('Delaying one minute')
        time.sleep(60)
    
    for post in all_posts:
        post_data = {
            "title": post["title"],
            "selftext": post["selftext"],
            "url": post["url"],
            "score": post["score"],
            "author": post["author"],
            "created_utc": post["created_utc"],
            "num_comments": post["num_comments"]
        }
        with open(filename, 'a') as f:
            toAdd = json.dumps({post["id"]:post_data}, indent=2, cls=json.JSONEncoder)
            toAdd = remove_first_last_line(toAdd)
            f.write(toAdd)
            f.write(',')
        post_count += 1
    
    current_date += 86400  # Move to the next day
    time.sleep(3)


print(f"Retrieved a total of {post_count} posts.")
add_json_boundaries(filename)
