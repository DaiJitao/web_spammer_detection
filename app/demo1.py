from oslo_config import cfg
from oslo_config import types
import sys

CONF = cfg.CONF

# 定义组
keystone_authtoken = cfg.OptGroup(name='keystone_authtoken', title='keystone_authtoken options')

# 自定义类型和范围
PortType = types.Integer(1, 65535)

# 定义配置文件中的值K/V,可以设置默认值
opts = [
    # 定义了一个Str类型的选项,名字是bind_host，默认值是0.0.0.0，还有帮助信息，用的是Opt的子类来定义的，所以无需指定类类型，因为类型已经定下来了就是Str类型（StrOpt）
    cfg.StrOpt('bind_host', default='0.0.0.0', help = 'help info'),
# 使用Opt类来定义一个选项，因为用的是基类，类型可以是任意的，所以需要使用type字段明确其类型，使用这种方式的好处我觉得就是可以定制类型的值范围
cfg.Opt('bind_port', default=9292, type=PortType),
]




keystone_opts = [

    cfg.StrOpt('auth_uri', default='http://controller:5000'),
    cfg.StrOpt('auth_url', help='Parameter can not be empty'),
    cfg.StrOpt('memcached_servers', help='Parameter can not be empty'),
    cfg.StrOpt('auth_type', help='Parameter can not be empty')
]

# 参数不解释-h就能看出参数的意义
cli_opts = [
    cfg.BoolOpt('verbose',
                short='v',
                default=False,
                help='Print more verbose output.'),
    cfg.BoolOpt('debug',
                short='d',
                default=False,
                help='Print debugging output.'),
]


# 定义完成参数,必须注册才可以使用
def add_register():
    # 默认组就default,这里的group指定就是配置文件的[default]这个
    CONF.register_opts(opts)
    # 这么写就可以不用事先定义group自己就会创建,group='keystone_authtoken'
    CONF.register_opts(keystone_opts, group='keystone_authtoken')

    # 注册cli命令,可以用-h查看效果
    CONF.register_cli_opts(cli_opts)


def start():
    add_register()
    # 配置文件路径['glance-api.conf']绝对相对都可以.一般这样用CONF(sys.argv[1:]  --config-dir
    CONF(default_config_files=['glance-api.conf'])
    # CONF(sys.argv[1:])


if __name__ == '__main__':
    #
    CONF = cfg.CONF
    start()
    print(CONF.bind_port, CONF.bind_host, CONF.keystone_authtoken.auth_uri)