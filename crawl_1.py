import urllib2
import urlparse
import re
import datetime
import time

def download(url,user_agent='wswp',proxy=None,num_retries=2):
    print "downloading:",url
    headers={'User-agent':user_agent}
    request=urllib2.Request(url,headers=headers)
    opener=urllib2.build_opener()
    if proxy:
        proxy_params={urlparse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html=opener.open(request).read()
    except urllib2.URLError as e:
        print 'Download error:',e.reason
        html=None
        if num_retries>0:
            if hasattr(e,'code') and 500<=e.code<600:
                return download(url,num_retries-1)
    return html
class Throttle:
    def __init__(self,delay):
        self.delay=delay
        self.domains={}
    def wait(self,url):
        domain=urlparse.urlparse(url).netloc
        last_accessed=self.domains.get(domain)
        if self.delay>0 and last_accessed is not None:
            sleep_secs=self.delay-(datetime.datetime.now()-last_accessed).seconds
            if sleep_secs>0:
                time.sleep(sleep_secs)
        self.domains[domain]=datetime.datetime.now()

def get_links(html):
    webpage_regex=re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    return webpage_regex.findall(html)

def link_crawl_queue(seed_url,link_regex,delay,max_depth=2):
    crawl_queue=[seed_url]
    seen={seed_url:0}
       ## set(crawl_queue)
    throttle=Throttle(delay)
    while crawl_queue:
        url=crawl_queue.pop()
        throttle.wait(url)
        html=download(url)
        depth=seen[url]
        if depth != max_depth:
            for link in get_links(html):
                if re.match(link_regex,link):
                    link=urlparse.urljoin(seed_url,link)
                    print link
                    if link not in crawl_queue:
                        seen[link]=depth+1
                        print seen
                        crawl_queue.append(link)
    return seen

f=link_crawl_queue("https://zhidao.baidu.com/question/711311640707979565.html",'/(question)',2)
print f