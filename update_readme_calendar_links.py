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

    zeilen_de = [
        "Die bereits erzeugten Kalender können direkt heruntergeladen werden:",
        "",
        "| Jahr | Ort | Mülltypen | Erinnerung | iCalendar | JSON |",
        "|---|---|---|---|---|---|",
    ]
    zeilen_en = [
        "Pre-generated calendars:",
        "",
        "| Year | Location | Waste types | Reminder | iCalendar | JSON |",
        "|---|---|---|---|---|---|",
    ]

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

    # Ort aufsteigend, neues Jahr zuerst, Erinnerung aufsteigend.
    # Die Filterkombination ist ein zusätzliches, deterministisches Kriterium.
    eintraege.sort(key=lambda e: (e[0].casefold(), -e[1], e[2], e[3]))

    for ort, jahr, erinnerung, filter_codes, dateiformate in eintraege:
        codes = filter_codes_zerlegen(filter_codes)
        deutsche_inhalte = ", ".join(FILTER_NAMEN_DE.get(code, code) for code in codes)
        englische_inhalte = ", ".join(FILTER_NAMEN_EN.get(code, code) for code in codes)

        links = (
            f"calendar/{dateiformate['ics'].name}",
            f"calendar/{dateiformate['json'].name}",
        )
        zeilen_de.append(
            f"| 20{jahr:02d} | {ort} | {deutsche_inhalte} | {erinnerung}:00 Uhr am Vortag | "
            f"[ICS herunterladen]({links[0]}) | [JSON herunterladen]({links[1]}) |"
        )
        zeilen_en.append(
            f"| 20{jahr:02d} | {ort} | {englische_inhalte} | {erinnerung}:00 on the previous day | "
            f"[Download ICS]({links[0]}) | [Download JSON]({links[1]}) |"
        )

    if len(zeilen_de) == 4:
        zeilen_de.extend(["", "Noch keine vollständigen Kalenderdateien vorhanden."])
        zeilen_en.extend(["", "No complete calendar files are available yet."])

    text = README_PATH.read_text(encoding="utf-8")
    text = ersetze_markierten_bereich(text, "calendar-downloads", "\n".join(zeilen_de))
    text = ersetze_markierten_bereich(text, "calendar-downloads-en", "\n".join(zeilen_en))
    README_PATH.write_text(text, encoding="utf-8", newline="\n")
    print(f"README aktualisiert: {len(dateien)} Kalenderdateipaar(e) gefunden.")


if __name__ == "__main__":
    aktualisiere_readme()
