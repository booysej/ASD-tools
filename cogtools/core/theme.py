from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication

def apply_flat_theme():
    app = QApplication.instance()
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor('#222'))
    palette.setColor(QPalette.WindowText, QColor('#fff'))
    palette.setColor(QPalette.Base, QColor('#333'))
    palette.setColor(QPalette.AlternateBase, QColor('#222'))
    palette.setColor(QPalette.ToolTipBase, QColor('#fff'))
    palette.setColor(QPalette.ToolTipText, QColor('#222'))
    palette.setColor(QPalette.Text, QColor('#fff'))
    palette.setColor(QPalette.Button, QColor('#444'))
    palette.setColor(QPalette.ButtonText, QColor('#fff'))
    palette.setColor(QPalette.BrightText, QColor('#ff0000'))
    app.setPalette(palette)