# filescompare
这是一个方便语言包文件本地化和对比差异的项目代码
#如果生成exe文件出现乱码
打开api_checkfile_excel.py，使用了raw_input方法的汉字后面添加.decode('utf-8').encode('gbk)。就可以解决问题了
