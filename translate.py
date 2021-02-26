import re
from io import StringIO

#読み込む文字数の上限（適当）
limit=5000

def is_float(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return True

def translate(text):
 # 改行で分割する
    lines = text.splitlines()

    outputs = []
    output = ""

    # 除去するutf8文字
    replace_strs = [b'\x00']

    is_blank_line = False

    # 分割した行でループ
    for line in lines:

        # byte文字列に変換
        line_utf8 = line.encode('utf-8')

        # 余分な文字を除去する
        for replace_str in replace_strs:
            line_utf8 = line_utf8.replace(replace_str, b'')

        # strに戻す
        line = line_utf8.decode()


        #正規表現カスタマイズゾーン
        # "を消す
        line=line.replace('"','')
        # [ ]を消す
        line=line.replace('[','')
        line=line.replace(']','')
        # ( )を消す
        line=line.replace('(','')
        line=line.replace(')','')
        # ;を消す
        line=line.replace(';','')
        # :を消す
        line=line.replace(':','')
        



        # 連続する空白を一つにする
        line = re.sub("[ ]+", " ", line)

        # 前後の空白を除く
        line = line.strip()
        #print("aft:[" + line + "]")

        # 空行は無視
        if len(line) == 0:
            is_blank_line = True
            continue

        # 数字だけの行は無視
        if is_float(line):
            continue

        # 1単語しかなく、末尾がピリオドで終わらないものは無視
        if line.split(" ").count == 1 and not line.endswith("."):
            continue

        # 文章の切れ目の場合
        if is_blank_line or output.endswith("."):
            # 文字数がlimitを超えていたらここで一旦区切る
            if(len(output) > limit):
                outputs.append(output)
                output = ""
            #else:
                #output += "\r\n"
        #前の行からの続きの場合
        elif not is_blank_line and output.endswith("-"):
            output = output[:-1]
        #それ以外の場合は、単語の切れ目として半角空白を入れる
        else:
            output += " "

        #print("[" + str(line) + "]")
        output += str(line)
        is_blank_line = False

    outputs.append(output)
    return outputs



t=''''''

print(translate(t))