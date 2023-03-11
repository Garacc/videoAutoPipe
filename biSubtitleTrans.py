# from bilibili Summary

def truncateTranscript(transcript):
    limit = 500

    transcript = [{"text": item["content"], "index": index, "timestamp": item["from"]} for index, item in enumerate(transcript)]
    text = " ".join([x["text"] for x in sorted(transcript, key=lambda x: x["index"])])

    bytes = len(text.encode('utf-8'))
    if bytes > limit:
        ratio = limit / bytes
        newStr = text[:int(len(text)*ratio)]
        text = newStr
    
    print("视频文本共{}字, 单次设定上限为{}字, 超出部分将被截断".format(bytes, limit))
    return text


def chunkTranscript(transcript):
    limit = 7000

    def textToBinaryString(str):
        escstr = str.encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')
        binstr = ""
        for c in escstr:
            binstr += f"{ord(c):08b}"
        return binstr


    def getChunkedTranscripts(textData, textDataOriginal):
        result = ""
        text = " ".join([x["text"] for x in sorted(textData, key=lambda x: x["index"])])
        bytes = len(textToBinaryString(text))
        
        if bytes > limit:
            evenTextData = [t for i, t in enumerate(textData) if i % 2 == 0]
            result = getChunkedTranscripts(evenTextData, textDataOriginal)
        else:
            if len(textDataOriginal) != len(textData):
                for obj in textDataOriginal:
                    if any(t["text"] == obj["text"] for t in textData):
                        continue
                    textData.append(obj)
                    newText = " ".join([x["text"] for x in sorted(textData, key=lambda x: x["index"])])

                    newBytes = len(textToBinaryString(newText))
                    # fill the newText to the limit
                    if newBytes < limit:
                        nextText = textDataOriginal[[t["text"] for t in textDataOriginal].index(obj["text"]) + 1]
                        nextTextBytes = len(textToBinaryString(nextText["text"]))
                        if newBytes + nextTextBytes > limit:
                            overRate = ((newBytes + nextTextBytes) - limit) / nextTextBytes
                            chunkedText = nextText["text"][:int(len(nextText["text"])*overRate)]
                            textData.append({"text": chunkedText, "index": nextText["index"]})
                            result = " ".join([x["text"] for x in sorted(textData, key=lambda x: x["index"])])
                        else:
                            result = newText
                    else:
                        break
            else:
                result = text
        originalText = " ".join([x["text"] for x in sorted(textDataOriginal, key=lambda x: x["index"])])
        return originalText if result == "" else result
    
    transcript = [{"text": item["content"], "index": index, "timestamp": item["from"]} for index, item in enumerate(transcript)]
    ans = getChunkedTranscripts(transcript, transcript)

    print("视频文本共{}字, 单次设定上限为{}字, 超出部分将被截断".format(len(ans.encode('utf-8')), limit / 8))

    return ans


def segTranscript(transcript):
    transcript = [{"text": item["content"], "index": index, "timestamp": item["from"]} for index, item in enumerate(transcript)]

    text = " ".join([x["text"] for x in sorted(transcript, key=lambda x: x["index"])])
    length = len(text.encode('utf-8'))
    seg_length = 3500
    n = length // seg_length + 1
    print("视频文本共{}字, 分为{}部分进行摘要".format(length, n))
    division = len(transcript) // n
    new_l = [transcript[i * division: (i + 1) * division] for i in range(n)]
    segedTranscipt = [" ".join([x["text"] for x in sorted(j, key=lambda x: x["index"])]) for j in new_l]

    return segedTranscipt

if __name__ == '__main__':
    case_subtitle = [
                    {'from': 0.46, 'to': 2.86, 'sid': 1, 'location': 2, 'content': '我总觉得我们打辩论的有些人', 'music': 0.0},
                    {'from': 2.86, 'to': 5.95, 'sid': 2, 'location': 2, 'content': '有些时候对这个世界太有攻击性', 'music': 0.0},
                    {'from': 5.95, 'to': 6.76, 'sid': 3, 'location': 2, 'content': '所以啊', 'music': 0.0},
                    {'from': 6.76, 'to': 10.26, 'sid': 4, 'location': 2, 'content': '所以今天我决定要进行一个不得罪人挑战', 'music': 0.0},
                    {'from': 10.26, 'to': 12.78, 'sid': 5, 'location': 2, 'content': '我们呢会观看很多非专业的辩手', 'music': 0.0},
                    {'from': 12.78, 'to': 14.7, 'sid': 6, 'location': 2, 'content': '尝试打辩论的一些视频', 'music': 0.0},
                    {'from': 14.7, 'to': 15.18, 'sid': 7, 'location': 2, 'content': '然后呢', 'music': 0.0},
                    {'from': 15.18, 'to': 18.58, 'sid': 8, 'location': 2, 'content': '我们必须要以专业的角度去对他们的内容', 'music': 0.0},
                    {'from': 18.58, 'to': 20.26, 'sid': 9, 'location': 2, 'content': '进行一些解释说明', 'music': 0.0},
                    {'from': 20.26, 'to': 20.92, 'sid': 10, 'location': 2, 'content': '当然了', 'music': 0.0},
                    {'from': 20.92, 'to': 22.84, 'sid': 11, 'location': 2, 'content': '我们不可以攻击他们', 'music': 0.0},
                    {'from': 22.84, 'to': 24.98, 'sid': 12, 'location': 2, 'content': '尤其不可以从专业的角度攻击他们', 'music': 0.0},
                    {'from': 24.98, 'to': 26.18, 'sid': 13, 'location': 2, 'content': '但如果我在途中', 'music': 0.0},
                    {'from': 26.18, 'to': 28.4, 'sid': 14, 'location': 2, 'content': '不小心攻击到了任何一位辩手呢', 'music': 0.0},
                    {'from': 28.4, 'to': 30.92, 'sid': 15, 'location': 2, 'content': '我就要接受一个没事找事的惩罚', 'music': 0.0},
                    {'from': 30.92, 'to': 33.28, 'sid': 16, 'location': 2, 'content': '今天呢我们就一起来欣嘿', 'music': 0.0},
                    {'from': 33.28, 'to': 35.25, 'sid': 17, 'location': 2, 'content': '没听懂看你就完', 'music': 0.0},
                    {'from': 39.43, 'to': 41.57, 'sid': 18, 'location': 2, 'content': '抱抱必须吧', 'music': 0.0},
                    {'from': 41.57, 'to': 44.33, 'sid': 19, 'location': 2, 'content': '就这我太喜欢tim tim的饭了', 'music': 0.0},
                    {'from': 44.33, 'to': 45.65, 'sid': 20, 'location': 2, 'content': '我天天吃的香喷了', 'music': 0.0},
                    {'from': 45.65, 'to': 46.37, 'sid': 21, 'location': 2, 'content': '我吃胖了', 'music': 0.0},
                    {'from': 46.37, 'to': 49.72, 'sid': 22, 'location': 2, 'content': '我都认为小说tm这个月就得饱饭', 'music': 0.0},
                    {'from': 49.72, 'to': 50.53, 'sid': 23, 'location': 2, 'content': '为什么呢', 'music': 0.0},
                    {'from': 50.53, 'to': 52.0, 'sid': 24, 'location': 2, 'content': '因为我热爱我的公司', 'music': 0.0},
                    {'from': 52.0, 'to': 53.14, 'sid': 25, 'location': 2, 'content': '我热爱我的团队', 'music': 0.0},
                    {'from': 53.14, 'to': 54.22, 'sid': 26, 'location': 2, 'content': '我跟大家一块吃饭', 'music': 0.0},
                    {'from': 54.22, 'to': 54.88, 'sid': 27, 'location': 2, 'content': '我开心', 'music': 0.0},
                    {'from': 54.88, 'to': 55.66, 'sid': 28, 'location': 2, 'content': '我开心了之后', 'music': 0.0},
                    {'from': 55.66, 'to': 56.8, 'sid': 29, 'location': 2, 'content': '我就有创作的热情', 'music': 0.0},
                    {'from': 56.8, 'to': 57.64, 'sid': 30, 'location': 2, 'content': '有了创作的热情', 'music': 0.0},
                    {'from': 57.64, 'to': 59.7, 'sid': 31, 'location': 2, 'content': '我就能继续给大家创作更好的视频', 'music': 0.0},
                    {'from': 59.7, 'to': 61.47, 'sid': 32, 'location': 2, 'content': '我跟大家的关系好了之后', 'music': 0.0},
                    {'from': 61.47, 'to': 63.9, 'sid': 33, 'location': 2, 'content': '我做出来的效果就非常的自然', 'music': 0.0},
                    {'from': 63.9, 'to': 65.64, 'sid': 34, 'location': 2, 'content': '这个视频就好看好看的', 'music': 0.0},
                    {'from': 65.64, 'to': 67.14, 'sid': 35, 'location': 2, 'content': '咱们这个数据就好', 'music': 0.0},
                    {'from': 67.14, 'to': 67.74, 'sid': 36, 'location': 2, 'content': '数据就好了', 'music': 0.0},
                    {'from': 67.74, 'to': 70.98, 'sid': 37, 'location': 2, 'content': '那这个公司的这个收入呢就会蹭蹭往上涨', 'music': 0.0},
                    {'from': 70.98, 'to': 72.12, 'sid': 38, 'location': 2, 'content': '然后涨了之后呢', 'music': 0.0},
                    {'from': 72.12, 'to': 74.04, 'sid': 39, 'location': 2, 'content': '他就有钱继续给我们包饭', 'music': 0.0},
                    {'from': 74.04, 'to': 75.06, 'sid': 40, 'location': 2, 'content': '划开最后一句啊', 'music': 0.0},
                    {'from': 75.06, 'to': 77.48, 'sid': 41, 'location': 2, 'content': '他是一个还是比较完整的一个逻辑链', 'music': 0.0},
                    {'from': 77.48, 'to': 80.48, 'sid': 42, 'location': 2, 'content': '这也是在我们打辩论当中非常需要重要的重', 'music': 0.0},
                    {'from': 80.48, 'to': 81.88, 'sid': 43, 'location': 2, 'content': '我嘴欠费了', 'music': 0.0},
                    {'from': 81.88, 'to': 84.52, 'sid': 44, 'location': 2, 'content': '这也是我们在打辩论当中非常重要的一点', 'music': 0.0},
                    {'from': 84.52, 'to': 87.82, 'sid': 45, 'location': 2, 'content': '就是你的逻辑链他需要调成一个完整的状态', 'music': 0.0},
                    {'from': 87.82, 'to': 89.26, 'sid': 46, 'location': 2, 'content': '你的结论a导向结论', 'music': 0.0},
                    {'from': 89.26, 'to': 92.44, 'sid': 47, 'location': 2, 'content': 'bb在导向结论c在反过来我们质询的时候', 'music': 0.0},
                    {'from': 92.44, 'to': 95.52, 'sid': 48, 'location': 2, 'content': '就是去听你到a到b到c中间是不是有缺乏', 'music': 0.0},
                    {'from': 95.52, 'to': 96.6, 'sid': 49, 'location': 2, 'content': '比如他刚刚那个例子', 'music': 0.0},
                    {'from': 96.6, 'to': 98.68, 'sid': 50, 'location': 2, 'content': '如果他把更好的创作这件事情去掉', 'music': 0.0},
                    {'from': 98.68, 'to': 100.36, 'sid': 51, 'location': 2, 'content': '直接说吃饱了就可以带来收益', 'music': 0.0},
                    {'from': 100.36, 'to': 102.04, 'sid': 52, 'location': 2, 'content': '那就属于一个逻辑切换的现象', 'music': 0.0},
                    {'from': 102.04, 'to': 104.18, 'sid': 53, 'location': 2, 'content': '首先正方说到公司包饭', 'music': 0.0},
                    {'from': 104.18, 'to': 104.84, 'sid': 54, 'location': 2, 'content': '你就开心', 'music': 0.0},
                    {'from': 104.84, 'to': 105.65, 'sid': 55, 'location': 2, 'content': '你开心', 'music': 0.0},
                    {'from': 105.65, 'to': 106.76, 'sid': 56, 'location': 2, 'content': '公司有收入', 'music': 0.0},
                    {'from': 106.76, 'to': 108.44, 'sid': 57, 'location': 2, 'content': '有收入就可以继续包饭', 'music': 0.0},
                    {'from': 108.44, 'to': 110.96, 'sid': 58, 'location': 2, 'content': '怎么让辩论赛看起来更像是真的辩论赛', 'music': 0.0},
                    {'from': 110.96, 'to': 113.18, 'sid': 59, 'location': 2, 'content': '就是你要让选手在不断的写东西', 'music': 0.0},
                    {'from': 113.18, 'to': 116.27, 'sid': 60, 'location': 2, 'content': '那在这里面小潮 院长就做的非常好', 'music': 0.0},
                    {'from': 116.27, 'to': 118.78, 'sid': 61, 'location': 2, 'content': '他在对方打野的时候一直在记东西', 'music': 0.0},
                    {'from': 118.78, 'to': 120.64, 'sid': 62, 'location': 2, 'content': '并且他在他的陈词开始之前', 'music': 0.0},
                    {'from': 120.64, 'to': 122.2, 'sid': 63, 'location': 2, 'content': '先总结一下对方的观点', 'music': 0.0},
                    {'from': 122.2, 'to': 125.24, 'sid': 64, 'location': 2, 'content': '这个在一个有很多论点的就常规辩论赛里面', 'music': 0.0},
                    {'from': 125.24, 'to': 127.34, 'sid': 65, 'location': 2, 'content': '真是让评委能够快速的知道', 'music': 0.0},
                    {'from': 127.34, 'to': 129.08, 'sid': 66, 'location': 2, 'content': '你接下来一段话想干什么', 'music': 0.0},
                    {'from': 129.08, 'to': 130.31, 'sid': 67, 'location': 2, 'content': '我不在开源节流', 'music': 0.0},
                    {'from': 130.31, 'to': 132.56, 'sid': 68, 'location': 2, 'content': '这个月如果要报案的话', 'music': 0.0},
                    {'from': 132.56, 'to': 134.15, 'sid': 69, 'location': 2, 'content': '就是要有一笔收入', 'music': 0.0},
                    {'from': 134.15, 'to': 135.35, 'sid': 70, 'location': 2, 'content': '但这笔收入不少', 'music': 0.0},
                    {'from': 135.35, 'to': 136.58, 'sid': 71, 'location': 2, 'content': '我们的人数多', 'music': 0.0},
                    {'from': 136.58, 'to': 137.84, 'sid': 72, 'location': 2, 'content': '成本高', 'music': 0.0},
                    {'from': 137.84, 'to': 140.76, 'sid': 73, 'location': 2, 'content': '收入用来包饭吃饭', 'music': 0.0},
                    {'from': 140.76, 'to': 143.82, 'sid': 74, 'location': 2, 'content': '就没有公司的其他内容', 'music': 0.0},
                    {'from': 143.82, 'to': 145.22, 'sid': 75, 'location': 2, 'content': '就拍不了视频', 'music': 0.0},
                    {'from': 145.22, 'to': 146.15, 'sid': 76, 'location': 2, 'content': '做不了视频', 'music': 0.0},
                    {'from': 146.15, 'to': 147.11, 'sid': 77, 'location': 2, 'content': '也赚不了钱', 'music': 0.0},
                    {'from': 147.11, 'to': 147.8, 'sid': 78, 'location': 2, 'content': '赚不了钱', 'music': 0.0},
                    {'from': 147.8, 'to': 148.88, 'sid': 79, 'location': 2, 'content': '我们就没饭吃', 'music': 0.0},
                    {'from': 148.88, 'to': 149.87, 'sid': 80, 'location': 2, 'content': '没饭吃', 'music': 0.0},
                    {'from': 149.87, 'to': 150.92, 'sid': 81, 'location': 2, 'content': '下个月吃不了', 'music': 0.0},
                    {'from': 150.92, 'to': 151.91, 'sid': 82, 'location': 2, 'content': '没白吃不了', 'music': 0.0},
                    {'from': 151.91, 'to': 153.079, 'sid': 83, 'location': 2, 'content': '所有都吃不了', 'music': 0.0},
                    {'from': 153.079, 'to': 154.279, 'sid': 84, 'location': 2, 'content': '反打的逻辑吗', 'music': 0.0},
                    {'from': 154.279, 'to': 155.059, 'sid': 85, 'location': 2, 'content': '包饭这件事情', 'music': 0.0},
                    {'from': 155.059, 'to': 157.38, 'sid': 86, 'location': 2, 'content': '最简单的前提就是要有钱才能包饭的', 'music': 0.0},
                    {'from': 157.38, 'to': 159.12, 'sid': 87, 'location': 2, 'content': '小潮院长已经攻击了他们', 'music': 0.0},
                    {'from': 159.12, 'to': 160.08, 'sid': 88, 'location': 2, 'content': '这个前提', 'music': 0.0},
                    {'from': 160.08, 'to': 161.4, 'sid': 89, 'location': 2, 'content': '当然他是内部辩论赛吗', 'music': 0.0},
                    {'from': 161.4, 'to': 162.86, 'sid': 90, 'location': 2, 'content': '你不要对脊椎那么的苛', 'music': 0.0},
                    {'from': 162.86, 'to': 165.14, 'sid': 91, 'location': 2, 'content': '我觉得老板说没钱哈哈', 'music': 0.0},
                    {'from': 165.14, 'to': 167.0, 'sid': 92, 'location': 2, 'content': '就当他真的没钱就行了', 'music': 0.0},
                    {'from': 167.0, 'to': 169.34, 'sid': 93, 'location': 2, 'content': '现在这幅大家看一下吧', 'music': 0.0},
                    {'from': 172.54, 'to': 174.0, 'sid': 94, 'location': 2, 'content': '剧本我蛮喜欢', 'music': 0.0},
                    {'from': 174.0, 'to': 176.19, 'sid': 95, 'location': 2, 'content': '其实这种表演型的片子', 'music': 0.0},
                    {'from': 176.19, 'to': 178.08, 'sid': 96, 'location': 2, 'content': '我觉得现在有的时候我们打辩论', 'music': 0.0},
                    {'from': 178.08, 'to': 181.1, 'sid': 97, 'location': 2, 'content': '有点太注重于那种文字上的交锋', 'music': 0.0},
                    {'from': 181.1, 'to': 182.36, 'sid': 98, 'location': 2, 'content': '其实你的语气', 'music': 0.0},
                    {'from': 182.36, 'to': 183.38, 'sid': 99, 'location': 2, 'content': '包括你的神经', 'music': 0.0},
                    {'from': 183.38, 'to': 185.24, 'sid': 100, 'location': 2, 'content': '包括你的一些辩论场合的状态', 'music': 0.0},
                    {'from': 185.24, 'to': 187.4, 'sid': 101, 'location': 2, 'content': '我确实也是说服的一部分了', 'music': 0.0},
                    {'from': 187.4, 'to': 191.7, 'sid': 102, 'location': 2, 'content': '剧本演呢哈哈哈哈哈哈哈', 'music': 0.0},
                    {'from': 191.7, 'to': 195.87, 'sid': 103, 'location': 2, 'content': '所以我方觉得这是一个恶性循环对', 'music': 0.0},
                    {'from': 195.87, 'to': 199.98, 'sid': 104, 'location': 2, 'content': '而且呢如果公司集体防范的话', 'music': 0.0},
                    {'from': 199.98, 'to': 202.16, 'sid': 105, 'location': 2, 'content': '首先不知道所有人都吃什么', 'music': 0.0},
                    {'from': 202.16, 'to': 203.24, 'sid': 106, 'location': 2, 'content': '喜欢吃什么', 'music': 0.0},
                    {'from': 204.32, 'to': 206.34, 'sid': 107, 'location': 2, 'content': '众口难调懂吗', 'music': 0.0},
                    {'from': 206.34, 'to': 208.56, 'sid': 108, 'location': 2, 'content': '而且你们的料我们也控制不了', 'music': 0.0},
                    {'from': 208.56, 'to': 210.24, 'sid': 109, 'location': 2, 'content': '那么如果今天我们点了东北菜', 'music': 0.0},
                    {'from': 210.24, 'to': 211.53, 'sid': 110, 'location': 2, 'content': '你们不喜欢吃', 'music': 0.0},
                    {'from': 211.53, 'to': 212.58, 'sid': 111, 'location': 2, 'content': '那怎么办呢', 'music': 0.0},
                    {'from': 212.58, 'to': 214.44, 'sid': 112, 'location': 2, 'content': '海王说的非常好', 'music': 0.0},
                    {'from': 215.36, 'to': 217.18, 'sid': 113, 'location': 2, 'content': '嗯在他们这个赛制里面', 'music': 0.0},
                    {'from': 217.18, 'to': 218.8, 'sid': 114, 'location': 2, 'content': '两个人可以这样交替发言', 'music': 0.0},
                    {'from': 218.8, 'to': 221.9, 'sid': 115, 'location': 2, 'content': '我觉得论点的整个transition做的还不错', 'music': 0.0},
                    {'from': 221.9, 'to': 223.88, 'sid': 116, 'location': 2, 'content': '从小潮院长第一个论点是没钱', 'music': 0.0},
                    {'from': 223.88, 'to': 224.96, 'sid': 117, 'location': 2, 'content': '然后他们第二个弊端', 'music': 0.0},
                    {'from': 224.96, 'to': 226.58, 'sid': 118, 'location': 2, 'content': '其实是众口难调或者浪费的', 'music': 0.0},
                    {'from': 226.58, 'to': 227.94, 'sid': 119, 'location': 2, 'content': '我觉得这个点还是不错的', 'music': 0.0},
                    {'from': 227.94, 'to': 230.1, 'sid': 120, 'location': 2, 'content': '他们那个传学生就第一次做非常有意思', 'music': 0.0},
                    {'from': 230.1, 'to': 231.0, 'sid': 121, 'location': 2, 'content': '很自然的过去', 'music': 0.0},
                    {'from': 231.0, 'to': 233.34, 'sid': 122, 'location': 2, 'content': '然后第二次就是可能是一些节目效果', 'music': 0.0},
                    {'from': 233.34, 'to': 236.02, 'sid': 123, 'location': 2, 'content': '如果我们的辩论赛也是这种很自由制度的话', 'music': 0.0},
                    {'from': 236.02, 'to': 236.62, 'sid': 124, 'location': 2, 'content': '我不知道', 'music': 0.0},
                    {'from': 236.62, 'to': 238.66, 'sid': 125, 'location': 2, 'content': '我感觉很有可能在专业辩论里面', 'music': 0.0},
                    {'from': 238.66, 'to': 241.36, 'sid': 126, 'location': 2, 'content': '百分百真男人现象就是会更加的普遍', 'music': 0.0},
                    {'from': 241.36, 'to': 244.21, 'sid': 127, 'location': 2, 'content': '我们天天如果说是东北菜', 'music': 0.0},
                    {'from': 244.21, 'to': 245.95, 'sid': 128, 'location': 2, 'content': '今天我想吃火锅', 'music': 0.0},
                    {'from': 245.95, 'to': 248.24, 'sid': 129, 'location': 2, 'content': '但是老板又给你点了东北菜', 'music': 0.0},
                    {'from': 248.24, 'to': 250.04, 'sid': 130, 'location': 2, 'content': '你能说老板点的不好吃吗', 'music': 0.0},
                    {'from': 250.04, 'to': 250.76, 'sid': 131, 'location': 2, 'content': '对呀', 'music': 0.0},
                    {'from': 250.76, 'to': 252.32, 'sid': 132, 'location': 2, 'content': '可是我天天点东北菜', 'music': 0.0},
                    {'from': 252.32, 'to': 253.4, 'sid': 133, 'location': 2, 'content': '那不吃', 'music': 0.0}
                ]
    trunres = truncateTranscript(case_subtitle)
    print("truncate ans")
    print(trunres)
    chunkres = chunkTranscript(case_subtitle)
    print("chunk ans")
    print(chunkres)
    segres = segTranscript(case_subtitle)
    print("segment ans")
    print(segres)