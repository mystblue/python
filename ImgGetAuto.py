#! C:\Python26\python.exe
# -*- coding:utf-8 -*-

"""
画像を全自動で取得するツール

■使い方
1. url.txt を作成する。
	url.txt のエンコードは、Shift_JIS。
	一行に「URL,出力するフォルダ名,画像の数」を記述する。
	フォルダ名は、日本語でもOK。
2. 「python ImgGetAuto.py」を実行する。

■処理の流れ
1. ダウンロード定義ファイル「url.txt」から情報を読み込む
2. URL を読み込んで、html の中身を取得する
3. 取得した html は、「data.html」として保存
4. html の中身から、画像の URL を抽出する
5. 画像の URL の数と正解数が一致すれば、6 へ。一致しない場合は処理を終了する。
6. 画像の URL から画像を取得し、指定したフォルダに可能する
7. 画像をまとめた ZIP ファイルを作成する

■実装予定機能
・複数の URL を設定できるようにする
・ダウンロードした URL などの情報を管理できるようにする

■更新履歴
0.1-devel
	・新規作成
"""

__author__ = 'mystblue'
__version__ = '0.1-devel'

import os
import re
import urllib2
import zipfile

class ZipArchive:
	# Zip に追加しないファイル名のリスト
	ExcludeFileName = ["data.html"]

	# ダウンロードから除外する拡張子
	ExcludeExtention = ["htm", "html", "txt"]

	def __message(self, str):
		'''コンソールに Shift_JIS に変換して出力する'''
		print str

	def __filter(self, folderName, fileName):
		'''Zip に追加するファイルのフィルタリングを行う'''
		# 特定のファイル名を除外
		for fn in self.ExcludeFileName:
			if fn == fileName:
				return False
		# 特定の拡張子を持つファイルを除外
		for ext in self.ExcludeExtention:
			if fileName.endswith(ext):
				return False
		return True

	def __createZipFile(self, folderName):
		'''Zip ファイルを作成する'''
		self.__message(folderName + u".zip を作成しています。".encode("cp932"))
		zip = zipfile.ZipFile(folderName + ".zip", 'w', zipfile.ZIP_DEFLATED)
		fileList = os.listdir(folderName)
		for item in fileList:
			if self.__filter(folderName, item):
				zip.write(os.path.join(folderName, item), os.path.join(folderName, item))
		zip.close()

	def __removeFiles(self, folderName):
		'''zip に固めたファイルを削除する'''
		fileList = os.listdir(folderName)
		for item in fileList:
			if self.__filter(folderName, item):
				os.remove(os.path.join(folderName, item))

	def compress(self, folderName):
		'''指定したフォルダを Zip 圧縮する'''
		if os.path.exists(folderName + u".zip".encode("cp932")):
			self.__message(folderName + u".zipはすでに存在します。処理をスキップします。".encode("cp932"))
			pass
		else:
			self.__createZipFile(folderName)
			self.__removeFiles(folderName)


#class BakufuDownloader(GeneralDownloader):
#	def __init__(self):
#		pattern = ""

class GeneralDownloader:
	# ダウンロード対象の URL
	__url = ""
	# ダウンロードするフォルダ
	__folderName = "."
	# 正解数
	__number = 0
	# URL を抽出するための正規表現
	__pattern = "href=\"?([^ \"]+)\"?[ >]"
	# バッファ
	__buf = ""
	# 文字コード
	__coding = ""
	# カウンタ
	__counter = 0
	__dlList = []
	__dlFailCount = 0

	def setURL(self, url):
		self.__url = url

	def setFolderName(self, folderName):
		self.__folderName = folderName

	def setNumber(self, number):
		self.__number = number

	def setCoding(self, coding):
		self.__coding = coding

	def __message(self, str):
		print str.encode("cp932")

	def __getHtml(self):
		'''URL から html を抽出する'''
		try:
			f = urllib2.urlopen(self.__url)
			return f.read()
		except Exception, e:
			self.__message(u"URL にアクセスするときに例外が発生しました。")
			raise e

	def __saveHtml(self):
		if not os.path.exists(self.__folderName):
			os.mkdir(self.__folderName)
		fw = file(os.path.join(self.__folderName, "data.html"), 'wb')
		fw.write(self.__buf)
		fw.close()

	def __getFileName(self, url):
		'''URL からファイル名を抽出する'''
		index = url.rfind('/')
		fileName = url[index + 1:]
		return fileName

	def __isFile(self, fileName):
		'''ファイルかどうか'''
		if fileName == "":
			return False
		if fileName.find('.') == -1:
			return False
		if not ( fileName.endswith(".jpg") or fileName.endswith(".png")):
			return False
		return True

	def __accepts(self, url):
		# ファイルならば受け入れる
		if self.__isFile(self.__getFileName(url)):
			return True
		else:
			return False

	def __normalizeURL(self, url):
		'''URL の末尾についた ? 以降を取り除く'''
		index = url.find('?')
		if index != -1:
			url = url[:index]
		return url
  
	def __createImageList(self):
		# MULTILINE モードで検索
		pattern = re.compile(self.__pattern)
		match = pattern.findall(self.__buf)
		listStr = ""
		if match:
			self.__counter = 0
			for url in match:
				url = self.__normalizeURL(url)
				if self.__accepts(url):
					self.__counter = self.__counter + 1
					listStr += url + '\n'
					self.__dlList.append(url)
			self.__message(repr(self.__counter) + u"個の URL が見つかりました。")
		else:
			self.__message(u"data.html の中から、URL が見つかりませんでした。")
		fw = file(os.path.join(self.__folderName, "ImageList.txt"), 'w')
		fw.write(listStr)
		fw.close()

	def __checkNum(self):
		if self.__number != 0:
			if self.__counter == self.__number:
				self.__message(u"[○]数が一致しています。")
				self.__download()
				return True
			if self.__counter == self.__number + 1:
				self.__message(u"[△]取得された URL がひとつ多いですが、実行します。")
				self.__download()
				return True
			else:
				self.__message(u"[×]数が一致してません。\n正解は" + repr(self.__number) + u"ですが、取得できた URL は" + repr(self.__counter) + u"です。")
				return False

	def __downloadImg(self, url):
		'''指定した URL の画像をダウンロードする'''
		self.__message(url + u"を処理しています。")
		try:
			f = urllib2.urlopen(url)
			fw = file(os.path.join(self.__folderName, self.__getFileName(url)), 'wb')
			fw.write(f.read())
			fw.close()

		except Exception, e:
			self.__dlFailCount = self.__dlFailCount + 1
			self.__message(url + u"のダウンロードに失敗しました。")

	def __download(self):
		for url in self.__dlList:
			self.__downloadImg(url)
		if self.__dlFailCount != 0:
			self.__message(repr(self.__dlFailCount) + u"件のダウンロードに失敗しました。")
		else:
			self.__message(u"正常に終了しました。")
			self.__zipCompress()

	def __zipCompress(self):
			zip = ZipArchive()
			zip.compress(self.__folderName)
	  
	def run(self):
		self.__buf = self.__getHtml()
		self.__saveHtml()
		self.__createImageList()
		return self.__checkNum()

class DownloadDispatcher:

	__TABLE = {"http://blog.livedoor.jp/samplems-bakufu/":GeneralDownloader()}

	def dispatch(self, url):
		return GeneralDownloader()

class ImgGetApp:
	'''画像取得アプリケーション'''
	DL_LIST_FILE = u"download.txt"
	DLD_LIST_FILE = u"downloaded.txt"

	__dlList = []

	__failList = []

	def __execute(self, url, folderName, number):
		dlr = GeneralDownloader()
		dlr.setURL(url)
		dlr.setNumber(number)
		dlr.setFolderName(folderName)
		return dlr.run()

	def __parse(self, line):
		findex = line.find(',')
		ret = []
		if findex == -1:
			return
		ret.append(line[:findex])
		sindex = line.find(',', findex + 1)
		if sindex == -1:
			return
		ret.append(line[findex + 1 : sindex])
		ret.append(line[sindex + 1 :])
		return ret

	def __processList(self):
		for line in self.__dlList:
			params = self.__parse(line)
			if params:
				ret = self.__execute(params[0], params[1], int(params[2]))
				if ret:
					self.__writeSuccess(line)
				else:
					self.__failList.append(line)
			else:
				self.__failList.append(line)

	def __loadFile(self):
		'''定義ファイルを読み込む'''
		fr = file(self.DL_LIST_FILE, 'r')
		buf = fr.read()
		fr.close()
		lines = buf.split('\n')
		for line in lines:
			if line != "":
				self.__dlList.append(line)

	def __writeSuccess(self, line):
		'''成功したものをログに追記する'''
		fa = file(self.DLD_LIST_FILE, 'a')
		buf = line + '\n'
		fa.write(buf)
		fa.close()

	def __writeFail(self):
		'''失敗したものをログに書きだす'''
		fw = file(self.DL_LIST_FILE, 'w')
		buf = ""
		for line in self.__failList:
			buf += line + '\n'
		fw.write(buf)
		fw.close()

	def __outputFail():
		for line in self.__failList:
			print u"Fail > " + line
		
	def run(self):
		'''実行する'''
		self.__loadFile()
		self.__processList()
		self.__outputFail()
		self.__writeFail()

if __name__ == "__main__":
	app = ImgGetApp()
	app.run()
