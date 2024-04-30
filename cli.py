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
        self.all_metrics = []

    def analyze_neighboring_files(self):
        if os.path.exists(self.directory):
            python_files = [os.path.join(self.directory, file) for file in os.listdir(self.directory) if file.endswith('.py')]
            for file_path in python_files:
                self.analyze_file(file_path)
        else:
            console.print("Directory 'cloneHere' does not exist.", style="error")

    def analyze_file(self, file_path):
        console.print(f"Analyzing file: [bold red]{file_path}[/bold red]")
        try:
            with open(file_path, 'r') as file:
                code = file.read()

            # Metrics calculation
            loc = sum(1 for _ in code.split('\n') if _)
            cc_results = complexity.cc_visit(code)
            cov = Coverage()
            cov.start()
            result = subprocess.run([sys.executable, '-m', 'coverage', 'run', '--parallel-mode', file_path], capture_output=True)
            cov.stop()
            cov.save()
            cov.combine()
            coverage_data = cov.report(file=sys.stdout)

            # Defect density calculation (assuming defects are tracked and counted separately)
            defects = 0  # Placeholder; replace or calculate as needed
            defect_density = defects / loc if loc > 0 else 0

            if result.returncode != 0:
                console.print(f"Error running file {file_path}: {result.stderr.decode('utf-8')}", style="error")
                return

            # Storing results
            file_metrics = {
                'file': file_path,
                'Lines of Code': loc,
                'Cyclomatic Complexity': cc_results,
                'Coverage Score': coverage_data,
                'Defect Density': defect_density,
                'Coverage Tips': 'Increase unit tests for better coverage.' if coverage_data < 75 else 'Good coverage!',
                'Defect Tips': 'Focus on reducing defects per LOC.' if defect_density > 0.1 else 'Low defect density, good job!'
            }
            self.all_metrics.append(file_metrics)
        except Exception as e:
            console.print(f"Error analyzing file: {e}", style="error")



    def get_all_metrics(self):
        return self.all_metrics

def display_summary_report():
    metrics = file_event_handler.get_all_metrics()
    directory = 'summaryReports'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_summary_report.txt")
    filepath = os.path.join(directory, filename)

    with open(filepath, 'w') as file:
        for metric in metrics:
            file.write(f"File: {metric['file']}\n")
            file.write(f"Lines of Code: {metric['Lines of Code']}\n")
            file.write("Cyclomatic Complexity:\n")
            for item in metric['Cyclomatic Complexity']:
                file.write(f"  Function: {item.name}, Complexity: {item.complexity}\n")
            file.write(f"Coverage Score: {metric['Coverage Score']:.2f}%\n")
            file.write(f"Defect Density: {metric['Defect Density']:.2f}\n")
            file.write(f"Suggestions based on Coverage: {metric['Coverage Tips']}\n")
            file.write(f"Suggestions based on Defect Density: {metric['Defect Tips']}\n\n")

        # General advice section
        file.write("\nGeneral Tips on Improving Code Quality:\n")
        file.write("1. Aim for higher test coverage to ensure more robust code.\n")
        file.write("2. Refactor code to simplify complex functions and reduce cyclomatic complexity.\n")
        file.write("3. Include more detailed inline comments and documentation for better maintainability.\n")

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