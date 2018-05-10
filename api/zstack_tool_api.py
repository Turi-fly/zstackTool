#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import json
import ConfigParser
import os
import sys
import time
sys.path.append("..")

from ansibleTool.ansibleapi import MyPlaybook
from ansibleTool.jinjiaToconf import Createtml


class zstack_tool_api(object):

    """Docstring for zstack_tool_api. """

    def __init__(self, **kwargs):
        self.header = {"Content-Type": "application/json"}
        self.lgconf = self.load_zstack_conf()
        self.myplaybook = MyPlaybook()

    def load_zstack_conf(self):
        conf_path = os.path.join(os.path.dirname(os.getcwd()), "zstacktool/conf/config.ini")

        if not os.path.exists(conf_path):
            raise Exception("zstack config file is not exists! please filling configuration file")

        conf = ConfigParser.ConfigParser()
        conf.read(conf_path)

        if not conf.has_section('zstack'):
            raise Exception("There is no configuration file 'zstack' configuration items")

        for para in ('url', 'url_result', 'username', 'password', 'user', 'passwd'):
            if not dict(conf.items('zstack')).get(para):
                raise Exception("There is no '%s' parameter in the configuration item 'zstack'" %(para))

        return dict(conf.items('zstack'))

    def api_call(self, session_uuid, api_id, api_content):
        if session_uuid:
            api_content["session"] = {"uuid": session_uuid}

        api_body = {api_id: api_content}

        try:
            request = requests.post(self.lgconf.get('url'), data=json.dumps(api_body), headers=self.header, timeout=2)
        except Exception as e:
            return {
                'code': '1',
                'msg': 'error:%s' %(e),
                'res': '%s' %(e)
            }

        response = json.loads(request.content)

        if "result" in response.keys():
            result = json.loads(response['result'])

            if result.values()[0]['success']:
                return {
                    'code': '0',
                    'msg': '%s api request success!' %(api_id),
                    'res': result.values()[0]
                }

            return {
                'code': '1',
                'msg': '%s api request fail!' %(api_id),
                'res': result.values()[0]
            }

        return {
            'code': '0',
            'msg': '%s api request susccess!' %(api_id),
            'res': response
        }

    def login(self):
        content = {
            "accountName": self.lgconf.get('username'),
            "password": self.lgconf.get('password')
        }

        rsp = self.api_call(None, "org.zstack.header.identity.APILogInByAccountMsg", content)

        if rsp['code'] == '0':
            session_uuid = rsp['res']['inventory']['uuid']
            print "successfully login, session uuid is: %s" % session_uuid
            return {
                'code': '0',
                'msg': 'account login success!',
                'res': session_uuid
            }

        print "fail login error %s" % rsp['res']
        return {
            'code': '1',
            'msg': 'account login fail!',
            'res': rsp['res']
        }

    def query_until_done(self, job_uuid):
        request = requests.get(self.lgconf.get('url_result') + str(job_uuid))
        response = json.loads(request.content)

        if response["state"] == "Done":
            return response

        time.sleep(1)
        print "Job[uuid:%s] is still in processing" % job_uuid

        return self.query_until_done(job_uuid)

    def query_all_resource(self, instanceOffering, image, l3Network, host, cluster, zone, session_uuid):
        result = []
        uuiddict = {}
        apidict = {
            instanceOffering: 'org.zstack.header.configuration.APIQueryInstanceOfferingMsg',
            image: 'org.zstack.header.image.APIQueryImageMsg',
            l3Network: 'org.zstack.header.network.l3.APIQueryL3NetworkMsg',
            host: 'org.zstack.header.host.APIQueryHostMsg',
            cluster: 'org.zstack.header.cluster.APIQueryClusterMsg',
            zone: 'org.zstack.header.zone.APIQueryZoneMsg'
        }

        for rs in apidict:
            content = {
                "conditions": [
                    {
                        "name": "name",
                        "value": rs,
                        "op": "="
                    }
                ]
            }

            rsp = self.api_call(session_uuid, apidict[rs], content)
            if rsp['code'] == '1':
                result.append(str(rsp['res']))
                continue

            if not rsp['res']['inventories']:
                result.append(rs + ' ' + apidict[rs])
                continue

            uuiddict[rs] = rsp['res']['inventories'][0]['uuid']

        if result:
            print 'error: %s No inquiries, please check after inquiries!' %(','.join(result))
            return {
                'code': '1',
                'msg': '%s No inquiries, please check after inquiries!' %(','.join(result)),
                'res': ''
            }

        return {
            'code': '0',
            'msg': 'Configure the query new success!',
            'res': uuiddict
        }

    def query_host_by_uuid(self, hostuuid, session_uuid):

        content = {
            "conditions": [
                {
                    "name": "uuid",
                    "value": hostuuid,
                    "op": "="
                }
            ]
        }
        rsp = self.api_call(session_uuid, "org.zstack.header.host.APIQueryHostMsg", content)

        return rsp['res']['inventories'][0]['managementIp']

    def start_vminstance(self, instanceuuid, session_uuid, name):
        content = {
            "uuid": instanceuuid
        }

        rsp = self.api_call(session_uuid, "org.zstack.header.vm.APIStartVmInstanceMsg", content)

        if rsp['code'] == '0':
            job_uuid = rsp['res']['uuid']
            res = self.query_until_done(job_uuid)
            res = json.loads(res['result'])
            if res.values()[0]['success']:
                print "successfully start VmInstance and create vm successfully:%s!" %(name)
                return {'code': '0', 'msg': 'successfully start VmInstance and create vm successfully:%s!' %(name), 'res': ''}

            print "fail start VmInstance!, details:%s" %(res.values()[0])
            return {'code': '1', 'msg': 'fail start VmInstance!', 'res': res.values()[0]}

        return rsp

    def stop_vminstance(self, instanceuuid, session_uuid, name):
        content = {
            "uuid": instanceuuid
        }

        rsp = self.api_call(session_uuid, "org.zstack.header.vm.APIStopVmInstanceMsg", content)

        if rsp['code'] == '0':
            job_uuid = rsp['res']['uuid']
            res = self.query_until_done(job_uuid)
            res = json.loads(res['result'])
            if res.values()[0]['success']:
                print "successfully stop VmInstance: %s!" %(name)
                return {'code': '0', 'msg': 'successfully stop VmInstance: %s!' %(name), 'res': ''}

            print "fail stop VmInstance: %s!, details:%s" %(name, res.values()[0])
            return {'code': '1', 'msg': 'fail stop VmInstance: %s!' %(name), 'res': res.values()[0]}

        return rsp

    def create_vminstance(self, name, ip, instanceOffering, image, l3Network, host, cluster, zone, description, login_res):
        if login_res['code'] == '1':
            print login_res['res']
            return login_res

        session_uuid = login_res['res']

        res = self.query_all_resource(instanceOffering, image, l3Network, host, cluster, zone, session_uuid)
        if res['code'] == '1':
            print res['res']
            return res

        content = {
            "name": name,
            "instanceOfferingUuid": res['res'][instanceOffering],
            "imageUuid": res['res'][image],
            "l3NetworkUuids": [res['res'][l3Network]],
            "hostUuid": res['res'][host],
            "clusterUuid": res['res'][cluster],
            "zoneUuid": res['res'][zone],
            "description": description,
            "systemTags": ["staticIp::{}::{}".format(res['res'][l3Network], ip), "hostname::{}".format(name)],
        }

        rsp = self.api_call(session_uuid, "org.zstack.header.vm.APICreateVmInstanceMsg", content)

        if rsp['code'] == '0':
            job_uuid = rsp['res']['uuid']
            res = self.query_until_done(job_uuid)
            res = json.loads(res['result'])
            if res.values()[0]['success']:
                print "successfully Create VmInstance but no ip and hostname in the system: %s!" %(name)

                path = res.values()[0]['inventory']['allVolumes'][0]['installPath']
                instanceuuid = res.values()[0]['inventory']['uuid']
                hostuuid = res.values()[0]['inventory']['hostUuid']

                hostip = self.query_host_by_uuid(hostuuid, session_uuid)

                res = self.stop_vminstance(instanceuuid, session_uuid, name)
                if res['code'] == '1':
                    return res

                self.tml(name, ip)

                os.system("echo '[hosts]\n%s ansible_ssh_user=%s ansible_ssh_pass=%s'  > /etc/ansible/hosts" %(hostip, self.lgconf.get('user'), self.lgconf.get('passwd')))

                extra_vars = {
                    "imagename": path,
                    "hostname": name,
                    "phost": hostip
                }

                myplaybook = MyPlaybook()
                myplaybook.run("uploadfile2vm.yaml", extra_vars)

                res = self.start_vminstance(instanceuuid, session_uuid, name)
                if res['code'] == '1':
                    return res
                print "successfully start VmInstance and create vm successfully:%s!" %(name)
                return {'code': '0', 'msg': 'successfully start VmInstance and create vm successfully:%s!' %(name), 'res': ''}

            print "fail Create VmInstance: %s, details:%s" %(name, res.values()[0])
            return {'code': '1', 'msg': 'An operation failed', 'res': res.values()[0]}

        return rsp

    def tml(self, hostname, ip):
        for i in ["network", "ifcfg-eth0"]:
            s = Createtml(hostname, ip, os.path.join("tml", i), os.path.join("transfile", i))
            s.tmltoconf()

    def logout(self, login_res):
        if login_res['code'] == '1':
            print login_res['res']
            return login_res

        session_uuid = login_res['res']
        content = {"sessionUuid": session_uuid}
        rsp = self.api_call(None, "org.zstack.header.identity.APILogOutMsg", content)

        if rsp['code'] == '0':
            print "successfully logout!"
            return rsp

        print "fail logout!"
        return rsp


if __name__ == "__main__":
    '''测试程序
    test = zstack_tool_api()
    res = test.login()
    test.create_vminstance('ll', '192.168.200.177', '8core6G', 'person-dev-template.xhj.com-new', '上地-Vlan200', 'yn-kvm-200-6.xhj.com', '上地机房', '线下环境','xxxx', res)
    test.logout(res)
    '''
    pass
