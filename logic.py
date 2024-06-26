import os
import sys
import subprocess
import shutil
from coverage import Coverage
import radon.complexity as complexity
from rich.console import Console
import stat

# Create an instance of the Console class
console = Console()

def on_rm_error(func, path, exc_info):
    """
    Error handler for shutil.rmtree.

    If the error is due to an access error (read-only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : shutil.rmtree(path, onerror=on_rm_error)
    """
    # Check if the file access issue is due to it being read-only
    if not os.access(path, os.W_OK):
        # Try making the file writable
        os.chmod(path, stat.S_IWUSR)
        # Try the delete operation again
        func(path)
    else:
        raise  # Re-raise the error if it's not a permission issue

class FileEventHandler:
    def __init__(self, directory='cloneHere'):
        self.directory = directory

    def analyze_neighboring_files(self):
        if os.path.exists(self.directory):
            python_files = [os.path.join(self.directory, file) for file in os.listdir(self.directory) if file.endswith('.py')]
            for file_path in python_files:
                self.analyze_file(file_path)
        else:
            console.print("Directory 'cloneHere' does not exist.")

    def analyze_file(self, file_path):
        console.print(f"Analyzing file: [bold red]{file_path}[/bold red]", style="bold red")

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
    Allows the user to exit back to the main menu without inputting a link.
    """
    # Check if the user wants to exit back to the main menu
    if git_link.lower() == 'exit':
        console.print("Exiting to main menu...", style="warning")
        return  # Exit the function early

    clone_dir = 'cloneHere'
    if os.path.exists(clone_dir) and os.listdir(clone_dir):
        response = input("The 'cloneHere' directory is not empty. Cloning will overwrite existing contents. Proceed? (y/n): ")
        if response.lower() != 'y':
            console.print("Cloning cancelled.", style="error")
            return
        shutil.rmtree(clone_dir)

    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)

    try:
        subprocess.run(['git', 'clone', git_link, clone_dir], check=True)
        console.print("Repository cloned successfully into 'cloneHere'.", style="success")
    except Exception as e:
        console.print(f"Error cloning repository: {e}", style="error")


# Add the missing delete_all_files function
def delete_all_files():
    """
    Deletes all files in 'cloneHere' after user confirmation.
    """
    clone_dir = 'cloneHere'
    if os.path.exists(clone_dir):
        # Asking for user confirmation before proceeding with the deletion
        confirmation = input("Are you sure you want to delete all files in 'cloneHere'? [y/N]: ")
        if confirmation.lower() == 'y':
            # Use the error handling function on_rm_error
            shutil.rmtree(clone_dir, onerror=on_rm_error)
            os.makedirs(clone_dir)
            print("All files deleted successfully.")
        else:
            print("Deletion cancelled.")
    else:
        print("'cloneHere' directory does not exist.")


# Add the missing display_summary_report function
def display_summary_report():
    """
    Displays a summary report of metrics.
    """
    print("Summary report feature is not implemented yet.")

# Remove the __main__ check as it's not needed anymore
