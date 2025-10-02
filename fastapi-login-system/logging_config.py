# logging_config.py
import warnings
from logging.config import dictConfig

def configure_logging():
    """Configure application logging and warning filters."""
    
    # Disable all Pydantic V2 deprecation warnings
    warnings.filterwarnings("ignore", 
                          message="Valid config keys have changed in V2",
                          category=UserWarning,
                          module="pydantic")
    
    # Configure structured logging
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'minimal': {
                'format': '%(message)s'
            },
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'minimal',
                'level': 'INFO',
                'stream': 'ext://sys.stdout'
            },
            'error_console': {
                'class': 'logging.StreamHandler',
                'formatter': 'detailed',
                'level': 'WARNING',
                'stream': 'ext://sys.stderr'
            }
        },
        'loggers': {
            'uvicorn': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False
            },
            'uvicorn.error': {
                'handlers': ['error_console'],
                'level': 'WARNING',
                'propagate': False
            },
            'uvicorn.access': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False
            },
            'sqlalchemy': {
                'level': 'WARNING',
                'handlers': ['error_console'],
                'propagate': False
            },
            'sqlalchemy.engine': {
                'level': 'ERROR',
                'handlers': ['error_console'],
                'propagate': False
            }
        },
        'root': {
            'level': 'WARNING',
            'handlers': ['console', 'error_console']
        }
    })

    # Additional safety for Pydantic warnings
    warnings.simplefilter("ignore", category=UserWarning)