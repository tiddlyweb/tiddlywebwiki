"""
structure and contents of a default TiddlyWebWiki instance
"""

from tiddlywebplugins.console.instance import (
    store_structure as console_store_structure)

instance_config = {
    'system_plugins': ['tiddlywebwiki'],
    'twanager_plugins': ['tiddlywebwiki']
}

store_contents = {
        'system': ['src/tiddlywebwiki.recipe']
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
                'owner': 'administrator'
            }
        },
        'common': {
            'desc': 'shared content',
            'policy': {
                'manage': ['R:ADMIN'],
                'owner': 'administrator'
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
                'owner': 'administrator'
            }
        }
    },
    'users': {
        'administrator': {  # XXX: obsolete?
            'note': 'system administrator',
            'roles': ['ADMIN']
        }
    }
}
store_structure['bags'].update(console_store_structure['bags'])
