#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: zhuima
# zhuima @ 2017-02-15 11:01:19
# Function:
"""
参考文档:
    https://github.com/nagexiucai/openstack/blob/55c71a27427ecae76db09f9274f5f6edfa16f176/core/virtedit.py
    http://libguestfs.org/guestfs-python.3.html


接收三个参数:
    imagename
        镜像名称，绝对路径
    localfile
        宿主机上的文件，绝对路径
    remotefile
        guest os上的文件，一般是一一对应的， 绝对路径

需要注意事项:
    1、么有容错
    2、远程调用问题
        调用ansible playbook api接口解决该问题
"""

import sys
import guestfs


class Upload(object):
    def __init__(self, imagename, diskformat="qcow2"):
        self.imagename = imagename
        self.diskformat = diskformat

    def sync(self, localfile, remotefile):
        g = guestfs.GuestFS(python_return_dict=True)
        g.add_drive_opts(self.imagename,
                         format=self.diskformat,
                         readonly=False)
        g.launch()
        g.inspect_os()
        ROOT = g.inspect_get_roots()  #['/dev/sda3']
        g.inspect_get_mountpoints(
            ROOT[0])  #{'/boot': '/dev/sda1', '/': '/dev/sda3'}
        g.inspect_get_filesystems(
            ROOT[0])  #['/dev/sda3', '/dev/sda1', '/dev/sda2']
        g.mount(ROOT[0], '/')
        g.upload(localfile, remotefile)
        g.shutdown()
        g.close()


def main():
    #imagename = "{0}{1}".format("/var/lib/libvirt/images/", sys.argv[1])
    imagename = sys.argv[1]
    localfile = sys.argv[2]
    remotefile = sys.argv[3]
    p2v = Upload(imagename)
    p2v.sync(localfile, remotefile)


if __name__ == '__main__':
    sys.exit(int(main() or 0))
