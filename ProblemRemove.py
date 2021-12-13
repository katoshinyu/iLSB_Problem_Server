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
