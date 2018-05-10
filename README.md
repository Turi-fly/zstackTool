# zstackTool
## Conditions of Use

    1.zstack2.0版本以上
    2.ansible 2.4版本以上
    3.宿主机需要安装python-libguestfs
    4.评估宿主机的资源情况

---
## Configuration
### config.ini

    1.key 'url": zstack api url
    2.key 'result_url': zstack api url_result
    3.key 'admin': zstack login user
    4.key 'password': zstack login user password (sha 512  encryption)
    5.key 'user': host machine ssh user
    6.key 'passwd': host machine ssh user password

### config.yml
    host1:                                  #section name              note:'section can not repeat'
       name: xxxxxxxxxxxxxxxxxxx            #name                      note:'zstack platform instance name and linux hostname'
       ip: 192.168.xxx.xx                   #ip                        note:'zstack platform ip address and linux ip address'
       offering: xxxxxxxx                   #offering                  note:'zstack platform instance offering name'
       template: xxxxxxxxxxxxxxxxxx         #template                  note:'zstack platform mirror template'
       l3network: xxxxxxxx                  #l3network                 note:'zstack platform l3network name'
       host:                                #host                      note:'zstack platform host machine name'
       zone: xxxxx                          #zone                      note:'zstack platform zone name'
       cluster: xxxxx                       #cluster                   note:'zstack platform cluster name'
       description: xxxxxxxx                #description               note:'zstack platform description comment'

### Example:
    config.ini:
        [zstack]
        url = http://192.168.xxx.xxx:8080/zstack/api/                           #zstack api地址
        url_result = http://192.168.xxx.xxx:8080/zstack/api/result/             #zstack api结果地址
        username = admin                                                        #zstack 用户名
        password = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #zstack 密码
        user = root                                                             #宿主机的ssh用户名
        passwd = xxxxxxxxxxxx                                                   #宿主机的密码

    config.yml:
        host1:
           name:  xxxxxxxxxxxxxxxxx
           ip: 192.168.xxx.xx
           offering: 8core8g
           template: Template-CentOS6.7
           l3network: vlan1120
           host: xxxxxxxxx
           zone: xxxxxx
           cluster: xxxxxx
           description: xxxxx

        host2:
           name:  xxxxxxxxxxxxxxxxx
           ip: 192.168.xxx.xx
           offering: 8core8g
           template: Template-CentOS6.7
           l3network: vlan1120
           host: xxxxxxxxx
           zone: xxxxxx
           cluster: xxxxxx
           description: xxxxx

---
## Usage
    $ pip install -r requirements.txt
    $ python main.py
