# Proxy Checker & Scraper

A Python project that **scrapes free proxy lists from multiple sources** and stores them in a local database for later checking or use.

This tool:
- Collects IP:PORT proxies from a list of sources
- Prevents duplicate entries
- Saves proxies into **SQLite via SQLAlchemy**
- Designed to be extensible with a proxy checker module

---

## Features

- Scrape proxy lists from multiple GitHub URLs
- Store proxies in a structured SQLite database
- Prevent duplicate proxies (host + port) on scrape
- Easy integration with a proxy **checker system**
- Minimal dependencies (requests, SQLAlchemy)

---

## Requirements

Make sure you have:

- Python 3.8+
- `requests`
- `SQLAlchemy`
- `PySocks`
- `schedule`

Install dependencies:

```bash
pip install -r requirements.txt
```
