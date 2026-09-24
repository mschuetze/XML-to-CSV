# XML to CSV

A small, local-only desktop utility for converting one or more XML files into
UTF-16 CSV files. It uses Python's standard library, so it runs on macOS Intel,
Apple silicon, and Windows without uploading or transmitting any file data.

## Requirements

- Python 3.9 or newer
  - download from here: https://www.python.org/downloads/
- macOS or Windows

## Run

- copy the XML-to-CSV.app to your Mac´s PROGRAM folder
- double-click the app icon

## Windows?

The Windows app is created at `dist\XML-to-CSV.exe`. PyInstaller builds for the
operating system it runs on, so macOS and Windows packages must be built on
their respective platforms.

The generated apps are local-only and have no network functionality.
