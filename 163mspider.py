# -*-coding:utf-8-*-
import webbrowser
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
from urllib.request import urlretrieve, build_opener, install_opener
import requests
import os

head={
    'Referer':'https://music.163.com/',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 QQBrowser/10.4.3587.400'
}
def fail():
    list.insert(END,'无效ID,下载失败！')
    list.see(END)
    list.update()
def downloadsongs():
    ssid=entry.get()
    if count.get()=='':
        fail()
        return
    cnt=int(count.get())
    j=0
    idurl='https://music.163.com/playlist'
    key={'id':str(ssid)}
    res=requests.get(idurl,params=key,headers=head).text
    music_dict={}
    r=BeautifulSoup(res,'html.parser')
    result=r.find('ul',{'class','f-hide'}).find_all('a')
    if sys.getsizeof(result)==80:
        fail()
        return
    i=1
    for music in result:
        if i>cnt:
            break
        music_id=music.get('href').strip('/song?id=')
        music_name=music.text
        music_name=re.sub('[*\|/:?"<>]','',music_name)
        music_dict[music_id]=music_name
        i+=1
    for id in music_dict:
        url='http://music.163.com/song/media/outer/url?id=%s'%id
        # print(url)
        path='163music\\%s.mp3'%music_dict[id]
        list.insert(END,'正在下载：%s'%music_dict[id])
        list.insert(END,url)
        list.see(END)
        list.update()
        opener=build_opener()
        opener.addheaders= [head]
        install_opener(opener)
        urlretrieve(url,path)
        j+=1
        if j>=cnt:
            break
    list.insert(END,'成功下载 %d 首歌！双击链接，在线试听'%j)
def downloadsong():
    id=songid.get()
    if id=='':
        fail()
        return
    url='http://music.163.com/song/media/outer/url?id=%s'% id
    surl='https://music.163.com/song?id=%s'%id
    res=requests.get(surl,headers=head).text
    r=BeautifulSoup(res,'html.parser').find('title')
    songname=r.text.rstrip(' - 单曲 - 网易云音乐')
    songname=re.sub('[*\|/:?"<>]','',songname)
    if songname=='':
        fail()
        return
    list.insert(END,'正在下载 %s'%songname)
    list.insert(END,url)
    list.see(END)
    list.update()
    opener=build_opener()
    opener.addheaders= [head]
    install_opener(opener)
    urlretrieve(url,r'163music\%s.mp3'% songname)
    list.insert(END,'成功下载 1 首歌！双击链接，在线试听')
def openf():
    os.startfile(r'163music')
def website():
    os.startfile(r'https://music.163.com/')
def linkst():
    try:
        h=requests.get(r'https://music.163.com/',timeout=1)
    except:
        list.insert(END,'无网络，请检查网络连接状态！')
        return
    list.insert(END,'网络连接正常，欢迎使用！')
def listen(self):
    webbrowser.open(str(list.get(list.curselection())))
def about():
    txts='关于本软件\n' \
         '软件名：网易云下载器\n' \
         '作    者：永仙\n' \
         '版    本：1.0\n' \
         '大    小：9.08MB\n' \
         '功    能：本程序是个半自动的python爬虫工具,采用的Tkinter图形界面。由于\n' \
         '              网易云的搜索结果加密了的，不能直接通过歌名下载，需要打开\n' \
         '              网站复制ID。比官方客户端内存小，而且能下载“VIP下载”的歌。\n\n' \
         '帮助及说明\n' \
         '1.打开官网通过网址查看歌单、歌曲的ID\n' \
         '2.链接标识：歌单playlist，歌曲song.查看ID时请核对!\n\n' \
         '1.暂不支持通过搜索、歌手、专辑等方式下载\n' \
         '2.本软件可下载的内容：免费播放(含VIP下载)、公开歌单等\n' \
         '3.本软件不可下载的内容：仅VIP播放、需购买歌曲、无版权歌曲、私人歌单等\n' \
         '4.部分歌曲下载成功但是无法播放'
    messagebox._show('关于网易云下载器',txts)

if not os.path.exists('163music'):
    os.makedirs('163music')
ft='微软雅黑'
root=Tk()
root.title('网易云音乐下载器')
root.geometry('665x630+480+240')
Label(root,text='方法一：请输入要下载的歌单ID:',font=(ft,18)).grid(row=0,column=0,padx=16,sticky=W)
entry=Entry(root,width=16,font=(ft,18))
entry.grid(row=0,column=1,padx=16,sticky=W)
Label(root,text='请输入要下载数量:',font=(ft,18)).grid(row=1,column=0,padx=16,sticky=W)
count=Entry(root,width=16,font=(ft,18))
count.grid(row=1,column=1,padx=16,sticky=W)
Button(root,text='打开文件夹',font=(ft,15),command=openf).grid(row=2,column=0,padx=16,sticky=W)
Button(root,text='歌单下载',font=(ft,15),command=downloadsongs).grid(row=2,column=1,padx=16,sticky=W)
label=Label(root,text='方法二：请输入要下载歌曲ID:',font=(ft,18)).grid(row=3,column=0,padx=16,sticky=W)
songid=Entry(root,width=16,font=(ft,18))
songid.grid(row=3,column=1,padx=16,sticky=W)
Button(root,text='单曲下载',font=(ft,15),command=downloadsong).grid(row=4,column=1,padx=16,sticky=W)
Label(root,text='搜索结果:',font=(ft,18)).grid(row=5,column=0,padx=16,sticky=W)
list=Listbox(root,width=45,font=(ft,18))
list.bind("<Double-Button-1>",listen)
list.grid(row=6,columnspan=2,padx=16,sticky=W)
Button(root,text='关于及帮助',font=(ft,15),command=about).grid(row=7,column=0,padx=16,sticky=W)
Button(root,text='网易云官网',font=(ft,15),command=website).grid(row=7,column=1,padx=16,sticky=W)
linkst()
root.mainloop()

#pyinstaller -F -w -i 0.ico 163mspider.py
