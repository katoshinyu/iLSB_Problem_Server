import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import re
import math
import urllib.request as req
from bs4 import BeautifulSoup
import pandas as pd
import json


#文頭の接続詞を省く処理
def Setsuzoku(sen):
    re_junc = ['しかし、', 'または、', 'ほかに、', 'なお、', 'しかし','また', 'このため']

    sen_modify = list()
    for junc in re_junc:
        if junc in sen[0:5]:
            sen_modify = sen.split(junc, 1)
            sen = sen_modify[-1]

        else:
            continue

    return(sen)

#改行, 空白文字などを省く処理
def EscapeKey(sen):
    re_key = ['\r', '\n', '\t', '\u3000']
    for remove_key in re_key:
        sen_modify = list()
        sen_modify = sen.split(remove_key)
        sen = sen_modify[-1]

    return(sen)

#実際にキーワードを穴埋めにする処理
def Anaume(sen_context):
    for sen in sen_context:
            if id_title[j] in sen:
                #sen = sen.replace('\r\n','')
                sen = EscapeKey(sen)
                sen = Setsuzoku(sen)
                problem_sen = str(sen.replace(id_title[j], '（　　　）'))

                problem_list.append(problem_sen)
                answer_list.append(id_title[j])


            else:
                continue


def sen_make(URL):
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

#iLSBからの問題生成に必要な内容が記述されたjsonファイル
jf = "mondai_resource.json"

with open(jf,"r",encoding="utf-8") as a:
        #b = '['+a.read()+']'
        b = a.read()
        c = json.loads(b)

df_main = c[0]
df_sub = pd.DataFrame(c[1])
df_Qkey = c[2]

#QurrentQKeyを処理にいれるための準備
main_title = c[0]['title']

id_URL = list()
id_title = list()
id_par = list()

for i in range(len(df_sub)):

    #展開された課題を省く処理
    if df_sub['title'][i] in df_Qkey:
        continue

    id_URL.append(df_sub['URL'][i])
    id_title.append(df_sub['title'][i])
    id_par.append(df_sub['parent'][i])



#問題のリスト初期値
problem_list = list()

#答えのリスト初期設定
answer_list = list()


#リストは＋を演算子として中身を追加しないと、新しいリストとして定義されない。appendとかだと連携してしまう。
id_all_title = id_title + [main_title]

for j in range(len(id_title)):
    #print('hel')

    if j > 0:
        if id_URL[j] == id_URL[j-1]:
            sen_part = PreviousSen
        else:
            sen_part = sen_make(id_URL[j])

    else:
        sen_part = sen_make(id_URL[j])

    
    #sen_part = sen_make(id_URL[j])

    #nanのtypeが'numpy.float64', Noneのtypeが'NoneType'なため無理やり文字列にし判別
    nan_none = str(id_par[j])
    if (nan_none == 'nan') or (nan_none == 'None'):
        Anaume(sen_part)

    #包含関係に関与してる場合
    else:
        Anaume(sen_part)


    PreviousSen = sen_part

problem_path = "/Users/katoushinyu/Desktop/express-app/answer_data.json"

#答えが格納された配列をJSONデータにし、更に見やすいようにインデントを設ける
answer_json = json.dumps(answer_list, ensure_ascii=False)

with open(problem_path, 'w') as f:
    f.writelines(answer_json)

#問題文生成結果
for pro_result in problem_list:
    print(pro_result)



#print('kato')
#print(problem_json)





#print(problem_array)
