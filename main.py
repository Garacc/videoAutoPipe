# import bilibili section info
from biDicts import sect
# import bilibili crawler func
from biCrawler import *
from biSubtitleTrans import segTranscript #, truncateTranscript, chunkTranscript
# imoprt * for get the api key
from biChatgpt import *
# import * for get the api key
from biNotion import *


def main():
    # token = 'your-token'
    # database_id = 'your-db-id'
    while True:
        blink = input("请输入B站视频链接: ")
        bvid = blink.split('/')[4]
        print("开始处理视频信息：{}".format(bvid))
        prompt = "我希望你是一名专业的视频内容编辑，请你尝试修正以下视频字幕文本中的拼写错误后，将其精华内容进行总结，然后以无序列表的方式返回，不要超过5条！确保所有的句子都足够精简，清晰完整。"
        transcript_text = biliSubtitle(bvid, biliPlayerList(bvid)[0])
        if transcript_text:
            print('字幕获取成功')
            seged_text = segTranscript(transcript_text)
            summarized_text = ""
            i = 1
            for entry in seged_text:
                try:
                    response = chatOpenAI(prompt, entry)
                    print("完成第{}部分摘要".format(str(i)))
                    i += 1
                except:
                    print("GPT接口摘要失败, 请检查网络连接")
                    response = "摘要失败"
                summarized_text += '\n' + response
            # gather the basic info of bvid
            bili_info = biliInfo(bvid)
            # insert the summary and basic info into notion
            insert2Notion(bili_info, summarized_text)
        else:
            print("字幕获取失败\n")

if __name__ == "__main__":
    main()