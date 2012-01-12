#! C:\Python26\python.exe
# -*- coding:utf-8 -*-

## @package tools
#
# 指定したディレクトリに以下にあるディレクトリを zip に圧縮する
import os
import zipfile

SRC_DIR = "C:\\Users\\314\\Documents\\htdocs\\tw\\test\\"

## CP932 にエンコードしてコンソール出力を行う
# @param mes 出力するメッセージ
def message(mes):
	print mes.encode("cp932")

## ディレクトリの内容をチェックする
## 対象となるディレクトリを検索する
def searchDir():
	fileList = os.listdir(SRC_DIR)
	for item in fileList:
		if os.path.isdir(SRC_DIR + item):
			message("[" + item + "] を圧縮します。")
			zipCompress(SRC_DIR, item)

## ZIP 圧縮を行う
def zipCompress(path, dirName):
	# 通常の ZIP 圧縮
	parentDir = path + dirName
	zip = zipfile.ZipFile(parentDir + ".zip", 'w', zipfile.ZIP_DEFLATED)
	fileList = os.listdir(parentDir)
	for item in fileList:
		zip.write(parentDir + "\\" + item, dirName + "\\" + item)
	zip.close()

def sort():
	return True

def compare(str1, str2):
    return str1.compare(str2)

## メインの処理
def main():
	if os.path.exists(SRC_DIR):
		searchDir()
	else:
		message("指定したディレクトリが存在しません。\n-> [" + SRC_DIR + "]")

if __name__ == "__main__":
	main()
	message("終了しました。")
