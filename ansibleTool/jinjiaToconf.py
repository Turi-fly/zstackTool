#! /usr/bin/env python
# encoding:utf-8

from jinja2 import Environment, FileSystemLoader, StrictUndefined
import os


class Createtml():

    """Docstring for Createtml. """

    def __init__(self, hostname, ip, template_file, output_file):
        self.hostname = hostname
        self.ip = ip
        self.gateway = "{0}.{1}".format(".".join(self.ip.split(".")[:3]), "1")
        self.template_file = template_file
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_file = os.path.join(self.base_dir, output_file)
        print self.ip, self.gateway, self.base_dir

    def tmltoconf(self):
        try:
            template_env = Environment(loader=FileSystemLoader(self.base_dir),
                                       undefined=StrictUndefined)
            tpl = template_env.get_template(self.template_file)
            render_result = tpl.render({"ip": self.ip, "hostname": self.hostname, "gateway": self.gateway}, env=None)
            with open(self.output_file, 'w') as stream:
                    stream.write(render_result)
        except Exception as e:
            raise e


if __name__ == "__main__":
    '''
    测试程序
    s = Createtml("liao", "192.168.202.21", os.path.join("tml", "network"), os.path.join("conf", "network"))
    s.tmltoconf()
    '''
    pass
