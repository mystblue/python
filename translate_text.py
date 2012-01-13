#! /usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
# クロスランゲージ翻訳サーバーでテキストを翻訳するサンプル
#----------------------------------------------------------------------

import urllib

SOAP_MES = u"<?xml version=\"1.0\" encoding=\"utf-8\"?>\
<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\
<soap:Body>\
<TranslateText xmlns=\"http://crosslanguage.co.jp/clsoap/2/schema\">\
<licence>just/just01 9a73a328fca01ff9548e512c49602126c431f19b</licenct>\
<engine>\
<eid>%(eid)s</eid>\
</engine>\
<blocks>\
<item>\
<text>%(text)s</text>\
</item>\
</blocks>\
</TranslateText></soap:Body>\
</soap:Envelope>"

def connect(eid, text):
	URL = u"http://ppp152.crosslanguage.co.jp:12000/clsoap/clsoap.cgi"
	proxies = proxies={"http": "http://www-gw:80"}

	MES = SOAP_MES % {u"eid":eid, u"text":text}
	filehandle  = urllib.urlopen(URL, MES.encode('utf-8'), proxies=proxies)
	buf = filehandle .read()
	filehandle .close()
	
	sindex = buf.find(u"<text>".encode("utf-8"))
	eindex = buf.find(u"</text>".encode("utf-8"))
	if (sindex != -1 and eindex != -1):
		return buf[sindex + 6 : eindex]
	else:
		return u""

if __name__ == "__main__":
	print connect("CR-JD", u"日本語")

def atok_plugin_run_process( a_request_data ):
	text_en = connect(u"CR-JE", a_request_data[ 'composition_string' ])
	text_ch = connect(u"CR-JC", a_request_data[ 'composition_string' ])
	text_k = connect(u"CR-JK", a_request_data[ 'composition_string' ])
	text_en = unicode(text_en, "utf-8", "ignore")
	text_ch = unicode(text_ch, "utf-8", "ignore")
	text_k = unicode(text_k, "utf-8", "ignore")

	result_data = {}

	candidate_array = []

	candidate_array.append( { 'hyoki' : text_en ,
		                        'comment' : u"英語の翻訳結果です" } )
	candidate_array.append( { 'hyoki' : text_ch ,
		                        'comment' : u"中国語の翻訳結果です" } )
	candidate_array.append( { 'hyoki' : text_k ,
		                        'comment' : u"韓国語の翻訳結果です" } )
	result_data[ 'candidate' ] = candidate_array

	return result_data
