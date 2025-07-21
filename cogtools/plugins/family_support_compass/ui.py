from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
from PySide6.QtCore import Qt
from .planner import PlannerWidget
from .exec_aid import ExecAidWidget
from .trigger_dashboard import TriggerDashboardWidget
from .comm_assistant import CommAssistantWidget
from .child_journal import ChildJournalWidget

class FamilySupportCompassWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Family Support & Relationship Compass")
        self.setStyleSheet("background: #222; color: #fff;")
        main_layout = QVBoxLayout()
        nav_layout = QHBoxLayout()
        self.stacked = QStackedWidget()

        # Navigation buttons
        self.btn_planner = QPushButton("Planner")
        self.btn_exec = QPushButton("Exec Aid")
        self.btn_triggers = QPushButton("Triggers")
        self.btn_comm = QPushButton("Comm Assist")
        self.btn_journal = QPushButton("Journal")
        for btn in [self.btn_planner, self.btn_exec, self.btn_triggers, self.btn_comm, self.btn_journal]:
            btn.setStyleSheet("background: #444; color: #fff; font-weight: bold; padding: 8px; border-radius: 6px;")
            nav_layout.addWidget(btn)

        # Add core component widgets
        self.planner = PlannerWidget()
        self.exec_aid = ExecAidWidget()
        self.triggers = TriggerDashboardWidget()
        self.comm = CommAssistantWidget()
        self.journal = ChildJournalWidget()
        self.stacked.addWidget(self.planner)
        self.stacked.addWidget(self.exec_aid)
        self.stacked.addWidget(self.triggers)
        self.stacked.addWidget(self.comm)
        self.stacked.addWidget(self.journal)

        # Button navigation logic
        self.btn_planner.clicked.connect(lambda: self.stacked.setCurrentWidget(self.planner))
        self.btn_exec.clicked.connect(lambda: self.stacked.setCurrentWidget(self.exec_aid))
        self.btn_triggers.clicked.connect(lambda: self.stacked.setCurrentWidget(self.triggers))
        self.btn_comm.clicked.connect(lambda: self.stacked.setCurrentWidget(self.comm))
        self.btn_journal.clicked.connect(lambda: self.stacked.setCurrentWidget(self.journal))

        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.stacked)
        self.setLayout(main_layout)
        self.stacked.setCurrentWidget(self.planner)