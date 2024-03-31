# CodeMetrics Terminal Tool (CMTT)

The CodeMetrics Terminal Tool (CMTT) is a Python-based software metrics analysis tool designed to provide software developers and project managers with immediate insights into code quality directly from the terminal. 

## Objective
CMTT aims to offer quick assessment of software quality metrics such as Lines of Code (LOC), Cyclomatic Complexity, Code Coverage, and Defect Density. It allows users to analyze codebases and identify areas for improvement.

## Features
- **Terminal-based:** CMTT operates directly from the terminal for swift and easy access.
- **Metric Collection:** Collects and analyzes essential software metrics including LOC and Cyclomatic Complexity.
- **Expandability:** Designed to support future integration of additional metrics and a Graphical User Interface (GUI).
- **Neighboring File Analysis:** Monitors a designated folder for Python files, automatically analyzing any dropped files for metrics.

## Getting Started
1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the `main_script.py` to start monitoring the designated folder.
4. Drop Python files into the monitored folder for automatic analysis.

## Dependencies
- Python 3.x
- watchdog library

## Usage
1. Ensure Python 3.x and the required dependencies are installed.
2. Run `python main_script.py` from the terminal.
3. Drop Python files into the monitored folder to trigger automatic analysis.

## Contributing
Contributions to enhance the tool or add new features are welcome! Please fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
