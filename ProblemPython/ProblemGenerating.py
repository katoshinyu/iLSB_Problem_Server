import re
import urllib.request as req
from bs4 import BeautifulSoup
import ProblemRemove
import ProblemRevenge
import json
import csv

from urllib.error import HTTPError
from urllib.error import URLError
from http.client import RemoteDisconnected



#答えのリスト初期設定
answer_list = list()

def SentenceMake(type,URL):
    # urlopen()でデータを取得
    try:
        res = req.urlopen(URL)
    except HTTPError as err:
        print(err)
        return URL
    except URLError as err:
        print(err)
        return URL
    except RemoteDisconnected:
        print('error!')
        return URL

    # BeautifulSoup()で解析
    # ここさえクリアすれば、後は時間はかからない
    soup = BeautifulSoup(res, 'html.parser')

    # pでくくられているところを抽出し、一塊ごと、配列に格納していく
    p_list = soup.find_all(type)

    p_join = ''

    # 上記で抽出したPの塊[0]...[p_list]をLoopで取り出してくる, そして結合

    for p in p_list:
        p_join += p.get_text()

    # 「。」で区切って、「。」を最後にくっつける
    return (re.findall(r'[^。]+(?:[。]|$)', p_join))



    #実際にキーワードを穴埋めにする処理
def AnaumeMake(sen_list, AnaumeWord, URL):
    #問題のリスト初期値
    problem_list = list()

    for sen in range(len(sen_list)):
        if AnaumeWord in sen_list[sen]:

            #変な問題を生成しないためにまずフィルターをかける
            sen_problem = ProblemRemove.EscapeKey(sen_list[sen])
            #sen = ProblemRemove.Setsuzoku(sen)
            #タイトルとかで穴埋めキーワードが用いられ、フィルターをかけて消えてしまった場合の対処
            if not AnaumeWord in sen_problem:
                sen_problem = sen_list[sen]
            #フィルターをかけ終わったらあとは穴埋めにするだけ
            problem_sen = sen_problem
            '''if (sen !=0) and (sen != len(sen_list)-1):
                problem_sen = sen_list[sen-1] + problem_sen + sen_list[sen+1]'''
            #problem_pro = '{' + 'PROBLEM:' + '"' + problem_sen  + '"' +',' + 'ANSWER:'+ '"' + AnaumeWord +  '"' +'}'

            problem_list.append(problem_sen)
            answer_list.append(AnaumeWord)


    if(problem_list == []):
        problem_list = NonProblemProcess("div", URL)

    return problem_list

#pタグで問題が生成, 出来なかった場合の処理
def NonProblemProcess(type, URL):
    
    return 'NoneProblem'


#キーワードレポジトリのキーワードがどれくらい含まれているかを判別する関数（包含関係もこの関数で判断）
def PriorityProblem(ReKey_list, problem_list):

    Max_problem = list()
    Max_judge = 0

    for sen in problem_list:
        Key_num = 0
        for ReKey in ReKey_list:
            if ReKey in sen:
                Key_num += 1

        if Max_judge < Key_num:
            Max_problem = list()
            Max_judge = Key_num
            Max_problem.append(sen)

        elif Max_judge == Key_num:
            Max_problem.append(sen)

    if Max_judge > 0:
        return Max_problem
    else:
        return problem_list

