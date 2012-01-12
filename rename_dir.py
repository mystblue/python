# -*- coding: utf-8 -*-

import os
import re

regexs = [ur"^\(一般小説\) \[([^\]]+)\] (.+)$".encode("cp932")]

if __name__ == '__main__':
    dirs = os.listdir(".")
    for dir in dirs:
        if os.path.isdir(os.path.join(".", dir)):
            print "[" + dir + "]"
            for regex in regexs:
                if re.match(regex, dir):
                    print "match"
                    print re.sub(regex, "\\1 - \\2", dir)
                    os.rename(dir, re.sub(regex, "\\1 - \\2", dir))
