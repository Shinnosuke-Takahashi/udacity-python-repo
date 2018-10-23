# THIS CODE IS CURRENTLY UNDER DEVELOPMENT AND IS UPDATED REGULARLY.
# This is a search engine under development.
# THE FOLLOWING IS A LOG OF UPDATES:
# 10-19-18: revised crawl_web to include indexing capability
# 10-18-18: defined add_page_to_index, which breaks page content into keywords, then calls add_to_index
# 10-14-18: added indexing/keyword association capability via add_to_index, also defined lookup function
# 10-9-18: defined crawl_web()
# 10-8-18: improved get_all_links() by calling newly defined function union()
# 10-2-18: defined get_all_links()
# 9-28-18: start date; defined get_next_target()

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

index = []

def add_to_index(index, keyword, url):
    for entry in index:
        if entry[0] == keyword:
            entry[1].append(url)
            return
    index.append([keyword, [url]])

def lookup(index, keyword):
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    return []

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            union(tocrawl,get_all_links(content))
            crawled.append(page)
    return index
