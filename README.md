LINE Weather Bot with flask
======

## 對話模式

####對話關鍵

* 天氣
	* 台灣23個縣市
* 其他：如果沒有「天氣」的關鍵字是一個 Echo Bot

## Deveplotment Environment

* python 

以下套件在本專案底下的 requirements.txt 

```
LINE-bot-sdk
flask
gevent
gunicorn
simplejson
requests
```

* Ruby 

管理 local serve

```
gem install foreman

``` 

* mac 

```
brew cask install ngrok
brew install libevent
```


## Fast Deploy  
如果

* 已經辦好 heroku 並從 heroku-CLI 登入
* 已經辦好 LINE@ 並申請好 channel 開啟 message-api 功能

那可以直接複製貼上以下的指令

```
git clone https://github.com/Nienzu/LINE-wb-flask
brew cask install ngrok libevent
pip install -r requirements.txt
heroku create 
git add .
git commit -m "Fast Deploy"
git push heroku master
```

接下來是你的環境變數設置

```
heroku config:set LINE_CHANNEL_SECRET=你LINE的 secret key
heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your-LINE-token
heroku config:set APIKEY=你從中央氣象局拿到的api-key

```

最後記得把你的 heroku app 的網址貼在你 LINE develop 的 webhook
例如

```
https://xxxxxxx.herokuapp.com/callback
```

##Tutorial for developer
1. 環境設置
2. run localy

### 環境設置
---

這個專案用到的服務有

* [LINE](https://business.LINE.me/zh-hant/)
* [heroku](https://dashboard.heroku.com/)
* [中央氣象局會員](http://opendata.cwb.gov.tw/index)

因此需先把上述的服務申請好

### Run localy
---

如果是正在開發中的 LINE-bot，每次要測試新功能或是除錯就要將檔案push到 heroku 的話其實是很麻煩的，因此以下的步驟是將開發流城透過第三方工具建立在本機上(但仍須網路來將網址轉換)

```
gem install foreman
brew cask install cgrok

```
foreman 會執行 Procfile 將機械人跑在本地端的 http://0.0.0.0:5000
ngrok 是協助我們將 local 的 http server 指向 ngrok 提供的 server

```
foreman start 
ngrok http 5000
```
最後把 ngrok 的 https 貼到 LINE developers 的 webhook
這樣如果有新功能要測試只要重開 foreman 即可  


## Reference

* [Flask Heroku](https://github.com/zachwill/flask_heroku)
* [[Bot] Line Echo Bot on Django](http://lee-w-blog.logdown.com/posts/1134898-line-echo-bot-on-django)
