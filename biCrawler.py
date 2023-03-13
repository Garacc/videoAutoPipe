import requests


# Get the video info
def biliInfo(bvid):
    params = (
        ('bvid', bvid),
    )
    # bilibili video info response
    response = requests.get('https://api.bilibili.com/x/web-interface/view', params=params)
    ans = response.json()['data']

    # add extra info
    ans['url'] = "https://www.bilibili.com/video/" + bvid

    # add tags info
    tags = biliTags(bvid)
    ans['tags'] = tags
    
    return ans


# Get the video tags
def biliTags(bvid):
    params = (
        ('bvid', bvid),
    )

    # bilibili video tags response
    response = requests.get('https://api.bilibili.com/x/web-interface/view/detail/tag', params=params)
    data = response.json()['data']
    if data:
        tags = [x['tag_name'] for x in data]
        if len(tags) > 5:
            tags = tags[:5]
    else:
        tags = []

    return tags


# Get the video player list / multi page
def biliPlayerList(bvid):
    response = requests.get('https://api.bilibili.com/x/player/pagelist?bvid=' + bvid)
    cid_list = [x['cid'] for x in response.json()['data']]

    return cid_list


def biliSubtitleList(bvid, cid, headers):
    response = requests.get(f'https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}', headers=headers)
    subtitles = response.json()['data']['subtitle']['subtitles']
    if subtitles:
        return ['https:' + x['subtitle_url'] for x in subtitles]
    else:
        return []


def biliSubtitle(bvid, cid):
    headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63'
    }
    
    subtitles = biliSubtitleList(bvid, cid, headers)
    if subtitles:
        response = requests.get(subtitles[0], headers=headers)
        if response.status_code == 200:
            body = response.json()['body']
            return body
    return []


if __name__ == "__main__":
    bvid = "BV1qo4y1r7qV"
    # test 1
    print("bili_info")
    print(biliInfo(bvid))
    # test 2
    print("bili_tags")
    print(biliTags(bvid))
    # test 3
    print("bili_player_list")
    print(biliPlayerList(bvid))
    # test 4
    subtitle_text = biliSubtitle(bvid, biliPlayerList(bvid)[0])
    print("bili_subtitle_text")
    print(subtitle_text)
