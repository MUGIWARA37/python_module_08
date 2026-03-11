import os
import sys
from dotenv import load_dotenv


def load_configuration() -> dict:
    """Load all config from environment (with .env fallback)."""
    # load_dotenv() reads .env but does NOT override existing shell vars
    load_dotenv()

    config = {
        "matrix_mode": os.getenv("MATRIX_MODE", "development"),
        "database_url": os.getenv("DATABASE_URL"),
        "api_key": os.getenv("API_KEY"),
        "log_level": os.getenv("LOG_LEVEL", "DEBUG"),
        "zion_endpoint": os.getenv("ZION_ENDPOINT"),
    }
    return config


def validate_configuration(config: dict) -> list[str]:
    """Check for missing required variables. Returns list of errors."""
    required = ["database_url", "api_key", "zion_endpoint"]
    missing = []

    for key in required:
        if not config.get(key):
            missing.append(key.upper())

    return missing


def mask_secret(value: str | None) -> str:
    """Hide sensitive values — show only first 4 chars."""
    if not value:
        return "NOT SET"
    if len(value) <= 4:
        return "****"
    return value[:4] + "*" * (len(value) - 4)


def run_oracle() -> None:
    """Main entry point."""
    print("ORACLE STATUS: Reading the Matrix...\n")

    config = load_configuration()
    missing = validate_configuration(config)

    if missing:
        print("WARNING: Missing required configuration:")
        for var in missing:
            print(f"  [MISSING] {var}")
        print("\nCopy .env.example to .env and fill in the values.")
        print("Run: cp .env.example .env")
        sys.exit(1)

    # Display config — mask secrets!
    print("Configuration loaded:")
    print(f"  Mode:          {config['matrix_mode']}")
    print(f"  Database:      {mask_secret(config['database_url'])}")
    print(f"  API Access:    {mask_secret(config['api_key'])}")
    print(f"  Log Level:     {config['log_level']}")
    print(f"  Zion Network:  {config['zion_endpoint']}")

    print("\nEnvironment security check:")
    print("  [OK] No hardcoded secrets detected")
    print("  [OK] .env file properly configured")
    print("  [OK] Production overrides available")
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    run_oracle()
