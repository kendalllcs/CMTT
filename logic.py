import os
import sys
import subprocess
import shutil
from coverage import Coverage
import radon.complexity as complexity
import radon.metrics as metrics
from rich.console import Console

cov = Coverage()

class FileEventHandler:
    def __init__(self, directory='cloneHere'):
        self.directory = directory

    def analyze_neighboring_files(self):
        if os.path.exists(self.directory):
            python_files = [os.path.join(self.directory, file) for file in os.listdir(self.directory) if file.endswith('.py')]
            for file_path in python_files:
                self.analyze_file(file_path)
        else:
            print("Directory 'cloneHere' does not exist.")

    def analyze_file(self, file_path):
        console = Console()
        console.print(f"Analyzing file: [bold red]{file_path}[/bold red]", style="bold red")

        try:
            with open(file_path, 'r') as file:
                code = file.read()

            # Lines of Code (LOC) - using radon
            loc = sum(1 for _ in code.split('\n') if _)

            # Cyclomatic Complexity - using radon
            cc_results = complexity.cc_visit(code)

            # Start a new coverage analysis session
            cov.erase()
            cov.start()

            # Execute the file
            result = subprocess.run([sys.executable, '-m', 'coverage', 'run', '--parallel-mode', file_path], capture_output=True)

            # Stop coverage and save data
            cov.stop()
            cov.save()
            cov.combine()
            cov.report(file=sys.stdout)
            cov.html_report(directory=os.path.join(self.directory, 'htmlcov'))

            if result.returncode != 0:
                console.print(f"Error running file {file_path}: {result.stderr.decode('utf-8')}", style="bold red")
                return

            # Output results
            console.print(f"Lines of Code (LOC): {loc}", style="bold green")

            console.print("Cyclomatic Complexity:", style="bold green")
            for item in cc_results:
                console.print(f"Function: {item.name}, Complexity: {item.complexity}", style="green")

            # Defect Density calculation - Placeholder for defects per LOC
            defects = 0  # You would replace this with the actual number of known defects
            defect_density = defects / (loc if loc > 0 else 1)
            console.print(f"Defect Density: {defect_density}", style="bold green")

        except Exception as e:
            console.print(f"Error analyzing file: {e}", style="bold red")

# Rest of the functions unchanged


# Add the missing clone_github_repo function
def clone_github_repo(git_link):
    """
    Clones a GitHub repository into the 'cloneHere' directory.
    """
    clone_dir = 'cloneHere'
    if os.path.exists(clone_dir) and os.listdir(clone_dir):
        response = input("The 'cloneHere' directory is not empty. Cloning will overwrite existing contents. Proceed? (y/n): ")
        if response.lower() != 'y':
            print("Cloning cancelled.")
            return
        shutil.rmtree(clone_dir)
    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)
    
    subprocess.run(['git', 'clone', git_link, clone_dir], check=True)
    print("Repository cloned successfully into 'cloneHere'.")

# Add the missing delete_all_files function
def delete_all_files():
    """
    Deletes all files in 'cloneHere'.
    """
    clone_dir = 'cloneHere'
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
        os.makedirs(clone_dir)
        print("All files deleted successfully.")
    else:
        print("'cloneHere' directory does not exist.")

# Add the missing display_summary_report function
def display_summary_report():
    """
    Displays a summary report of metrics.
    """
    print("Summary report feature is not implemented yet.")

# Remove the __main__ check as it's not needed anymore