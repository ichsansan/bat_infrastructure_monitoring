FOLDER_NAME = 'dst/files'

DOCKER_ALIAS = {
    'bat-fuse-pct1': {
        'name': 'UI Service',
        'restart-required': False,
    },
    'services-combustion-pct1': {
        'name': 'COPT Backend Service',
        'restart-required': False,
    },
    'ml-runner-pct1': {
        'name': 'COPT Machine Learning',
        'restart-required': False,
    },
    'combustion-scheduler-api-pct1': {
        'name': 'COPT Scheduler',
        'restart-required': False,
    },
    'watchdog': {
        'name': 'Watchdog',
        'restart-required': True,
    },
    'read_write_pct1': {
        'name': 'OPC Read-Write',
        'restart-required': True,
    },
    'soket-bat-pct1': {
        'name': 'SOPT Backend Service',
        'restart-required': True,
    },
    'mariadb': {
        'name': 'MariaDB',
        'restart-required': False,
    },
    'registry': {
        'name': 'Internal Registry',
        'restart-required': False,
    }
}