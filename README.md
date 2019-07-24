# build-markdown
将 markdown 文件转换成 html  

+ 支持自定义皮肤
+ 支持文档变量替换
+ 支持将图片转换成 base64
+ 自定义 header 和 footer
+ 可将h1...h9标签索引，并显示悬浮窗在右侧

## 使用方法
使用以下命令查看使用方法：

	> python md2html.py --help
    using: python md2html.py [options] [arg]
	 -h, --help            : 显示使用帮助
     -t, --title           : 生成的HTML文档的title
     -o, --output          : 生成的HTML文档的保存位置
         --theme           : 生成的HTML文档额外的CSS样式
         --header          : 在正文之前（<body>标签后边）加入html内容
         --footer          : 在正文之后（</body>标签前边）加入html内容
         --image-base64    : 将图片转换成base64
         --index-max-depth : 将h1...h9标签编排成树状索引显示在页面的右侧，设置索引的最大深度，默认为0（不启用索引）
     -D foo=bar            : 定义变量，替换markdown文档中的“%foo%”字样
     arg                   : 要转换的markdown文件
