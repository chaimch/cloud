# cloud
基于docker的云资源(mysql, redis)分配系统

#### 项目启动方式

~~~python
# python3环境, 构建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行项目
python app.py
~~~

####项目结构描述

~~~markdown
|config		配置包
	|__init__.py		提供了DevConfig, TestConfig, ProdConfig
	|baseconfig.py	配置基类包
		|BpConfig.py	蓝图配置, 自己封装了下, 以实现动态蓝图注册
		|SerializeConfig.py		序列化配置
		|BaseConfig.py		配置基类
  |devconfig.py			开发环境基类配置模块
  |prodconfig.py		生产环境基类配置模块
  |testconfig.py		测试环境基类配置模块
|const.py					常量包
	|const.py				简单的常量模块
	|enum.py				枚举常量模块
|exts			插件包
	|cloudapi.py			基于flask_restful的api扩展插件, 可支持接口处自定义code值, 自定义序列化等
	|cloudflask.py		基于flask的扩展插件, 提供配置解析与蓝图动态注册
  |cloudform.py			基于wtforms的form扩展插件, 方便直接检验与取出错误信息
  |decorator.py			装饰器模块, 暂未用到, 可不看
  |serialize.py			序列化模块, 主要针对时间和字节类型的扩展处理
|mysql_bp		mysql的蓝图包
	|form.py					form检验模块, 主要验证参数是否合法与提供对应的提示
	|server.py				mysql对应的服务模块, 提交接口功能支持
	|urls.py					接口地址定义
|redis_bp		redis的蓝图包, 其余同mysql的蓝图包类似
|resource		restful扩展资源包
	|base.py					flask_restful的Resource的扩展基础模块, 提供请求钩子处理, 参数归整等功能
	|docker.py				flask_restful的Resource的docker资源扩展模块, 提供容器的声明周期管理
	|os.py						flask_restful的Resource的os资源扩展模块, 提供端口冲突检测等功能
~~~

#### 接口详情

| method | url                        | desc                                    |
| ------ | -------------------------- | --------------------------------------- |
| post   | /api/mysql/create_instance | [mysql实例创建](#mysql实例创建)         |
| get    | /api/mysql/get_config      | [mysql实例配置获取](#mysql实例配置获取) |
| post   | /api/redis/create_instance | [redis实例创建](#redis实例创建)         |
| get    | /api/redis/get_config      | [redis实例配置获取](#redis实例配置获取) |

#### mysql实例创建

**url**

~~~http
POST  /api/mysql/create_instance
~~~

**params**

| params     | type | necessary | desc                                      |
| ---------- | ---- | --------- | ----------------------------------------- |
| image_name | str  | yes       | 镜像名称(当前限制为mysql)                 |
| name       | str  | yes       | 容器名称                                  |
| ports      | int  | yes       | 端口绑定, eg: { "3306/tcp": 3306}         |
| mem_limit  | int  | yes       | 容器最大使用内存, 单位为bytes             |
| database   | str  | yes       | 用户自定义数据库                          |
| charset    | str  | yes       | 用户自定义字符集(当前限制为utf8, utf8mb4) |

**example**

```json
{
    "code": 0,
    "data": {
        "password": "nd3YEW9R5mwH6Y7I",
        "id": "069011802b43fe9e564f704bcf5c2cc93aa7eb9a03624a397a340fb0d61cdb8b",
        "short_id": "069011802b",
        "repotags": [
            "mysql:latest"
        ],
        "labels": {},
        "name": "mysql_02",
        "ports": {},
        "status": "created",
        "create_time": "2019-06-10T23:45:17.187524046Z"
    },
    "msg": "ok"
}
```

#### mysql实例配置获取

**url**

~~~http
GET  /api/mysql/get_config
~~~

**params**

| params | type | necessary | desc     |
| ------ | ---- | --------- | -------- |
| name   | str  | yes       | 容器名称 |

**example**

```json
{
    "code": 0,
    "data": {
        "id": "069011802b43fe9e564f704bcf5c2cc93aa7eb9a03624a397a340fb0d61cdb8b",
        "short_id": "069011802b",
        "repotags": [
            "mysql:latest"
        ],
        "labels": {},
        "name": "mysql_02",
        "ports": {
            "3306/tcp": [
                {
                    "HostIp": "0.0.0.0",
                    "HostPort": "3307"
                }
            ],
            "33060/tcp": null
        },
        "status": "running",
        "create_time": "2019-06-10T23:45:17.187524046Z",
        "total_memory": 1073741824
    },
    "msg": "ok"
}
```

#### redis实例创建

**url**

~~~http
POST  /api/redis/create_instance
~~~

**params**

| params     | type | necessary | desc                              |
| ---------- | ---- | --------- | --------------------------------- |
| image_name | str  | yes       | 镜像名称(当前限制为mysql)         |
| name       | str  | yes       | 容器名称                          |
| ports      | int  | yes       | 端口绑定, eg: { "6379/tcp": 6379} |
| mem_limit  | int  | yes       | 容器最大使用内存, 单位为bytes     |

**example**

```json
{
    "code": 0,
    "data": {
        "password": "Y1Aut63MuJeVv0UC",
        "id": "4b5d9c05561b2d16ebf0b87379cf351c15bd748f31e7e735b9b7ab4e0449e9cd",
        "short_id": "4b5d9c0556",
        "repotags": [
            "redis:latest"
        ],
        "labels": {},
        "name": "test_02",
        "ports": {},
        "status": "created",
        "create_time": "2019-11-23T07:54:34.494834316Z"
    },
    "msg": "ok"
}
```

#### Redis实例配置获取

**url**

~~~http
GET  /api/redis/get_config
~~~

**params**

| params | type | necessary | desc     |
| ------ | ---- | --------- | -------- |
| name   | str  | yes       | 容器名称 |

**example**

```json
{
    "code": 0,
    "data": {
        "id": "4b5d9c05561b2d16ebf0b87379cf351c15bd748f31e7e735b9b7ab4e0449e9cd",
        "short_id": "4b5d9c0556",
        "repotags": [
            "redis:latest"
        ],
        "labels": {},
        "name": "test_02",
        "ports": {
            "6379/tcp": [
                {
                    "HostIp": "0.0.0.0",
                    "HostPort": "6380"
                }
            ]
        },
        "status": "running",
        "create_time": "2019-11-23T07:54:34.494834316Z",
        "total_memory": 134217728
    },
    "msg": "ok"
}
```