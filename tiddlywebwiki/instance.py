instance_config = {
    'system_plugins': ['tiddlywebwiki'],
    'twanager_plugins': ['tiddlywebwiki']
}

store_contents = {
    'system': [
        'http://svn.tiddlywiki.org/Trunk/verticals/TiddlyWebWiki/index.recipe'
    ]
}

store_structure = {
    'bags': {
        'system': {
            'desc': 'TiddlyWebWiki client plugins',
            'policy': {
                'read': [],
                'write': ['R:ADMIN'],
                'create': ['R:ADMIN'],
                'delete': ['R:ADMIN'],
                'manage': ['R:ADMIN'],
                'accept': ['R:ADMIN'],
                'owner': 'administrator' # XXX: meaningless?
            }
        },
        'common': {
            'desc': 'shared content',
            'policy': {
                'read': [],
                'delete': ['R:ADMIN'],
                'manage': ['R:ADMIN'],
                'owner': 'administrator' # XXX: meaningless?
            }
        }
    },
    'recipes': {
        'default': {
            'desc': 'standard TiddlyWebWiki environment',
            'recipe': [
                ('system', ''),
                ('common', '')
            ],
            'policy': {
                'read': [],
                'write': ['R:ADMIN'],
                'manage': ['R:ADMIN'],
                'delete': ['R:ADMIN'],
                'owner': 'administrator' # XXX: meaningless?
            }
        }
    },
    'users': {
        'administrator': { # XXX: DEBUG; for demo purposes only
            'note': 'system administrator',
            'roles': ['ADMIN']
        }
    }
}
