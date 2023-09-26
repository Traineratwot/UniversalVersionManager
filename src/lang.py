import locale
import warnings

lang = {
    'ru': {
        "help.select": "Выбрать версию для использования",
        "help.off": "Отменить выбор версии",
        "help.list": "Показать все доступные версии",
        "help.install": "Установить новую версию",
        "help.remove": "Удалить версию",
        "help.path": "Получить путь к исходной папке",
        "help.search": "Показывает все версии, доступные для установки",
        "help.addGlobal": "(node) добавить глобальный пакет во все версии, например: typescript",
        "help.service": "1 из поддерживаемых приложений",
        "help.version": "Желаемая версия",

        "unknown": "Неизвестно",
        "lts": "Поддеживается",
        "arch": "Архитектура",
        "version": "Версия",
        "released": "Релиз",
        "used": "Сейчас используестя {}: {} ",
    },
    'en': {
        "help.select": "Select version to use",
        "help.off": "Deselect version",
        "help.list": "Show all available versions",
        "help.install": "Install new version",
        "help.remove": "Remove version",
        "help.path": "get path to source folder",
        "help.search": "Shows all versions available for installation",
        "help.addGlobal": "(node) add a global package to all versions, for example: typescript",
        "help.service": "1 from supported applications",
        "help.version": "Desired version",

        "unknown": "Unknown",
        "lts": "Lts",
        "arch": "Arch",
        "version": "Version",
        "released": "Released",
        "used": "Now used {}: {} ",
    }
}


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
