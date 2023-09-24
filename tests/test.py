from version_parser import Version

from utils import strToVersion

print(Version(strToVersion('20')) > Version(strToVersion('20.9.8')))
