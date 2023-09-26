import sys

from cement import Controller, ex

from src.lang import _
from src.service.Php import Php

php = None
if 'php' in sys.argv and not php:
    php = Php()


class PhpCli(Controller):
    class Meta:
        label = 'php'
        title = 'NODE'
        stacked_type = 'nested'

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def _default(self):
        print(self.app.pargs)

    @ex(
        help=_("help.use"),
        arguments=[
            (['version'], {"help": _("help.use"), 'nargs': "?"}),
        ]
    )
    def use(self):
        print(php.use(self.app.pargs))
        pass

    @ex(
        help=_("help.off"),
        arguments=[
            (['version'], {"help": _("help.off"), 'nargs': 1}),
        ]
    )
    def off(self):
        print(php.off(self.app.pargs))
        pass

    @ex(
        help=_("help.list"),
        arguments=[
            (['version'], {"help": _("help.list"), 'nargs': 1}),
        ]
    )
    def list(self):
        print(php.list(self.app.pargs))
        pass

    @ex(
        help=_("help.install"),
        arguments=[
            (['version'], {"help": _("help.install"), 'nargs': 1}),
        ]
    )
    def install(self):
        print(php.install(self.app.pargs))
        pass

    @ex(
        help=_("help.remove"),
        arguments=[
            (['version'], {"help": _("help.remove"), 'nargs': 1}),
        ]
    )
    def remove(self):
        print(php.remove(self.app.pargs))
        pass

    @ex(
        help=_("help.path"),
        arguments=[
            (['version'], {"help": _("help.path"), 'nargs': 1}),
        ]
    )
    def path(self):
        print(php.path(self.app.pargs))
        pass

    @ex(
        help=_("help.search"),
        arguments=[
            (['version'], {"help": _("help.search"), 'nargs': "?"}),
        ]
    )
    def search(self):
        print(php.search(self.app.pargs))
        pass
