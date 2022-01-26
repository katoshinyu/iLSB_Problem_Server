import pandas as pd
import ProblemGenerating
import random

GlobalURL = ''
count = 0

URLremoeList = ["https://www3.nhk.or.jp/news/html/20220124/k10013446431000.html",
                "https://www2.nhk.or.jp/school/movie/clip.cgi?das_id=D0005311251_00000"]

reURL = list()


def ProblemProcess(mondai_json, d_type):
        GlobalURL = mondai_json
        #課題, リポジトリのキーワードの情報, 展開されている課題の情報を分ける
        df_main = mondai_json[0]
        df_sub = pd.DataFrame(mondai_json[1])
        df_Qkey = mondai_json[2]

        #初期課題以外の場合読み込む
        df_parentKey = mondai_json[3]

        #QurrentQKeyを処理にいれるための準備
        main_title = mondai_json[0]['title']

        id_URL = list()
        id_title = list()
        id_par = list()

        id_all_title = list()
        id_Qkey_KeyID = list()
        id_Qkey_title = list()
        id_Qkey = list()

        for i in range(len(df_sub)):

        #展開された課題を省く処理
                if df_sub['title'][i] in df_Qkey:
                        id_Qkey_KeyID.append(df_sub['KeywordID'][i])
                        id_Qkey_title.append(df_sub['title'][i])
                        continue

                if df_sub['URL'][i] in URLremoeList:
                        continue
                if df_sub['URL'][i] in reURL:
                        continue

                id_URL.append(df_sub['URL'][i])
                id_title.append(df_sub['title'][i])
                id_par.append(df_sub['parent'][i])

        id_sub = [id_title, id_URL, id_par]
        #親課題を含むリポジトリ群の定義
        for all_key in range(len(df_sub)):
                id_all_title.append(df_sub['title'][all_key])
        all_title = id_all_title + [main_title]
        id_Qkey.append(id_Qkey_KeyID)
        id_Qkey.append(id_Qkey_title)

        #QurrentQKeyを処理にいれる
        ProblemList = RelationJudge(all_title, id_sub, id_Qkey, df_parentKey, d_type)

        #同文一致処理
        AskText = [];
        AskAnswer = [];
        for ProNum in range(len(ProblemList)):
                nowProblem = ProblemList[ProNum]
                if not AskText:
                        AskText.append(nowProblem['problem'])
                        AskAnswer.append(nowProblem['Answer'])
                else:
                        if nowProblem['problem'] in AskText:
                                AskNum = AskText.index(nowProblem['problem'],0)
                                answerList = [];
                                if type(AskAnswer[AskNum]) == str:
                                        answerList.append(AskAnswer[AskNum])
                                else:
                                        for AskAns in AskAnswer[AskNum]:
                                                answerList.append(AskAns)
                                answerList.append(nowProblem['Answer'])
                                AskAnswer[AskNum] = answerList
                        else:
                                AskText.append(nowProblem['problem'])
                                AskAnswer.append(nowProblem['Answer'])
        ProblemList = [];
        for FiNum in range(len(AskText)):
                ProblemBrackets = BlacketsSet(AskText[FiNum], AskAnswer[FiNum])
                ProblemAnaume = AnaumeSet(AskText[FiNum], AskAnswer[FiNum])

                ProblemInf = {"Problem":ProblemBrackets, "Answer":AskAnswer[FiNum],"Anaume":ProblemAnaume}
                ProblemList.append(ProblemInf)
        #最終的な値を返す
        
        if len(ProblemList)==0:
                print('divです')
                if d_type == "div":
                        ProblemList = {"Problem":'None', "Answer":'None',"Anaume":'None'}
                        return [ProblemList]
                else:
                        d_type = "div"
                        ProblemList = ProblemProcess(mondai_json, d_type)
        if len(ProblemList)>2:
                ProblemList = random.sample(ProblemList, 2)
        random.shuffle(ProblemList)
        return ProblemList

def BlacketsSet(Text, Answer):
        if type(Answer)==str:
                Text = Text.replace(Answer, '【'+ Answer +'】')
        else:
                for ans in Answer:
                        Text = Text.replace(ans, '【'+ ans +'】')
        return Text

def AnaumeSet(Text, Answer):
        if type(Answer)==str:
                Text = Text.replace(Answer, '【　　　　】')
        else:
                for ans in Answer:
                        Text = Text.replace(ans, '【　　　　】')
        return Text


def RelationJudge(all_title, id_sub, id_Qkey, df_parentKey, d_type):

        '''id_title = id_sub[0]
        id_URL = id_sub[1]
        id_par = id_sub[2]'''

        #リストは＋を演算子として中身を追加しないと、新しいリストとして定義されない。appendとかだと変数を連携してしまう。
        #id_all_title = id_sub[0] + [main_title]
        ProblemList = list()
        #ここからURLをSentenceMakeの関数にURLを送ってテキストを引っ張ってきてもらう処理
        for j in range(len(id_sub[0])):

        #同じURLかどうかの判別処理：同じURLだったらWebスクレイピングせずすぐ穴埋め問題が生成できるように
                if j > 0:
                        if id_sub[1][j] == id_sub[1][j-1]:
                                sen_part = PreviousSen

                        else:
                                sen_part = ProblemGenerating.SentenceMake(d_type,id_sub[1][j])
                                #例外処理が出てきてしまった場合の対処
                                if sen_part == id_sub[1][j]:
                                        if not sen_part in reURL:
                                                reURL.append(sen_part)

                else:
                        sen_part = ProblemGenerating.SentenceMake(d_type,id_sub[1][j])
                        if sen_part == id_sub[1][j]:
                                if not sen_part in reURL:
                                        reURL.append(sen_part)

                #同じURLだった場合に用いるテキストデータをPreviousSenにキャッシュ
                PreviousSen = sen_part


                #nanのtypeが'numpy.float64', Noneのtypeが'NoneType'なため無理やり文字列にし判別
                nan_none = str(id_sub[2][j])

                #包含関係に関与していない場合
                if (nan_none == 'nan') or (nan_none == 'None'):
                        problem_list = ProblemGenerating.AnaumeMake(sen_part, id_sub[0][j], id_sub[1][j])

                        if problem_list != 'NoneProblem':
                                ProblemList = ProblemResult(all_title, problem_list, id_sub[0][j], df_parentKey, ProblemList)

                #包含関係に関与してる場合
                else:
                        InKey_list = InclusionJudge(id_sub[2], id_sub[0], j)

                        #展開されている課題で包含関係にあるものがあれば、格納
                        for KeyID in range(len(id_Qkey[0])):
                                if id_sub[2][j] == id_Qkey[0][KeyID]:
                                        InKey_list.append(id_Qkey[1][KeyID])

                        problem_list = ProblemGenerating.AnaumeMake(sen_part, id_sub[0][j], id_sub[1][j])
                        

                        #包含関係のあるキーワードが含まれる問題を判別
                        InKey_Problem = ProblemGenerating.PriorityProblem(InKey_list, problem_list)

                        #包含関係のキーワードが問題に含まれていた場合
                        if InKey_Problem:
                                if len(InKey_Problem) == 1:
                                        ProblemInf = {"problem":InKey_Problem[0], "Answer":id_sub[0][j]}
                                        ProblemList.append(ProblemInf)
                                else:   
                                        ProblemList = ProblemResult(all_title, InKey_Problem, id_sub[0][j],df_parentKey, ProblemList)
                                        
                        else:
                                if problem_list != 'NoneProblem':
                                        ProblemList = ProblemResult(all_title, problem_list, id_sub[0][j], df_parentKey, ProblemList)

        return ProblemList
                                
#問題作成の最終段階
def ProblemResult(all_title, problem_list, Answer, df_parentKey, ProblemList):
        Rekey_list = ProblemGenerating.PriorityProblem(all_title, problem_list)
        [Finish_list, ProType] = RekeyJudge(Rekey_list, df_parentKey)
        ProblemInf = {"problem":Finish_list, "Answer":Answer}

        ProblemList.append(ProblemInf)

        return ProblemList

#①包含関係のキーワードをリストとして引っ張ってくるための関数
def InclusionJudge(parent_list, title_list, nowID):
        InKey_list = list()
        count = 0 #parentとtitleの配列の要素を照らし合わせるためのカウンター
        for InKey in parent_list:
                if InKey == parent_list[nowID]:
                        if title_list[count] == title_list[nowID]:
                                count += 1
                                continue
                        InKey_list.append(title_list[nowID])
                        count += 1
                else:
                        count += 1

        return InKey_list

#②PriorityProblemから帰ってきた問題リストが1つかどうかで対応する関数
def RekeyJudge(Rekey_list, df_parentKey):
        if len(Rekey_list) > 1:
                return ParentJudge(Rekey_list, df_parentKey)

        elif len(Rekey_list) == 1:
                return [Rekey_list[0],"myRepo"]

#③もう親ノードのリポジトリを使うしかない場合
def ParentJudge(problem_list,df_parentKey):
        if(df_parentKey):
                Parkey_list = ProblemGenerating.PriorityProblem(df_parentKey, problem_list)
                if len(Parkey_list) == 1:
                        return [Parkey_list[0], "parRepo"]
                else:
                        return [random.choice(Parkey_list),"Random"]
        else:
                return [random.choice(problem_list),"Random"]


