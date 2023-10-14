from sys import exit

from cement import Controller, ex

from src.lang import _
from src.utils import isInstalled, install


def php():
    if not isInstalled():
        if not install():
            exit(1)
        pass
    from src.service.Php import Php
    return Php()


class PhpCli(Controller):
    class Meta:
        aliases = ['p']
        label = 'php'
        title = _('meta.title', "PHP")
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
        print(php().use(self.app.pargs))
        pass

    @ex(
        help=_("help.off"),
        arguments=[
            (['version'], {"help": _("help.off"), }),
        ]
    )
    def off(self):
        print(php().off(self.app.pargs))
        pass

    @ex(
        aliases=['l'],
        help=_("help.list")
    )
    def list(self):
        print(php().list(self.app.pargs))
        pass

    @ex(
        help=_("help.install"),
        aliases=['i'],
        arguments=[
            (['version'], {"help": _("help.install"), }),
        ]
    )
    def install(self):
        print(php().install(self.app.pargs))
        pass

    @ex(
        help=_("help.remove"),

        arguments=[
            (['version'], {"help": _("help.remove"), }),
        ]
    )
    def remove(self):
        print(php().remove(self.app.pargs))
        pass

    @ex(
        help=_("help.path"),
        aliases=['p'],
        arguments=[
            (['version'], {"help": _("help.path"), 'nargs': "?" }),
        ]
    )
    def path(self):
        print(php().path(self.app.pargs))
        pass

    @ex(
        help=_("help.search"),
        aliases=['s'],
        arguments=[
            (['version'], {"help": _("help.search"), 'nargs': "?"}),
        ]
    )
    def search(self):
        print(php().search(self.app.pargs))
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
        print(php().addGlobal(self.app.pargs))
        pass
