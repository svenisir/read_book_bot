import sys

logging_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default':  {
            'format': '[{asctime}] #{levelname:8} {filename}:'
                      '{lineno} - {name}:{funcName} - {message} - 1',
            'style': '{'
        }
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'user_handlers': {
            'level': 'DEBUG',
            'handlers': ['default']
        }
    },
    'root': {
        'formatter': 'default',
        'handlers': ['default'],
        'level': 'DEBUG'
    }
}