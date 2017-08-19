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
   配置好python环境与mysql环境，其中python版本为2.7.9，不要超过此版本，python的版本兼容性不是很好，mysql的版本号为5.6.29。
   进入\NewsSpider\news_spider，输入命令scrapy crawl tencent
   抓取到的内容目前存放在testdata/data/tencent/类型/下，一条新闻对应一个文本文件，文本文件中以键值对的形式保存了新闻的url,
   title,time,content.文件名为新闻的id.例如http://sports.qq.com/a/20170806/037976.htm 对应的文件为037976.txt，
   文件位置testdata/data/tencent/sports/037976.txt
## 文档
   整个项目的相关文档（架构设计，数据库设计）放在doc下。sql脚本放在sql/下
   
## 备注
	当前只能抓取腾讯体育,误乐,科技,财经,汽车,房产,时常,文件新闻


