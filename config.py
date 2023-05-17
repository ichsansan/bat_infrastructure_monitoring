FOLDER_NAME = 'dst/files'

# Database
DATABASE_CONNECTION = {
    'IP': '0.0.0.0',
    'PORT': '3306',
}

DOCKER_ALIAS = {
    # TJA Unit 1
    'bat-fuse-tja1': {
        'name': 'UI Service',
        'restart-required': False,
    },
    'soket-bat-tja1': {
        'name': 'SOPT Backend Service',
        'restart-required': False,
    },
    'comb-service-tja1': {
        'name': 'COPT Backend Service',
        'restart-required': False,
    },
    'sokket-bat-opc-read': {
        'name': 'OPC Read',
        'restart-required': True,
    },
    'subs': {
        'name': 'OPC Read',
        'restart-required': False,
    },
    'opc-write-copt': {
        'name': 'OPC Write COPT',
        'restart-required': True,
    },
    'sokket-bat-raw-read': {
        'name': 'OPC Read',
        'restart-required': False,
    },
    'ml-runner': {
        'name': 'COPT Machine Learning',
        'restart-required': False,
    },
    'comb-scheduler-tja1': {
        'name': 'COPT Scheduler',
        'restart-required': False,
    },
    
    
    # TJA Unit 2
    'bat-fuse-tja2': {
        'name': 'UI Service',
        'restart-required': False,
    },
    'soket-bat-tja2': {
        'name': 'SOPT Backend Service',
        'restart-required': False,
    },
    'comb-service-tja2': {
        'name': 'COPT Backend Service',
        'restart-required': False,
    },
    'ml-runner': {
        'name': 'COPT Machine Learning',
        'restart-required': False,
    },
    'opc-write-copt': {
        'name': 'OPC Write COPT',
        'restart-required': True,
    },
    'sokket-bat-opc-read': {
        'name': 'OPC Read',
        'restart-required': True,
    },
    'comb-scheduler-tja2': {
        'name': 'COPT Scheduler',
        'restart-required': False,
    },
    
    
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
    'write-copt-pct1': {
        'name': 'OPC Write for COPT',
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
        'name': 'Database System',
        'restart-required': False,
    },
    'registry': {
        'name': 'Internal Registry',
        'restart-required': False,
    }
}
