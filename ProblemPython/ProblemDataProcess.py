import pandas as pd
import ProblemGenerating
import random



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
        ProblemInformation = RelationJudge(all_title, id_sub, id_Qkey)
        return ProblemInformation

def RelationJudge(all_title, id_sub, id_Qkey):

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
                                sen_part = ProblemGenerating.SentenceMake(id_sub[1][j])

                else:
                        sen_part = ProblemGenerating.SentenceMake(id_sub[1][j])

                #同じURLだった場合に用いるテキストデータをPreviousSenにキャッシュ
                PreviousSen = sen_part

                #nanのtypeが'numpy.float64', Noneのtypeが'NoneType'なため無理やり文字列にし判別
                nan_none = str(id_sub[2][j])

                if (nan_none == 'nan') or (nan_none == 'None'):
                        problem_list = ProblemGenerating.AnaumeMake(sen_part, id_sub[0][j])
                        Rekey_list = ProblemGenerating.PriorityProblem(all_title, problem_list)
                        [Finish_list, ProType] = RekeyJudge(Rekey_list)
                        ProblemInf = {"problem":Finish_list, "Answer":id_sub[0][j], "ProType":ProType}
                        ProblemList.append(ProblemInf)
                        #ProblemGenerating.OutputProblem(RekeyJudge(Rekey_list))
                        #print(RekeyJudge(Rekey_list)+"【"+id_sub[0][j]+"】")


                #包含関係に関与してる場合
                else:
                        InKey_list = InclusionJudge(id_sub[2], id_sub[0], j)

                        #展開されている課題で包含関係にあるものがあれば、格納
                        for KeyID in range(len(id_Qkey[0])):
                                if id_sub[2][j] == id_Qkey[0][KeyID]:
                                        InKey_list.append(id_Qkey[1][KeyID])

                        problem_list = ProblemGenerating.AnaumeMake(sen_part, id_sub[0][j])

                        #包含関係のあるキーワードが含まれる問題を判別
                        InKey_Problem = ProblemGenerating.PriorityProblem(InKey_list, problem_list)

                        #包含関係のキーワードが問題に含まれていた場合
                        if InKey_Problem:
                                if len(InKey_Problem) == 1:
                                        #ProblemGenerating.OutputProblem(InKey_Problem[0])
                                        ProblemInf = {"problem":InKey_Problem[0], "Answer":id_sub[0][j], "ProType":"Inclusion"}
                                        ProblemList.append(ProblemInf)
                                        #print(InKey_Problem[0]+"【"+id_sub[0][j]+"】")
                                else:
                                        Rekey_list = ProblemGenerating.PriorityProblem(all_title, InKey_Problem)
                                        [Finish_list, ProType] = RekeyJudge(Rekey_list)
                                        ProblemInf = {"problem":Finish_list, "Answer":id_sub[0][j], "ProType":ProType}
                                        ProblemList.append(ProblemInf)
                                        #ProblemGenerating.OutputProblem(RekeyJudge(Rekey_list))
                                        #print(RekeyJudge(Rekey_list)+"【"+id_sub[0][j]+"】")

                        else:
                                Rekey_list = ProblemGenerating.PriorityProblem(all_title, problem_list)
                                [Finish_list, ProType] = RekeyJudge(Rekey_list)
                                ProblemInf = {"problem":Finish_list, "Answer":id_sub[0][j], "ProType":ProType}
                                ProblemList.append(ProblemInf)
                                #ProblemGenerating.OutputProblem(RekeyJudge(Rekey_list))
                                #print(RekeyJudge(Rekey_list)+"【"+id_sub[0][j]+"】")

        #print(ProblemList)
        return ProblemList




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


def RekeyJudge(Rekey_list):
        if len(Rekey_list) > 1:
        #print(childProblem(Rekey_list))
                return ParentProblem(Rekey_list)

        elif len(Rekey_list) == 1:
        #print(Rekey_list[0])
                return [Rekey_list[0],"myRepo"]

#もう親ノードのリポジトリを使うしかない場合
def ParentProblem(problem_list):
        return [random.choice(problem_list),"parRepo"]