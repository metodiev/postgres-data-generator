from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import yaml
from typing import Dict

CONFIG_PATH = "config/config.yaml"

def load_config(path: str = CONFIG_PATH) -> dict:
    """Load YAML configuration for databases."""
    with open(path, "r") as f:
        return yaml.safe_load(f)

def create_db_engine(db_config: dict) -> Engine:
    """Create a SQLAlchemy engine with optional pooling settings."""
    url = (
        f"postgresql+psycopg2://{db_config['user']}:"
        f"{db_config['password']}@{db_config['host']}:"
        f"{db_config['port']}/{db_config['name']}"
    )
    # You can adjust pool_size, max_overflow, etc., as needed
    engine = create_engine(url, pool_size=10, max_overflow=20)
    return engine

def get_engines() -> Dict[str, Engine]:
    """Return SQLAlchemy engines for all databases in config."""
    cfg = load_config()
    engines = {}
    for name, db in cfg.get("databases", {}).items():
        try:
            engines[name] = create_db_engine(db)
        except Exception as e:
            print(f"Failed to create engine for {name}: {e}")
    return engines

def get_engine(db_name: str) -> Engine:
    """Return a single engine by database name."""
    engines = get_engines()
    if db_name not in engines:
        raise ValueError(f"Database '{db_name}' not found in config.")
    return engines[db_name]
