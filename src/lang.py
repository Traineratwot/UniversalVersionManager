import locale
import warnings

from SimpleCache2 import simple_cache

from src.cache import MEMORY

lang = {
    'ru': {
        "log.addedToPath": "Добавлено в Path '{}'",
        "log.removeToPath": "Удалено из Path '{}'",

        "err.versionNotFound": "Не удалоь найти версияю по запросу: '{}'",

        "help.use": "Выбрать версию для использования",
        "help.off": "Отменить выбор версии",
        "help.list": "Показать все доступные версии",
        "help.install": "Установить новую версию",
        "help.remove": "Удалить версию",
        "help.path": "Получить путь к исходной папке",
        "help.search": "Показывает все версии, доступные для установки",
        "help.addGlobal": "Добавить глобальный пакет во все версии, например: typescript",
        "help.service": "1 из поддерживаемых приложений",
        "help.version": "[Опционально] Желаемая версия",

        "help.base.deInstall": "Полное удаление UVM",
        "help.base.install": "Установка UVM",
        "help.base.printVersion": "Получить текущую версию ({})",
        "help.base.clearCache": "Очистить кеш",

        "ask.alternative": r"""
Найдены альтернативные установленные версии "{}".:
{}
Вы хотите заменить их?
""",
        "ask.install": r"""
Установить в "{}"? 
""",
        "ask.deInstall": "Вы действительно хотите удалить UVM?",
        "ask.OpenServer": "Желаете включить интеграцию с OpenServer?",
        "ask.newVersion": "Доступна новая версия UVМ {}. {} Желаете обновить?",
        "unknown": "Неизвестно",
        "lts": "Поддеживается",
        "arch": "Архитектура",
        "version": "Версия",
        "released": "Релиз",
        "used": "Сейчас используестя {}: {} ",
        "path": "путь",

        "meta.title": "{} Менеджер версий"

    },
    'en': {
        "log.addedToPath": "added to Path '{}'",
        "log.removeToPath": "removed from Path '{}'",

        "err.versionNotFound": "Could not find the version by : '{}'",

        "help.use": "Select version to use",
        "help.off": "Deselect version",
        "help.list": "Show all available versions",
        "help.install": "Install new version",
        "help.remove": "Remove version",
        "help.path": "get path to source folder",
        "help.search": "Shows all versions available for installation",
        "help.addGlobal": "Add a global package to all versions, for example: typescript",
        "help.service": "1 from supported applications",
        "help.version": "[Optional] Desired version",

        "help.base.deInstall": "FULL removal UVM",
        "help.base.install": "Install UVM",
        "help.base.printVersion": "Get current version ({})",
        "help.base.clearCache": "Clear cache data",

        "ask.alternative": r"""
Alternative "{}" installations have been found:
{}
Do you want to replace them?
""",
        "ask.install": r"""
Install in "{}"? 
""",
        "ask.deInstall": r"""
Do you really want to remove UVM? 
""",
        "ask.OpenServer": "Would you like to enable integration with OpenServer?",
        "ask.newVersion": "A new version of UVM {} is available. {} Would you like to update? ",
        "unknown": "Unknown",
        "lts": "Lts",
        "arch": "Arch",
        "version": "Version",
        "released": "Released",
        "used": "Now used {}: {} ",
        "path": "path",

        "meta.title": "{}  Version Manager"
    }
}


@simple_cache(MEMORY)
def get_system_language():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=DeprecationWarning)
        language_code = locale.getdefaultlocale()[0]
    if language_code:
        return language_code.split("_")[0].lower()
    return "en"


langKey = get_system_language()


def _(text: str, *args):
    if langKey in lang and text in lang[langKey]:
        if len(args):
            return lang[langKey][text].format(*args)
        return lang[langKey][text]
    return text
