# /usr/bin/env python
# encoding:utf-8


import yaml
import os

from api import zstack_tool_api


yml_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf/config.yml')


def main():
    yml_f = open(yml_file)
    try:
        dataMap = yaml.safe_load(yml_f)
        yml_f.close()
    except Exception:
        raise "your yaml file is error fomart."

    cvm = zstack_tool_api.zstack_tool_api()
    res = cvm.login()

    for conf in dataMap.values():
        cvm.create_vminstance(
            conf['name'], conf['ip'],
            conf['offering'], conf['template'],
            conf['l3network'],
            conf['host'],
            conf['zone'],
            conf['cluster'],
            conf['description'],
            res
        )
    cvm.logout(res)


if __name__ == '__main__':
    main()
