from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class FamilySupportCompassWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Family Support & Relationship Compass"))
        layout.addWidget(QLabel("- Co-Parenting Planner"))
        layout.addWidget(QLabel("- Executive Function Aid"))
        layout.addWidget(QLabel("- Trigger Management Dashboard"))
        layout.addWidget(QLabel("- Tone-Friendly Communication Assistant"))
        layout.addWidget(QLabel("- Child Behavior Journal"))
        self.setLayout(layout)