# coding:utf-8
import os
import re
import sys
import time

global param_source_header_name
global param_des_header_path
global param_search_dir

param_source_header_name = ""
param_des_header_path = ""
# 搜索目录
param_search_dir = ""

global g_search_dir
global g_included_header
global g_std_headers

g_search_dir = []
g_included_header = []
g_std_headers = []


def initParam():
    global param_source_header_name
    global param_des_header_path
    global param_search_dir

    if len(sys.argv) != 4:
        print 'the number of param is wrong !'
        print '调用方式：assembler from.h to.h [searchpath1;searchpath2;...]'
        return False

    param_source_header_name = sys.argv[1]
    param_search_dir = sys.argv[2]
    param_des_header_path = sys.argv[3]

    return True


def initSearchDirs(paths):
    global g_search_dir
    print "searchd dirs ", paths
    g_search_dir = paths.split(';')
    if paths.endswith(';') or g_search_dir[-1] == "":
        g_search_dir.pop()

    for dir in g_search_dir:
        print ' 初始化搜索路径：', dir
    return


def getTimeStamp():
    return time.asctime(time.localtime(time.time()))


def saveLines(lines, path):
    global g_std_headers
    path = os.path.abspath(path)
    print ' 合并至:', path

    buf = '#pragma once \r\n\r\n'
    buf.join('// 本文件由 python  Header Assembler 自动生成，请勿手动修改\r\n')
    buf.join('// https://github.com/icexile/HeaderAssembler \r\n')
    buf.join('生成时间: ').join(getTimeStamp()).join('\r\n')

    for header in g_std_headers:
        buf.join('#include<').join(header).join('>\r\n')

    for line in lines:
        buf.join(line).join('\r\n')

    header_file = open(path, 'w')
    header_file.write(buf)

    header_file.close()

    return


# 校验文件存在并转化为绝对路径
def resolve(file_name):
    global g_search_dir

    for current_dir in g_search_dir:

        abs_current_dir = os.path.abspath(current_dir)
        findFile(abs_current_dir, file_name)
        # todo
        abs_file_path = findFile(abs_current_dir, file_name)

        if abs_file_path != 'null':
            print 'abs_file_path-->', abs_file_path
            return abs_file_path

    raise Exception("无法定位文件：", file_name)


def findFile(abs_dir, file_name):
    for root, sub_dirs, files in os.walk(abs_dir):
        for file in files:
            if file_name == file:
                return os.path.join(root, file)

    return 'null'


def assmbleHeader(file_name):
    global g_included_header
    global g_std_headers
    global g_search_dir

    if file_name not in g_included_header:  # 当不存在时

        file_path = resolve(file_name)

        print ' 读取', file_path

        once_pattern = r'=(^\s*#pragma\s*once\s*$)='
        std_header_pattern = r'=(^\s*#\s*include\s*<([.\w]+)>\s*$)='
        my_header_pattern = r'=(^\s*#\s*include\s*"([.\\/\w]+)"\s*$)='

        file = open(file_path, 'r')
        file_lines = file.readlines()
        result_lines = []

        for line in file_lines:

            if re.match(once_pattern, line):
                g_included_header.append(file_name)
            elif re.match(std_header_pattern, line):
                g_std_headers.append()
            elif re.match(my_header_pattern, line):
                g_search_dir.append(os.path.pardir(file_path))
                sub_lines = assmbleHeader()
                g_search_dir.pop()
                result_lines.extend(sub_lines)
            else:
                result_lines.append(line)
        file.close()

    return result_lines


if __name__ == '__main__':

    print ' 头文件自动合并开始'
    if initParam():
        # try:
        initSearchDirs(param_search_dir)
        lines = assmbleHeader(param_source_header_name)
        saveLines(lines, param_des_header_path)

        # except BaseException:
        #     print ' 合并文件失败'
