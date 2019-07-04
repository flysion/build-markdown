#coding:utf8
"""
pip install makedown
pip install pillow
pip install requests
"""
import os,sys
import re
import markdown
from PIL import Image
import io
import base64
import getopt
import requests

def usage():
    print(f"using: python {sys.argv[0]} [options] [arg]")
    print(" -h, --help         : 显示使用帮助")
    print(" -t, --title        : 生成的HTML文档的title")
    print(" -o, --output       : 生成的HTML文档的保存位置")
    print("     --theme        : 生成的HTML文档额外的CSS样式")
    print("     --header       : 在正文之前（<body>标签后边）加入html内容")
    print("     --footer       : 在正文之后（</body>标签前边）加入html内容")
    print("     --image-base64 : 将图片转换成base64")
    print(" -D foo=bar         : 定义变量，替换markdown文档中的“%foo%”字样")
    print(" arg                : 要转换的markdown文件")
    
def download_image(url):
    resp = requests.get(url)
    return io.BytesIO(resp.content)
    
def image_to_base64(byteio):
    with Image.open(byteio) as image:
        image.verify()

    mime = Image.MIME[image.format]
    b64data = str(base64.b64encode(byteio.getvalue()), encoding='utf-8')
        
    return f"data:{mime};base64,{b64data}"

SCRIPT_DIR = os.path.split(os.path.realpath(__file__))[0]
OPTIONS = {
    "variables": {},
    "title": "",
    "output": "",
    "theme": f"{SCRIPT_DIR}/theme.css",
    "enable_image_base64": False,
    "header": "",
    "footer": "",
}

opts, args = getopt.getopt(sys.argv[1:], "hD:t:o:", ["help", "title=", "output=", "theme=", "theme=", "header=", "footer=", "image-base64"])
if len(args) == 0:
    usage() ; quit()
    
for k,v in opts:
    if k == '-D':
        var = v.split("=", 1)
        OPTIONS['variables'][var[0]] = var[1]
    elif k == '--title' or k == '-t':
        OPTIONS['title'] = v
    elif k == '--output' or k == '-o':
        OPTIONS['output'] = v
    elif k == '--theme':
        OPTIONS['theme'] = v
    elif k == '--header':
        OPTIONS['header'] = v
    elif k == '--footer':
        OPTIONS['footer'] = v
    elif k == '--image-base64':
        OPTIONS['enable_image_base64'] = True
    elif k == '--help' or k == '-h':
        usage() ; quit()

md_file = args[0]
filepath, filename = os.path.split(os.path.abspath(md_file))
name, ext = os.path.splitext(filename)

if OPTIONS['title'] == "":
    OPTIONS['title'] = name
    
if OPTIONS['output'] == "":
    OPTIONS['output'] = f"{name}.html"

with open(md_file, 'r') as f:
    md_text = f.read()
    
for varname in OPTIONS['variables']:
    md_text = md_text.replace(f"%{varname}%", OPTIONS['variables'][varname])
    
with open(OPTIONS['theme'], 'r') as f:
    theme_text = re.sub("\s*[\r\n]\s*", "", f.read())

with open(f"{SCRIPT_DIR}/jquery-3.3.1.min.js", 'r') as f:
    jquery_text = re.sub("\s*[\r\n]\s*", "", f.read())

with open(f"{SCRIPT_DIR}/common.js", 'r') as f:
    js_text = re.sub("\s*[\r\n]\s*", "", f.read())
    
header_text = ""
if OPTIONS['header']:
    with open(OPTIONS['header'], 'r') as f:
        header_text = f.read()
        
footer_text = ""
if OPTIONS['footer']:
    with open(OPTIONS['footer'], 'r') as f:
        footer_text = f.read()
    
html = markdown.markdown(md_text)

if OPTIONS['enable_image_base64']:
    for img in re.findall("<img.*?src.*?=.*?('|\")(.*?)\\1.*?>", html):
        if img[1][:8] == 'https://' or img[1][:7] == 'http://' or img[1][:2] == '//':
            ifile = download_image(img[1])
        else:
            if os.path.isfile(img[1]):
                imgpath = img[1]
            else:
                imgpath = os.path.join(filepath, img[1])

            with open(imgpath, 'rb') as f:
                ifile = io.BytesIO(f.read())

        src = image_to_base64(ifile)

        html = re.sub(re.compile(r"(<img.*?src.*?=.*?" + img[0] + ")" + re.escape(img[1]) + "(" + img[0] + ".*?>)"), f"\\g<1>{src}\\g<2>", html)

output_text = f"""<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8"/>
        <title>{OPTIONS['title']}</title>
		<style type="text/css">{theme_text}</style>
        <script type="text/javascript">{jquery_text}</script>
        <script type="text/javascript">{js_text}</script>
    </head>
    <body>{header_text}<div style="width:1080px; margin:0 auto;">{html}</div>{footer_text}</body>
</html>"""

with open(OPTIONS['output'], 'w') as f:
    f.write(output_text)