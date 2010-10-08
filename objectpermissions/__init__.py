__version_info__ = {
    'major': 0,
    'minor': 3,
    'micro': 3,
    'releaselevel': 'final',
    'serial': 0
}

def get_version():
    vers = ["%(major)i.%(minor)i" % __version_info__, ]

    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final':
        vers.append('%(releaselevel)s%(serial)i' % __version_info__)
    return ''.join(vers)

__version__ = get_version()

try:
    from registration import register, AlreadyRegistered
    from models import UnknownPermission

    __all__ = ('register', 'AlreadyRegistered', 'UnknownPermission')
except ImportError:
    pass
