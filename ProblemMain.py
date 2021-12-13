import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import ProblemDataProcess
import json

#iLSBからの問題生成に必要な内容が記述されたjsonファイル
jf = "ProblemResource/mondai_resource.json"

#JSONデータを辞書型として扱えるように
with open(jf,"r",encoding="utf-8") as mondai_txt:
        mondai_txt = mondai_txt.read()
        mondai_json = json.loads(mondai_txt)

#辞書型データををデータ処理の関数に渡す
ProblemDataProcess.ProblemProcess(mondai_json)
