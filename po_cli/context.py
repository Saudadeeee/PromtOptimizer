import json
import os
from pathlib import Path
from dotenv import set_key, load_dotenv

CONFIG_FILE = Path.home() / ".po_config.json"
ENV_FILE = Path.home() / ".po_env"

DEFAULT_CONFIG = {
    "projects": {},
    "settings": {
        "engine": "cli",
        "model": "gemini-2.5-flash"
    }
}

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

def load_config():
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        try:
            config = json.load(f)
            # Merge with default to ensure keys exist
            if "projects" not in config:
                config["projects"] = {}
            if "settings" not in config:
                config["settings"] = DEFAULT_CONFIG["settings"].copy()
            return config
        except json.JSONDecodeError:
            return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def add_project(name: str, description: str):
    config = load_config()
    config["projects"][name] = description
    save_config(config)

def remove_project(name: str) -> bool:
    config = load_config()
    if name in config["projects"]:
        del config["projects"][name]
        save_config(config)
        return True
    return False

def update_project(name: str, description: str) -> bool:
    config = load_config()
    if name in config["projects"]:
        config["projects"][name] = description
        save_config(config)
        return True
    return False

def get_project(name: str):
    config = load_config()
    return config.get("projects", {}).get(name, None)

def list_projects():
    config = load_config()
    return config.get("projects", {})

def get_config_value(key: str, default=None):
    if "API_KEY" in key.upper():
        return os.environ.get(key, default)
    config = load_config()
    return config.get("settings", {}).get(key, default)

def set_config_value(key: str, value: str):
    if "API_KEY" in key.upper():
        if not ENV_FILE.exists():
            ENV_FILE.touch()
        set_key(str(ENV_FILE), key, value)
        os.environ[key] = value
    else:
        config = load_config()
        config["settings"][key] = value
        save_config(config)

def list_configs():
    config = load_config()
    configs = config.get("settings", {})
    # Map API keys from environment variables loaded via .env
    for k, v in os.environ.items():
        if "API_KEY" in k.upper() and (str(ENV_FILE) in str(os.environ) or True):
            # Just listing known user environment keys that contain API_KEY
            # To be safer, we only read from the file directly
            pass
            
    # Better logic to list only keys stored in our ENV_FILE
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    configs[k] = v.strip("'").strip('"')
    return configs
