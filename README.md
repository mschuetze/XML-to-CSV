# XML to CSV

A small, local-only desktop utility for converting one or more XML files into
UTF-16 CSV files. It uses Python's standard library, so it runs on macOS Intel,
Apple silicon, and Windows without uploading or transmitting any file data.

## Requirements

- Python 3.9 or newer
- macOS or Windows

## Run

```bash
python3 xml_to_csv.py
```

The file picker opens immediately. Select one or more XML files; each CSV is
written next to its source with the same filename and a `.csv` extension.

The converter treats repeated child elements as records. For example, repeated
`<item>` elements become rows. Nested values are flattened into column names
such as `customer.name`, and XML attributes use names such as `@id`.

If an XML file has no repeated element, its first-level children are treated as
rows. Existing CSV files are replaced only after the XML has parsed
successfully.

## Build a standalone app

On macOS, install PyInstaller once and build the double-clickable application:

```bash
python3 -m pip install pyinstaller
python3 -m PyInstaller --clean --noconfirm --windowed --target-architecture universal2 --name XML-to-CSV xml_to_csv.py
```

The app is created at `dist/XML-to-CSV.app`. Open it from Finder or copy it to
Applications. It launches the XML file picker immediately and does not open a
terminal window.

To build a Windows executable, run the same command on Windows:

```powershell
py -m pip install pyinstaller
py -m PyInstaller --clean --noconfirm --windowed --name XML-to-CSV xml_to_csv.py
```

The Windows app is created at `dist\XML-to-CSV.exe`. PyInstaller builds for the
operating system it runs on, so macOS and Windows packages must be built on
their respective platforms.

The generated apps are local-only and have no network functionality.
