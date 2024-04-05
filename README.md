# CodeMetrics Terminal Tool (CMTT)

![Alt text](CMTT/ASSET/MainMenu.png)


The CodeMetrics Terminal Tool (CMTT) is a Python-based software metrics analysis tool designed to provide software developers and project managers with immediate insights into code quality directly from the terminal. 

## Objective

CMTT aims to offer quick assessments of software quality metrics such as Lines of Code (LOC), Cyclomatic Complexity, Code Coverage, and Defect Density. It allows users to analyze codebases and identify areas for improvement.

## Features

- **Terminal-based:** Operates directly from the terminal for swift and easy access.
- **Metric Collection:** Collects and analyzes essential software metrics including LOC, Cyclomatic Complexity, Code Coverage, and Defect Density.
- **Expandability:** Designed with future integration of additional metrics and a Graphical User Interface (GUI) in mind.
- **Neighboring File Analysis:** Monitors a designated folder for Python files, automatically analyzing any new files for metrics.

## Getting Started

1. Clone the repository to your local machine.
2. Install the required dependencies with `pip install -r requirements.txt`.
3. Execute `python main.py testFileName.py` to start monitoring the designated folder.
4. Drop Python files into the monitored folder for automatic analysis.

## Dependencies

Ensure you have Python 3.x installed and then install project dependencies:
pip install -r requirements.txt

## Contributing

Contributions to enhance the tool or add new features are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

