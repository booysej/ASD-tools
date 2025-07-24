from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
from PySide6.QtCore import Qt
from .planner import PlannerWidget
from .exec_aid import ExecAidWidget
from .trigger_dashboard import TriggerDashboardWidget
from .comm_assistant import CommAssistantWidget
from .child_journal import ChildJournalWidget
from .sensory_toolkit import SensoryToolkitWidget
from .social_skills_trainer import SocialSkillsTrainerWidget

class FamilySupportCompassWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Family Support & Relationship Compass")
        self.setup_ui()

    def setup_ui(self):
        """Setup the enhanced family support compass UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header with title
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background-color: #007AFF;
                color: white;
                padding: 15px;
            }
        """)
        header_layout = QHBoxLayout(header_widget)
        
        title_label = QLabel("👨‍👩‍👧‍👦 Family Support & Relationship Compass")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: white;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        main_layout.addWidget(header_widget)
        
        # Navigation and content
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Enhanced navigation sidebar
        nav_widget = QWidget()
        nav_widget.setFixedWidth(250)
        nav_widget.setStyleSheet("""
            QWidget {
                background-color: #F2F2F7;
                border-right: 1px solid #E5E5EA;
            }
        """)
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(10, 20, 10, 20)
        nav_layout.setSpacing(5)
        
        # Navigation buttons with better styling
        self.nav_buttons = []
        self.stacked = QStackedWidget()
        
        # Define all sections with descriptions
        sections = [
            ("📅 Daily Planner", "Organize routines and schedules", "planner"),
            ("🎯 Executive Aid", "Focus and organization support", "exec_aid"),
            ("⚡ Trigger Dashboard", "Track and manage stress triggers", "triggers"),
            ("🗣️ Communication Assistant", "Improve family conversations", "comm"),
            ("📝 Child Journal", "Track moods and behaviors", "journal"),
            ("🎭 Sensory Toolkit", "Sensory processing support", "sensory"),
            ("🤝 Social Skills Trainer", "Practice social interactions", "social")
        ]
        
        for title, description, key in sections:
            btn_widget = QWidget()
            btn_layout = QVBoxLayout(btn_widget)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setSpacing(2)
            
            btn = QPushButton(title)
            btn.setProperty("nav_button", True)
            btn.setStyleSheet("""
                QPushButton[nav_button="true"] {
                    background: white;
                    border: 1px solid #E5E5EA;
                    border-radius: 8px;
                    padding: 12px;
                    text-align: left;
                    font-weight: 600;
                    color: #333333;
                }
                QPushButton[nav_button="true"]:hover {
                    background: #007AFF;
                    color: white;
                }
                QPushButton[nav_button="true"]:checked {
                    background: #007AFF;
                    color: white;
                }
            """)
            btn.setCheckable(True)
            
            desc_label = QLabel(description)
            desc_label.setStyleSheet("""
                font-size: 11px;
                color: #666666;
                padding-left: 12px;
                margin-bottom: 5px;
            """)
            desc_label.setWordWrap(True)
            
            btn_layout.addWidget(btn)
            btn_layout.addWidget(desc_label)
            
            nav_layout.addWidget(btn_widget)
            self.nav_buttons.append(btn)
        
        nav_layout.addStretch()
        
        # Create component widgets
        self.planner = PlannerWidget()
        self.exec_aid = ExecAidWidget()
        self.triggers = TriggerDashboardWidget()
        self.comm = CommAssistantWidget()
        self.journal = ChildJournalWidget()
        self.sensory = SensoryToolkitWidget()
        self.social = SocialSkillsTrainerWidget()
        
        # Add widgets to stack
        widgets = [
            self.planner, self.exec_aid, self.triggers, 
            self.comm, self.journal, self.sensory, self.social
        ]
        
        for widget in widgets:
            # Add padding around each widget
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(20, 20, 20, 20)
            container_layout.addWidget(widget)
            self.stacked.addWidget(container)
        
        # Connect navigation buttons
        for i, btn in enumerate(self.nav_buttons):
            btn.clicked.connect(lambda checked, index=i: self.switch_to_section(index))
        
        # Set initial selection
        self.nav_buttons[0].setChecked(True)
        self.stacked.setCurrentIndex(0)
        
        # Add to content layout
        content_layout.addWidget(nav_widget)
        content_layout.addWidget(self.stacked, 1)
        
        main_layout.addWidget(content_widget)
    
    def switch_to_section(self, index):
        """Switch to the selected section"""
        # Update button states
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        
        # Switch content
        self.stacked.setCurrentIndex(index)
        
        # Optional: Add section-specific initialization
        if index == 2:  # Trigger dashboard
            # Could refresh trigger data when selected
            pass
        elif index == 5:  # Sensory toolkit
            # Could check for sensory profile updates
            pass