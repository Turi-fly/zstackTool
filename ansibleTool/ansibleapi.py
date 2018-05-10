#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: zhuima
# zhuima @ 2017-02-15 11:01:19
# Function:
"""
USAGE:

    python kansible_api.py xxxyaml  hostname phost
    xxxyaml:
        palybook yaml file
    hostname:
        to yaml file
        use find guest os image path for remote KVM  physical host
    phost:
        remote KVM  physical host

"""

import os
# import sys
# import ansible.runner

from ansible.playbook import PlayBook
from ansible import callbacks, utils

API_DIR = os.path.dirname(os.path.abspath(__file__))
ANSIBLE_DIR = os.path.join(API_DIR, 'playbooks')


class MyPlaybook(object):
    """
    this is my playbook object for execute playbook.
    """

    def __init__(self, *args, **kwargs):
        super(MyPlaybook, self).__init__(*args, **kwargs)

    def run(self, playbook_relational_path, extra_vars=None):
        """
        run ansible playbook,
        only surport relational path.
        """
        stats = callbacks.AggregateStats()
        playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        runner_cb = callbacks.PlaybookRunnerCallbacks(stats,
                                                      verbose=utils.VERBOSITY)
        playbook_path = os.path.join(ANSIBLE_DIR, playbook_relational_path)

        pb = PlayBook(playbook=playbook_path,
                      stats=stats,
                      callbacks=playbook_cb,
                      runner_callbacks=runner_cb,
                      extra_vars=extra_vars,
                      check=False)

        results = pb.run()
        print results
        return results


'''
测试程序
def main():
   extra_vars = {
              "imagename": "/home/kvm/images/rootVolumes/acct-36c27e8ff05c4780bf6d2fa65700f22e/vol-323011911119463aa7692a66303db36b/323011911119463aa7692a66303db36b.qcow2",
              "hostname": "test-vm-101",
              "phost": "192.168.202.50",
            }
   myplaybook = MyPlaybook()
   myplaybook.run("uploadfile2vm.yaml", extra_vars)
'''

if __name__ == '__main__':
   # main()
   pass
