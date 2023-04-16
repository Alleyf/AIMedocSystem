import re
from time import sleep

from lxml import etree
from selenium import webdriver
# 实现规避检测
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# from selenium.webdriver.common.by import By
# from seleniumwire import webdriver


def get_zhiwang_data(keywords: str, start: int = 0, end: int = 10) -> tuple:
    # 这个是一个用来控制chrome以无界面模式打开的浏览器
    # 创建一个参数对象，用来控制chrome以无界面的方式打开
    try:
        chrome_options = Options()
        # 后面的两个是固定写法 必须这么写
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        # 实现规避检测
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])

        # 启动服务
        s = Service("chromedriver_new.exe")
        driver = webdriver.Chrome(service=s, chrome_options=chrome_options, options=option)
        # api_url = 'https://openai.yugin.top/v1'
        #
        # driver.get(api_url)
        #
        # # a = driver.find_element_by_xpath('/html/body/pre').text  # 获取代理
        # a = driver.find_element(By.XPATH, '/html/body/pre').text  # 获取代理
        #
        # option.add_argument('--proxy-server=http://%s' % a)  # 添加代理
        #
        # driver.delete_all_cookies()  # 清楚cookies

        # 知网内容的爬取
        # driver.get("https://www.cnki.net/")
        driver.get("https://www.cnki.net/")
        print(driver)
        search_input = driver.find_element(by="id", value="txt_SearchText")
        # search_input = driver.find_element(by="id", value="txt_search")

        # keywords = "心脏"
        print(search_input.id, keywords)
        search_input.send_keys(keywords)
        print(search_input.text)
        button = driver.find_element(by="class name", value="search-btn")
        print(button.id)
        button.click()
        # 如果网速慢搜索不到就延长时间
        sleep(2)
        zhiwang_data = []
        status = 200
        # 数据解析
        page_text = driver.page_source
        tree = etree.HTML(page_text)
        print("源数据：", page_text)
        final_name = ""
        st = 'recid=&(.*?)&DbName='  # 正则表达式
        all_li = tree.xpath("//a[@class='fz14']")
        for index, li in enumerate(all_li):
            if start <= index < end:
                all_name = li.xpath("./text() | ./font/text()")
                all_href = li.xpath("./@href")
                for name in all_name:
                    final_name = final_name + name
                result = re.findall(st, all_href[0])
                for item in result:
                    href = "https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CAPJ&dbname=CAPJLAST&" + item
                data_dict = {'name': final_name, 'href': href}
                zhiwang_data.append(data_dict)
                # print(str(index) + ":", final_name)
                final_name = ""
        if not zhiwang_data:
            status = 403
    except Exception as e:
        status = 403
        zhiwang_data = []
    finally:
        return status, zhiwang_data


if __name__ == "__main__":
    print(get_zhiwang_data(keywords="静脉曲张", start=0, end=20))
