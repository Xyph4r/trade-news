#!/usr/bin/env python3
"""Fetch closing levels for the market tables from free, keyless sources.

Usage:
  python3 scripts/market_data.py                    # latest closes
  python3 scripts/market_data.py --date 2026-11-20  # last close on or before that date
  python3 scripts/market_data.py --week 2026-11-20  # weekly table: that Friday vs the previous Friday

Prints a Markdown table: market, close, change in %, date of the close, source.
Any market it cannot fetch is printed as n/a. It never guesses. Only fixed URLs below are
contacted; nothing is sent except the request itself.
"""
import argparse
import csv
import datetime as dt
import io
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET

UA = {"User-Agent": "Mozilla/5.0 (compatible; markets-briefing/1.0)"}
TIMEOUT = 20
# Futures (Brent, WTI, gold, copper) are continuous front-month contracts; on a contract
# roll day the change can differ from news reports. Say so in the post when they disagree.

# (label, kind, id). Yahoo chart symbols; MSCI indices are not free, so iShares ETFs stand in.
MARKETS = [
    ("S&P 500", "yahoo", "^GSPC"),
    ("Nasdaq 100", "yahoo", "^NDX"),
    ("Dow Jones", "yahoo", "^DJI"),
    ("Euro Stoxx 50", "yahoo", "^STOXX50E"),
    ("DAX", "yahoo", "^GDAXI"),
    ("FTSE 100", "yahoo", "^FTSE"),
    ("CAC 40", "yahoo", "^FCHI"),
    ("SMI", "yahoo", "^SSMI"),
    ("Nikkei 225", "yahoo", "^N225"),
    ("Hang Seng", "yahoo", "^HSI"),
    ("Shanghai Composite", "yahoo", "000001.SS"),
    ("KOSPI", "yahoo", "^KS11"),
    ("Sensex", "yahoo", "^BSESN"),
    ("MSCI World (iShares ETF, USD)", "yahoo", "URTH"),
    ("MSCI Emerging Markets (iShares ETF, USD)", "yahoo", "EEM"),
    ("VIX", "yahoo", "^VIX"),
    ("EUR/USD (ECB reference rate)", "ecb", "USD"),
    ("EUR/USD (market)", "yahoo", "EURUSD=X"),
    ("USD/JPY", "yahoo", "JPY=X"),
    ("US 10y yield (%)", "fred", "DGS10"),
    ("Bund 10y yield (%)", "bbk", "BBSIS/D.I.ZST.ZI.EUR.S1311.B.A604.R10XX.R.A.A._Z._Z.A"),
    ("Brent crude (USD)", "yahoo", "BZ=F"),
    ("WTI crude (USD)", "yahoo", "CL=F"),
    ("Gold (USD/oz, futures)", "yahoo", "GC=F"),
    ("Copper (USD/lb, futures)", "yahoo", "HG=F"),
]
SOURCE_NAME = {"yahoo": "Yahoo Finance", "ecb": "ECB", "fred": "FRED", "bbk": "Bundesbank"}


def get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or UA)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def series_yahoo(sym):
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
           + urllib.request.quote(sym) + "?range=3mo&interval=1d")
    res = json.loads(get(url))["chart"]["result"][0]
    out = []
    for ts, c in zip(res["timestamp"], res["indicators"]["quote"][0]["close"]):
        if c is not None:
            out.append((dt.datetime.utcfromtimestamp(ts).date(), float(c)))
    return out


def series_ecb(cur):
    xml = get("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml")
    root = ET.fromstring(xml)
    out = []
    for cube in root.iter():
        t = cube.attrib.get("time")
        if t:
            for c in cube:
                if c.attrib.get("currency") == cur:
                    out.append((dt.date.fromisoformat(t), float(c.attrib["rate"])))
    return sorted(out)


def series_fred(sid):
    # FRED stalls on browser-like User-Agents but answers plain command-line clients.
    text = get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}", {"User-Agent": "curl/8.5.0"})
    out = []
    for row in list(csv.reader(io.StringIO(text)))[1:]:
        try:
            out.append((dt.date.fromisoformat(row[0]), float(row[1])))
        except (ValueError, IndexError):
            continue
    return out[-120:]


def series_bbk(key):
    flow, series = key.split("/", 1)
    text = get(f"https://api.statistiken.bundesbank.de/rest/download/{flow}/{series}?format=csv&lang=en")
    out = []
    for row in csv.reader(io.StringIO(text)):
        if len(row) >= 2:
            try:
                out.append((dt.date.fromisoformat(row[0]), float(row[1].replace(",", "."))))
            except ValueError:
                continue
    return out[-120:]


FETCH = {"yahoo": series_yahoo, "ecb": series_ecb, "fred": series_fred, "bbk": series_bbk}


def on_or_before(series, day):
    pts = [p for p in series if p[0] <= day]
    return pts


def fmt(x):
    return f"{x:,.2f}" if abs(x) >= 10 else f"{x:,.4f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", type=dt.date.fromisoformat)
    ap.add_argument("--week", type=dt.date.fromisoformat, help="Friday of the week to summarise")
    a = ap.parse_args()
    end = a.week or a.date or dt.date.today()

    if a.week:
        print("| Market | Close | Week | Close date | Source |")
    else:
        print("| Market | Close | Change | Close date | Source |")
    print("|---|---|---|---|---|")
    failures = 0
    for label, kind, ident in MARKETS:
        try:
            pts = on_or_before(FETCH[kind](ident), end)
            last_d, last = pts[-1]
            if a.week:
                ref = [p for p in pts if p[0] <= last_d - dt.timedelta(days=7)]
                prev = ref[-1][1]
            else:
                prev = pts[-2][1]
            if "yield" in label:
                chg = f"{(last - prev) * 100:+.0f} bp"
            else:
                chg = f"{(last / prev - 1) * 100:+.2f}%"
            print(f"| {label} | {fmt(last)} | {chg} | {last_d.isoformat()} | {SOURCE_NAME[kind]} |")
        except Exception as e:  # noqa: BLE001 - one failed source must not stop the table
            failures += 1
            print(f"| {label} | n/a | n/a | | {SOURCE_NAME[kind]} (failed: {type(e).__name__}) |")
    print(f"\n{len(MARKETS) - failures} of {len(MARKETS)} markets fetched.", file=sys.stderr)


if __name__ == "__main__":
    main()
