import os
import sys
import time
import coverage
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import radon.metrics as metrics
import radon.complexity as complexity
from rich import print

cov = coverage.Coverage()
cov.start()


def check_neighboring_file(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    neighboring_dir = os.path.join(script_dir, 'cloneHere')
    neighboring_file_path = os.path.join(neighboring_dir, filename)
    if os.path.isfile(neighboring_file_path):
        return neighboring_file_path
    else:
        return None


def analyze_neighboring_file(filename):
    neighboring_file_path = check_neighboring_file(filename)
    if neighboring_file_path:
        with open(neighboring_file_path, 'r') as file:
            code = file.read()
            print("[bold cyan]Code from neighboring file:[/bold cyan]")
            print(code)
            loc = code.count('\n') + 1
            cc_results = complexity.cc_visit(code)
            print("[blue]LOC:[/blue] [cyan]" + str(loc) + "[/cyan]")
            print("[bold cyan]Cyclomatic Complexity:[/bold cyan]")
            for result in cc_results:
                print("[green]Function:[/green] [bold green]" + result.name + "[/bold green], [green]Complexity:[/green] [bold green]" + str(result.complexity) + "[/bold green]")
            missed_lines = code.count('\n')
            total_lines = loc
            defect_density = missed_lines / total_lines if total_lines > 0 else 0
            print("[blue]Defect Density:[/blue] [cyan]" + "{:.2f}".format(defect_density) + "[/cyan]")
    else:
        print("Neighboring file not found.")


class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        elif event.src_path.endswith('.py'):
            print("[bold yellow]Analyzing file: {event.src_path}[/bold yellow]")
            with open(event.src_path, 'r') as file:
                code = file.read()
                print("[bold cyan]Code from created file:[/bold cyan]")
                print(code)
                loc = metrics.loc(code)
                cc = metrics.cc_visit(code)
                coverage_result = cov.analysis2(os.path.abspath(event.src_path))
                missed_lines = coverage_result[2]
                total_lines = coverage_result[1]
                defect_density = missed_lines / total_lines if total_lines > 0 else 0
                print(f"LOC: {loc}, Cyclomatic Complexity: {cc}, Defect Density: {defect_density:.2f}")


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
    if len(sys.argv) < 2:
        print("[bold red]Please provide the filename of the neighboring file.[/bold red]")
        sys.exit(1)

    filename = sys.argv[1]
    analyze_neighboring_file(filename)

    monitored_folder = 'cloneHere'
    start_monitoring(monitored_folder)

    cov.stop()
    cov.save()
    print("[bold magenta]Coverage Report[/bold magenta]")
    cov.report(show_missing=False, ignore_errors=True, file=sys.stdout)