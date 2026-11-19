# Abfallkalender Florstadt

Python-Skript zum Auslesen des Abfallkalenders der Stadt Florstadt und zum Export der Termine als iCalendar (`.ics`) sowie JSON (`.json`).

## Inhaltsverzeichnis

- [Vorbereitete Kalender herunterladen](#vorbereitete-kalender-herunterladen)
- [Übersicht](#übersicht)
- [Unterstützte Orte](#unterstützte-orte)
- [Mülltypen](#mülltypen)
- [Installieren und Ausführen](#installieren-und-ausführen)
- [Kommandozeilen-Optionen](#kommandozeilen-optionen)
- [Beispiele](#beispiele)
- [Dateiname und Ausgabe](#dateiname-und-ausgabe)
- [Kalender importieren](#kalender-importieren)
- [README-Downloadtabelle aktualisieren](#readme-downloadtabelle-aktualisieren)
- [Hinweise und Haftung](#hinweise-und-haftung)
- [English version](#english-version)

## Vorbereitete Kalender herunterladen

<!-- calendar-downloads:start -->
Die bereits erzeugten Kalender können direkt heruntergeladen werden:

<table>
  <thead>
    <tr>
      <th>Jahr</th>
      <th>Ort</th>
      <th>Mülltypen</th>
      <th>Erinnerung</th>
      <th>iCalendar</th>
      <th>JSON</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2026</td>
      <td>Nieder-Florstadt</td>
      <td>Restmüll, Blaue Tonne, Gelbe Tonne</td>
      <td>18:00 Uhr am Vortag</td>
      <td><a href="calendar/abfall_26_nflo_RBG_18h.ics">ICS herunterladen</a></td>
      <td><a href="calendar/abfall_26_nflo_RBG_18h.json">JSON herunterladen</a></td>
    </tr>
    <tr>
      <td>2026</td>
      <td>Nieder-Florstadt</td>
      <td>Restmüll, Blaue Tonne, Gelbe Tonne, Kompost/Bioabfall</td>
      <td>18:00 Uhr am Vortag</td>
      <td><a href="calendar/abfall_26_nflo_RBGK_18h.ics">ICS herunterladen</a></td>
      <td><a href="calendar/abfall_26_nflo_RBGK_18h.json">JSON herunterladen</a></td>
    </tr>
    <tr>
      <td>2026</td>
      <td>Nieder-Mockstadt</td>
      <td>Restmüll, Blaue Tonne, Gelbe Tonne</td>
      <td>18:00 Uhr am Vortag</td>
      <td><a href="calendar/abfall_26_nimo_RBG_18h.ics">ICS herunterladen</a></td>
      <td><a href="calendar/abfall_26_nimo_RBG_18h.json">JSON herunterladen</a></td>
    </tr>
    <tr>
      <td>2026</td>
      <td>Nieder-Mockstadt</td>
      <td>Restmüll, Blaue Tonne, Gelbe Tonne, Kompost/Bioabfall</td>
      <td>18:00 Uhr am Vortag</td>
      <td><a href="calendar/abfall_26_nimo_RBGK_18h.ics">ICS herunterladen</a></td>
      <td><a href="calendar/abfall_26_nimo_RBGK_18h.json">JSON herunterladen</a></td>
    </tr>
    <tr>
      <td>2026</td>
      <td>Stammheim</td>
      <td>Restmüll, Blaue Tonne, Gelbe Tonne</td>
      <td>18:00 Uhr am Vortag</td>
      <td><a href="calendar/abfall_26_stam_RBG_18h.ics">ICS herunterladen</a></td>
      <td><a href="calendar/abfall_26_stam_RBG_18h.json">JSON herunterladen</a></td>
    </tr>
    <tr>
      <td>2026</td>
      <td>Stammheim</td>
      <td>Restmüll, Blaue Tonne, Gelbe Tonne, Kompost/Bioabfall</td>
      <td>18:00 Uhr am Vortag</td>
      <td><a href="calendar/abfall_26_stam_RBGK_18h.ics">ICS herunterladen</a></td>
      <td><a href="calendar/abfall_26_stam_RBGK_18h.json">JSON herunterladen</a></td>
    </tr>
  </tbody>
</table>
<!-- calendar-downloads:end -->

> [!NOTE]
> **Hinweis vom Maintainer**
>
> Wenn ihr Wünsche für weitere Kalender habt, meldet euch bei mir hier über die Issues oder über andere Kanäle. Ich kann nicht garantieren, dass das dann direkt umgesetzt wird.
>
> Kalender für das Folgejahr stehen erst zur Verfügung, wenn die Stadt Florstadt die entsprechenden Informationen veröffentlicht. Meldet euch bitte, falls ich die Veröffentlichung nicht mitbekomme.

[Wie kann ich einen Kalender importieren?](#kalender-importieren)

## Übersicht

Das Skript öffnet den Abfallkalender auf [florstadt.de](https://www.florstadt.de/abfallkalender/), liest die Termine für einen ausgewählten Stadtteil und exportiert sie in ein Maschinen-lesbares JSON-Dateiformat und in eine iCalendar-Datei.

Standardmäßig werden folgende Mülltypen erzeugt:

- Restmüll
- Blaue Tonne
- Gelbe Tonne

## Unterstützte Orte

- Leidhecken
- Nieder-Florstadt
- Nieder-Mockstadt
- Ober-Florstadt
- Staden
- Stammheim

## Mülltypen

| Filtercode | Mülltyp |
|---|---|
| `R` | Restmüll |
| `B` | Blaue Tonne |
| `G` | Gelbe Tonne |
| `K` | Kompost/Bioabfall |
| `Gr` | Grünabfälle |
| `A` | Abfallsammelplatz |

Mehrere Codes können kombiniert werden, zum Beispiel `RBGK` oder `KB`.

## Installieren und Ausführen

### Voraussetzungen

- Python 3
- Chromium über Playwright
- Internetzugang zur Florstädter Abfallkalender-Seite

### Installation

```bash
pip install beautifulsoup4 playwright
playwright install chromium
```

Dann im Projektverzeichnis ausführen:

```bash
python abfall_florstadt.py
```

Ohne zusätzliche Parameter werden die Termine für **Stammheim**, das Jahr **des aktuellen Systems**, die Filter **RBG** und eine Erinnerung um **18:00 Uhr am Vortag** erzeugt.

## Kommandozeilen-Optionen

| Option | Bedeutung | Standard |
|---|---|---|
| `-o`, `--ort` | Stadtteil | `Stammheim` |
| `-f`, `--filter` | Mülltypen-Codes | `RBG` |
| `-e`, `--erinnerung` | Erinnerung am Vortag in Uhrstunden | `18` |
| `-y`, `--year` | Nur ein bestimmtes Jahr exportieren | aktuelles Jahr |
| `--show` | Chromium-Fenster sichtbar öffnen | deaktiviert |

## Beispiele

```bash
python abfall_florstadt.py
python abfall_florstadt.py -o Staden
python abfall_florstadt.py -o Nieder-Florstadt -f RBGK -e 17
python abfall_florstadt.py -f K -e 10
python abfall_florstadt.py -y 2027 -f RBG
python abfall_florstadt.py --show
```

## Dateiname und Ausgabe

Die Dateien werden im Ordner `calendar/` gespeichert:

```text
abfall_<zweistelliges Jahr>_<Ortskürzel>_<Filter>_<Erinnerungsstunde>h
```

Beispiel:

```text
abfall_26_stam_RBG_18h.ics
abfall_26_stam_RBG_18h.json
```

Die Datei wird wie folgt erzeugt:

- `26` = Jahr 2026
- `stam` = Stammheim
- `RBG` = Restmüll, Blaue Tonne und Gelbe Tonne
- `18h` = Erinnerung um 18:00 Uhr am Vortag

Das JSON enthält Objekte mit dem Datum und der Müllart:

```json
[
  {
    "datum": "2026-02-06",
    "art": "Restmüll"
  }
]
```

Die ICS-Datei enthält ganztägige Kalenderereignisse samt Erinnerung.

## Kalender importieren

### Samsung Kalender und andere Android-Kalender

1. Auf dem Android-Gerät eine vorhandene `.ics`-Datei anklicken.
2. Mit der entsprechenden App öffnen (z. B. Samsung Kalender, Google Kalender).
3. Der Rest sollte von selbst passieren. Je nach App kann es sein, dass man den Kalender noch auswählen oder umbenennen muss.

### Google Calendar

1. [Eine vorhandene ICS-Datei](calendar/abfall_26_stam_RBG_18h.ics) herunterladen.
2. Google Calendar öffnen.
3. Über das Zahnradsymbol **Einstellungen → Kalender importieren** auswählen.
4. Die Datei auswählen und den gewünschten Kalender bestimmen.

### Apple Calendar

1. Eine vorhandene `.ics`-Datei herunterladen.
2. Die Datei in Apple Calendar öffnen oder per Drag-and-Drop hinzufügen.
3. Den Importkalender auswählen und gegebenenfalls umbenennen.

### Microsoft Outlook

1. Eine vorhandene `.ics`-Datei herunterladen.
2. In Outlook „Kalender importieren oder öffnen“ beziehungsweise „Aus Datei importieren“ auswählen.
3. Die Datei auswählen und den Import bestätigen.

Hinweis: Die ICS-Dateien verwenden Terminerinnerungen am Tag vor dem Abholtermin. Je nach Kalender-App werden Erinnerungen beim Import anders dargestellt oder in den Einstellungen angepasst.

## README-Downloadtabelle aktualisieren

Ein Hilfsskript zum Aktualisieren der Download-Links in dieser README-Datei ist vorhanden:

```bash
python update_readme_calendar_links.py
```

## Hinweise und Haftung

- Die Daten werden von der öffentlichen Website der Stadt Florstadt bezogen.
- Änderungen auf der Website oder eine vorübergehende Nichterreichbarkeit können den Abruf beeinträchtigen.
- Vor der Verwendung sollte die Aktualität der Termine mit dem offiziellen Abfallkalender abgeglichen werden.
- Das Projekt übernimmt keine Gewähr für Vollständigkeit, Aktualität oder korrekte Abfuhrzeiten.
- Das Projekt speichert keine persönlichen Daten.

Lizenz: [MIT License](LICENSE)

## English version

# Waste Collection Calendar for Florstadt

Python script that reads waste collection appointments for Florstadt, Germany, and exports them as iCalendar (`.ics`) and JSON (`.json`) files.

## Table of contents

- [Download existing calendars](#download-existing-calendars)
- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Command-line options](#command-line-options)
- [Examples](#examples)
- [Output files](#output-files)
- [Disclaimer and license](#disclaimer-and-license)

## Download existing calendars

<!-- calendar-downloads-en:start -->
Pre-generated calendars:

<table>
  <thead>
    <tr>
      <th>Year</th>
      <th>Location</th>
      <th>Waste types</th>
      <th>Reminder</th>
      <th>iCalendar</th>
      <th>JSON</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2026</td>
      <td>Nieder-Florstadt</td>
      <td>Residual waste, Blue bin, Yellow bin</td>
      <td>18:00 on the previous day</td>
      <td><a href="calendar/abfall_26_nflo_RBG_18h.ics">Download ICS</a></td>
      <td><a href="calendar/abfall_26_nflo_RBG_18h.json">Download JSON</a></td>
    </tr>
    <tr>
      <td>2026</td>
      <td>Nieder-Florstadt</td>
      <td>Residual waste, Blue bin, Yellow bin, Compost/bio waste</td>
      <td>18:00 on the previous day</td>
      <td><a href="calendar/abfall_26_nflo_RBGK_18h.ics">Download ICS</a></td>
      <td><a href="calendar/abfall_26_nflo_RBGK_18h.json">Download JSON</a></td>
    </tr>
    <tr>
      <td>2026</td>
      <td>Nieder-Mockstadt</td>
      <td>Residual waste, Blue bin, Yellow bin</td>
      <td>18:00 on the previous day</td>
      <td><a href="calendar/abfall_26_nimo_RBG_18h.ics">Download ICS</a></td>
      <td><a href="calendar/abfall_26_nimo_RBG_18h.json">Download JSON</a></td>
    </tr>
    <tr>
      <td>2026</td>
      <td>Nieder-Mockstadt</td>
      <td>Residual waste, Blue bin, Yellow bin, Compost/bio waste</td>
      <td>18:00 on the previous day</td>
      <td><a href="calendar/abfall_26_nimo_RBGK_18h.ics">Download ICS</a></td>
      <td><a href="calendar/abfall_26_nimo_RBGK_18h.json">Download JSON</a></td>
    </tr>
    <tr>
      <td>2026</td>
      <td>Stammheim</td>
      <td>Residual waste, Blue bin, Yellow bin</td>
      <td>18:00 on the previous day</td>
      <td><a href="calendar/abfall_26_stam_RBG_18h.ics">Download ICS</a></td>
      <td><a href="calendar/abfall_26_stam_RBG_18h.json">Download JSON</a></td>
    </tr>
    <tr>
      <td>2026</td>
      <td>Stammheim</td>
      <td>Residual waste, Blue bin, Yellow bin, Compost/bio waste</td>
      <td>18:00 on the previous day</td>
      <td><a href="calendar/abfall_26_stam_RBGK_18h.ics">Download ICS</a></td>
      <td><a href="calendar/abfall_26_stam_RBGK_18h.json">Download JSON</a></td>
    </tr>
  </tbody>
</table>
<!-- calendar-downloads-en:end -->

> [!NOTE]
> **Maintainer's Note**
>
> If you have requests for additional calendars, please contact me via the issues or through other channels. Implementation cannot be guaranteed or scheduled.
>
> Calendars for the following year will only be available when the city of Florstadt publishes the corresponding information. Please let me know if I miss the publication.

## Requirements

- Python 3
- Chromium via Playwright
- Internet access to the Florstadt waste calendar page

## Quick start

To run the script with default settings (Stammheim, current year, RBG filter, 18:00 alarm), use:

```bash
python abfall_florstadt.py
```

## Command-line options

| Option | Description | Default |
|---|---|---|
| `-o`, `--ort` | District | `Stammheim` |
| `-f`, `--filter` | Waste type codes | `RBG` |
| `-e`, `--erinnerung` | Alarm time the day before in hours | `18` |
| `-y`, `--year` | Export only a specific year | current year |
| `--show` | Open Chromium window visibly | disabled |

## Examples

```bash
python abfall_florstadt.py
python abfall_florstadt.py -o Staden
python abfall_florstadt.py -o Nieder-Florstadt -f RBGK -e 17
python abfall_florstadt.py -f K -e 10
python abfall_florstadt.py -y 2027 -f RBG
python abfall_florstadt.py --show
```

## Output files

The files are saved in the `calendar/` folder:

```text
abfall_<two-digit year>_<location code>_<filter>_<alarm hour>h
```

Example:

```text
abfall_26_stam_RBG_18h.ics
abfall_26_stam_RBG_18h.json
```

The file is generated as follows:

- `26` = Year 2026
- `stam` = Stammheim
- `RBG` = Residual waste, Blue bin, and Yellow bin
- `18h` = Alarm at 18:00 on the previous day

The JSON file contains objects with the date and waste type:

```json
[
  {
    "datum": "2026-02-06",
    "art": "Restmüll"
  }
]
```

The ICS file contains all-day calendar events with reminders.

## Importing calendars

### Samsung Calendar and other Android calendars

1. On the Android device, click on an existing `.ics` file.
2. Open with the corresponding app (e.g., Samsung Calendar, Google Calendar).
3. The rest should happen automatically. Depending on the app, you may need to select or rename the calendar.

### Google Calendar

1. [Download an existing ICS file](calendar/abfall_26_stam_RBG_18h.ics).
2. Open Google Calendar.
3. Select **Settings → Import calendar** via the gear icon.
4. Choose the file and specify the desired calendar.

### Apple Calendar

1. Download an existing `.ics` file.
2. Open the file in Apple Calendar or add it via drag-and-drop.
3. Select and rename the import calendar if necessary.

### Microsoft Outlook

1. Download an existing `.ics` file.
2. Select "Import or open calendar" or "Import from file" in Outlook.
3. Choose the file and confirm the import.

Note: The ICS files use reminder settings for the day before the collection date. Depending on the calendar app, reminders may be displayed differently or adjusted in the settings during import.

## Disclaimer and license

- Data is sourced from the public website of the city of Florstadt.
- Changes on the website or temporary unavailability may affect data retrieval.
- Please verify the currency of the dates with the official waste calendar before use.
- This project does not guarantee completeness, timeliness, or correct collection times.
- This project does not store any personal data.

License: [MIT License](LICENSE)
