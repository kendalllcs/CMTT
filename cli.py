import os
import sys
import argparse
from rich.console import Console
from rich import print
from logic import clone_github_repo, delete_all_files, display_summary_report, FileEventHandler

console = Console()

def center_text(text):
    terminal_width = os.get_terminal_size().columns
    horizontal_padding = (terminal_width - len(text.splitlines()[0])) // 2
    centered_text = '\n'.join([' ' * horizontal_padding + line for line in text.splitlines()])
    return centered_text

def main_menu():
    ascii_art = "Code Metrics Tool CLI"  # Placeholder for actual ASCII art if available
    print(center_text(ascii_art))
    print(center_text("Welcome to Code Metrics Tool CLI"))
    print(center_text("[1] - How to use"))
    print(center_text("[2] - Clone a GitHub repo into cloneHere"))
    print(center_text("[3] - Get Metrics"))
    print(center_text("[6] - Generate and display a summary report"))
    print(center_text("[7] - Delete all files"))
    print(center_text("[8] - Exit"))

    file_event_handler = FileEventHandler()  # Create an instance of FileEventHandler

    while True:
        choice = input("\nEnter your choice (1-8), or 'exit' to quit: ")

        if choice == 'exit' or choice == '8':
            break

        if choice == '1':
            print("How to use instructions...")

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
            print("Invalid choice. Please enter a valid option.")

    print("Exiting Code Metrics Tool CLI.")

def main():
    parser = argparse.ArgumentParser(description='Code Metrics Tool CLI')
    parser.add_argument('--folder', '-f', help='(Deprecated) Folder parameter is no longer used.')
    args = parser.parse_args()

    if args.folder:
        print("Note: The '--folder' option is deprecated and will be ignored.")

    main_menu()

if __name__ == "__main__":
    main()
