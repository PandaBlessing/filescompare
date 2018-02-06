#!/usr/bin/python
#coding:utf-8

import xlwt
import xlrd
import os
import api_checkfile
import api_list_cmp as listcmp


class ExcelOperation(object):
    def __init__(self):
        pass
    def write(self,path,file,path2):
        self.path = path
        self.file = file
        book = xlwt.Workbook(encoding='utf-8',style_compression=0)
        sheet = book.add_sheet('test',cell_overwrite_ok=True)
        sheet.write(0,0,'key')
        sheet.write(0,1,'value')
        if path2:
            sheet.write(0, 2, 'key')
            sheet.write(0, 3, 'value')

        for idx,item in enumerate(file):
            sheet.write(idx + 1,0,item[0])
            sheet.write(idx + 1, 1, item[1])
            if path2:
                sheet.write(idx + 1, 2, item[2])
                sheet.write(idx + 1, 3, item[3])

        print u'写入完成！！！'

        book.save(self.path)
        print u'保存成功' + path

    def read(self,path,path2 = False):
        self.path = path
        self.path2 = path2
        book = xlrd.open_workbook(path)
        sheet0 = book.sheet_by_index(0)
        sheet_name = book.sheet_names()[0]
        sheet1 = book.sheet_by_name(sheet_name)
        nrows = sheet0.nrows
        ncols = sheet0.ncols

        #判断取出数据的位置
        idxArr = []
        if path2:
            idxArr.append(2)
            idxArr.append(3)
        else:
            idxArr.append(0)
            idxArr.append(1)

        arr = []
        for i in range(nrows - 1):
            cell_value1 = sheet0.cell_value(i + 1,idxArr[0])
            cell_value2 = sheet0.cell_value(i + 1, idxArr[1])
            kvArr = []
            kvArr.append(cell_value1)
            kvArr.append(cell_value2)
            arr.append(kvArr)

        print u'提取成功'
        arr.sort(key=lambda list1: list1[0])
        print u'完成排序'
        str = api_checkfile.getJsonStr(arr)
        return str


#写入方法
def write(path1,path2):
    lngArr = api_checkfile.getStrArr(path1)
    #拿到lng中的所有key
    keysArr = []
    for kvArr in lngArr:
        keysArr.append(kvArr[0])

    # arr = [] + lngArr
    arr = []
    #如果第二个比较文件存在
    if path2:
        lng2Arr = api_checkfile.getStrArr(path2)
        #拿到lng2中的所有key
        keys2Arr = []
        for kvArr in lng2Arr:
            keys2Arr.append(kvArr[0])
        #遍历lng1，判断是否在lng2中，如果在，key缓存到一个数组中
        commonArr = []
        for kvArr in lngArr:
            key = kvArr[0]
            lngIdx = keysArr.index(key)
            if key in keys2Arr:
                lng2Idx = keys2Arr.index(key)
                commonArr.append(key)
                #放入新数组中
                needArr = []
                needArr.append(key)
                needArr.append(lngArr[keysArr.index(key)][1])
                needArr.append(key)
                needArr.append(lng2Arr[keys2Arr.index(key)][1])
                arr.append(needArr)

            #     arr[lngIdx].append(key)
            #     arr[lngIdx].append(lng2Arr[lng2Idx][1])
            # else:
            #     #lng2中不存在的kv使用空字符串代替
            #     arr[lngIdx].append('')
            #     arr[lngIdx].append('')

        #两个数组中，不相同的补充在arr数组的最后面
        lngDiff = listcmp.complement(keysArr, commonArr)
        lng2Diff = listcmp.complement(keys2Arr, commonArr)
        # print lngDiff
        # print lng2Diff

        for key in lng2Diff:
            needArr = []
            needArr.append(key)
            needArr.append('')
            needArr.append(key)
            needArr.append(lng2Arr[keys2Arr.index(key)][1])
            arr.insert(0, needArr)

        for key in lngDiff:
            needArr = []
            needArr.append(key)
            needArr.append(lngArr[keysArr.index(key)][1])
            needArr.append(key)
            needArr.append('')
            arr.insert(0, needArr)
    else:
        arr = [] + lngArr
    #操作文件，进行写入操作
    excelOp = ExcelOperation()
    excelOp.write(r'./lng.xls', arr,path2)


def readAndBuildJson(path1, path2):
    excelOp = ExcelOperation()
    str = excelOp.read(path1, path2)
    api_checkfile.buildJson(str)


def main(path1,path2):
    # write(path1,path2)

    # readAndBuildJson(r'./lng.xls',True)
    input()


def input():
    inputType = raw_input(u'请选择：\n1、导入js（最后会生成xls文件）\n2、导出json文件（当前目录下必须有lng.xls文件）\n')
    path2 = False
    if inputType == '1':
        path1 = raw_input(u'请输入第一个js的路径（必须输入）\n')
        path2 = raw_input(u'输入第二个js路径,如果不需要请输入2\n')
        if path2 == '2':
            path2 = False

        write(path1, path2)
    elif inputType == '2':
        path2 = raw_input(u'如果需要导出xls的第3、4列，请输入1\n否则请输入2\n')
        if path2 == '1':
            path2 = True
        elif path2 == '2':
            path2 = False

        readAndBuildJson(r'./lng.xls', path2)
    else:
        print u'请输入正确的序号！'
        input()

if __name__ == '__main__':
    # main(r'./_lng.js', r'./_lng2.js')
    input()
