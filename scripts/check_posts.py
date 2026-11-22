#!/usr/bin/env python3
"""Safety and privacy checks for posts before they are committed and published.

Usage: python3 scripts/check_posts.py [files...]   (default: every file in _posts/)
Exits 1 and lists every problem if a check fails.
"""
import pathlib
import re
import sys

ISIN = re.compile(r"\b([A-Z]{2}[A-Z0-9]{9}[0-9])\b")
FORBIDDEN_HTML = [
    (re.compile(r"<\s*(script|iframe|object|embed|form|input|style|link|meta|base|svg)\b", re.I), "forbidden HTML tag"),
    (re.compile(r"\son[a-z]+\s*=", re.I), "inline event handler"),
    (re.compile(r"javascript\s*:", re.I), "javascript: URL"),
    (re.compile(r"data\s*:\s*text/html", re.I), "data: HTML URL"),
    (re.compile(r"!\[[^\]]*\]\(\s*https?://", re.I), "external image"),
    (re.compile(r"<\s*img\b", re.I), "HTML image"),
    (re.compile(r"\]\(\s*http://", re.I), "non-HTTPS link"),
]
PRIVATE_WORDS = re.compile(r"\b(my (portfolio|holdings?|depot|position)|mein(e|em)? (depot|portfolio|position)|position size)\b", re.I)
SECRET = re.compile(r"(gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9-]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
NAME = re.compile(r"^\d{4}-\d{2}-\d{2}-(daily|weekly-recap|weekend)\.md$")
REQUIRED_FM = ("layout:", "title:", "title_de:", "date:", "categories:")


def isin_valid(code: str) -> bool:
    digits = "".join(str(int(c, 36)) for c in code[:-1])
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2 == 0:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return (10 - total % 10) % 10 == int(code[-1])


def check(path: pathlib.Path) -> list:
    problems = []
    if path.name == ".gitkeep":
        return problems
    if not NAME.match(path.name):
        problems.append("file name must be YYYY-MM-DD-daily.md, -weekly-recap.md or -weekend.md")
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or text.count("\n---\n") < 1:
        problems.append("missing front matter")
    else:
        fm = text.split("\n---\n", 1)[0]
        for key in REQUIRED_FM:
            if key not in fm:
                problems.append(f"front matter lacks {key.rstrip(':')}")
        m = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", fm, re.M)
        if m and not path.name.startswith(m.group(1)):
            problems.append("date in front matter does not match the file name")
    if 'class="lang-en"' not in text or 'class="lang-de"' not in text:
        problems.append("needs both an English and a German block")
    for code in set(ISIN.findall(text)):
        if isin_valid(code):
            problems.append(f"contains an ISIN ({code}); holdings must stay private")
    for rx, label in FORBIDDEN_HTML:
        if rx.search(text):
            problems.append(label)
    if PRIVATE_WORDS.search(text):
        problems.append("mentions personal holdings or positions")
    if SECRET.search(text):
        problems.append("looks like it contains a secret or token")
    for marker in ("TODO", "YYYY-MM-DD", "DD MONTH", "<!--"):
        if marker in text:
            problems.append(f"leftover template text: {marker}")
    return problems


def main(argv):
    files = [pathlib.Path(a) for a in argv] or sorted(pathlib.Path("_posts").glob("*"))
    failed = False
    for f in files:
        for p in check(f):
            failed = True
            print(f"{f}: {p}")
    if failed:
        return 1
    print(f"OK: {len(files)} file(s) checked")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
