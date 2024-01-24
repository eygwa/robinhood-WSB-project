import json
import datetime

symbol = 'SPY'

topAuthors = [
    "OPINION_IS_UNPOPULAR",
    "leanturkeyforlunch",
    "catbulliesdog",
    "j__walla",
    "ddcy1845",
    "rebelo55",
    "Unaheari",
    "Joey-tv-show-season2",
    "xltaylx",
    "recycledraptors",
]

symbols = ['SPY', 'NVDA', 'MSFT', 'GOOG', 'GME', 'AI', 'AAPL']

for i in symbols:
        # Load sentiment data
    with open(f'getPosts/wallstreetbets_{i}_posts_2022.json', 'r') as f:
        inJson = json.load(f)
    
    outDict = {};
    
    for id, data in inJson.items():
        if (data["author"] in topAuthors):
            utc_time = datetime.datetime.utcfromtimestamp(data["created_utc"])
            formatted_date = utc_time.strftime('%Y-%m-%d')
            if (formatted_date in outDict.keys()):
                outDict[formatted_date]+=1;
            else:
                outDict[formatted_date] = 1;

    # save data to a JSON file
    with open(('topAuthorsPerDay/' + i + '_topAuthorPosts_2022.json'), "w") as f:
        json.dump(outDict, f)
