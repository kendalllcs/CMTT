import os
import sys
import subprocess
import shutil
import argparse
from coverage import Coverage
import radon.complexity as complexity
from rich.console import Console
from rich.theme import Theme

from logic import clone_github_repo, delete_all_files, display_summary_report, FileEventHandler
from instructions import display_instructions  # Importing the instructions module
from ascii_art import get_ascii_art

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

            # Defect Density calculation - Placeholder for defects per LOC
            defects = 0  # You would replace this with the actual number of known defects
            defect_density = defects / (loc if loc > 0 else 1)
            console.print(f"Defect Density: {defect_density}", style="success")

        except Exception as e:
            console.print(f"Error analyzing file: {e}", style="error")

def wait_and_clear():
    """Waits for the user to press 'c' and then clears the screen."""
    input("\nPress Enter to continue...")
    console.clear()

def main_menu():
    # Create an instance of FileEventHandler
    file_event_handler = FileEventHandler(directory='cloneHere')

    while True:
        console.clear()  # Clear the screen before displaying the menu
        console.print(get_ascii_art(), style="bold magenta")  # Display the ASCII logo
        console.print("[1] - How to use", style="info")
        console.print("[2] - Get Metrics", style="info")
        console.print("[3] - Generate and display a summary report", style="info")
        console.print("[0] - Exit", style="info")

        choice = console.input("\nEnter your choice (1-3 or 0 to EXIT), or 'exit' to quit: ")

        if choice.lower() == 'exit' or choice == '0':
            break

        if choice == '1':
            clear_screen()  # Clear the screen before displaying instructions
            display_instructions()  # Assuming this function prints the instructions
            wait_and_clear()

        elif choice == '2':
            clear_screen()
            # Use the file_event_handler instance here
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

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls')

def main():
    parser = argparse.ArgumentParser(description='Code Metrics Tool CLI')
    parser.add_argument('--folder', '-f', help='(Deprecated) Folder parameter is no longer used.')
    args = parser.parse_args()

    if args.folder:
        console.print("Note: The '--folder' option is deprecated and will be ignored.", style="warning")

    main_menu()

if __name__ == "__main__":
    main()
