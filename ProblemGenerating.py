import re
import urllib.request as req
from bs4 import BeautifulSoup
import ProblemRemove
import json

def SentenceMake(URL):
    # urlopen()でデータを取得
    res = req.urlopen(URL)

    # BeautifulSoup()で解析
    soup = BeautifulSoup(res, 'html.parser')

    # pでくくられているところを抽出し、一塊ごと、配列に格納していく
    p_list = soup.find_all("p")

    p_join = ''

    # 上記で抽出したPの塊[0]...[p_list]をLoopで取り出してくる, そして結合

    for p in p_list:
        p_join += p.get_text()

    # 「。」で区切って、「。」を最後にくっつける
    return (re.findall(r'[^。]+(?:[。]|$)', p_join))


    #実際にキーワードを穴埋めにする処理
def AnaumeMake(sen_list, AnaumeWord):
    #問題のリスト初期値
    problem_list = list()

    #答えのリスト初期設定
    answer_list = list()

    for sen in sen_list:
        if AnaumeWord in sen:

            #変な問題を生成しないためにまずフィルターをかける
            sen = ProblemRemove.EscapeKey(sen)
            sen = ProblemRemove.Setsuzoku(sen)

            #フィルターをかけ終わったらあとは穴埋めにするだけ
            problem_sen = str(sen.replace(AnaumeWord, '（　　　）'))

            problem_list.append(problem_sen)
            answer_list.append(AnaumeWord)


        else:
            continue

    ProblemOutPut(problem_list, answer_list)

#ここでの関数の処理の結果がサーバー側に渡される
def ProblemOutPut(ProblemData, AnswerData):
    problem_path = "ProblemResource/answer_data.json"

    #答えが格納された配列をJSONデータにし、更に見やすいようにインデントを設ける
    answer_json = json.dumps(AnswerData, ensure_ascii=False)

    with open(problem_path, 'w') as f:
            f.writelines(answer_json)

    #問題文生成結果
    for pro_result in ProblemData:
            print(pro_result)