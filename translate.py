import re
from io import StringIO

limit=10000

def is_float(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return True

def trans(text):

    text = re.sub("\(.+?\)", "", text)

    # 改行で分割する
    lines = text.splitlines()

    outputs = ""
    output = ""

    # 除去するutf8文字
    replace_strs = [b'\x00']

    is_blank_line = False

    # 分割した行でループ
    for line in lines:

        line= re.sub("e\.g\.", "", line)
        # ()を消す
        line = re.sub("\(.+?\)", "", line)

        # byte文字列に変換
        line_utf8 = line.encode('utf-8')

        # 余分な文字を除去する
        for replace_str in replace_strs:
            line_utf8 = line_utf8.replace(replace_str, b'')

        # strに戻す
        line = line_utf8.decode()
        
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
            
        # ピリオドで改行
        line = line.replace('.','.\n')

        # 文章の切れ目の場合
        if is_blank_line or output.endswith("."):
            # 文字数がlimitを超えていたらここで一旦区切る
            if(len(output) > limit):
                outputs.append(output)
                output = ""
            #else:
                #output += "\r."

        #前の行からの続きの場合
        elif not is_blank_line and output.endswith("-"):
            output = output[:-1]
        #それ以外の場合は、単語の切れ目として半角空白を入れる
        else:
            output += " "

        output += str(line)
        is_blank_line = False

    outputs += output
    
    # ()を中身ごと消す
    outputs = re.sub("\(.+?\)", "", outputs)
    
    return outputs

t='''Conditional statements are ubiquitous in both ordinary and scientific discourse. They
are used for many purposes, from laying down rules for guiding behaviour to expressing
scientific hypotheses (Evans & Over, 2004). One basic use of conditionals is to express
uncertainty. We are unsure about the weather, and so we say that we will have an alfresco
lunch if it is sunny. We are unconvinced by our colleagues’ arguments, but conclude that
their theory will be confirmed if there is a significant result in an experiment. Uncertainty
is always with us in human affairs, and indicative conditionals are of great importance for
this reason alone. It is unsurprising that so much research has been done on them since the
ancient Greeks (Sanford, 1989).
Though people often use a conditional to express uncertainty, they can of course be
uncertain about the conditional itself. They can have high or low confidence in it, judging
it to have high or low probability. For a Saturday in the summer, our friends can be fairly
confident that, if it is sunny, we will have an alfresco lunch. Our colleagues would be less
confident that, if we are given a deadline for finishing our marking, then we will meet it.'''

print(trans(t))