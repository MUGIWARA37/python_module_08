import sys
import importlib


def check_dependency(package_name: str) -> tuple[bool, str]:

    try:
        module = importlib.import_module(package_name)
        version = getattr(module, "__version__", "unknown")
        return True, version
    except ImportError:
        return False, "not installed"


def check_all_dependencies() -> dict[str, tuple[bool, str]]:

    packages = ["pandas", "numpy", "matplotlib"]
    results = {}
    for pkg in packages:
        available, version = check_dependency(pkg)
        results[pkg] = (available, version)
    return results


def display_dependency_status(results: dict[str, tuple[bool, str]]) -> bool:

    print("Checking dependencies:")
    all_ok = True
    for pkg, (available, version) in results.items():
        if available:
            print(f"  [OK] {pkg} ({version})")
        else:
            print(f"  [MISSING] {pkg} - not installed")
            all_ok = False

    if not all_ok:
        print()
        print("Missing dependencies detected!")
        print("Install with pip:")
        print("  pip install -r requirements.txt\n")

        print("Or install with Poetry:")
        print("  poetry install")

    return all_ok


def show_pip_vs_poetry() -> None:
    print()
    print("=" * 50)
    print("PIP vs POETRY - Dependency Management")
    print("=" * 50)
    print()
    print("pip (requirements.txt):")
    print("  - Simple, built into Python")
    print("  - Manually manage versions")
    print("  - No lock file by default")
    print("  - Install: pip install -r requirements.txt\n")

    print("Poetry (pyproject.toml):")
    print("  - Modern dependency resolver")
    print("  - Auto-generates poetry.lock")
    print("  - Manages virtual envs automatically")
    print("  - Install: poetry install")
    print("  - Run: poetry run python loading.py\n")


def analyze_matrix_data() -> None:

    try:
        import numpy as np
        import pandas as pd

        print("Analyzing Matrix data...")

        # Simulate 1000 data points representing Matrix signals
        np.random.seed(42)
        data = {
            "timestamp": pd.date_range("2026-01-01", periods=1000, freq="h"),
            "signal_strength": np.random.normal(50, 15, 1000),
            "anomaly_score": np.random.exponential(2, 1000),
            "agent_activity": np.random.randint(0, 10, 1000),
        }

        df = pd.DataFrame(data)
        print(f"Processing {len(df)} data points...")

        # Basic stats
        print()
        print("Matrix Signal Analysis:")
        print(f"  Avg signal strength : {df['signal_strength'].mean():.2f}")
        print(f"  Max anomaly score   : {df['anomaly_score'].max():.2f}")
        print(f"  Total agent activity: {df['agent_activity'].sum()}")

        return df

    except Exception as e:
        print(f"Error during analysis: {e}")
        return None


def generate_visualization(df: object) -> None:

    try:
        import matplotlib
        matplotlib.use("Agg")  # Non-interactive backend for file saving
        import matplotlib.pyplot as plt

        print()
        print("Generating visualization...")

        fig, axes = plt.subplots(2, 1, figsize=(10, 8))
        fig.suptitle("Matrix Data Analysis", fontsize=14, fontweight="bold")

        # Plot 1: Signal strength over time
        axes[0].plot(
            df["timestamp"][:100],
            df["signal_strength"][:100],
            color="green",
            linewidth=0.8
        )
        axes[0].set_title("Signal Strength (first 100 hours)")
        axes[0].set_ylabel("Strength")
        axes[0].grid(True, alpha=0.3)

        # Plot 2: Agent activity histogram
        axes[1].hist(
            df["agent_activity"],
            bins=10,
            color="red",
            alpha=0.7,
            edgecolor="black"
        )
        axes[1].set_title("Agent Activity Distribution")
        axes[1].set_xlabel("Activity Level")
        axes[1].set_ylabel("Frequency")
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        output_file = "matrix_analysis.png"
        plt.savefig(output_file, dpi=100)
        plt.close()

        print(f"Results saved to: {output_file}")

    except Exception as e:
        print(f"Error generating visualization: {e}")


def main() -> None:

    print("LOADING STATUS: Loading programs...")
    print()

    # Check dependencies
    results = check_all_dependencies()
    all_ok = display_dependency_status(results)

    if not all_ok:
        sys.exit(1)

    # Show pip vs Poetry comparison
    show_pip_vs_poetry()

    # Run analysis
    df = analyze_matrix_data()

    if df is not None:
        generate_visualization(df)
        print()
        print("Analysis complete!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
