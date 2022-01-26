import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import ProblemDataProcess
import json

def main():
        #iLSBからの問題生成に必要な内容が記述されたjsonファイル
        jf = "ProblemResource/mondai_resource.json"

        #JSONデータを辞書型として扱えるように
        with open(jf,"r",encoding="utf-8") as mondai_txt:
                mondai_txt = mondai_txt.read()
                mondai_json = json.loads(mondai_txt)

        #辞書型データををデータ処理の関数に渡す
        ProblemInformation = ProblemDataProcess.ProblemProcess(mondai_json)
        print(ProblemInformation)
        ProblemOutPut(ProblemInformation)


#ここでの関数の処理の結果がサーバー側に渡される
def ProblemOutPut(ProblemData):
        problem_path = "ProblemResource/ProblemInformation.json"

        #答えが格納された配列をJSONデータにし、更に見やすいようにインデントを設ける
        Problem_json = json.dumps(ProblemData, ensure_ascii = False)

        with open(problem_path, 'w') as f:
                f.writelines(Problem_json)


if __name__ == "__main__":
        main()