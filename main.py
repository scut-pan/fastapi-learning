from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import HTTPException

# 创建 FastAPI 实例
app = FastAPI()


# 路由：URL 和处理函数的映射
# 装饰器：@FastAPI实例.请求方法("请求路径")
# 处理函数：定义请求路径对应的处理逻辑
# 相应结果：处理函数的返回值
@app.get("/")
async def root():
    return {"message": "Hello World"}


# 路径参数 - Path类型注解
@app.get("/book/{id}")
async def get_book(id: int = Path(..., gt=0, lt=101, description="书籍id， 取值范围1-100")):
    return {"id": id, "title": f"这是第{id}本书"}

@app.get("/author/{name}")
async def get_author(name: str = Path(..., min_length=2, max_length=10)):
    return {"msg": f"这是{name}的信息"}


# 查询参数 - Query类型注解
# 需求 查询新闻 → 分页， skip: 跳过的记录数， limit: 返回的记录数 10
@app.get("/news/news_list")
async def get_news_list(
    skip: int = Query(0, description="跳过的记录数", le=100),
    limit: int = Query(10, description="返回的记录数", le=50)
):
    return {"skip": skip, "limit": limit}


# 请求体参数 - Field类型注解
# 注册：用户名和密码 → str
class User(BaseModel):
    username: str = Field(default="张三", min_length=2, max_length=10, description="用户名，长度要求2-10个字")
    password: str = Field(..., min_length=6, max_length=20, description="密码，长度要求6-20个字符")
    
@app.post("/register")
async def register(user: User):
    return user


# 响应类型
# 响应HTML内容
@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return "<h1>这是一级标题</h1>"


# 响应File内容
@app.get("/file", response_class=FileResponse)
async def get_file():
    path = "./files/bird.jpg"  # 文件路径
    return FileResponse(path)


# 自定义响应数据格式
# 需求：新增接口 + 相应数据格式 id, title, content
class News(BaseModel):
    id: int
    title: str
    content: str
    
@app.get("/news/{id}", response_model=News)
async def get_news(id: int):
    # 异常处理
    # 需求：按 id 查询新闻 → 1-6
    id_list = [1, 2, 3, 4, 5, 6]
    if id not in id_list:
        raise HTTPException(status_code=404, detail="您查找的新闻不存在")
    return {
        "id": id,
        "title": f"这是第{id}条新闻标题",
        "content": f"这是第{id}条新闻内容"
    }