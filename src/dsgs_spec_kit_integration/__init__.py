"""
DSGS与spec.kit整合项目 - 项目的主入口点
"""
from .core import (
    CommandParser,
    SkillMapper,
    PythonBridge,
    SkillExecutor,
    CommandHandler,
    InteractiveShell,
    CliDetector,
    ConfigGenerator,
    IntegrationValidator,
    AutoConfigurator,
    PlatformUtils
)

__version__ = "0.2.0"
__all__ = [
    'CommandParser',
    'SkillMapper',
    'PythonBridge',
    'SkillExecutor',
    'CommandHandler',
    'InteractiveShell',
    'CliDetector',
    'ConfigGenerator',
    'IntegrationValidator',
    'AutoConfigurator',
    'PlatformUtils'
]