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

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def _default(self):
        self.use()

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
            (['version'], {"help": _("help.path"), }),
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
        aliases=['addglobal', 'global'],
        help=_("help.addGlobal"),
        label="add-global",
        arguments=[
            (['packages'], {"help": _("help.addGlobal"), 'nargs': "+"}),
        ]
    )
    def addGlobal(self):
        print(node().addGlobal(self.app.pargs))
        pass
