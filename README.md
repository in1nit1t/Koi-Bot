<p align="center">
  <img src="https://i.loli.net/2021/09/21/c9DMFSUVONI8mg4.png" width="200" height="200">
</p>

<div align="center">

# Koi Bot

一个基于 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 开发，以 [MySQL](https://www.mysql.com/) 作为数据库的 qq 群~~功能型~~机器人

</div>

<p align="center">
  <a href="https://github.com/in1nit1t/Koi-Bot/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Mrs4s/go-cqhttp?color=blue" alt="license">
  </a>
  <a href="https://github.com/Mrs4s/go-cqhttp/">
    <img src="https://img.shields.io/badge/go--cqhttp-1.0.0-orange" alt="go-cqhttp">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.7%2B-green?logo=python" alt="python">
  </a>
  <a href="https://www.mysql.com/">
    <img src="https://img.shields.io/badge/mysql-8.0.17%2B-d42328?logo=mysql" alt="mysql">
  </a>
</p>

## 简介

这是个一时兴起而产出的项目，起因是觉得平时混的一个群的 bot 不够好玩，直接原因是 [koi 欢](https://space.bilibili.com/210127180) 实在是太可爱了。所以，一个为 koi 定制的 bot —— Koi Bot 诞生了

> #### 实现思路

1. 搭建本地 server 与 go-cqhttp 的反向 HTTP 代理对接，获取 bot 所在 qq 群的消息及事件
2. 解析消息和事件的语义，生成响应消息
3. 响应消息交由 go-cqhttp 的 API 发送到群里，实现与群友的互动

<br>

> #### 技术栈

1. 装饰器
2. 面向对象
3. 正则表达式
4. 网络与爬虫
5. 多线程并发
6. MySQL 数据库

PS. 没有使用 nonebot + 协程，就是想看看轮子是怎么造的（

<br>

> #### 开发周期
>

利用一些课余的零碎时间，前前后后共花了两个星期来完成初始版本的开发和部署

<br>

> #### 小声 bb
>

欢迎大家来 [qq群](https://jq.qq.com/?_wv=1027&k=e4okN6Q5) 调戏 kb，希望群大佬能为 kb 开发更多的功能。使用过程中遇到 bug 或者对 kb 有什么建议，麻烦私聊我或者提 Issue，Thanks♪(･ω･)ﾉ

<br>

## 技能列表

<details>
<summary>主动技能</summary>

1. 菜单
   - 所有功能概述
   - 每种功能的详细解释（指令格式及效果等）
2. 签到
   - 完成今日签到，获得积分
   - 查询历史签到情况
3. 积分兑换
   - 列出可兑换物品（普通及限时物品）
   - 用户兑换指定物品后，通过私聊发送
4. 好康的图（咳咳）
   - 返回图片的同时携带标题、pid、画师信息
   - 支持 tag 搜索
   - 支持获取原画画质的图片
5. 梗百科
   - 支持通过关键词查找梗出处
   - 列出满足条件的所有条目
   - 可以展开任意条目获取详细信息
6. 群语音操作
   - 保存语音
   - 播放历史语音
   - 添加语音标签
   - 查看语音标签
   - 修改语音标签
   - 通过标签搜索语音
   - 删除已保存语音
7. 摆烂模式
8. 网易云点歌
9. 多语种互译
10. 毒鸡汤
11. 土味情话
12. 舔狗日记
13. 查询拼音缩写的含义
14. 生成器
    - 生成绝绝子
    - 生成记仇表情包
</details>

<details>
<summary>被动技能</summary>

1. 发言数日榜/周榜
2. 每日早安推送
   - 随机 ACG 图片一张
   - 历史上的今天
   - 今日早报
3. koi 发送早晚安时回应（发病）
4. 复读
5. 特殊字符/句型反应（好好好/捏/是吧/草）
6. 戳一戳，回应以下之一
   - 戳回去
   - 钉宫语音
   - 回应一句话
   - 随机 ACG 图片一张
   - 戳的次数多了，禁言 1 分钟
7. 自动通过好友申请，并发送打招呼消息
8. 群新成员欢迎
9. 被艾特后回应
10. b 站通知
    - 新动态（携带动态截图）
    - 新作品（携带作品截图）
    - 新粉丝（携带新粉丝头像及id）
</details>

<br>

## 部署 & 配置

这个版块将介绍如何分别在 Windows 本地和 Linux 服务器上部署 bot


### Windows 本地部署

> <span id="windows_cqhttp_setup">go-cqhttp 配置</span>

首先从 go-cqhttp 的 [release](https://github.com/Mrs4s/go-cqhttp/releases) 页面下载最新版可执行程序：

<p align="center">
<img src="https://i.loli.net/2021/09/21/F9khMzoby8Duiml.png">
</p>

以 **64** 位系统为例，下载 **go-cqhttp_windows_amd64.zip** 并解压（当然直接下载 exe 也是可以的）

运行 go-cqhttp.exe，会提示没有找到配置文件，这里输入 **1**，然后回车：

<p align="center">
<img src="https://i.loli.net/2021/09/21/nEah3jtdFODqiGI.png">
</p>

关闭控制台，此时同级目录下会生成一个 **config.yml** 文件，使用文本编辑器将其打开，修改以下三项：

- account -> uin：改为 bot 的 qq 号（找一个不用的 qq 号作为 bot）
- account -> password：改为 qq 号对应的密码
- servers -> http -> post：增加 url 子项，值为 `127.0.0.1:5701`（注意在 url 前面添加短横）

<p align="center">
<img src="https://i.loli.net/2021/09/21/U9gNRehDoLarp6S.png">

<img src="https://i.loli.net/2021/09/21/7ZhYAOQzJ6B1TGq.png">
</p>

<br>

> <span id="windows_mysql_setup">MySQL 数据库导入</span>

首先确保 MySQL 数据库版本为 **8.0.17** 及以上，可以通过 `mysql --version` 命令查看

之后通过登入 MySQL 命令行或使用图形化工具（如 Navicat 等）创建一个数据库，名字任取，再将项目根目录下的 **koibot.sql** 导入创建的数据库

这里以命令行操作为例，登入后：

1. `create database koi_bot;` 语句创建一个名为 koi_bot 的数据库
2. `use koi_bot;` 语句指定操作的数据库
3. `source [koibot.sql文件所在的路径];` 导入数据表

<p align="center">
<img src="https://i.loli.net/2021/09/21/8tjsHLfCbnAiKE1.png">
</p>

<br>

> Python 依赖安装

首先确保 Python 版本为 **3.7** 及以上，可以通过 `python --version` 命令查看

在项目根目录下执行 `python -m pip install -r requirements.txt`，等待库安装完毕即可

<br>

> 运行

1. 依照 **[Koi Bot 自身配置](#self_config)** 版块对**账号、数据库、API、杂项**部分进行配置
2. 确保命令行工作路径在项目根路径下，输入 `python main.py` ，出现 `[+] Server successfully launched at 127.0.0.1:5701` 提示
3. 运行 go-cqhttp.exe，等待一段时间，控制台会输出一个二维码，使用 bot 的 qq 扫描登录
4. 确保 bot 在监听的群中，在群里发送 **菜单** 命令，开始使用 bot

<br>

### Linux 服务器部署

这里以腾讯云服务器为例，环境如下：

- 操作系统：CentOS 7 x86_64
- Python 版本：3.8.0
- MySQL 版本：14.14 Distrib 5.7.35

<br>

> go-cqhttp 配置

首先从 go-cqhttp 的 [release](https://github.com/Mrs4s/go-cqhttp/releases) 页面下载最新版可执行程序到服务器：

<p align="center">
<img src="https://i.loli.net/2021/09/21/qAYpJZwiUWgxCf8.png">
</p>

执行下列命令：

```bash
mkdir go_cqhttp
tar zxvf go-cqhttp_linux_amd64.tar.gz -C go_cqhttp
cd go_cqhttp
./go-cqhttp
```

接下来的操作和 **Windows 本地部署** 的 [这一板块](#windows_cqhttp_setup) 相同

<br>

> MySQL 数据库导入

与 **Windows 本地部署** 的 [这一板块](#windows_mysql_setup) 相同

<br>

> Python 依赖安装

首先确保 Python 版本为 **3.7** 及以上，可以通过 `python3 --version` 命令查看

在项目根目录下执行 `pip3 install -r requirements.txt`，等待库安装完毕

<br>

> 运行

1. 依照 [Koi Bot 自身配置](#self_config) 版块对**账号、数据库、API、杂项**部分进行配置
2. 确保命令行工作路径在项目根路径下，测试 `python3 main.py` 命令是否正常执行，而后退出并执行 `nohup python3 main.py > /dev/null 2>&1 &` 命令，将进程长期挂在后台
3. 执行 `./go-cqhttp`，等待一段时间，控制台会输出一个二维码，使用 bot 的 qq 扫描登录，登陆成功后退出并执行 `nohup ./go-cqhttp > /dev/null 2>cqlog &` 命令，将进程长期挂在后台
4. 确保 bot 在监听的群中，在群里发送 **菜单** 命令，开始使用 bot

<br>

> go-cqhttp 日志管理

上个版块第 3 点命令中的 `2>cqlog` 会将标准错误流重定向到 cqlog 文件，这样查看 cqlog 文件就能获得 go-cqhttp 程序的日志输出

不过这个文件大小会随着时间推进越来越大，这里推荐使用 **logrotate** 来自动地分割日志和丢弃旧日志，参考文章 [日志切割之Logrotate](https://www.cnblogs.com/clsn/p/8428257.html)，下面贴出我的配置文件（/etc/logrotate.d/cqlog）

```
/home/in1t/koibot/cqlog {
    daily
    dateext
    rotate 5
    missingok
    create 644 in1t in1t
    postrotate
        /usr/bin/killall -HUP rsyslogd
    endscript
}
```

<br>

<h3 id="self_config">Koi Bot 自身配置</h3>
项目根目录下有一个 <strong>setting.json</strong> 配置文件，这里进行逐行解释

```c++
{
  // 账号信息相关配置
  "account": {
    "qq": {
      "bot": 123456789,    // bot 的 qq 号
      "koi": 987654321,    // koi 的 qq 号
      "admin": 123456789,  // 管理者的 qq 号（对 bot 有完全控制权）
      "target_group": 976519594   // bot 监听的 qq 群号
    },
    "bilibili": {
      "koi_uid": 210127180  // koi 的 bilibili uid
    }
  },

  // 数据库配置
  "database": {
    "user": "root",          // 用户名
    "host": "localhost",     // 主机名
    "db_name": "koi_bot",    // 数据库名，保持与之前创建的数据库名相同
    "db_password": "XXXXXX"  // 数据库连接密码
  },

  // bot 功能配置
  "service": {
    "group": {
      "sign_in": {        // 签到功能
        "enable": true,     // 是否启用
        "base_points": 3,   // 每次签到获得的基础分
        "refresh_time": {   // 每日签到的刷新时间（24小时制）
          "hour": 5,        // 默认为凌晨5点
          "minute": 0
        }
      },
      "jichou": {        // 记仇表情包生成器
        "enable": true,    // 是否启用
        "version": "old"   // 表情包版本，可选值为old/new，old版本比较有内味
      },
      "auto_save": {       // 自动保存功能
        "enable" : false,  // 是否启用，此功能目前可能存在 bug，慎用
        "voice": {       // 语音类消息自动保存
          "enable": true,  // 是否启用
          "target_qq": [123456789]  // 监听的 qq 号列表
        }
      },
      "bilibili": {      // bilibili 功能
        "notice": {        // 通知类功能
          "new_post": {      // 新作品
            "enable": true,    // 是否启用
            "with_screenshot": true  // 是否携带动态截图
          },
          "new_dynamic": {   // 新动态（普通动态）
            "enable": true,    // 是否启用
            "with_screenshot": true  // 是否携带动态截图
          },
          "new_dynamic_forwarding": {  // 新动态（转发动态）
            "enable": true,    // 是否启用
            "with_screenshot": true  // 是否携带动态截图
          },
          "new_follower": {  // 新粉丝
            "enable": false,   // 是否启用
            "with_avatar": true  // 是否携带新粉丝头像
          }
        }
      },
      "message_context": {   // 消息上下文分析
        "enable": true,   // 是否启用
        "fudu_limit_count": 5,  // 复读临界次数
        "probability": {  // 特殊句式响应概率，范围0-100
          "haohaohao": 30,  // 好好好
          "haoye": 30,  // 好耶
          "cao": 30,    // 草
          "jxt": 30,    // 捏
          "shiba": 30,  // 是吧
          "fudu_break": 30  // 打断复读
        },
        "bai_lan_mode": {  // 摆烂模式
          "enable": true,       // 是否启用
          "recovery_time": 180  // 恢复时间，单位秒
        }
      },
      "poke": {     // 戳一戳
        "enable": true,   // 是否启用
        "ban": {    // 禁言
          "limit_times": 3,   // 被同一用户戳的次数达到这个数值时，依概率禁言
          "probability": 50,  // 禁言概率
          "time": 60   // 禁言时间，单位秒
        },
        "voice_source": "kugimiya"  // 语音源：钉宫，目前仅有这个选项
      },
      "cosplay": {  // cosplay图片
        "enable": true   // 是否启用
      }
    }
  },

  // API 相关配置
  "api": {
    "baidu_translate": {    // 百度翻译，获取方式见下一个版块
      "appid": 99999999999999999,  // APPID
      "secret_key": "XXXXXXXXXXXXXXXXXXXX"  // SECRET KEY
    },
    "alapi": {    // ALAPI，获取方式见下个版块
      "token": "XXXXXXXXXXXXXXXX"  // 个人TOKEN
    }
  },

  // 杂项
  "misc": {
    "log_directory": "D:\\log",       // 日志存放目录
    "cache_directory": "D:\\cache",   // 缓存目录
    "web": {   // web服务配置
      "root_directory": "/usr/share/nginx/html",   // web根目录
      "host": "https://abc.xyz"    // 通过公网访问web服务的url
    },
    "executable_path": {   // 项目所依赖的可执行文件的路径
      "chrome_driver": "D:\\chromedriver.exe"  // chrome驱动
    }
  }
}
```

<br>

### 其他必要配置

1. 百度翻译 API 的 appid 及 secret key 需要自行去百度翻译开放平台申请，参考 [百度翻译 API 接入文档](https://api.fanyi.baidu.com/product/113)
2. ALAPI 的 token 需要到 [官网](https://www.alapi.cn/) 注册，然后进入个人中心查看

<br>

### 可能不必要的配置

1. 项目中用到的 PyExecJs 模块需要 js 环境，对于 **Linux** 服务器来说，一般需要额外安装 Node.js
2. 使用 bilibili 动态通知功能，并勾选携带截图功能时，对于 **Linux** 服务器来说，返回的截图中可能无法显示中文，这是因为系统没有安装中文字体，可以参照文章 [linux字体安装与卸载](https://www.jianshu.com/p/59fca91ac0cc) 进行字体安装（推荐安装本项目中 **resource/font** 目录下的 WenQuanYi Micro Hei.ttf）
3. 使用 bilibili 动态通知功能，并勾选携带截图功能时，项目中用到 selenium + chrome 驱动进行爬虫任务，因此不论是 Windows 还是 Linux，都需要下载 chrome 浏览器及**对应版本**的 chrome 驱动，并配置 `misc -> executable_path -> chrome_driver` 为驱动路径
   -  Windows 下：下载 chrome 浏览器，在其中访问 [设置页面](chrome://settings/help)，查看版本号，再到 [驱动下载网站](https://npm.taobao.org/mirrors/chromedriver/) 下载对应版本的驱动压缩包并解压
   -  Linux 下：参考 [CSDN 文章](https://blog.csdn.net/qq_42396168/article/details/89784436)
4. 使用积分兑换，且兑换物类型为 voice 时，需要配置 `misc -> web`，其中 `root_directory` 为服务器 web 服务的根目录，`host` 为通过公网访问 web 服务的 url

<br>

## 废弃提案

1. ~~AI对话 —— 图灵机器人api~~（要钱）

2. ~~图片文字识别~~（qq 自带提取图片功能，没必要造轮子）

<br>

## TODO

- [ ] 抽卡
- [ ] 题库
- [ ] 科幻片、科幻小说安利功能

<br>

## 鸣谢

- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [XUN_bot](https://github.com/Angel-Hair/XUN_Bot)：参考了一些有趣的想法
- [zhenxun_bot](https://github.com/HibiKier/zhenxun_bot)：参考了一些有趣的想法，并借了一些语音包（
