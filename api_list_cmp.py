#!/usr/bin/python
#coding:utf-8

# '''
#     数组差异化比较
# '''

#交集
def intersection(listA, listB):
    # ret = [i for i in listA if i in listB]
    ret = list(set(listA).intersection(set(listB)))
    return ret


#并集
def union(listA,listB):
    ret = list(set(listA).union(set(listB)))
    return ret


#差集
def complement(listA,listB):
    ret = list(set(listA).difference(set(listB)))
    return ret

if __name__ == '__main__':
    a = [1,2,3]
    b = [4,3,5]
    print complement(a,b)