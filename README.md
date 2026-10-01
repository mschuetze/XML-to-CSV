# XML to CSV

A small, local-only desktop utility for converting one or more XML files into
UTF-16 CSV files. It uses Python's standard library, so it runs on macOS Intel,
Apple silicon, and Windows without uploading or transmitting any file data.

## What it does

- Lets you select one or more XML files using a desktop file picker.
- Converts the XML records and nested values into CSV columns.
- Writes each result as a UTF-16 CSV file next to the source XML file.
- Names the output using the format `filename_UTF-16.csv`.
- Keeps all files on the local computer; no data is uploaded or transmitted.

## Requirements

- Python 3.9 or newer
  - download from here: https://www.python.org/downloads/
- macOS or Windows

## Installation

- download the ZIP file
- unzip the ZIP file
- copy the XML-to-CSV.app to your Mac´s PROGRAM folder
- double-click the app icon

## How to use the tool

1. Open the XML-to-CSV app.
2. When the file picker opens, choose one or more XML files from your computer.
3. The app converts each selected XML file into a CSV file in the same folder as the original file.
4. The new file name follows this pattern: `filename_UTF-16.csv`.
5. If conversion works, a success message appears in the app. If a file is unreadable or malformed, the app skips that file and reports the problem.
6. Open the generated CSV in Excel, Numbers, or another spreadsheet app to review the converted data.

Tip: For best results, select XML files that contain a repeated record pattern, such as multiple items under a common parent element. The tool detects repeated child groups automatically and writes them into columns.

## Windows?

The Windows app is created at `dist\XML-to-CSV.exe`. PyInstaller builds for the
operating system it runs on, so macOS and Windows packages must be built on
their respective platforms.

The generated apps are local-only and have no network functionality.
