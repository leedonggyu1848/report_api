import requests
from bs4 import BeautifulSoup

def hankyun_api(text, start, end, COorIN=True):
    report_type = 'IN' if COorIN else 'CO'
    text = text.encode('euc-kr')
    url = 'http://consensus.hankyung.com/apps.analysis/analysis.list'
    base_url = 'http://consensus.hankyung.com'
    now_page = 1
    ret = []
    params = {
        'sdate': start,
        'edate': end,
        'search_text': text,
        'report_type': report_type,
        'pagenum': 100
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'}
    while True:
        res = requests.get(url, params={**params, 'now_page': now_page}, headers=headers)
        bs = BeautifulSoup(res.content.decode('euc-kr', 'replace'), 'html.parser')
        items = bs.select('tbody > tr')
        if len(items) == 0:
            break
        print(now_page)
        for item in items:
            slots = item.find_all('td')
            date = slots[0].text.strip()
            title = slots[1].find('strong').text.strip()
            consensus = slots[2].text.strip()
            author = slots[3].text.strip()
            company = slots[4].text.strip()
            pdf_name = slots[6].find('a')['title']
            pdf_link = base_url + slots[6].find('a')['href']
            ret.append({
                'date':date,
                'title':title,
                'consensus':consensus,
                'author': author,
                'company': company,
                'pdf_name': pdf_name,
                'pdf_link': pdf_link
            })
        now_page += 1
    return ret