from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QListWidget, QListWidgetItem, QPushButton, QComboBox,
                               QTextEdit, QDialog, QDialogButtonBox, QDateEdit,
                               QProgressBar, QSlider, QGroupBox, QCheckBox, QTimer)
from PySide6.QtCore import Qt, Signal, QDate, QTime, QDateTime
from PySide6.QtGui import QColor, QFont
from datetime import datetime, timedelta
import json

class CooldownTimer(QWidget):
    """Cooldown timer widget for managing meltdowns"""
    
    timer_finished = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.countdown_seconds = 300  # 5 minutes default
        self.current_seconds = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.is_running = False
        self.setup_ui()
        
    def setup_ui(self):
        """Setup cooldown timer UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("🧘 Cooldown Timer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #FF9500;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        # Time display
        self.time_label = QLabel("5:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("""
            font-size: 36px;
            font-weight: 300;
            color: #FF9500;
            margin: 15px 0px;
        """)
        layout.addWidget(self.time_label)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMaximum(self.countdown_seconds)
        self.progress.setValue(0)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #F2F2F7;
                height: 8px;
            }
            QProgressBar::chunk {
                background-color: #FF9500;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress)
        
        # Duration selector
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("Duration:"))
        
        self.duration_slider = QSlider(Qt.Horizontal)
        self.duration_slider.setRange(60, 900)  # 1-15 minutes
        self.duration_slider.setValue(300)  # 5 minutes
        self.duration_slider.valueChanged.connect(self.update_duration)
        
        self.duration_label = QLabel("5 min")
        
        duration_layout.addWidget(self.duration_slider)
        duration_layout.addWidget(self.duration_label)
        
        layout.addLayout(duration_layout)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.toggle_timer)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9500;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #E6850E;
            }
        """)
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_timer)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #8E8E93;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #6D6D7A;
            }
        """)
        
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.reset_btn)
        
        layout.addLayout(controls_layout)
        
        # Breathing guide
        breathing_label = QLabel("💨 Focus on deep, slow breathing")
        breathing_label.setAlignment(Qt.AlignCenter)
        breathing_label.setStyleSheet("""
            font-size: 12px;
            color: #8E8E93;
            margin-top: 10px;
        """)
        layout.addWidget(breathing_label)
    
    def update_duration(self, value):
        """Update timer duration"""
        minutes = value // 60
        seconds = value % 60
        if seconds == 0:
            self.duration_label.setText(f"{minutes} min")
        else:
            self.duration_label.setText(f"{minutes}:{seconds:02d}")
        
        if not self.is_running:
            self.countdown_seconds = value
            self.current_seconds = 0
            self.progress.setMaximum(value)
            self.progress.setValue(0)
            self.time_label.setText(f"{minutes}:{seconds:02d}")
    
    def toggle_timer(self):
        """Start or stop the timer"""
        if self.is_running:
            self.timer.stop()
            self.start_btn.setText("Start")
            self.is_running = False
        else:
            self.timer.start(1000)  # 1 second interval
            self.start_btn.setText("Pause")
            self.is_running = True
    
    def reset_timer(self):
        """Reset the timer"""
        self.timer.stop()
        self.is_running = False
        self.start_btn.setText("Start")
        self.current_seconds = 0
        self.progress.setValue(0)
        
        minutes = self.countdown_seconds // 60
        seconds = self.countdown_seconds % 60
        self.time_label.setText(f"{minutes}:{seconds:02d}")
    
    def update_timer(self):
        """Update timer countdown"""
        self.current_seconds += 1
        self.progress.setValue(self.current_seconds)
        
        remaining = self.countdown_seconds - self.current_seconds
        if remaining <= 0:
            self.timer.stop()
            self.is_running = False
            self.start_btn.setText("Start")
            self.time_label.setText("0:00")
            self.timer_finished.emit()
        else:
            minutes = remaining // 60
            seconds = remaining % 60
            self.time_label.setText(f"{minutes}:{seconds:02d}")

class IncidentDialog(QDialog):
    """Dialog for logging trigger incidents"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Log Incident")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup incident dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Date/time
        layout.addWidget(QLabel("Date & Time:"))
        self.datetime_edit = QDateEdit()
        self.datetime_edit.setDate(QDate.currentDate())
        self.datetime_edit.setCalendarPopup(True)
        layout.addWidget(self.datetime_edit)
        
        # Trigger type
        layout.addWidget(QLabel("Trigger Type:"))
        self.trigger_combo = QComboBox()
        self.trigger_combo.addItems([
            "Sensory Overload",
            "Noise",
            "Bright Lights", 
            "Unexpected Change",
            "Social Situation",
            "Transition",
            "Mess/Clutter",
            "Tone of Voice",
            "Physical Discomfort",
            "Hunger/Fatigue",
            "Other"
        ])
        layout.addWidget(self.trigger_combo)
        
        # Intensity
        layout.addWidget(QLabel("Intensity (1-10):"))
        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setRange(1, 10)
        self.intensity_slider.setValue(5)
        self.intensity_slider.valueChanged.connect(self.update_intensity_label)
        
        intensity_layout = QHBoxLayout()
        intensity_layout.addWidget(self.intensity_slider)
        self.intensity_label = QLabel("5")
        self.intensity_label.setMinimumWidth(20)
        intensity_layout.addWidget(self.intensity_label)
        layout.addLayout(intensity_layout)
        
        # Location
        layout.addWidget(QLabel("Location:"))
        self.location_combo = QComboBox()
        self.location_combo.setEditable(True)
        self.location_combo.addItems([
            "Living Room",
            "Kitchen",
            "Bedroom",
            "Bathroom",
            "Car",
            "School",
            "Store",
            "Restaurant",
            "Other"
        ])
        layout.addWidget(self.location_combo)
        
        # People present
        layout.addWidget(QLabel("People Present:"))
        self.people_edit = QTextEdit()
        self.people_edit.setMaximumHeight(60)
        self.people_edit.setPlaceholderText("Who was present during the incident?")
        layout.addWidget(self.people_edit)
        
        # Description
        layout.addWidget(QLabel("Description:"))
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        self.description_edit.setPlaceholderText("Describe what happened, triggers noticed, response...")
        layout.addWidget(self.description_edit)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def update_intensity_label(self, value):
        """Update intensity label"""
        self.intensity_label.setText(str(value))
        
        # Color code the intensity
        if value <= 3:
            color = "#34C759"  # Green
        elif value <= 6:
            color = "#FF9500"  # Orange
        else:
            color = "#FF3B30"  # Red
        
        self.intensity_label.setStyleSheet(f"color: {color}; font-weight: bold;")
    
    def get_incident_data(self):
        """Get the incident data from the form"""
        return {
            'date': self.datetime_edit.date().toString("yyyy-MM-dd"),
            'trigger_type': self.trigger_combo.currentText(),
            'intensity': self.intensity_slider.value(),
            'location': self.location_combo.currentText(),
            'people_present': self.people_edit.toPlainText(),
            'description': self.description_edit.toPlainText(),
            'timestamp': datetime.now().isoformat()
        }

class TriggerDashboardWidget(QWidget):
    """Enhanced trigger dashboard for family support"""
    
    def __init__(self):
        super().__init__()
        self.trigger_data = []
        self.incident_log = []
        self.load_sample_data()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main dashboard UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("🎯 Family Trigger Dashboard")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #1C1C1E;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        # Main content in two columns
        main_layout = QHBoxLayout()
        
        # Left column
        left_column = QVBoxLayout()
        
        # Quick action buttons
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QVBoxLayout(actions_group)
        
        log_incident_btn = QPushButton("📝 Log New Incident")
        log_incident_btn.clicked.connect(self.log_incident)
        log_incident_btn.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: 600;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #0056CC;
            }
        """)
        
        start_cooldown_btn = QPushButton("🧘 Start Cooldown")
        start_cooldown_btn.clicked.connect(self.show_cooldown_timer)
        start_cooldown_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9500;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: 600;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #E6850E;
            }
        """)
        
        actions_layout.addWidget(log_incident_btn)
        actions_layout.addWidget(start_cooldown_btn)
        
        left_column.addWidget(actions_group)
        
        # Common triggers
        triggers_group = QGroupBox("Common Triggers")
        triggers_layout = QVBoxLayout(triggers_group)
        
        self.triggers_list = QListWidget()
        self.triggers_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #E5E5EA;
                border-radius: 8px;
                background-color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F2F2F7;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #F2F2F7;
            }
        """)
        triggers_layout.addWidget(self.triggers_list)
        
        left_column.addWidget(triggers_group)
        
        # Right column
        right_column = QVBoxLayout()
        
        # Recent incidents
        incidents_group = QGroupBox("Recent Incidents")
        incidents_layout = QVBoxLayout(incidents_group)
        
        self.incidents_list = QListWidget()
        self.incidents_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #E5E5EA;
                border-radius: 8px;
                background-color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #F2F2F7;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #F2F2F7;
            }
        """)
        incidents_layout.addWidget(self.incidents_list)
        
        right_column.addWidget(incidents_group)
        
        # Coping strategies
        coping_group = QGroupBox("Coping Strategies")
        coping_layout = QVBoxLayout(coping_group)
        
        strategies_text = QLabel("""
🧘 Deep breathing exercises
🎵 Calming music or white noise
🏃 Physical activity or movement
🤗 Comfort items (weighted blanket, fidget toys)
📱 Visual schedules and countdown timers
🌅 Quiet space with dim lighting
💧 Hydration and healthy snacks
        """)
        strategies_text.setWordWrap(True)
        strategies_text.setStyleSheet("""
            font-size: 12px;
            color: #666666;
            line-height: 1.4;
            padding: 10px;
            background-color: #F9F9F9;
            border-radius: 8px;
        """)
        coping_layout.addWidget(strategies_text)
        
        right_column.addWidget(coping_group)
        
        # Add columns to main layout
        main_layout.addLayout(left_column, 1)
        main_layout.addLayout(right_column, 1)
        
        layout.addLayout(main_layout)
        
        # Cooldown timer (initially hidden)
        self.cooldown_timer = CooldownTimer()
        self.cooldown_timer.timer_finished.connect(self.on_cooldown_finished)
        self.cooldown_timer.hide()
        layout.addWidget(self.cooldown_timer)
        
        # Load data
        self.refresh_displays()
    
    def load_sample_data(self):
        """Load sample trigger and incident data"""
        self.trigger_data = [
            {"name": "Loud Noises", "frequency": 8, "last_occurred": "2024-01-12"},
            {"name": "Unexpected Changes", "frequency": 6, "last_occurred": "2024-01-11"},
            {"name": "Bright Lights", "frequency": 4, "last_occurred": "2024-01-10"},
            {"name": "Social Situations", "frequency": 5, "last_occurred": "2024-01-09"},
            {"name": "Transitions", "frequency": 7, "last_occurred": "2024-01-08"}
        ]
        
        self.incident_log = [
            {
                "date": "2024-01-12",
                "trigger_type": "Loud Noises",
                "intensity": 8,
                "location": "Living Room",
                "description": "Construction noise outside triggered meltdown"
            },
            {
                "date": "2024-01-11", 
                "trigger_type": "Unexpected Changes",
                "intensity": 6,
                "location": "Kitchen",
                "description": "Change in dinner plans caused distress"
            },
            {
                "date": "2024-01-10",
                "trigger_type": "Bright Lights",
                "intensity": 5,
                "location": "Store",
                "description": "Fluorescent lights at grocery store"
            }
        ]
    
    def refresh_displays(self):
        """Refresh the trigger and incident displays"""
        # Update triggers list
        self.triggers_list.clear()
        for trigger in self.trigger_data:
            item_text = f"{trigger['name']} (Frequency: {trigger['frequency']}/10)"
            item = QListWidgetItem(item_text)
            
            # Color code by frequency
            if trigger['frequency'] >= 7:
                item.setBackground(QColor("#FFE5E5"))  # Light red
            elif trigger['frequency'] >= 4:
                item.setBackground(QColor("#FFF2E5"))  # Light orange
            else:
                item.setBackground(QColor("#E5F7E5"))  # Light green
            
            self.triggers_list.addItem(item)
        
        # Update incidents list
        self.incidents_list.clear()
        for incident in self.incident_log[-5:]:  # Show last 5 incidents
            item_text = f"{incident['date']}: {incident['trigger_type']}\nIntensity: {incident['intensity']}/10 - {incident['location']}"
            item = QListWidgetItem(item_text)
            
            # Color code by intensity
            if incident['intensity'] >= 7:
                item.setBackground(QColor("#FFE5E5"))  # Light red
            elif incident['intensity'] >= 4:
                item.setBackground(QColor("#FFF2E5"))  # Light orange
            else:
                item.setBackground(QColor("#E5F7E5"))  # Light green
            
            self.incidents_list.addItem(item)
    
    def log_incident(self):
        """Open dialog to log a new incident"""
        dialog = IncidentDialog(self)
        if dialog.exec():
            incident_data = dialog.get_incident_data()
            self.incident_log.append(incident_data)
            
            # Update trigger frequency if it exists
            for trigger in self.trigger_data:
                if trigger['name'] == incident_data['trigger_type']:
                    trigger['frequency'] = min(10, trigger['frequency'] + 1)
                    trigger['last_occurred'] = incident_data['date']
                    break
            
            self.refresh_displays()
    
    def show_cooldown_timer(self):
        """Show/hide the cooldown timer"""
        if self.cooldown_timer.isVisible():
            self.cooldown_timer.hide()
        else:
            self.cooldown_timer.show()
    
    def on_cooldown_finished(self):
        """Handle cooldown timer completion"""
        # Could trigger a notification or other response
        print("Cooldown timer finished - feeling better?")