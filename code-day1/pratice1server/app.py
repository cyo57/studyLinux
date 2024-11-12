from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import requests
from bs4 import BeautifulSoup

# 创建 FastAPI 实例
app = FastAPI()

# 配置 Jinja2 模板引擎
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

# 配置静态文件路径，供CSS和图片等静态资源访问
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_student_info(student_id: str):
    url = f'https://hnjm.cloudyshore.top/ryjf/sturyjfmx.aspx?xh={student_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    student_info = {'学号': student_id}
    student_info['班级'] = soup.find(id='lb_bjmc').text.strip()
    student_info['姓名'] = soup.find(id='lb_xm').text.strip()

    # 提取其他键值对
    rows = soup.find_all(class_=['rowstyle', 'altrowstyle'])
    for row in rows:
        tds = row.find_all('td')
        if len(tds) >= 6:
            category = tds[3].text.strip()
            points_text = tds[5].text.strip()
            try:
                points = float(points_text)
                student_info[category] = round(student_info.get(category, 0) + points, 2)
            except ValueError:
                pass
    return student_info


# 首页
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 根据学号查找学生信息
@app.post("/student", response_class=HTMLResponse)
async def get_student(request: Request, student_id: str = Form(...)):
    student_data = get_student_info(student_id)
    if student_data.get('姓名'):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "student_data": student_data
        })
    else:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "学号不存在，请检查后重新输入！"
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)