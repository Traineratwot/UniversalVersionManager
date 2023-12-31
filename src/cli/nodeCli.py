from sys import exit

from cement import Controller, ex

from src.lang import _
from src.utils import isInstalled, install

_node = None


def node():
    if not isInstalled():
        if not install():
            exit(1)
        pass
    from src.service.Node import Node
    return Node()


class NodeCli(Controller):
    """Cli node"""

    class Meta:
        aliases = ['n']
        label = 'node'
        title = _('meta.title', "NODE")
        stacked_type = 'nested'

    @ex(hide=True)
    def _default(self):
        if isInstalled():
            self._parser.print_help()
            exit(0)
        else:
            install()

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    @ex(
        help=_("help.use"),
        aliases=['u'],
        arguments=[
            (['version'], {"help": _("help.use"), 'nargs': "?"}),
        ]
    )
    def use(self):
        print(node().use(self.app.pargs))
        pass

    @ex(
        help=_("help.off"),
        arguments=[
            (['version'], {"help": _("help.off"), }),
        ]
    )
    def off(self):
        print(node().off(self.app.pargs))
        pass

    @ex(
        help=_("help.list"),
        aliases=['l']
    )
    def list(self):
        print(node().list(self.app.pargs))
        pass

    @ex(
        help=_("help.install"),
        aliases=['i'],
        arguments=[
            (['version'], {"help": _("help.install"), }),
        ]
    )
    def install(self):
        print(node().install(self.app.pargs))
        pass

    @ex(
        help=_("help.remove"),
        arguments=[
            (['version'], {"help": _("help.remove"), }),
        ]
    )
    def remove(self):
        print(node().remove(self.app.pargs))
        pass

    @ex(
        help=_("help.path"),
        aliases=['p'],
        arguments=[
            (['version'], {"help": _("help.path"), 'nargs': "?"}),
        ]
    )
    def path(self):
        print(node().path(self.app.pargs))
        pass

    @ex(
        help=_("help.search"),
        aliases=['s'],
        arguments=[
            (['version'], {"help": _("help.search"), 'nargs': "?"}),
        ]
    )
    def search(self):
        print(node().search(self.app.pargs))
        pass

    @ex(
        aliases=['g'],
        help=_("help.addGlobal"),
        label="global",
        arguments=[
            (['packages'], {"help": _("help.addGlobal"), 'nargs': "*"}),
        ]
    )
    def addGlobal(self):
        print(node().addGlobal(self.app.pargs))
        pass
