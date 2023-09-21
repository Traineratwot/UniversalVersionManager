from version_parser import Version

from utils import strToVersion

print(Version(strToVersion('20.1')) > Version(strToVersion('19.9.8')))
