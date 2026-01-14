"""
Configuration loader utility for the documentation analysis tool.
"""
import yaml
import json
from typing import Dict, Any, Union
from pathlib import Path


class ConfigLoader:
    """
    Utility class to load and manage configuration for the documentation analysis tool.
    """
    
    DEFAULT_CONFIG = {
        "processing": {
            "max_file_size": "10MB",
            "supported_formats": ["md", "html", "pdf", "txt"],
            "max_total_size": "100MB"
        },
        "output": {
            "format": "yaml",
            "include_traceability": True,
            "priority_threshold": "P2"
        },
        "nlp": {
            "model": "en_core_web_sm",
            "accuracy_threshold": 0.8
        }
    }
    
    def __init__(self, config_path: str = None):
        """
        Initialize the configuration loader.
        
        Args:
            config_path: Path to the configuration file (optional)
        """
        if config_path and Path(config_path).exists():
            self.config = self.load_config(config_path)
        else:
            self.config = self.DEFAULT_CONFIG.copy()
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from a file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Dictionary containing the configuration
        """
        config_path = Path(config_path)
        
        if config_path.suffix.lower() in ['.yaml', '.yml']:
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        elif config_path.suffix.lower() == '.json':
            with open(config_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            raise ValueError(f"Unsupported config file format: {config_path.suffix}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Key in dot notation (e.g., 'processing.max_file_size')
            default: Default value if key is not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value using dot notation.
        
        Args:
            key: Key in dot notation (e.g., 'processing.max_file_size')
            value: Value to set
        """
        keys = key.split('.')
        config_ref = self.config
        
        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]
        
        config_ref[keys[-1]] = value
    
    def validate_config(self) -> bool:
        """
        Validate the configuration values.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        # Validate processing settings
        processing = self.config.get('processing', {})
        if not isinstance(processing, dict):
            raise ValueError("Processing configuration must be a dictionary")
        
        supported_formats = processing.get('supported_formats', [])
        if not isinstance(supported_formats, list) or not all(isinstance(fmt, str) for fmt in supported_formats):
            raise ValueError("Supported formats must be a list of strings")
        
        # Validate output settings
        output = self.config.get('output', {})
        if not isinstance(output, dict):
            raise ValueError("Output configuration must be a dictionary")
        
        output_format = output.get('format', 'yaml')
        if output_format not in ['yaml', 'json']:
            raise ValueError("Output format must be either 'yaml' or 'json'")
        
        priority_threshold = output.get('priority_threshold', 'P2')
        if priority_threshold not in ['P1', 'P2', 'P3']:
            raise ValueError("Priority threshold must be one of 'P1', 'P2', or 'P3'")
        
        # Validate NLP settings
        nlp = self.config.get('nlp', {})
        if not isinstance(nlp, dict):
            raise ValueError("NLP configuration must be a dictionary")
        
        accuracy_threshold = nlp.get('accuracy_threshold', 0.8)
        if not isinstance(accuracy_threshold, (int, float)) or not 0 <= accuracy_threshold <= 1:
            raise ValueError("Accuracy threshold must be a number between 0 and 1")
        
        return True