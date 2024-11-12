import requests
from bs4 import BeautifulSoup


id = input('请输入学号：')
print('正在查询，请稍等...')

url = f'https://hnjm.cloudyshore.top/ryjf/sturyjfmx.aspx?xh={id}'
response = requests.get(url)
print('查询到结果，正在解析...')

soup = BeautifulSoup(response.text, 'html.parser')
user_info = {}
user_info['class']= soup.find(id='lb_bjmc').text
user_info['name'] = soup.find(id='lb_xm').text
rows = soup.find_all(class_=['rowstyle', 'altrowstyle'])
for i in rows:
    row = i.find_all('td')
    # print(row)
    user_info[row[3].text] = round(user_info.get(row[3].text, 0) + float(row[5].text), 2)



print(user_info)