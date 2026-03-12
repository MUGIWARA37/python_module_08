import sys
import os
import site


def is_virtual_env() -> bool:
    # In a venv, sys.prefix points to the venv dir while sys.base_prefix points
    # to the base Python install — they only differ when inside a venv
    return sys.prefix != sys.base_prefix


def get_venv_name() -> str:
    # sys.prefix is the full venv path (e.g. /home/user/matrix_env),
    # basename extracts just the folder name
    return os.path.basename(sys.prefix)


def get_package_path() -> str:
    try:
        # getsitepackages() returns a list of paths; grab the primary one
        packages = site.getsitepackages()
        return packages[0] if packages else "Unknown"
    except AttributeError:
        # fall back to the user-specific site-packages path
        return site.getusersitepackages()


def display_outside_venv() -> None:
    print("MATRIX STATUS: You're still plugged in\n")

    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected\n")

    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.\n")

    # Provide OS-specific instructions for creating and activating a venv
    print("To enter the construct, run:")
    print("  python3 -m venv matrix_env or python3 -m virtualenv matrix_env")
    print("  source matrix_env/bin/activate")
    print("or\n  source matrix_env/bin/activate.fish  (if you are using fish "
          "terminal)")
    print("  matrix_env\\Scripts\\activate     # On Windows\n")
    print("Then run this program again.")


def display_inside_venv() -> None:
    venv_name = get_venv_name()
    venv_path = sys.prefix  # Full path to the active virtual environment
    package_path = get_package_path()

    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {venv_name}")
    print(f"Environment Path: {venv_path}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print()
    print("Package installation path:")
    print(f"  {package_path}")


def main() -> None:
    # Route to the appropriate display based on venv status
    if is_virtual_env():
        display_inside_venv()
    else:
        display_outside_venv()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)