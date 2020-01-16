import json
import logging
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from selenium import webdriver

from utils.SystemUtils import SystemUtils

logging.basicConfig(level=logging.INFO)


class HtmlUtils:
    """"html工具类"""

    @staticmethod
    def generate_img(htmlpath):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--dns-prefetch-disable')
            options.add_argument('--no-referrers')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-audio')
            options.add_argument('--no-sandbox')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--allow-insecure-localhost')
            dpath = "./static/chrome/chromedriver" + (".exe" if SystemUtils.is_windows() else "")
            driver = webdriver.Chrome(dpath, options=options)
            # driver = webdriver.Chrome("/usr/local/Cellar/chromedriver", options=options)
            abhtmlpat = "file:///" + SystemUtils.get_file_absolute(htmlpath)
            # print("===========" + abhtmlpat)
            driver.get(abhtmlpat)
            width = driver.execute_script(
                "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);")
            height = driver.execute_script(
                "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
            driver.set_window_size(width, height)
            img_path = htmlpath[:-5] + ".png"
            driver.save_screenshot(img_path)
            driver.close()
            return img_path
        except BaseException as e:
            print(e.msg)
            logging.error('生成图片失败:htmlpath:' + htmlpath, e.msg)

    @staticmethod
    def generate_html(templatepath, filename, data):
        try:
            env = Environment(loader=FileSystemLoader(templatepath))  # 加载模板
            template = env.get_template(filename)
            nfilepath = "./static/out/" + datetime.now().strftime(
                '%Y%m%d%H%M%S') + ".html"
            with open(nfilepath, 'w') as fout:
                html_content = template.render(json_data=json.dumps(data))
                fout.write(html_content)  # 写入模板 生成html
                fout.flush()
                fout.close()
            return nfilepath
        except BaseException as e:
            print(e.msg)
            logging.error('生成html失败:templatepath:' + templatepath + " filename：" + filename, e.msg)


def main():
    HtmlUtils.generate_img("/Users/lihuan/works/jrwork/myStockStrategy/static/out/20200116004000.html")


if __name__ == "__main__": main()
