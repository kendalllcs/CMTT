import os
import time
import argparse
import subprocess
import shutil
from coverage import Coverage
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich import print
import radon.complexity as complexity
from ascii_art import get_ascii_art

cov = Coverage()
cov.start()

analyzed_files = set()  # Keep track of analyzed files

class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        elif event.src_path.endswith('.py'):
            if event.src_path not in analyzed_files:  # Check if file has already been analyzed
                print("[bold yellow]Analyzing file:[/bold yellow] {event.src_path}")
                analyze_neighboring_file(event.src_path)
                analyzed_files.add(event.src_path)  # Add file to analyzed_files set

def clone_github_repo(git_link):
    """
    Clones a GitHub repository into the 'cloneHere' directory.
    """
    try:
        if os.path.exists('cloneHere') and os.listdir('cloneHere'):
            # Prompt user to confirm if they want to proceed with cloning
            response = input("The 'cloneHere' directory is not empty. "
                             "Cloning will overwrite existing contents. Proceed? (y/n): ")
            if response.lower() != 'y':
                print("Cloning cancelled.")
                return
            # Clear existing contents of 'cloneHere' directory
            shutil.rmtree('cloneHere')
        subprocess.run(['git', 'clone', git_link, 'cloneHere'])
        print("Cloning done.")
        print("Your file is ready to be analyzed.")
    except Exception as e:
        print(f"Error cloning repository: {e}")

def delete_all_files():
    """
    Deletes all files and directories in the 'cloneHere' directory.
    """
    try:
        if os.path.exists('cloneHere') and os.path.isdir('cloneHere'):
            shutil.rmtree('cloneHere')
            os.mkdir('cloneHere')  # Recreate the 'cloneHere' directory after deletion
            print("All files deleted successfully.")
        else:
            print("'cloneHere' directory does not exist.")
    except Exception as e:
        print(f"Error deleting files: {e}")

def analyze_neighboring_file(file_path):
    """
    Analyzes a Python file for LOC, Cyclomatic Complexity, Defect Density,
    and includes code coverage.
    """
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r') as file:
                code = file.read()
                print("[bold cyan]Code from file:[/bold cyan]")
                print(code)

                loc = code.count('\n') + 1
                cc_results = complexity.cc_visit(code)
                print("[blue]LOC:[/blue] [cyan]" + str(loc) + "[/cyan]")

                print("[bold cyan]Cyclomatic Complexity:[/bold cyan]")
                for result in cc_results:
                    print("[green]Function:[/green] [bold green]" + result.name + "[/bold green], [green]Complexity:[/green] [bold green]" + str(result.complexity) + "[/bold green]")

                # Start coverage analysis
                cov.start()

                # Execute the Python file
                subprocess.run(['python', file_path], check=True)

                # Stop coverage and save the report
                cov.stop()

                # Coverage reporting
                with open('coverage_report.txt', 'w') as coverage_file:
                    cov.report(file=coverage_file)  # Report coverage for the analyzed file

                # Display coverage report
                with open('coverage_report.txt', 'r') as coverage_file:
                    print("[bold magenta]Coverage Report[/bold magenta]")
                    print(coverage_file.read())

                missed_lines = code.count('\n')
                total_lines = loc
                defect_density = missed_lines / total_lines if total_lines > 0 else 0
                print("[blue]Defect Density:[/blue] [cyan]" + "{:.2f}".format(defect_density) + "[/cyan]")

                print("[bold magenta]Coverage Report Generated.[/bold magenta]")

        except Exception as e:
            print(f"Error analyzing file: {e}")
    else:
        print("File not found.")

def start_monitoring(folder):
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

def generate_summary_report():
    """
    Generate a summary report of metrics.
    """
    print("Generating summary report...")
    # You can include any summary metrics you want here
    # For example, average LOC, average complexity, etc.
    # This function should generate a report summarizing the metrics obtained from the analysis.

def display_summary_report():
    """
    Display a summary report of metrics.
    """
    print("Displaying summary report...")
    generate_summary_report()
    # You can display the generated summary report here

def main_menu():
    ascii_art = get_ascii_art()
    print(center_text(ascii_art))
    print(center_text("Welcome to Code Metrics Tool CLI"))
    print(center_text("[1] - How to use"))
    print(center_text("[2] - Clone a GitHub repo into cloneHere"))
    print(center_text("[3] - Get Metrics"))
    print(center_text("[6] - Generate and display a summary report"))
    print(center_text("[7] - Delete all files"))
    print(center_text("[8] - Exit"))

    choice = input("\nEnter your choice (1-8), or 'exit' to quit: ")

    if choice == '2':
        git_link = input("Enter the .git link to clone: ")
        clone_github_repo(git_link)

    if choice == '3':
        folder_to_monitor = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cloneHere'))
        print("Neighboring directory:", folder_to_monitor)
        start_monitoring(folder_to_monitor)


def center_text(text):
    # Get terminal width
    terminal_width = os.get_terminal_size().columns

    # Calculate padding for horizontal centering
    horizontal_padding = (terminal_width - len(text.splitlines()[0])) // 2

    # Create centered text with padding
    centered_text = '\n'.join([' ' * horizontal_padding + line for line in text.splitlines()])
    return centered_text

def main():
    parser = argparse.ArgumentParser(description='Code Metrics Tool CLI')
    parser.add_argument('--folder', '-f', default='cloneHere', help='Folder to monitor')
    parser.add_argument('--file', '-F', help='Path to specific Python file to analyze')
    args = parser.parse_args()

    # Convert the monitored_folder to an absolute path to ensure consistency
    monitored_folder = os.path.abspath(args.folder)

    # Start monitoring folder
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, monitored_folder, recursive=False)
    observer.start()

    try:
        while True:
            # Clear terminal
            os.system('cls' if os.name == 'nt' else 'clear')

            # Print the main menu
            main_menu()

            choice = input("\nEnter your choice (1-8), or 'exit' to quit: ")

            # Check for exit condition
            if choice.lower() == 'exit' or choice == '8':
                break

            if choice == '2':
                git_link = input("Enter the .git link to clone: ")
                clone_github_repo(git_link)
            elif choice == '3':
                # Placeholder for analyzing a specific Python file
                pass

    except KeyboardInterrupt:
        pass
    finally:
        # Stop monitoring before exiting
        observer.stop()
        observer.join()

if __name__ == "__main__": 
    main()
