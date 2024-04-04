import sys
import os
from logic import analyze_neighboring_file, start_monitoring, stop_coverage
from rich import print

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[bold red]Please provide the filename of the neighboring file.[/bold red]")
        sys.exit(1)

    filename = os.path.basename(sys.argv[1])  # Extract just the filename
    print("Filename:", filename)  # Debug print
    analyze_neighboring_file(filename)

    monitored_folder = 'cloneHere'
    start_monitoring(monitored_folder)

    stop_coverage()
