import os
import sys
import subprocess
import shutil
import argparse
from coverage import Coverage
import radon.complexity as complexity
import datetime
from rich.console import Console
from rich.theme import Theme

from logic import clone_github_repo, delete_all_files  # Assuming these functions are defined
from instructions import display_instructions  # Importing the instructions module
from ascii_art import get_ascii_art  # Assuming this is defined

# Custom theme for the Rich Console
custom_theme = Theme({
    "info": "bold magenta",    # Information text in bold magenta
    "error": "bold red",       # Error messages in bold red
    "success": "bold green",   # Success messages in bold green
    "warning": "bold yellow",  # Warning messages in bold yellow
    "emphasis": "italic",      # Emphasized text in italic
    "strong": "bold",          # Strong text in bold
    "background": "purple",    # Purple background
})

# Initialize Rich Console with custom theme
console = Console(theme=custom_theme)

class FileEventHandler:
    def __init__(self, directory='cloneHere'):
        self.directory = directory

    def analyze_neighboring_files(self):
        if os.path.exists(self.directory):
            python_files = [os.path.join(self.directory, file) for file in os.listdir(self.directory) if file.endswith('.py')]
            for file_path in python_files:
                self.analyze_file(file_path)
        else:
            console.print("Directory 'cloneHere' does not exist.", style="error")

    def analyze_file(self, file_path):
        console.clear()  # Clear the screen before displaying analysis results
        console.print(f"Analyzing file: [bold red]{file_path}[/bold red]")

        try:
            with open(file_path, 'r') as file:
                code = file.read()

            # Lines of Code (LOC) - using radon
            loc = sum(1 for _ in code.split('\n') if _)

            # Cyclomatic Complexity - using radon
            cc_results = complexity.cc_visit(code)

            # Start a new coverage analysis session
            cov = Coverage()
            cov.start()

            # Execute the file
            result = subprocess.run([sys.executable, '-m', 'coverage', 'run', '--parallel-mode', file_path], capture_output=True)

            # Stop coverage and save data
            cov.stop()
            cov.save()
            cov.combine()

            # Print code coverage in orange
            cov.report(file=sys.stdout)

            if result.returncode != 0:
                console.print(f"Error running file {file_path}: {result.stderr.decode('utf-8')}", style="error")
                return

            # Output results
            console.print(f"Lines of Code (LOC): {loc}", style="success")
            console.print("Cyclomatic Complexity:")
            for item in cc_results:
                console.print(f"Function: {item.name}, Complexity: {item.complexity}", style="success")

            # Assuming defect density calculation happens here
            defects = 0  # Placeholder for actual defect count
            defect_density = defects / (loc if loc > 0 else 1)
            console.print(f"Defect Density: {defect_density}", style="success")

            # Store metrics for report generation
            self.metrics = {
                'Lines of Code': loc,
                'Cyclomatic Complexity': [f"{item.name}: {item.complexity}" for item in cc_results],
                'Defect Density': defect_density
            }

        except Exception as e:
            console.print(f"Error analyzing file: {e}", style="error")

    def get_metrics(self):
        return self.metrics if hasattr(self, 'metrics') else {}

def display_summary_report():
    directory = 'summaryReports'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_summary_report.txt")
    filepath = os.path.join(directory, filename)
    metrics = file_event_handler.get_metrics()
    with open(filepath, 'w') as file:
        file.write("Metrics Summary:\n")
        for metric_name, values in metrics.items():
            if isinstance(values, list):
                file.write(f"{metric_name}:\n")
                for value in values:
                    file.write(f"    {value}\n")
            else:
                file.write(f"{metric_name}: {values}\n")
        file.write("\nTips on Improving Metrics:\n")
        file.write("1. Reduce complexity by simplifying function logic.\n")
        file.write("2. Increase code coverage by adding more comprehensive tests.\n")
        file.write("\nHow to Achieve the Best Scores:\n")
        file.write("Focus on writing clean, readable, and well-documented code. Prioritize unit testing to ensure robustness.\n")
    console.print(f"Summary report generated and saved to {filepath}", style="success")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_and_clear():
    input("\nPress Enter to continue...")
    console.clear()

def main_menu():
    global file_event_handler
    file_event_handler = FileEventHandler(directory='cloneHere')
    while True:
        clear_screen()
        console.print(get_ascii_art(), style="bold magenta")
        console.print("[1] - How to use", style="info")
        console.print("[2] - Get Metrics", style="info")
        console.print("[3] - Generate and display a summary report", style="info")
        console.print("[0] - Exit", style="info")
        choice = console.input("\nEnter your choice (1-3 or 0 to EXIT), or 'exit' to quit: ")
        if choice.lower() == 'exit' or choice == '0':
            break
        elif choice == '1':
            clear_screen()
            display_instructions()
            wait_and_clear()
        elif choice == '2':
            clear_screen()
            file_event_handler.analyze_neighboring_files()
            wait_and_clear()
        elif choice == '3':
            clear_screen()
            display_summary_report()
            wait_and_clear()
        else:
            console.print("Invalid choice. Please enter a valid option.", style="error")
            wait_and_clear()
    console.print("Exiting Code Metrics Tool CLI.", style="warning")

def main():
    parser = argparse.ArgumentParser(description='Code Metrics Tool CLI')
    parser.add_argument('--folder', '-f', help='(Deprecated) Folder parameter is no longer used.')
    args = parser.parse_args()
    if args.folder:
        console.print("Note: The '--folder' option is deprecated and will be ignored.", style="warning")
    main_menu()

if __name__ == "__main__":
    main()
