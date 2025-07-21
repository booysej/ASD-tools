from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class SettingsPanelWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings Panel (cognitive assist options coming soon)"))
        self.setLayout(layout)