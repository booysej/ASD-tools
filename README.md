# CogTools: Cognitive Assist Tool Suite

A cross-platform, modular Python desktop suite for neurodiverse users, featuring a system tray launcher and plugin-based tools for focus, memory, executive function, and more.

## Features
- **System tray integration** (Windows, Mac, Linux)
- **Plugin architecture** for tools (task manager, memory vault, coding helper, etc.)
- **Accessible, minimal UI** (PySide6/Qt)
- **File-based data (YAML/MD/JSON)**, Git-friendly
- **Offline-first** with optional sync

## Requirements
- Python 3.9+
- [PySide6](https://pypi.org/project/PySide6/)
- (Optional) ruamel.yaml, markdown, other plugin deps

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

## Plugins
- Focus Task Manager (Kanban, reminders)
- Memory & Reference Vault (notes, recall, summarizer)
- Visual Coding Helper (flowcharts, code gen)
- Executive Function Coach (planner, timer, rewards)
- Settings Panel (cognitive assist, UI tweaks)

## Cross-Platform Notes
- **Windows**: System tray icon in notification area
- **Mac**: Tray icon in menu bar
- **Linux**: Tray icon in supported DEs (KDE, GNOME, XFCE, etc.)

## License
MIT
