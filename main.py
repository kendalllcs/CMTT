import os
import sys
import time
import coverage  # Import coverage module
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import radon.metrics as metrics  # For code metrics calculation (e.g., LOC, Cyclomatic Complexity)
import radon.complexity as complexity


# Start coverage
cov = coverage.Coverage()
cov.start()

# Function to check if a file exists in the neighboring directory
def check_neighboring_file(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    neighboring_dir = os.path.join(script_dir, 'cloneHere')
    neighboring_file_path = os.path.join(neighboring_dir, filename)
    if os.path.isfile(neighboring_file_path):
        return neighboring_file_path
    else:
        return None

# Function to read and analyze code from a neighboring file
def analyze_neighboring_file(filename):
    neighboring_file_path = check_neighboring_file(filename)
    if neighboring_file_path:
        with open(neighboring_file_path, 'r') as file:
            code = file.read()
            # Print code for verification
            print("Code from neighboring file:")
            print(code)
            # Calculate metrics
            loc = code.count('\n') + 1
            cc_results = complexity.cc_visit(code)
            print(f"LOC: {loc}")
            print("Cyclomatic Complexity:")
            for result in cc_results:
                print(f"Function: {result.name}, Complexity: {result.complexity}")
    else:
        print("Neighboring file not found.")


# Function to analyze Python files dropped into the monitored folder
class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        elif event.src_path.endswith('.py'):
            print(f"Analyzing file: {event.src_path}")
            with open(event.src_path, 'r') as file:
                code = file.read()
                # Print code for verification
                print("Code from created file:")
                print(code)
                # Calculate metrics
                loc = metrics.loc(code)
                cc = metrics.cc_visit(code)
                coverage_result = cov.analysis2(os.path.abspath(event.src_path))  # Get coverage result
                print(f"LOC: {loc}, Cyclomatic Complexity: {cc}, Code Coverage: {coverage_result[3]}%")

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

if __name__ == "__main__":
    # Check if a filename is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Please provide the filename of the neighboring file.")
        sys.exit(1)

    filename = sys.argv[1]
    analyze_neighboring_file(filename)

    # Monitoring the 'cloneHere' folder for Python files
    monitored_folder = 'cloneHere'
    start_monitoring(monitored_folder)

# Stop coverage and generate report
cov.stop()
cov.save()
cov.report()
