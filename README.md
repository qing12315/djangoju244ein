# 高校就业分析与可视化系统项目说明

## 一、项目概述
本项目是一个高校就业分析与可视化系统，采用 Django 框架开发，实现了毕业生信息管理、就业数据管理、公告信息管理等功能，同时支持用户注册、登录、认证等操作。项目还包含了数据统计、智能推荐、投票等特色功能，并集成了 Hive 数据库和 PySpark 进行数据分析。

## 二、项目结构
### 1. 主要目录
- `djangoju244ein/`：项目根目录
  - `djangoju244ein/`：项目配置目录
    - `main/`：主要应用目录，包含模型、视图等文件
      - `models.py`：模型文件，定义数据库表结构
      - `Jiuyeshuju_v.py`、`Gonggaoxinxi_v.py`：视图文件，处理业务逻辑和请求响应
    - `templates/`：模板文件目录，包含前端页面模板
    - `xmiddleware/`：中间件目录，包含认证、参数处理等中间件
    - `util/`：工具函数目录，包含加密、配置读取、数据处理等工具函数
  - `db/`：数据库脚本目录，包含 MySQL 和 Hive 数据库的创建脚本
  - `config.ini`：配置文件，存储数据库连接信息等配置

### 2. MTV 结构对应文件
- **M（Model）**：`djangoju244ein/main/model.py` 定义了基础模型类，实际的模型表结构定义可能在 `djangoju244ein/main/models.py` 中（代码未完整提供）。
- **T（Template）**：`djangoju244ein/templates/` 目录下的 `.vue` 文件为前端页面模板，如 `jiuyeshuju/list.vue`、`biyesheng/add - or - update.vue` 等。
- **V（View）**：`djangoju244ein/main/Jiuyeshuju_v.py`、`djangoju244ein/main/Gonggaoxinxi_v.py` 等文件为视图文件，处理业务逻辑和请求响应。

## 三、环境准备
### 1. 安装依赖
项目依赖的 Python 库可以通过 `requirements.txt` 文件进行安装：
```bash
pip install -r requirements.txt
```
依赖的前端库信息可以在 `djangoju244ein/templates/front/admin/package-lock.json` 文件中查看。

### 2. 配置数据库
编辑 `config.ini` 文件，配置数据库连接信息：
```ini
[sql]
type = mysql  # 数据库类型，支持 mysql、mssql
host = localhost  # 数据库主机地址
port = 3306  # 数据库端口号
user = root  # 数据库用户名
passwd = your_password  # 数据库密码
db = djangoju244ein  # 数据库名
charset = utf8  # 字符集
hasHadoop = yes  # 是否使用 Hadoop
```

## 四、项目初始化
### 1. 创建数据库
运行以下命令创建数据库：
```bash
python init.py initdb
```

### 2. 初始化数据表
运行以下命令初始化数据表：
```bash
python init.py initsql
```

### 3. 初始化 Hive 数据库（可选）
如果配置了使用 Hadoop，运行以下命令初始化 Hive 数据库：
```bash
python initial_hive_database.py
```

## 五、项目运行
启动 Django 开发服务器：
```bash
python manage.py runserver
```
访问 `http://localhost:8000` 即可进入系统。

## 六、主要功能说明
### 1. 用户管理
- **注册**：支持毕业生用户和其他用户的注册功能。
- **登录**：用户可以使用用户名和密码登录系统。
- **登出**：用户可以退出登录。
- **重置密码**：用户可以重置密码。

### 2. 信息管理
- **毕业生信息管理**：支持毕业生信息的新增、修改、删除、查询等操作。
- **就业数据管理**：支持就业数据的新增、修改、删除、查询等操作，同时提供搜索功能。
- **公告信息管理**：支持公告信息的新增、修改、删除、查询等操作。

### 3. 统计分析
- **数据统计**：支持按时间、按字段等多种方式进行数据统计。
- **智能推荐**：根据用户点击记录，推荐最近点击的或最新添加的记录。
- **投票功能**：支持对信息进行投票。

### 4. 数据分析（PySpark）
- **线性回归分析**：对指定表进行线性回归分析。
- **聚类分析**：对指定表进行聚类分析。
- **分类分析**：对指定表进行分类分析。

## 七、注意事项
- 项目中使用了 Hive 数据库和 PySpark 进行数据分析，需要确保相应的环境已经正确配置。
- 项目中的支付宝密钥文件 `djangoju244ein/util/alipay_key/app_private_2048.txt` 和 `djangoju244ein/util/alipay_key/alipay_public_2048.txt` 目前为空，需要根据实际情况进行配置。
- 部分视图函数的具体实现代码被省略，需要根据需求进行完善。
