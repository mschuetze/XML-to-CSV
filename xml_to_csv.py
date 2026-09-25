"""Convert XML files to UTF-16 CSV files using a native file picker."""

from __future__ import annotations

import csv
import os
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Dict, Iterable, List, Sequence
import xml.etree.ElementTree as ET

APP_VERSION = "1.0.0"


def local_name(tag: str) -> str:
    """Remove an XML namespace from a tag name."""
    return tag.rsplit("}", 1)[-1]


def add_value(row: Dict[str, str], key: str, value: str) -> None:
    """Keep duplicate leaf values instead of silently losing information."""
    if key not in row:
        row[key] = value
        return

    suffix = 2
    candidate = f"{key}_{suffix}"
    while candidate in row:
        suffix += 1
        candidate = f"{key}_{suffix}"
    row[candidate] = value


def flatten_element(element: ET.Element, prefix: str = "") -> Dict[str, str]:
    """Flatten an XML element's attributes and leaf descendants into a row."""
    row: Dict[str, str] = {}
    for name, value in element.attrib.items():
        add_value(row, f"{prefix}@{local_name(name)}", value)

    children = list(element)
    text = (element.text or "").strip()
    if text and not children:
        add_value(row, prefix or local_name(element.tag), text)

    for child in children:
        child_name = local_name(child.tag)
        child_prefix = f"{prefix}.{child_name}" if prefix else child_name
        child_row = flatten_element(child, child_prefix)
        for key, value in child_row.items():
            add_value(row, key, value)

    return row


def repeated_children(parent: ET.Element) -> List[ET.Element]:
    """Find the first group of repeated child tags, preserving document order."""
    children = list(parent)
    for child in children:
        same_tag = [candidate for candidate in children if local_name(candidate.tag) == local_name(child.tag)]
        if len(same_tag) > 1:
            return same_tag
    return []


def find_records(root: ET.Element) -> List[ET.Element]:
    """Find a natural repeated record group, falling back to the root's children."""
    direct_records = repeated_children(root)
    if direct_records:
        return direct_records

    for parent in root.iter():
        records = repeated_children(parent)
        if records:
            return records

    children = list(root)
    return children or [root]


def convert_xml(source: Path) -> Path:
    """Convert one XML file and return the path of the generated CSV."""
    root = ET.parse(source).getroot()
    rows = [flatten_element(record) for record in find_records(root)]

    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)

    destination = source.with_name(f"{source.stem}_UTF-16.csv")
    with destination.open("w", encoding="utf-16", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return destination


def format_error(source: Path, error: Exception) -> str:
    return f"{source.name}: {error}"


class ConverterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(f"XML to CSV v{APP_VERSION}")
        self.root.geometry("620x390")
        self.root.minsize(520, 320)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.status = tk.StringVar(value="Choose XML files to begin")
        self.progress = tk.DoubleVar(value=0)
        self.details = tk.Text(root, height=12, state="disabled", wrap="word")
        self.details.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        ttk.Progressbar(root, variable=self.progress, maximum=1).pack(fill="x", padx=20)
        ttk.Label(root, textvariable=self.status).pack(anchor="w", padx=20, pady=(8, 14))
        self.write_details(f"XML to CSV v{APP_VERSION}\n")

        root.after(150, self.choose_files)

    def choose_files(self) -> None:
        paths = filedialog.askopenfilenames(
            title="Choose XML files",
            filetypes=[("XML files", "*.xml"), ("All files", "*")],
        )
        if paths:
            self.convert_files([Path(path) for path in paths])
        else:
            self.status.set("No files selected")

    def convert_files(self, sources: Sequence[Path]) -> None:
        self.progress.set(0)
        self.status.set(f"Converting {len(sources)} file(s)...")
        self.write_details("Conversion started. Files stay on this computer.\n")
        threading.Thread(target=self._convert_files, args=(sources,), daemon=True).start()

    def _convert_files(self, sources: Sequence[Path]) -> None:
        converted: List[Path] = []
        errors: List[str] = []
        for index, source in enumerate(sources, start=1):
            try:
                destination = convert_xml(source)
                converted.append(destination)
                self.root.after(0, self.write_details, f"Created {destination}\n")
            except (OSError, ET.ParseError, csv.Error) as error:
                errors.append(format_error(source, error))
                self.root.after(0, self.write_details, f"Skipped {format_error(source, error)}\n")
            self.root.after(0, self.progress.set, index / len(sources))

        self.root.after(0, self.finished, converted, errors)

    def finished(self, converted: Iterable[Path], errors: Sequence[str]) -> None:
        converted_count = len(list(converted))
        if errors:
            self.status.set(f"Finished with {len(errors)} error(s)")
            messagebox.showwarning(
                "Conversion finished",
                f"Created {converted_count} CSV file(s).\n\n" + "\n".join(errors),
                parent=self.root,
            )
        else:
            self.status.set(f"Created {converted_count} CSV file(s)")
            messagebox.showinfo("Conversion finished", f"Created {converted_count} UTF-16 CSV file(s).", parent=self.root)

    def write_details(self, text: str) -> None:
        self.details.configure(state="normal")
        self.details.insert("end", text)
        self.details.see("end")
        self.details.configure(state="disabled")


def main() -> None:
    if sys.platform == "darwin":
        os.environ.setdefault("TK_SILENCE_DEPRECATION", "1")
    root = tk.Tk()
    ConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()