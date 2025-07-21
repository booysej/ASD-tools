import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from cogtools.core.tray import CogToolsTray
from cogtools.core.theme import theme

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("CogTools")
    app.setOrganizationName("CogTools")
    
    # Apply Apple-style theme
    theme.apply_theme()
    
    if not hasattr(QApplication, 'isSystemTrayAvailable') or not QApplication.isSystemTrayAvailable():
        QMessageBox.critical(None, "CogTools", "No system tray detected on this system.")
        sys.exit(1)
    QApplication.setQuitOnLastWindowClosed(False)
    tray = CogToolsTray()
    tray.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()