# Zstack api Package
## Conditions of Use

    1.zstack0.6版本以上
    2.ansible 1.9版本
    3.宿主机需要安装python-libguestfs
    4.评估宿主机的资源情况

---
## Configuration
### config.ini
    1.config.ini
        1.zstack的api url
          zstack用户名和密码(sha512加密过的)
        2.拥有模板的map关系
          模板名字和模板uuid的名字map关系
        3.宿主机的宿主机uuid map关系
          目前只能添加一项
        4.zone和uuid的map关系
          目前只能添加一项
        5.cluster和uuid的map关系
          目前只能添加一项
        6.defaultL3网络和uuid的map关系
          目前只能添加一项
        7.L3网络和uuid的map关系
          目前只能添加一项
        8.instanceoffering和uuid的map关系
          目前只能添加一项

### Example

        [zstack]
        url = http://192.168.200.205:8080/zstack/api/
        url_result = http://192.168.200.205:8080/zstack/api/result/
        name = xxxxxx
        password = xxxxxxx

        [template]
        t-php55.xhj.com.tml = 0fab418bc62d4d49bea5d5bb586eac56
        t-php56.xhj.com.tml = db5e3a4a34764bc0a30146f1cdf680f6
        t-node0.xhj.com.tml = 50d8be1f659e4aed9299cb026946d91a
        t-node4.xhj.com.tml = c7d344bb95574505ba082f75de66cddc
        t-mmysql.xhj.com.tml = 144c4a4579844aa9a8b7e0a3ef9328e9
        t-smysql.xhj.com.tml = f9122ea714904e03ab7bc5c63c371ec1
        t-redis.xhj.com.tml = bd3e5d73c40044e3a5f02701861e6b31
        t-mongo.xhj.com.tml = eb4d2efe2aeb43638a02797e382a9b30
        t-inproxy.xhj.com.tml = bd6229a6cc75444d86d7c0e7ee2a107f
        t-outproxy.xhj.com.tml = 3f757d39fd0d44e7bd4a9b78b2bd9fe1
        t-es-mq.xhj.com.tml = 5643e5408bfc49de880acb93d9b3735e
        t-jenkins.xhj.com.tml = 1cefe8969472418ab88fe9bfab9a689e

        [kvmhost]
        yn-kvm-202-50.xhj.com = 5cd21a449e404e26b0bea5c773118991

        [zone]
        zone1 = 09964ba240f84d97b92d4f377049b52b

        [cluster]
        cluster1 = 1ffabf07d65c462480cf20d6cf1bf9fc

        [L3m]
        L3202 = 5c6f59ec81ba4313a3da7dee30e7c6db

        [L3s]
        L3202 = 7dcf25944e834f3e9b75251d826fba3a

        [instanceoffering]
        4cpu6G = 0d681e7c53ba40f2a04304484b7def9b
        #2cpu2G = 1431dfe5a02d474c95be19accc330c93


---
### config.yml

    1.config.yml
     创建主机配置的参数
     需要多少台就配置多少台
     参数:
         hostname
         ip
         模板名称
         描述信息


### Example

    host1:
        name: f80-php55.xhj.com
        ip: 192.168.202.81
        template: t-php55.xhj.com.tml
        description: feature80 测试环境 192.168.202.81
    host2:
        name: f80-php56.xhj.com
        ip: 192.168.202.82
        template: t-php56.xhj.com.tml
        description: feature80 测试环境 192.168.202.82
    host3:
        name: f80-node0.xhj.com
        ip: 192.168.202.83
        template: t-node0.xhj.com.tml
        description: feature80 测试环境 192.168.202.83
    host4:
        name: f80-node4.xhj.com
        ip: 192.168.202.84
        template: t-node4.xhj.com.tml
        description: feature80 测试环境 192.168.202.84

    注意:模板名字填写不正确在config.ini不存在创建不成功,IP不能冲突

---
## Execute program

    time python main.py
    注意:主机资源不够的情况下会自动退出做好映射关系



---
## 流程如下:
#### 代码逻辑:
![程序流程](http://blogmingling.oss-cn-shanghai.aliyuncs.com/%E6%9C%8D%E5%8A%A1/zk.jpg)
#### 操作步骤:
![操作流程](http://blogmingling.oss-cn-shanghai.aliyuncs.com/%E6%9C%8D%E5%8A%A1/zk_op.jpg)


