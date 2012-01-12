#! C:Python26python.exe
# -*- coding:utf-8 -*-

'''Unit tests for the sort.py library'''

__author__ = 'mystblue'
__version__ = '0.1-devel'

import unittest

import sort

class SortTest(unittest.TestCase):
    def testCompare(self):
        self.assertEqual(0, sort.compare("a", "a"))
        self.assertEqual(1, sort.compare("b", "a"))
        self.assertEqual(-1, sort.compare("a", "b"))
        self.assertEqual(0, sort.compare("1", "1"))
        self.assertEqual(-1, sort.compare("1", "2"))
        self.assertEqual(1, sort.compare("2", "1"))
        self.assertEqual(0, sort.compare("111", "111"))
        self.assertEqual(0, sort.compare("_", "_"))
        self.assertEqual(-1, sort.compare("!", "_"))
        self.assertEqual(-1, sort.compare("-.jpg", "1.jpg"))
        self.assertEqual(-1, sort.compare("001.jpg", "01.jpg"))
        self.assertEqual(1, sort.compare(u"001.jpg".encode("cp932"), u"_001.jpg".encode("cp932")))
        self.assertEqual(1, sort.compare(u"001.jpg".encode("cp932"), u"-001.jpg".encode("cp932")))
        self.assertEqual(1, sort.compare(u"001.jpg".encode("cp932"), u"+001.jpg".encode("cp932")))
        self.assertEqual(1, sort.compare(u"001.jpg".encode("cp932"), u"##001.jpg".encode("cp932")))
        self.assertEqual(1, sort.compare(u"001.jpg".encode("cp932"), u"^001.jpg".encode("cp932")))
        self.assertEqual(1, sort.compare(u"001.jpg".encode("cp932"), u":001.jpg".encode("cp932")))
        self.assertEqual(1, sort.compare(u"001.jpg".encode("cp932"), u"(001.jpg".encode("cp932")))
        self.assertEqual(-1, sort.compare("001.jpg", "a001.jpg"))
        
    def testSort1(self):
        file_list = ['88.txt', '5.txt', '11.txt']
        sorted_list = sort.sort(file_list)
        success_file_list = ['5.txt', '11.txt', '88.txt']
        self.assertEqual(success_file_list, sorted_list)

    def testSort2(self):
        file_list = ['Ie5', 'Ie6', 'Ie4_01', 'Ie401sp2', 'Ie4_128', 'Ie501sp2']
        sorted_list = sort.sort(file_list)
        success_file_list = ['Ie4_01', 'Ie4_128', 'Ie5', 'Ie6', 'Ie401sp2', 'Ie501sp2']
        self.assertEqual(success_file_list, sorted_list)

if __name__ == '__main__':
    unittest.main()
