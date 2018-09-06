"""
@Project   : web-crawl
@Module    : weibo_first.py
@Author    : Jeff [arfu.guo@gmail.com]
@Created   : 2018/9/5 下午10:30
@Desc      : 
"""
import requests


def weibo_first():
    try:
        url = "https://www.weibo.com"

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
        default_request_headers = {
            'Connection': 'Keep-Alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        response0 = requests.get(url,
                                headers=default_request_headers)
        print(response0.headers)
        html0 = response0.content
        print('Successfully get html.')
        print(html0.decode('gb2312'))
        print(response0.url)
        response = requests.get(response0.url,
                                headers=default_request_headers)
        html = response.content
        print('Successfully get html.')
        print(html.decode('gb2312'))
        print(html0 == html)
        print(response0.url == response.url)
        print(response0 == response)
        print(response0)
        print(response)
        return html
    except Exception as e:
        print("Error: ", e)


if __name__ == '__main__':
    weibo_first()
