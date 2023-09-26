from cement import Controller, ex

from src.lang import _
from src.service.Node import Node


class NodeCli(Controller):
    """Cli node"""

    class Meta:
        label = 'node'
        title = 'NODE'
        stacked_type = 'nested'

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.node = Node()

    @ex(
        help=_("help.use"),
        arguments=[
            (['version'], {"help": _("help.version"), 'nargs': "?"}),
        ]
    )
    def use(self):
        print(self.node.use(self.app.pargs))
        pass

    @ex(
        help=_("help.off"),
    )
    def off(self):
        pass

    @ex(
        help=_("help.list"),
    )
    def list(self):
        pass

    @ex(
        help=_("help.install"),
    )
    def install(self):
        pass

    @ex(
        help=_("help.remove"),
    )
    def remove(self):
        pass

    @ex(
        help=_("help.path"),
    )
    def path(self):
        pass

    @ex(
        help=_("help.search"),
    )
    def search(self):
        pass

    @ex(
        help=_("help.addGlobal"),
    )
    def addGlobal(self):
        pass
