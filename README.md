# Cwelium – Refactored Discord Tool

**Modernized, modularized, cleaned-up version of the original Cwelium raiding tool**

**Original author**: Tips-Discord  
**Original repo**: https://github.com/Tips-Discord/Cwelium  
**Refactored & improved by**: [ryuka](https://ryukap.netlify.app/)  
**Date of refactor**: January 2026

## What is Cwelium?

Cwelium is a multi-functional Discord utility / raiding tool that includes:

- Mass joining / leaving servers
- Channel & DM spamming
- Voice join / soundboard spam
- Member scraping
- Token checking & formatting
- Reaction / button automation
- Nickname / bio mass changing
- Thread / typing spam
- Onboarding / rules screening bypass
- Call spamming

**Important legal notice**  
This tool was created for **educational and security research purposes only**.  
Using it to harm servers, harass users, spam, raid, or violate Discord's ToS is **strictly prohibited** and can result in permanent account termination and/or legal consequences.

## Why this refactor exists

The original Cwelium was written as a **single ~2000+ line file** — very hard to read, maintain, extend or debug.

This version keeps **100% of the original functionality** but applies modern Python best practices:

| Aspect                        | Original (single file)                     | Refactored version                              |
|-------------------------------|---------------------------------------------|-------------------------------------------------|
| File structure                | Everything in one file                      | Modular package (9 files)                       |
| Code organization             | Global variables, mixed concerns            | Clear separation of concerns                    |
| Imports                       | Many at top, some repeated                  | Clean, local imports per file                   |
| Relative imports              | Not used                                    | Proper package-style relative imports           |
| Threading / proxy logic       | Inline, repeated code                       | Centralized in `raider._run_threads()`          |
| Error handling                | Inconsistent                                | More consistent logging + try/except blocks     |
| Readability                   | Low (long functions, no separation)         | High (short methods, docstrings, type hints)    |
| Extensibility                 | Very difficult                              | Easy to add new features / actions              |

## Code layout (project structure)
```bash
Cwelium/
├── cwelium/                        # ← actual Python package
│   ├── init.py
│   ├── config.py                   # colors, config loading
│   ├── console.py                  # ASCII art, logging, prompts, UI
│   ├── files.py                    # config/folders/files/tokens/proxies handling
│   ├── utils.py                    # helpers (random string, decorator, member range logic)
│   ├── scraper.py                  # Discord gateway WebSocket member scraper
│   ├── raider.py                   # core Discord API actions (join, spam, dm, voice, etc.)
│   ├── menu.py                     # interactive CLI menu + option handlers
│   └── main.py                     # entry point – initializes everything & starts menu
│
├── data/
│   ├── tokens.txt                  # one token per line
│   └── proxies.txt                 # http proxies (optional)
│
├── scraped/                        # auto-generated member ID caches
│
├── config.json                     # auto-created (proxies on/off, theme color)
└── README.md                       # ← you're reading this
```


## Installation & Usage

1. Clone / download this repository
2. Install dependencies

```bash
pip install -r requirements.txt
```

2. Add tokens Put your Discord tokens (one per line) into:
```bash
data/tokens.txt
```

3. (Optional) Add proxies
```bash
data/proxies.txt
```
Format: ip:port or user:pass@ip:port

4. Run the tool
   
Make sure you run this in the home dir (\Cwelium)
```bash
python -m cwelium.main
```
Alternative (after adding sys.path hack to main.py):
```bash
python main.py
```

Use responsibly.
Stay safe.
Have fun learning.









