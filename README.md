## 包含网站：
- 今日头条
- 网易新闻
- 腾讯新闻

## 主要功能
  - 新闻抓取
  - 索引构建
  - 前端搜索

### [整体结构](https://github.com/lzjqsdd/NewsSpider/blob/master/Frame.md)

## 运行
   配置好环境，进入\NewsSpider\news_spider，输入命令scrapy crawl tencent
   抓取到的内容目前存放在testdata/data/tencent/类型/下，一条新闻对应一个文本文件，文本文件中以键值对的形式保存了新闻的url,
   title,time,content.文件名为新闻的id.例如http://sports.qq.com/a/20170806/037976.htm 对应的文件为037976.txt，
   文件位置testdata/data/tencent/sports/037976.txt
   
## 备注
	当前只能抓取腾讯体育,误乐,科技,财经新闻


