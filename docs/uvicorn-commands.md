# Uvicorn 常用命令

Uvicorn 是一个基于 ASGI 的轻量级、超快速的 HTTP 服务器，用于运行 FastAPI 等 ASGI 应用程序。

## 基本运行命令

```bash
# 基本运行（使用默认配置）
uvicorn main:app

# 指定模块和应用实例（格式：模块名:应用实例名）
uvicorn 模块名:ASGI应用实例名
```

## 常用启动参数

### 主机和端口

```bash
# 指定主机和端口
uvicorn main:app --host 0.0.0.0 --port 8000

# 使用简写参数
uvicorn main:app -h 0.0.0.0 -p 8000

# 只指定端口（主机默认为 127.0.0.1）
uvicorn main:app --port 9000
```

### 热重载（开发环境）

```bash
# 启用自动重载（代码变更时自动重启）
uvicorn main:app --reload

# 指定重载的目录
uvicorn main:app --reload --reload-dir ./app

# 排除不需要重载的目录
uvicorn main:app --reload --reload-exclude "*.log"
```

### 工作进程（生产环境）

```bash
# 指定工作进程数量（多进程）
uvicorn main:app --workers 4

# 结合 uvicorn[standard] 使用可充分发挥性能
```

## 日志配置

```bash
# 设置日志级别（critical, error, warning, info, debug, trace）
uvicorn main:app --log-level info
uvicorn main:app --log-level debug

# 启用访问日志
uvicorn main:app --access-log

# 禁用访问日志
uvicorn main:app --no-access-log

# 自定义日志格式
uvicorn main:app --log-config logging.conf
```

## SSL/HTTPS 配置

```bash
# 启用 HTTPS
uvicorn main:app --ssl-keyfile key.pem --ssl-certfile cert.pem

# 指定 SSL 版本
uvicorn main:app --ssl-version 3

# 指定密码
uvicorn main:app --ssl-keyfile-password your_password
```

## 其他实用参数

```bash
# 设置请求超时时间（默认 5 秒，单位：秒）
uvicorn main:app --timeout-keep-alive 30

# 设置限制最大请求数（达到后自动重启）
uvicorn main:app --limit-concurrency 1000

# 设置 backlog 参数
uvicorn main:app --backlog 2048

# 指定应用目录
uvicorn main:app --app-dir /path/to/app

# 查看帮助信息
uvicorn --help

# 查看版本信息
uvicorn --version
```

## 子目录中的应用

当应用文件位于子目录中时（如 `orm/main.py`），有几种运行方式：

### 方式 1：使用模块路径（推荐）

```bash
# 使用点号分隔的模块路径
uv run uvicorn orm.main:app --reload

# 指定端口
uv run uvicorn orm.main:app --reload --port 8000
```

### 方式 2：使用 --app-dir 参数

```bash
# 指定应用所在目录
uv run uvicorn main:app --app-dir orm --reload
```

### 方式 3：切换到子目录运行

```bash
# 先进入子目录，再运行
cd orm
uv run uvicorn main:app --reload
```

**模块路径说明**：
- `main:app` → `main.py` 文件中的 `app` 实例
- `orm.main:app` → `orm/main.py` 文件中的 `app` 实例
- `api.v1.main:app` → `api/v1/main.py` 文件中的 `app` 实例

## 结合 uv 使用（推荐）

```bash
# 使用 uv 运行 uvicorn（推荐方式）
uv run uvicorn main:app

# 使用 uv 运行并启用热重载
uv run uvicorn main:app --reload

# 使用 uv 运行并指定端口
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

## 常见使用场景

### 开发环境

```bash
# 本地开发，启用热重载，详细日志
uv run uvicorn main:app --reload --log-level debug
```

### 生产环境

```bash
# 多进程，绑定所有网络接口
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --access-log
```

### 测试环境

```bash
# 指定端口，简化日志
uvicorn main:app --port 8080 --log-level warning --no-access-log
```

## 与 Gunicorn 配合（生产环境推荐）

```bash
# 使用 Gunicorn + Uvicorn workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 环境变量

```bash
# 通过环境变量设置配置
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8000
UVICORN_LOG_LEVEL=info
```

## 注意事项

1. **开发环境**：使用 `--reload` 参数可以实时看到代码变更效果
2. **生产环境**：建议使用 `--workers` 参数启用多进程，或配合 Gunicorn 使用
3. **端口冲突**：如果端口被占用，请更换其他端口或停止占用端口的程序
4. **权限问题**：绑定 1024 以下的端口需要管理员权限
5. **Windows 限制**：Windows 不支持 `--workers` 参数（多进程），可考虑使用 Gunicorn

## 参考资源

- [Uvicorn 官方文档](https://www.uvicorn.org/)
- [FastAPI 部署文档](https://fastapi.tiangolo.com/deployment/)
