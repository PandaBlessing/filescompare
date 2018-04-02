#!usr/bin/python
#coding:utf-8

import os
import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#全局变量
#左侧显示的kv数组信息
STR_ARR_LEFT = []
#右侧显示的kv数组信息
STR_ARR_RIGHT = []
#保存一些异常的数据
STR_ARR_UNNORMAL = []

# 获得json文件内容
def get_json(path):
    str = ''
    with open(path, 'r') as f:
        str += f.read()
        f.close()
    # print str
    return str

#获得指定的匹配内容
def getMatchArr(str = ''):
    matchStr = ''
    startStr = '{{'
    endStr = '}}'

    matchStr = str[(str.index(startStr) + len(startStr)):str.index(endStr)]

    strArr = matchStr.split(',')
    arr = []
    for sstr in strArr:
        # 空字符串直接过滤掉
        if sstr.isspace():
            continue
        #字符串前后的空格、换行
        arr.append(sstr.strip())

    # arr.sort()
    #数组中字符串的key和value转化成标准的双引号格式
    kvStrArr = []
    for kvStr in arr:
        kvArr = kvStr.split(':')

        #因为某种原因，分割字符串的时候导致数组中只有一个元素，需要先隔离掉，后面再做处理
        global STR_ARR_UNNORMAL
        if len(kvArr) == 1:
            STR_ARR_UNNORMAL.append(kvArr[0])
            continue

        #去除字符串前后的空格
        kvArr[0] = kvArr[0].strip()
        kvArr[1] = kvArr[1].strip()
        #去除字符串中因为随意拼写而引入的单引号和双引号，统一掉
        newStr = ''
        for ss in kvArr[0]:
            if ss == '\'' or ss == '\"':
                continue
            newStr += ss
        kvArr[0] = newStr

        kvStrArr.append(kvArr)

    #对数组进行默认排序，参数为排序方法
    kvStrArr.sort(key=lambda list1: list1[0])
    global STR_ARR_LEFT
    STR_ARR_LEFT += kvStrArr
    return kvStrArr

#获得新的json字符串
def getJsonStr(arr = []):
    sstr = '{' + '\n'
    for kvArr in arr:
        vStr = kvArr[1]
        vStr = vStr.strip();
        if vStr.startswith('\''):
            vStr = '\"' + vStr + '\"'
        vStr = vStr.replace('\"\'','\"')
        vStr = vStr.replace('\'\"','\"')
        sstr += '\t' + '\"' + kvArr[0] + '\"' + ':' + vStr + ',\n'
    sstr = sstr.rstrip()
    sstr = sstr.rstrip(',')
    sstr += '\n}'
    return sstr


#将字符串写入json文件中
def buildJson(sstr):
    with open(r'./lng.json', 'wb') as f:
        f.write(sstr)
        f.close()
        print '操作成功！！！！'
        for sstr in STR_ARR_UNNORMAL:
            print sstr


def getStrArr(path):
    print u'开始解析。。。' + path
    str = get_json(path)
    # exeJs(str)
    arr = getMatchArr(str)
    print u'解析完成！！！'
    return arr

#######调试信息##########
# if __name__ == '__main__':
#     print '开始解析。。。'
#     str = get_js(r'./_lng.js')
#     # exeJs(str)
#     arr = getMatchArr(str)
#     jsonStr = getJsonStr(arr)
#     buildJson(jsonStr)
