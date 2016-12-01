# coding:utf-8
import sys

if __name__ == '__main__':

    print "script name :", sys.argv[0]
    for i in range(1, len(sys.argv)):
        print "param ", i, "is", sys.argv[i]
