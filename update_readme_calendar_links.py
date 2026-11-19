#!/usr/bin/env python3
"""Aktualisiert die Downloadtabellen in README.md aus dem calendar/-Ordner."""

import re
from pathlib import Path

PROJEKT_DIR = Path(__file__).resolve().parent
CALENDAR_DIR = PROJEKT_DIR / "calendar"
README_PATH = PROJEKT_DIR / "README.md"

ORTS_KURZNAMEN = {
    "oflo": "Ober-Florstadt",
    "nflo": "Nieder-Florstadt",
    "stad": "Staden",
    "stam": "Stammheim",
    "nimo": "Nieder-Mockstadt",
    "leid": "Leidhecken",
}

FILTER_NAMEN_DE = {
    "R": "Restmüll",
    "B": "Blaue Tonne",
    "G": "Gelbe Tonne",
    "K": "Kompost/Bioabfall",
    "GR": "Grünabfälle",
    "A": "Abfallsammelplatz",
}
FILTER_NAMEN_EN = {
    "R": "Residual waste",
    "B": "Blue bin",
    "G": "Yellow bin",
    "K": "Compost/bio waste",
    "GR": "Green waste",
    "A": "Recycling center",
}


def filter_codes_zerlegen(filter_codes: str) -> list[str]:
    codes = []
    i = 0
    while i < len(filter_codes):
        code = "GR" if filter_codes[i:i + 2] == "GR" else filter_codes[i]
        codes.append(code)
        i += len(code)
    return codes


def ersetze_markierten_bereich(text: str, name: str, content: str) -> str:
    start = f"<!-- {name}:start -->"
    end = f"<!-- {name}:end -->"
    if start not in text or end not in text:
        return text
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return f"{before}{start}\n{content}\n{end}{after}"


def erstelle_html_tabelle(headers: list[str], zeilen: list[list[str]]) -> str:
    kopf = "\n".join(f"      <th>{wert}</th>" for wert in headers)
    reihen = []
    for zeile in zeilen:
        zellen = "\n".join(f"      <td>{wert}</td>" for wert in zeile)
        reihen.append("    <tr>\n" + zellen + "\n    </tr>")

    return (
        '<table>\n'
        '  <thead>\n'
        '    <tr>\n'
        f'{kopf}\n'
        '    </tr>\n'
        '  </thead>\n'
        '  <tbody>\n'
        + "\n".join(reihen)
        + '\n  </tbody>\n'
        '</table>'
    )


def sammle_kalender() -> dict[str, dict[str, Path]]:
    dateien: dict[str, dict[str, Path]] = {}
    muster = re.compile(r"abfall_(\d{2})_(.+)_([A-ZGRKA]+)_([0-9]+)h\.(ics|json)")

    for pfad in sorted(CALENDAR_DIR.glob("abfall_*.*")):
        match = muster.fullmatch(pfad.name)
        if not match:
            continue
        _, _, _, _, extension = match.groups()
        stem = pfad.stem
        dateien.setdefault(stem, {})[extension] = pfad

    return dateien


def aktualisiere_readme() -> None:
    dateien = sammle_kalender()

    muster = re.compile(r"abfall_(\d{2})_(.+)_([A-ZGRKA]+)_([0-9]+)h")

    eintraege = []
    for stem in dateien:
        dateiformate = dateien[stem]
        if "ics" not in dateiformate or "json" not in dateiformate:
            continue

        match = muster.fullmatch(stem)
        if not match:
            continue

        jahr, ortkurz, filter_codes, erinnerung = match.groups()
        eintraege.append((
            ORTS_KURZNAMEN.get(ortkurz, ortkurz),
            int(jahr),
            int(erinnerung),
            filter_codes,
            dateiformate,
        ))

    eintraege.sort(key=lambda e: (e[0].casefold(), -e[1], e[2], e[3]))

    zeilen_de = []
    zeilen_en = []

    for ort, jahr, erinnerung, filter_codes, dateiformate in eintraege:
        codes = filter_codes_zerlegen(filter_codes)
        deutsche_inhalte = ", ".join(FILTER_NAMEN_DE.get(code, code) for code in codes)
        englische_inhalte = ", ".join(FILTER_NAMEN_EN.get(code, code) for code in codes)
        links = (
            f"calendar/{dateiformate['ics'].name}",
            f"calendar/{dateiformate['json'].name}",
        )

        zeilen_de.append([
            f"20{jahr:02d}", ort, deutsche_inhalte, f"{erinnerung}:00 Uhr am Vortag",
            f'<a href="{links[0]}">ICS herunterladen</a>',
            f'<a href="{links[1]}">JSON herunterladen</a>',
        ])
        zeilen_en.append([
            f"20{jahr:02d}", ort, englische_inhalte, f"{erinnerung}:00 on the previous day",
            f'<a href="{links[0]}">Download ICS</a>',
            f'<a href="{links[1]}">Download JSON</a>',
        ])

    if zeilen_de:
        tabelle_de = erstelle_html_tabelle(
            ["Jahr", "Ort", "Mülltypen", "Erinnerung", "iCalendar", "JSON"], zeilen_de
        )
        tabelle_en = erstelle_html_tabelle(
            ["Year", "Location", "Waste types", "Reminder", "iCalendar", "JSON"], zeilen_en
        )
    else:
        tabelle_de = "Noch keine vollständigen Kalenderdateien vorhanden."
        tabelle_en = "No complete calendar files are available yet."

    text = README_PATH.read_text(encoding="utf-8")
    inhalt_de = "Die bereits erzeugten Kalender können direkt heruntergeladen werden:\n\n" + tabelle_de
    inhalt_en = "Pre-generated calendars:\n\n" + tabelle_en
    text = ersetze_markierten_bereich(text, "calendar-downloads", inhalt_de)
    text = ersetze_markierten_bereich(text, "calendar-downloads-en", inhalt_en)
    README_PATH.write_text(text, encoding="utf-8", newline="\n")
    print(f"README aktualisiert: {len(dateien)} Kalenderdateipaar(e) gefunden.")


if __name__ == "__main__":
    aktualisiere_readme()
