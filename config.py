FOLDER_NAME = 'dst/files'

DOCKER_ALIAS = {
    # Pacitan Unit 1
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
    'read_write_pct1': {
        'name': 'OPC Read-Write',
        'restart-required': True,
    },
    'soket-bat-pct1': {
        'name': 'SOPT Backend Service',
        'restart-required': True,
    },
    
    # Rembang Unit1 (20)
    'bat-fuse-rbg1': {
        'name': 'UI Service',
        'restart-required': False,
    },
    'soket-bat-rbg1': {
        'name': 'SOPT Backend Service',
        'restart-required': True,
    },
    'services-combustion-rbg1': {
        'name': 'COPT Backend Service',
        'restart-required': True,
    },
    'scheduler-combustion-rbg1': {
        'name': 'COPT Scheduler',
        'restart-required': False,
    },
    'ml-runner-rbg1': {
        'name': 'COPT Machine Learning',
        'restart-required': False,
    },
    
    # Rembang Unit2 (10)
    'bat-fuse-rbg2': {
        'name': 'UI Service',
        'restart-required': False,
    },
    'soket-bat-rbg2': {
        'name': 'SOPT Backend Service',
        'restart-required': True,
    },
    'services-combustion-rbg2': {
        'name': 'COPT Backend Service',
        'restart-required': True,
    },
    'scheduler-combustion-rbg2': {
        'name': 'COPT Scheduler',
        'restart-required': False,
    },
    'ml-runner-rbg2': {
        'name': 'COPT Machine Learning',
        'restart-required': False,
    },
    
    # Universal
    'subs_async_ich': {
        'name': 'OPC Read',
        'restart-required': True,
    },
    'write': {
        'name': 'OPC Write SOPT',
        'restart-required': True,
    },
    'write_copt': {
        'name': 'OPC Write COPT',
        'restart-required': True,
    },
    'watchdog': {
        'name': 'Watchdog',
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
