#!/usr/bin/env python3
"""Liest den Abfallkalender von florstadt.de für einen Stadtteil aus (Playwright).

Aufruf:
    pip install playwright beautifulsoup4 && playwright install chromium
    python abfall_florstadt.py                         # Stammheim -> calendar/abfall_26_stam_RBG_18h.{json,ics}
    python abfall_florstadt.py -o Staden
    python abfall_florstadt.py -f RBG -e 18            # R=Restmüll, B=Blaue Tonne, G=Gelbe Tonne; Alarm um 18:00
    python abfall_florstadt.py -f K -e 10              # Nur Kompost/Bioabfall um 10:00
    python abfall_florstadt.py -y 2027                 # Nur Termine für 2027
    python abfall_florstadt.py --show                  # Browser sichtbar (zum Debuggen)
"""
import argparse
import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL = "https://www.florstadt.de/abfallkalender/"
ORTE = {  # Term-IDs aus dem <select>
    "Leidhecken": "948", "Nieder-Florstadt": "946", "Nieder-Mockstadt": "950",
    "Ober-Florstadt": "947", "Staden": "949", "Stammheim": "951",
}
ORTS_KURZNAMEN = {
    "Ober-Florstadt": "oflo",
    "Nieder-Florstadt": "nflo",
    "Staden": "stad",
    "Stammheim": "stam",
    "Nieder-Mockstadt": "nimo",
    "Leidhecken": "leid",
}
CALENDAR_DIR = Path(__file__).resolve().parent / "calendar"
MONATE = {"jan": 1, "feb": 2, "mär": 3, "mrz": 3, "apr": 4, "mai": 5, "jun": 6,
          "jul": 7, "aug": 8, "sep": 9, "okt": 10, "nov": 11, "dez": 12}
LIST = "#filter-query-id"
CARD = f"{LIST} .jet-listing-grid__item"
ABFALL_TYPEN = {
    "R": "Restmüll",
    "B": "Blaue Tonne",
    "G": "Gelbe Tonne",
    "K": "Kompost/Bioabfall",
    "Gr": "Grünabfälle",
    "A": "Abfallsammelplatz",
}
FILTER_TYPEN = {"Restmüll", "Blaue Tonne", "Gelbe Tonne"}  # Default-Filter (R, B, G)


def parse_datum(s: str) -> date:
    m = re.match(r"\s*(\d{1,2})\.\s*([A-Za-zäÄ]+)\.?\s*(\d{4})", s)
    return date(int(m.group(3)), MONATE[m.group(2).lower()[:3]], int(m.group(1)))


def parse_karten(html: str, filter_typen=None):
    if filter_typen is None:
        filter_typen = FILTER_TYPEN
    soup = BeautifulSoup(html, "html.parser")
    out = set()
    for card in soup.select(".jet-listing-grid__item"):
        h = card.select_one("h4.elementor-heading-title")
        d = card.select_one(".jet-listing-dynamic-field__content")
        if h and d:
            art = h.get_text(strip=True)
            # Nur gewünschte Mülltypen hinzufügen
            if art in filter_typen:
                out.add((parse_datum(d.get_text()), art))
    return sorted(out)


def scrape(ort: str, headless: bool = True, filter_typen=None):
    if filter_typen is None:
        filter_typen = FILTER_TYPEN
    with sync_playwright() as p:
        b = p.chromium.launch(headless=headless)
        page = b.new_page(locale="de-DE")
        page.goto(URL, wait_until="networkidle")

        # Cookie-Banner (Borlabs) wegklicken, falls vorhanden
        for txt in ("Alle akzeptieren", "Nur essenzielle Cookies akzeptieren", "Ablehnen"):
            btn = page.get_by_role("button", name=txt)
            if btn.count():
                btn.first.click()
                break

        page.select_option("select[name='abfallkalender-kategorie']", value=ORTE[ort])
        page.wait_for_timeout(500)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)

        # "Mehr anzeigen" klicken, bis der Link verschwindet oder nichts mehr nachkommt
        while True:
            more = page.locator("#mehr-anzeigen")
            if not more.count() or not more.first.is_visible():
                break
            vorher = page.locator(CARD).count()
            more.first.evaluate("el => el.click()")  # JS-Klick, umgeht Overlays
            try:
                page.wait_for_function(
                    "([sel, n]) => document.querySelectorAll(sel).length > n",
                    arg=[CARD, vorher], timeout=8000)
            except Exception:
                break
            page.wait_for_load_state("networkidle")

        html = page.inner_html(LIST)
        b.close()
    return parse_karten(html, filter_typen)


def schreibe_ics(termine, ort, pfad, erinnerung_uhr=18):
    zeilen = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//abfall-florstadt//DE",
              f"X-WR-CALNAME:Abfall {ort}", "CALSCALE:GREGORIAN"]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    # Berechne relative Stunden vor Event-Start (00:00)
    stunden_davor = 24 - erinnerung_uhr
    for d, art in termine:
        slug = re.sub(r"\W+", "", art)
        zeilen += ["BEGIN:VEVENT", f"UID:{d:%Y%m%d}-{slug}@{ort}.florstadt", f"DTSTAMP:{stamp}",
                   f"DTSTART;VALUE=DATE:{d:%Y%m%d}",
                   f"DTEND;VALUE=DATE:{d + timedelta(days=1):%Y%m%d}",
                   f"SUMMARY:{art}",
                   "BEGIN:VALARM", "ACTION:DISPLAY",
                   f"TRIGGER:-PT{stunden_davor}H",
                   f"DESCRIPTION:Erinnerung: {art}", "END:VALARM",
                   "END:VEVENT"]
    zeilen.append("END:VCALENDAR")
    with open(pfad, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(zeilen) + "\r\n")


def ersetze_markierten_bereich(text: str, name: str, content: str) -> str:
    start = f"<!-- {name}:start -->"
    end = f"<!-- {name}:end -->"
    if start not in text or end not in text:
        return text
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return f"{before}{start}\n{content}\n{end}{after}"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Liest den Abfallkalender von florstadt.de und exportiert als JSON/ICS.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Beispiele:\n"
               "  python abfall_florstadt.py\n"
               "  python abfall_florstadt.py -o Staden -f RBG -e 17\n"
               "  python abfall_florstadt.py -f K -e 9\n"
               "  python abfall_florstadt.py -y 2027 -f RBG\n"
               "  python abfall_florstadt.py --show\n"
    )
    ap.add_argument(
        "-o", "--ort",
        default="Stammheim",
        choices=ORTE,
        help="Stadtteil (Standard: Stammheim)"
    )
    ap.add_argument(
        "-f", "--filter",
        default="RBG",
        help="Mülltypen-Filter (R=Restmüll, B=Blaue Tonne, G=Gelbe Tonne, K=Kompost/Bioabfall, Gr=Grünabfälle, A=Abfallsammelplatz) - Standard: RBG"
    )
    ap.add_argument(
        "-e", "--erinnerung",
        type=int,
        default=18,
        choices=range(0, 24),
        metavar="STUNDE",
        help="Uhrzeit der Erinnerung am Vortag (0-23, Standard: 18)"
    )
    ap.add_argument(
        "-y", "--year",
        type=int,
        help="Nur Termine für ein bestimmtes Jahr (z.B. 2026, 2027)"
    )
    ap.add_argument(
        "--show",
        action="store_true",
        help="Browser sichtbar machen (zum Debuggen)"
    )
    a = ap.parse_args()
    
    # Filter-Codes in Typ-Namen umwandeln
    filter_codes = a.filter.upper()
    filter_typen = set()
    i = 0
    while i < len(filter_codes):
        # Prüfe auf zweistellige Codes (Gr)
        if i + 1 < len(filter_codes) and filter_codes[i:i+2] == "GR":
            if "Gr" in ABFALL_TYPEN:
                filter_typen.add(ABFALL_TYPEN["Gr"])
            i += 2
        elif filter_codes[i] in ABFALL_TYPEN:
            filter_typen.add(ABFALL_TYPEN[filter_codes[i]])
            i += 1
        else:
            ap.error(f"Ungültiger Filter-Code: '{filter_codes[i]}'. Nutzen Sie: R, B, G, K, Gr, A")
    
    if not filter_typen:
        ap.error(f"Ungültige Filter-Codes: {filter_codes}. Nutzen Sie: R (Restmüll), B (Blaue Tonne), G (Gelbe Tonne), K (Kompost), Gr (Grünabfälle), A (Sammelplatz)")
    
    termine = scrape(a.ort, headless=not a.show, filter_typen=filter_typen)
    
    # Filter nach Jahr, falls angegeben
    jahr = a.year if a.year else date.today().year
    if a.year:
        termine = [(d, t) for d, t in termine if d.year == a.year]
    
    # Generiere Dateinamen: abfall_{jahr2}_{ortkurz}_{filter}_{erinnerung}h
    kurzort = ORTS_KURZNAMEN[a.ort]
    jahr_zweistellig = jahr % 100
    basis_name = f"abfall_{jahr_zweistellig:02d}_{kurzort}_{a.filter.upper()}_{a.erinnerung}h"

    CALENDAR_DIR.mkdir(parents=True, exist_ok=True)
    json_pfad = CALENDAR_DIR / f"{basis_name}.json"
    ics_pfad = CALENDAR_DIR / f"{basis_name}.ics"

    with open(json_pfad, "w", encoding="utf-8") as f:
        json.dump([{"datum": d.isoformat(), "art": t} for d, t in termine],
                  f, ensure_ascii=False, indent=1)
    schreibe_ics(termine, a.ort, ics_pfad, erinnerung_uhr=a.erinnerung)
    print(f"{len(termine)} Termine für {a.ort}: "
          f"{termine[0][0] if termine else '-'} bis {termine[-1][0] if termine else '-'}")
