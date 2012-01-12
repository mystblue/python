# -*- coding: utf-8 -*-

import codecs
import os
import re
import urllib2
import zipfile

SETTING_LIST = [['http://alfalfalfa.com/','<div class="main">','<div id="ad2">'],
['http://blog.livedoor.jp/samplems-bakufu/','<div class="article-body-inner">','<TABLE width="100%" cellspacing="1" border="0" cellpadding="0" bgcolor="#dfdfdf">'],
['http://morinogorira.seesaa.net/','<div class="blogbody">','<div id="article-ad"'],
['http://blog.livedoor.jp/nwknews/','<div class="article-title-outer">','<div class="related-articles">'],
['http://blog.livedoor.jp/nicovip2ch/','<h2 class="article-title entry-title">','<div id="ad2">'],
['http://rajic.2chblog.jp/','<div class="article-outer hentry">','<div id="rss-under">'],
['http://blog.livedoor.jp/insidears/','<div id="ad_rs" class="ad_rs_b">','<b><最新記事></b>'],
['http://blog.livedoor.jp/kinisoku/','<div class="article_body">','<h3>コメント</h3>'],
['http://minkch.com/','<div class="article-outer-2" style="text-align:center;">','《オススメ記事》<br />'],
['http://hamusoku.com/','<div class="article-outer hentry">','<div class="article-option" id="comments-list">'],
['http://news.2chblog.jp/','<div class="article-title-outer">','<div class="article-option" id="comments-list">'],
['http://vippers.jp/','<div id="article">','<div id="oneText">'],
['http://nantuka.blog119.fc2.com/','<!--▼ エントリー（記事）▼-->','<div class="bottom_navi">'],
['http://blog.esuteru.com/','<div id="entry">','<div class="clearfix">'],
['http://news4vip.livedoor.biz/','<div class="ently_navi_top">','<div class="related-articles">'],
['http://blog.livedoor.jp/news23vip/','<div class="article-outer hentry">','<div class="article-footer">'],
['http://neetetsu.com/','<div class="article-outer hentry">','<a name="comment-form"></a>'],
['http://nanntokasokuhou.blog.fc2.com/','<!--▼ エントリー（記事）▼-->','<!--▲ エントリー（記事）▲-->'],
['http://blog.livedoor.jp/himasoku123/','<div class="article-body entry-content">','<div class="dashed2">'],
['http://2chcopipe.com/','<div class="article-outer-3">','<div class="article-footer">'],
['http://blog.livedoor.jp/goldennews/','<div class="blogbody">','<div class="formbodytop"></div>'],
['http://yutori2ch.blog67.fc2.com/','<div class="entry">','<div class="form">'],
['http://blog.livedoor.jp/nonvip/','<div class="entry">','<h3>コメント一覧</h3>'],
['http://brow2ing.doorblog.jp/','<div class="article_title">','<div class="article_info">'],
['http://blog.livedoor.jp/negigasuki/','<div class="article-body entry-content">','<div class="article-footer">'],
['http://mudainodqnment.ldblog.jp/','<div class="article-header">','<div class="article-footer">'],
['http://chaos2ch.com/archives/','<div class="article-body entry-content">','<div class="article-footer">'],
['http://news.2chblog.jp/archives/','<div class="article-body entry-content">','<div class="article-option" id="comments-list">'],
['http://mamesoku.com/archives/','<div class="entrybody">','<div class="commentbody">'],
['http://itaishinja.com/archives/','<div class="article-body entry-content">','<div class="sbm">'],
['http://michaelsan.livedoor.biz/archives/','<div class="blogbody">','<div id="ad2"></div>'],
['http://digital-thread.com/archives/','<div class="top-contents">','<h3>コメント一覧</h3>'],
['http://jin115.com/archives/','<div class="article_header">','<div id="comment_list">'],
['http://umashika-news.jp/archives/','<div class="contents-in">','<div class="article-option" id="comment-form">'],
['http://yukkuri.livedoor.biz/archives/','<div class="article-body-more">','<!-- articleBody End -->'],
['http://lifehack2ch.livedoor.biz/archives/','<div class="posted1p">','<div id="commenttop"></div>']]

def download(url):
    u = urllib2.urlopen(url)
    with open("raw.html", "wb") as f:
        f.write(u.read())

def readText():
    with open("read.txt") as f:
        lines = f.readlines()
        for line in lines:
            items = line.rstrip().split(',')
            if len(items) == 3:
                download(items[0])
            else:
                print "設定ファイルが不正です。"

def get_encoding(filename):
    with codecs.open(filename, "r","iso-8859-1") as f:
        regex = re.compile(r"charset[ ]*=[ ]*\"?([0-9a-zA-Z|\-|_]+)\"?")
        m = regex.search(f.read())
        if m:
            return m.group(1)
        else:
            return None

def normalize1():
    encoding = get_encoding("raw.html")
    if encoding:
        with codecs.open("raw.html", "r", "utf-8") as f:
            buf = f.read()
        with open("raw.txt", "w") as f:
            f.write(buf.encode("utf-8"))
    else:
        print "エンコードが取得できません。"
        exit()

def scraping(url):
    for setting in SETTING_LIST:
        if not url.find(setting[0]) == -1:
            with codecs.open("raw.txt", "r", "utf-8") as f:
                buf = f.read()
                sindex = buf.find(setting[1])
                eindex = buf.find(setting[2])
                if sindex != -1 and eindex != -1:
                    with open("scraping.txt", "w") as fw:
                        fw.write(buf[sindex:eindex].encode("utf-8"))
                        return True
    return False

def normalize():
    with codecs.open("scraping.txt", "r", "utf-8") as f:
        buf = f.read()

        buf = buf.replace("\n", "")
        buf = buf.replace("\r", "")

        buf = re.sub("<!--((?!-->).)*-->", "", buf)
        buf = re.sub("<script((?!<\/script>).)*<\/script>", "", buf)
        buf = re.sub("<noscript((?!<\/noscript>).)*<\/noscript>", "", buf)

        buf = re.sub(re.compile("<h2[^>]*>", re.I), "", buf)
        buf = re.sub(re.compile("</h2>", re.I), "", buf)

        buf = re.sub(re.compile("<div[^>]*>", re.I), "", buf)
        buf = re.sub(re.compile("<\/div>", re.I), "", buf)
        buf = re.sub(re.compile("<span[^>]*>", re.I), "", buf)
        buf = re.sub(re.compile("</span>", re.I), "", buf)
        buf = re.sub(re.compile("<font[^>]*>", re.I), "", buf)
        buf = re.sub(re.compile("</font>", re.I), "", buf)
        buf = re.sub(re.compile("<b[^>r][^>]*>", re.I), "", buf)
        buf = re.sub(re.compile("<b>", re.I), "", buf)
        buf = re.sub(re.compile("</b>", re.I), "", buf)
        buf = re.sub(re.compile("<p[^>a][^>]*>", re.I), "", buf)
        buf = re.sub(re.compile("</p>", re.I), "", buf)
        buf = re.sub(re.compile("<u[^>]*>", re.I), "", buf)
        buf = re.sub(re.compile("</u>", re.I), "", buf)
        
        buf = re.sub(re.compile("<dl[^>]*>", re.I), "", buf)
        buf = re.sub(re.compile("<dd[^>]*>", re.I), "\r\n", buf)
        buf = re.sub(re.compile("<dt>", re.I), "\r\n", buf)
        buf = re.sub(re.compile("</dl>", re.I), "", buf)
        buf = re.sub(re.compile("</dd>", re.I), "", buf)
        buf = re.sub(re.compile("</dt>", re.I), "", buf)

        buf = re.sub(re.compile("<a name=\"more\"></a>", re.I), "", buf)

        buf = buf.replace("&lt;", "<")
        buf = buf.replace("&gt;", ">")
        buf = buf.replace("&nbsp;", " ")

        buf = re.sub(re.compile("<br>", re.I), "\n", buf)
        buf = re.sub(re.compile("<br/>", re.I), "\n", buf)
        buf = re.sub(re.compile("<br />", re.I), "\n", buf)

        buf = re.sub(re.compile('<img [^\/>]*src="?([^ "]+)"?[^\/>]*\/?>', re.I), '<img src="\\1">', buf)
        buf = re.sub(re.compile('<a [^\/>]*href="?([^ "]+)"?[^\/>]*\/?>', re.I), '<a href="\\1">', buf)
        buf = re.sub(re.compile('<a [^>]*(?!href)[^>]*>([^<]+)<\/a>', re.I), '\\1', buf)
        buf = buf.replace("</A>", "</a>")

#	buf = buf.replace("&#9833;", "♩")
#	buf = buf.replace("&hellip;", "…")

        buf = re.sub(re.compile("^\t+", re.M), "", buf)

        buf = re.sub(re.compile("^[ ]+", re.M), "", buf)

        buf = re.sub("\t+\n2", "", buf)

        buf = re.sub("\n{2,}", "\r\n\r\n", buf)

        with open("result.txt", "wb") as f:
            f.write(buf.encode("utf-8"))

def get_img_list():
    ilist = []
    with codecs.open("result.txt", "r", "utf-8") as f:
        buf = f.read()
        l = re.findall(r"<img src=\"([^\"]+(.je?pg|.png|.gif|.bmp))\">", buf)
        for i in l:
            ilist.append(i[0])
    return ilist

def download(ary):
    for url in ary:
        filename = url[url.rfind("/") + 1:]
        u = urllib2.urlopen(url)
        with open(os.path.join("img", filename), "wb") as f:
            f.write(u.read())

def down_img():
    if not os.path.exists("img"):
        os.mkdir("img")
    download(get_img_list())

def rewrite_path():
    with codecs.open("result.txt", "r", "utf-8") as f:
        buf = f.read()
        buf = re.sub(r"<img src=\".+/([^/]+(.jpe?g|.gif|.png|.bmp))\">", "<img src=\"\\1\">", buf)
        with open(os.path.join("img", "result.txt"), "w") as fw:
            fw.write(buf.encode("utf-8"))

def zip_archive():
    zip = zipfile.ZipFile(u"2011-12-12 キャバ嬢に人生初の逆ナンされた".encode("cp932") + u".zip".encode("cp932"), 'w', zipfile.ZIP_DEFLATED)
    for file in os.listdir("img"):
        zip.write(os.path.join("img", file), file)
    zip.close()
    
if __name__ == '__main__':
#    readText()
#    normalize1()
#    scraping("http://blog.livedoor.jp/nicovip2ch/archives/1731140.html")
#    normalize()
#    down_img()
#    rewrite_path()
    zip_archive()
