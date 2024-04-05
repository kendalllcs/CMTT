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

# Add the missing clone_github_repo function
# Add the missing delete_all_files function
# Add the missing display_summary_report function

# Add main function
def main_menu():
    ascii_logo = get_ascii_art()
    console.print(center_text(ascii_logo))
    console.print(center_text("Welcome to Code Metrics Tool CLI"))
    console.print(center_text("[1] - How to use"))
    console.print(center_text("[2] - Clone a GitHub repo into cloneHere"))
    console.print(center_text("[3] - Get Metrics"))
    console.print(center_text("[6] - Generate and display a summary report"))
    console.print(center_text("[7] - Delete all files"))
    console.print(center_text("[8] - Exit"))
    

    file_event_handler = FileEventHandler()  # Create an instance of FileEventHandler

    while True:
        choice = input("\nEnter your choice (1-8), or 'exit' to quit: ")

        if choice == 'exit' or choice == '8':
            break

        if choice == '1':
            console.print("How to use instructions...")

        elif choice == '2':
            git_link = input("Enter the .git link to clone: ")
            clone_github_repo(git_link)

        elif choice == '3':
            file_event_handler.analyze_neighboring_files()

        elif choice == '6':
            display_summary_report()

        elif choice == '7':
            delete_all_files()

        else:
            console.print("Invalid choice. Please enter a valid option.")

    console.print("Exiting Code Metrics Tool CLI.")

def main():
    parser = argparse.ArgumentParser(description='Code Metrics Tool CLI')
    parser.add_argument('--folder', '-f', help='(Deprecated) Folder parameter is no longer used.')
    args = parser.parse_args()

    if args.folder:
        console.print("Note: The '--folder' option is deprecated and will be ignored.", style="warning")

    main_menu()

def center_text(text):
    terminal_width = os.get_terminal_size().columns
    horizontal_padding = (terminal_width - len(text.splitlines()[0])) // 2
    centered_text = '\n'.join([' ' * horizontal_padding + line for line in text.splitlines()])
    return centered_text

if __name__ == "__main__":
    main()
