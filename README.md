# WeChat Robot MCP Server (Python)

微信机器人 MCP 服务器 - Python 实现版本

## 项目简介

这是一个基于 Model Context Protocol (MCP) 的微信机器人服务器，使用 Python 实现。支持多租户架构，每个机器人可以有独立的数据库配置。

## 功能特性

- ✅ 基于 MCP 协议的标准服务器实现
- ✅ 多租户支持（基于 RobotCode 的数据库隔离）
- ✅ 上下文管理（使用 contextvars 实现线程安全）
- ✅ 数据库连接池管理
- ✅ 中间件支持（租户识别、数据库自动切换）

## 项目结构

```
.
├── src/
│   ├── __init__.py
│   ├── main.py                 # 主程序入口
│   ├── config/                 # 配置模块
│   │   ├── __init__.py
│   │   └── config.py          # 配置加载和管理
│   ├── middleware/             # 中间件模块
│   │   ├── __init__.py
│   │   └── tenant.py          # 租户中间件
│   ├── robot_context/          # 机器人上下文
│   │   ├── __init__.py
│   │   └── context.py         # 上下文管理
│   ├── model/                  # 数据模型
│   └── protobuf/               # Protobuf 消息定义
├── pyproject.toml              # 项目配置
├── requirements.txt            # 依赖列表
├── run.py                      # 启动脚本
└── .env.example               # 环境变量示例

```

## 安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd wechat-robot-mcp-server-python
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入实际配置
```

## 配置说明

在 `.env` 文件中配置以下环境变量：

```bash
# MCP 服务器端口
MCP_SERVER_PORT=9000

# MySQL 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password

# 开发模式
GO_ENV=dev
```

## 运行

### 方式 1：使用启动脚本

```bash
python run.py
```

### 方式 2：作为模块运行

```bash
python -m src.main
```

### 方式 3：使用已安装的命令（安装后）

```bash
pip install -e .
wechat-robot-mcp-server
```

## 开发指南

### 架构说明

#### 1. 上下文管理

使用 Python 的 `contextvars` 模块实现线程安全的上下文传递：

```python
from src.robot_context import get_robot_context, get_db

# 获取当前机器人上下文
rc = get_robot_context()
if rc:
    print(f"Robot ID: {rc.robot_id}")
    print(f"Robot Code: {rc.robot_code}")

# 获取当前数据库会话
db = get_db()
```

#### 2. 中间件

租户中间件会自动从请求的 meta 数据中解析机器人上下文，并设置对应的数据库连接：

```python
# 请求中的 meta 数据会被自动解析
{
    "RobotCode": "robot_001",
    "RobotID": 123,
    "RobotWxID": "wxid_xxx",
    ...
}
```

#### 3. 数据库连接

每个 RobotCode 对应一个独立的数据库，连接会被缓存以提高性能：

```python
from src.config import get_db_by_robot_code

# 获取指定机器人的数据库会话
db = get_db_by_robot_code("robot_001")
```

### 添加新功能

1. 在 `src/main.py` 中注册工具：

```python
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="your_tool",
            description="工具描述",
            inputSchema={
                "type": "object",
                "properties": {...}
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "your_tool":
        # 实现工具逻辑
        return [TextContent(text="结果")]
```

## 与 Go 版本的区别

| 特性 | Go 版本 | Python 版本 |
|------|---------|-------------|
| 上下文管理 | context.Context | contextvars |
| 数据库 ORM | GORM | SQLAlchemy |
| HTTP 服务器 | net/http | MCP stdio |
| 中间件 | 函数包装 | 函数包装 |
| 并发模型 | goroutine | asyncio |

## 依赖说明

- `mcp`: Model Context Protocol SDK
- `pydantic`: 数据验证
- `sqlalchemy`: ORM 和数据库连接
- `python-dotenv`: 环境变量管理
- `pymysql`: MySQL 数据库驱动

## 许可证

[LICENSE]

## 贡献

欢迎提交 Issue 和 Pull Request！
