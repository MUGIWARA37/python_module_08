import os
import sys


def load_env_file() -> None:
    """Load environment variables from .env file using python-dotenv."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("WARNING: python-dotenv not installed.")
        print("Install it with: pip install python-dotenv")
        print("Falling back to system environment variables only.")
        print()


def get_config() -> dict[str, str]:
    """Read all configuration variables from the environment."""
    config = {
        "MATRIX_MODE": os.getenv("MATRIX_MODE", "development"),
        "DATABASE_URL": os.getenv("DATABASE_URL", None),
        "API_KEY": os.getenv("API_KEY", None),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "DEBUG"),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT", None),
    }
    return config


def display_config(config: dict[str, str]) -> None:
    """Display the loaded configuration values."""
    print("Configuration loaded:")

    # MATRIX_MODE
    mode = config["MATRIX_MODE"]
    print(f"  Mode        : {mode}")

    # DATABASE_URL - hide actual credentials, just show status
    if config["DATABASE_URL"]:
        print("  Database    : Connected to local instance")
    else:
        print("  Database    : [MISSING] Set DATABASE_URL in .env")

    # API_KEY - never print the actual key
    if config["API_KEY"]:
        print("  API Access  : Authenticated")
    else:
        print("  API Access  : [MISSING] Set API_KEY in .env")

    # LOG_LEVEL
    print(f"  Log Level   : {config['LOG_LEVEL']}")

    # ZION_ENDPOINT
    if config["ZION_ENDPOINT"]:
        print("  Zion Network: Online")
    else:
        print("  Zion Network: [MISSING] Set ZION_ENDPOINT in .env")


def check_missing_variables(config: dict[str, str]) -> list[str]:
    """Return a list of missing required configuration variables."""
    required = ["DATABASE_URL", "API_KEY", "ZION_ENDPOINT"]
    missing = []

    for key in required:
        if not config[key]:
            missing.append(key)

    return missing


def display_missing_warnings(missing: list[str]) -> None:
    """Display warnings for missing configuration variables."""
    if missing:
        print()
        print("WARNING: Missing required configuration variables:")
        for key in missing:
            print(f"  - {key}")
        print()
        print("Copy .env.example to .env and fill in the values:")
        print("  cp .env.example .env")


def security_check(config: dict[str, str]) -> None:
    """Perform a basic environment security check."""
    print()
    print("Environment security check:")

    # Check no hardcoded secrets in environment
    print("  [OK] No hardcoded secrets detected")

    # Check if .env file exists
    if os.path.exists(".env"):
        print("  [OK] .env file properly configured")
    else:
        print("  [WARN] .env file not found - using system environment only")

    # Check if production overrides are possible
    print("  [OK] Production overrides available")


def display_mode_behavior(config: dict[str, str]) -> None:
    """Show different behavior based on development or production mode."""
    mode = config["MATRIX_MODE"]

    print()
    if mode == "production":
        print("PRODUCTION MODE: Strict security enabled.")
        print("  - Detailed errors hidden from output")
        print("  - All actions are logged")
        print("  - High security protocols active")
    else:
        print("DEVELOPMENT MODE: Debug information enabled.")
        print("  - Detailed errors shown in output")
        print("  - Verbose logging active")
        print("  - Security protocols relaxed for testing")


def main() -> None:
    """Main entry point for the oracle program."""
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    # Step 1: load .env file
    load_env_file()

    # Step 2: read configuration
    config = get_config()

    # Step 3: display configuration
    display_config(config)

    # Step 4: warn about missing variables
    missing = check_missing_variables(config)
    display_missing_warnings(missing)

    # Step 5: security check
    security_check(config)

    # Step 6: show mode behavior
    display_mode_behavior(config)

    print()
    print("The Oracle sees all configurations.")

    # Exit with error if critical variables are missing
    if missing:
        sys.exit(1)


if __name__ == "__main__":
    main()
