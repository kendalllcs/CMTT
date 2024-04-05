from rich.console import Console

def display_instructions():
    console = Console()

    console.print("[bold cyan]How to Use Code Metrics Tool CLI[/bold cyan]\n")
    console.print("[bold yellow]1.[/bold yellow] Choose an option from the main menu by entering the corresponding number.")
    console.print("[bold yellow]2.[/bold yellow] Follow the prompts and instructions provided for each option.")
    console.print("[bold yellow]3.[/bold yellow] Press Enter to return to the main menu after completing an action.\n")

    console.print("[bold cyan]Understanding Metrics[/bold cyan]\n")
    console.print("[bold yellow]Lines of Code (LOC):[/bold yellow] The number of lines of code in the analyzed file.")
    console.print("[bold yellow]Cyclomatic Complexity (CC):[/bold yellow] A software metric used to measure the complexity of a program. It directly measures the number of linearly independent paths through a program's source code.")
    console.print("[bold yellow]Defect Density (DD):[/bold yellow] The number of defects per line of code. It indicates the likelihood of encountering defects in the code.")
    console.print("[bold yellow]Code Coverage:[/bold yellow] Code coverage is a measure used to describe the degree to which the source code of a program is executed when a particular test suite runs. It is usually expressed as a percentage.\n")

    console.print("[bold cyan]Example Output[/bold cyan]\n")
    console.print("[bold yellow]Analyzing file: cloneHere\test.py[/bold yellow]")
    console.print("[bold green]Name                Stmts   Miss  Cover[/bold green]")
    console.print("[bold green]---------------------------------------[/bold green]")
    console.print("[bold green]cloneHere\test.py      20      2    90%[/bold green]")
    console.print("[bold green]---------------------------------------[/bold green]")
    console.print("[bold green]TOTAL                  20      2    90%[/bold green]")
    console.print("[bold yellow]Lines of Code (LOC):[/bold yellow] 33")
    console.print("[bold yellow]Cyclomatic Complexity:[/bold yellow]")
    console.print("[bold yellow]Function: calculate_factorial, Complexity: 2[/bold yellow]")
    console.print("[bold yellow]Function: fibonacci, Complexity: 2[/bold yellow]")
    console.print("[bold yellow]Function: is_prime, Complexity: 4[/bold yellow]")
    console.print("[bold yellow]Defect Density:[/bold yellow] 0.0")
    console.print("[bold yellow]Press Enter to return to the main menu.[/bold yellow]")

if __name__ == "__main__":
    display_instructions()