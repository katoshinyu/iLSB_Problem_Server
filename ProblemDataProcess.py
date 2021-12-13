import pandas as pd
import ProblemGenerating


def ProblemProcess(mondai_json):

        #課題, リポジトリのキーワードの情報, 展開されている課題の情報を分ける
        df_main = mondai_json[0]
        df_sub = pd.DataFrame(mondai_json[1])
        df_Qkey = mondai_json[2]

        #QurrentQKeyを処理にいれるための準備
        main_title = mondai_json[0]['title']

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

        id_sub = [id_title, id_URL, id_par]

        #QurrentQKeyを処理にいれる
        RelationJudge(df_main['title'], id_sub)

def RelationJudge(main_title, id_sub):

        '''id_title = id_sub[0]
        id_URL = id_sub[1]
        id_par = id_sub[2]'''

        #リストは＋を演算子として中身を追加しないと、新しいリストとして定義されない。appendとかだと変数を連携してしまう。
        id_all_title = id_sub[0] + [main_title]

        #ここからURLをSentenceMakeの関数にURLを送ってテキストを引っ張ってきてもらう処理
        for j in range(len(id_sub[0])):

        #同じURLかどうかの判別処理：同じURLだったらWebスクレイピングせずすぐ穴埋め問題が生成できるように
                if j > 0:
                        if id_sub[1][j] == id_sub[1][j-1]:
                                sen_part = PreviousSen

                        else:
                                sen_part = ProblemGenerating.SentenceMake(id_sub[1][j])

                else:
                        sen_part = ProblemGenerating.SentenceMake(id_sub[1][j])

                #同じURLだった場合に用いるテキストデータをPreviousSenにキャッシュ
                PreviousSen = sen_part

                #nanのtypeが'numpy.float64', Noneのtypeが'NoneType'なため無理やり文字列にし判別
                nan_none = str(id_sub[2][j])

                if (nan_none == 'nan') or (nan_none == 'None'):
                        RelationNotInclude(sen_part, id_sub[0][j])

                #包含関係に関与してる場合
                else:
                        RelationInclude(sen_part, id_sub[0][j])

def RelationInclude(sen_part, AnaumeWord):
        ProblemGenerating.AnaumeMake(sen_part, AnaumeWord)

def RelationNotInclude(sen_part, AnaumeWord):
        ProblemGenerating.AnaumeMake(sen_part, AnaumeWord)




