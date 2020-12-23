# 基于Django的服务端开发模板


### 介绍

工程为Django模板，包含一个基础的用户系统及其相关接口与管理平台，同时在本地启动后，每次修改文件支持自动热重启，同时在部署到服务器后，uwsgi也支持自动热重启，这也就意味着，当你使用一些工具，例如sublimetext的sftp工具将文件直接同步至服务器时，服务器将自动热重启，重新访问接口将看到修改后的效果，该功能可在uwsgi的配置文件中关闭。开发者若打算直接使用本工程进行开发，在修改工程名称时，需要修改多个地方，建议对Django大致有一定了解后再去修改，也可以采用自己创建工程后创建应用，然后再拷贝此项目的相关文件夹对其进行替换的方式。

### 数据库相关

工程使用的是MySQL数据库，请确保在开发前正确安装了Mysql数据库，否则请自行修改settings.py文件中的数据库配置信息，工程settings.py中包含两个版本数据库配置信息，在Debug模式启动时调用本地数据库配置，Debug模式关闭时调用服务端数据配置，主要针对本地与服务端部署时数据库配置不同的情况，所以在你将工程部署到服务端时，请将Debug模式关闭掉，数据库配置信息不正确将造成工程启动不正常的情况，当然，你也可以在服务端本地创建一个数据库用来调试用。

### 相关信息

由于Python包含多个版本，不同工程有可能使用到不同的Python版本进行开发，而且不同工程所需要的依赖库也不同，因而我们用到virtualenv进行Python的虚拟环境管理，具体信息请查阅virtualenv相关文档，同时，使用virtualenv进行虚拟环境的启动及切换相对繁琐，所以我们又用到了virtualenvwrapper来进行虚拟环境的管理切换等工作，具体信息请查阅virtualenvwrapper相关文档。

### 注意

工程下包含一个sftp-config.json的文件，该文件为sublimetext安装sftp插件后将工程文件上传到服务器所用到的配置文件，一般不上传至服务器，所以在你的工程中，请把它添加到.gitignore中，若你使用的方式为git推送后自动部署，请忽略此文件。


### 配置开发环境

1. 安装virtualenv及virtualenvwrapper
    ```bash
    pip install virutalenv virtualenvwrapper
    ```
2. 配置virtualenvwrapper
    ```bash
    # 例如MacOSX下这样配置，第一个为虚拟环境存放目录，第二个为virtualenvwrapper的脚本所在目录
    export WORKON_HOME=~/Workspace/python/.venv
    source /usr/local/bin/virtualenvwrapper.sh
    ```
3. 使用Python3.6创建一个虚拟环境
    ```bash
    mkvirtualenv dj -p python3.6
    ```
4. 切换到创建好的虚拟环境
    ```bash
    # 单独执行workon命令可查看当前有哪些虚拟环境
    workon dj
    ```
5. 安装依赖库
    ```bash
    pip install -r requirements.txt
    ```


### 配置工程

**若您修改了工程名称，请确保uwsgi目录下的xml文件名与工程名字一样，这样uwsgi的配置文件才能自动配置成功**

1. 获取管理平台静态文件
    ```bash
    python manage.py collectstatic
    ```
2. 创建数据库
    ```bash
    # 使用root用户登录数据库
    mysql -uroot -p
    # 创建数据库django
    mysql> CREATE DATABASE IF NOT EXISTS `django` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
    # 查看创建出来的数据库
    mysql> show databases;
    ```
3. 新增用户django，密码设置为123456， 并设置其对django数据库拥有所有权限
    ```bash
    mysql> grant all on django.* to django@"localhost" Identified by "123456";
    # 退出数据库
    mysql> exit
    ```
4. 数据库用户密码修改方式
    ```bash
    # 方法一
    mysqladmin -u root password oldpass "newpass"
    # 方法二
    mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('newpass');
    ```
5. 使用django用户登录数据库
    ```bash
    mysql -udjango -p django
    # 执行后应该显示为空
    mysql> show tables;
    ```
6. 创建表映射
    ```bash
    python manage.py makemigrations mauth
    ```
7. 生成删除数据库中所有表的命令，出错时重新操作，而不用整个删除数据库重新创建和分配权限
    ```bash
    mysql> SELECT CONCAT('drop table ',table_name,';') FROM information_schema.`TABLES` WHERE table_schema='django';
    ```
8. 将表映射实现到数据库中
    ```bash
    python manage.py migrate
    # 登录数据库
    mysql -udjango -p django
    # 此时应该显示出了创建好的表
    mysql> show tables;
    ```
9. 为Django管理平台创建管理用户
    ```bash
    # 用户名：admin 密码：test123456
    python manage.py createsuperuser
    ```
10. 访问管理后台网址：http://127.0.0.1:8000/admin/ 输入刚才创建的用户名密码登录


### 测试接口

1. 注册
    ```bash
    # 注册两个用户
    curl -d "username=User01&password=1234567" http://127.0.0.1:8000/auth/register/
    curl -d "username=User02&password=123456" http://127.0.0.1:8000/auth/register/
    ```
2. 登录
    ```bash
    # 获取到的token_text用于后续接口的token字段
    curl -d "username=User01&password=1234567" http://127.0.0.1:8000/auth/login/
    ```
3. 修改密码
    ```bash
    curl -X PUT -d "old_password=1234567&new_password=123456" http://127.0.0.1:8000/auth/password/?token=804920f0b7fb11e8a28538c986110fcb
    ```
4. 获取用户信息
    ```bash
    curl http://127.0.0.1:8000/auth/userinfo/?token=804920f0b7fb11e8a28538c986110fcb
    ```
5. 修改用户信息
    ```bash
    curl -X PUT -d "age=10" http://127.0.0.1:8000/auth/userinfo/?token=804920f0b7fb11e8a28538c986110fcb
    ```
6. 搜索用户
    ```bash
    curl http://127.0.0.1:8000/auth/search/?q=User01
    ```


### 工具类

**工程提供了一个工具类rzutils，包含如下功能（相关平台信息配置均在config.py文件中）**
1. 正则表达式验证
2. 权限验证
3. 错误类型
4. Http响应封装
5. 装饰器
6. 数据库模板通用方法
7. 通用视图
8. 字符串处理
9. 时间处理
10. 基于LBS的地理位置距离计算
11. 基于IP地址获取位置信息
12. 发送短信
13. 发送邮件
14. 阿里云存储
15. 微信支付
16. 微信授权获取信息
17. 高通AR目标管理
