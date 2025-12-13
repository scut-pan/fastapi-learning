from fastapi import FastAPI

app = FastAPI()

# 中间件：为每个请求添加统一的处理逻辑
# （记录日志、身份认证、跨域、设置响应头、性能监控等）
# 中间件的执行顺序：自下而上
@app.middleware("http")
async def middleware1(request, call_next):
    print("中间件1 start")
    response = await call_next(request)
    print("中间件1 end")
    return response


@app.middleware("http")
async def middleware2(request, call_next):
    print("中间件2 start")
    response = await call_next(request)
    print("中间件2 end")
    return response


@app.get("/")
async def root():
    return {"message": "Hello World"}