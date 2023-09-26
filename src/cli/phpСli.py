from cement import Controller, ex

from src.lang import _


class PhpCli(Controller):
    class Meta:
        label = 'php'
        title = 'NODE'
        stacked_type = 'nested'

    @ex(
        help=_("help.use"),
        arguments=[
            (['-b'],
             {'help': 'cmd1 b option'}),
        ]
    )
    def use(self):
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
