import sys
import platform
from PySide6.QtWidgets import QApplication, QMessageBox
from cogtools.core.tray import CogToolsTray
from cogtools.core.main_window import CogToolsMainWindow
from cogtools.core.theme import theme

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("CogTools")
    app.setOrganizationName("CogTools")
    
    # Apply Apple-style theme
    theme.apply_theme()

    is_mac = platform.system() == "Darwin"
    tray_available = hasattr(QApplication, 'isSystemTrayAvailable') and QApplication.isSystemTrayAvailable()

    if tray_available:
        QApplication.setQuitOnLastWindowClosed(False)
        tray = CogToolsTray()
        tray.show()
        sys.exit(app.exec())
    else:
        # On macOS or if no tray, show main window directly as fallback
        if is_mac:
            main_window = CogToolsMainWindow()
            main_window.show()
            sys.exit(app.exec())
        else:
            QMessageBox.critical(None, "CogTools", "No system tray detected on this system.")
            sys.exit(1)

if __name__ == "__main__":
    main()