import sys

from cement import Controller, ex

from src.lang import _
from src.service.Node import Node

node = None
if 'node' in sys.argv and not node:
    node = Node()


class NodeCli(Controller):
    """Cli node"""

    class Meta:
        label = 'node'
        title = 'NODE'
        stacked_type = 'nested'

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def _default(self):
        self.use()

    @ex(
        help=_("help.use"),
        arguments=[
            (['version'], {"help": _("help.use"), 'nargs': "?"}),
        ]
    )
    def use(self):
        print(node.use(self.app.pargs))
        pass

    @ex(
        help=_("help.off"),
        arguments=[
            (['version'], {"help": _("help.off"), 'nargs': 1}),
        ]
    )
    def off(self):
        print(node.off(self.app.pargs))
        pass

    @ex(
        help=_("help.list"),
        arguments=[
            (['version'], {"help": _("help.list"), 'nargs': 1}),
        ]
    )
    def list(self):
        print(node.list(self.app.pargs))
        pass

    @ex(
        help=_("help.install"),
        arguments=[
            (['version'], {"help": _("help.install"), 'nargs': 1}),
        ]
    )
    def install(self):
        print(node.install(self.app.pargs))
        pass

    @ex(
        help=_("help.remove"),
        arguments=[
            (['version'], {"help": _("help.remove"), 'nargs': 1}),
        ]
    )
    def remove(self):
        print(node.remove(self.app.pargs))
        pass

    @ex(
        help=_("help.path"),
        arguments=[
            (['version'], {"help": _("help.path"), 'nargs': 1}),
        ]
    )
    def path(self):
        print(node.path(self.app.pargs))
        pass

    @ex(
        help=_("help.search"),
        arguments=[
            (['version'], {"help": _("help.search"), 'nargs': "?"}),
        ]
    )
    def search(self):
        print(node.search(self.app.pargs))
        pass

    @ex(
        help=_("help.addGlobal"),
        arguments=[
            (['packages'], {"help": _("help.addGlobal"), 'nargs': "+"}),
        ]
    )
    def addGlobal(self):
        print(node.addGlobal(self.app.pargs))
        pass