from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QTabWidget, QScrollArea, QFrame, QPushButton, 
                               QProgressBar, QListWidget, QListWidgetItem,
                               QDialog, QDialogButtonBox, QSpinBox, QTimeEdit,
                               QCalendarWidget, QTextEdit, QCheckBox, QSlider)
from PySide6.QtCore import Qt, Signal, QTimer, QTime, QDate, pyqtSignal
from PySide6.QtGui import QIcon, QFont
from cogtools.core.widgets import (AppleCard, AppleButton, AppleTextField, 
                                   AppleTextArea, AppleSegmentedControl, AppleNotification)
from cogtools.core.theme import AppleColors, AppleTheme
from datetime import datetime, timedelta
import json

class PomodoroTimer(AppleCard):
    """Pomodoro timer for focus sessions"""
    
    session_completed = Signal(str)  # session type
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.work_minutes = 25
        self.break_minutes = 5
        self.long_break_minutes = 15
        self.sessions_count = 0
        self.current_time = self.work_minutes * 60
        self.is_work_session = True
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.is_running = False
        self.setup_ui()
        
    def setup_ui(self):
        """Setup timer UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🍅 Pomodoro Timer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        # Time display
        self.time_label = QLabel(self.format_time(self.current_time))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("""
            font-size: 48px;
            font-weight: 300;
            color: #007AFF;
            margin: 20px 0px;
        """)
        layout.addWidget(self.time_label)
        
        # Session type
        self.session_label = QLabel("Work Session")
        self.session_label.setAlignment(Qt.AlignCenter)
        self.session_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #8E8E93;
        """)
        layout.addWidget(self.session_label)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMaximum(self.work_minutes * 60)
        self.progress.setValue(0)
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 4px;
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                height: 8px;
            }}
            QProgressBar::chunk {{
                background-color: {AppleColors.ACCENT.name()};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(self.progress)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.start_btn = AppleButton("Start")
        self.start_btn.clicked.connect(self.toggle_timer)
        
        self.reset_btn = AppleButton("Reset", style="secondary")
        self.reset_btn.clicked.connect(self.reset_timer)
        
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.reset_btn)
        
        layout.addLayout(controls_layout)
        
        # Sessions completed
        self.sessions_label = QLabel(f"Sessions completed: {self.sessions_count}")
        self.sessions_label.setAlignment(Qt.AlignCenter)
        self.sessions_label.setStyleSheet("""
            font-size: 12px;
            color: #8E8E93;
            margin-top: 10px;
        """)
        layout.addWidget(self.sessions_label)
    
    def format_time(self, seconds):
        """Format seconds to MM:SS"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def toggle_timer(self):
        """Start or pause the timer"""
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
        
        if self.is_work_session:
            self.current_time = self.work_minutes * 60
            self.progress.setMaximum(self.work_minutes * 60)
        else:
            if self.sessions_count % 4 == 0 and self.sessions_count > 0:
                self.current_time = self.long_break_minutes * 60
                self.progress.setMaximum(self.long_break_minutes * 60)
            else:
                self.current_time = self.break_minutes * 60
                self.progress.setMaximum(self.break_minutes * 60)
        
        self.progress.setValue(0)
        self.time_label.setText(self.format_time(self.current_time))
    
    def update_timer(self):
        """Update timer countdown"""
        if self.current_time > 0:
            self.current_time -= 1
            self.time_label.setText(self.format_time(self.current_time))
            
            # Update progress
            max_time = self.progress.maximum()
            self.progress.setValue(max_time - self.current_time)
        else:
            # Session completed
            self.timer.stop()
            self.is_running = False
            self.start_btn.setText("Start")
            
            if self.is_work_session:
                self.sessions_count += 1
                self.sessions_label.setText(f"Sessions completed: {self.sessions_count}")
                self.session_completed.emit("work")
                
                # Switch to break
                self.is_work_session = False
                if self.sessions_count % 4 == 0:
                    self.current_time = self.long_break_minutes * 60
                    self.session_label.setText("Long Break")
                    self.progress.setMaximum(self.long_break_minutes * 60)
                else:
                    self.current_time = self.break_minutes * 60
                    self.session_label.setText("Short Break")
                    self.progress.setMaximum(self.break_minutes * 60)
            else:
                self.session_completed.emit("break")
                
                # Switch to work
                self.is_work_session = True
                self.current_time = self.work_minutes * 60
                self.session_label.setText("Work Session")
                self.progress.setMaximum(self.work_minutes * 60)
            
            self.progress.setValue(0)
            self.time_label.setText(self.format_time(self.current_time))
            
            # Show notification
            AppleNotification.show_success(
                self, 
                "Session Complete!",
                "Time for a break!" if self.is_work_session else "Ready to focus!"
            )

class TaskBreakdownWidget(AppleCard):
    """Widget for breaking down complex tasks"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup task breakdown UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🧩 Task Breakdown")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Main task input
        layout.addWidget(QLabel("Main Task:"))
        self.main_task = AppleTextField("Enter complex task...")
        layout.addWidget(self.main_task)
        
        # Complexity slider
        complexity_layout = QHBoxLayout()
        complexity_layout.addWidget(QLabel("Complexity:"))
        self.complexity_slider = QSlider(Qt.Horizontal)
        self.complexity_slider.setRange(1, 10)
        self.complexity_slider.setValue(5)
        self.complexity_slider.valueChanged.connect(self.update_breakdown)
        
        self.complexity_label = QLabel("5")
        self.complexity_label.setMinimumWidth(20)
        
        complexity_layout.addWidget(self.complexity_slider)
        complexity_layout.addWidget(self.complexity_label)
        layout.addLayout(complexity_layout)
        
        # Break down button
        breakdown_btn = AppleButton("Break Down Task")
        breakdown_btn.clicked.connect(self.generate_breakdown)
        layout.addWidget(breakdown_btn)
        
        # Subtasks list
        layout.addWidget(QLabel("Subtasks:"))
        self.subtasks_list = QListWidget()
        self.subtasks_list.setMaximumHeight(200)
        self.subtasks_list.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid {AppleColors.LIGHT_SEPARATOR.name()};
                border-radius: 8px;
                background-color: white;
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {AppleColors.LIGHT_SEPARATOR.name()};
            }}
            QListWidget::item:last {{
                border-bottom: none;
            }}
        """)
        layout.addWidget(self.subtasks_list)
    
    def update_breakdown(self, value):
        """Update complexity label"""
        self.complexity_label.setText(str(value))
    
    def generate_breakdown(self):
        """Generate task breakdown based on complexity"""
        main_task = self.main_task.text().strip()
        if not main_task:
            return
        
        complexity = self.complexity_slider.value()
        
        # Clear existing subtasks
        self.subtasks_list.clear()
        
        # Generate subtasks based on complexity
        if complexity <= 3:
            subtasks = [
                f"Plan approach for: {main_task}",
                f"Execute: {main_task}",
                f"Review and complete: {main_task}"
            ]
        elif complexity <= 6:
            subtasks = [
                f"Research requirements for: {main_task}",
                f"Break down components",
                f"Create timeline",
                f"Execute phase 1",
                f"Execute phase 2", 
                f"Review and refine",
                f"Finalize: {main_task}"
            ]
        else:
            subtasks = [
                f"Define scope and objectives",
                f"Research and gather resources",
                f"Identify dependencies",
                f"Create detailed plan",
                f"Break into phases",
                f"Execute phase 1",
                f"Review phase 1",
                f"Execute phase 2",
                f"Review phase 2", 
                f"Execute phase 3",
                f"Final review and testing",
                f"Complete: {main_task}"
            ]
        
        # Add subtasks to list
        for i, subtask in enumerate(subtasks, 1):
            item = QListWidgetItem(f"{i}. {subtask}")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.subtasks_list.addItem(item)

class ExecFunctionCoachWidget(QWidget):
    """Main widget for Executive Function Coach"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Executive Function Coach")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Tab widget for different tools
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {AppleColors.LIGHT_SEPARATOR.name()};
                border-radius: 8px;
                background-color: white;
            }}
            QTabBar::tab {{
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            QTabBar::tab:selected {{
                background-color: white;
                border-bottom: 2px solid {AppleColors.ACCENT.name()};
            }}
        """)
        
        # Focus Timer tab
        focus_widget = QWidget()
        focus_layout = QVBoxLayout(focus_widget)
        focus_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add pomodoro timer
        self.pomodoro = PomodoroTimer()
        self.pomodoro.session_completed.connect(self.on_session_completed)
        focus_layout.addWidget(self.pomodoro)
        
        # Daily focus goals
        focus_goals = AppleCard()
        goals_layout = QVBoxLayout(focus_goals)
        goals_layout.addWidget(QLabel("📋 Today's Focus Goals"))
        
        self.goals_list = QListWidget()
        self.goals_list.setMaximumHeight(150)
        self.add_sample_goals()
        
        goals_layout.addWidget(self.goals_list)
        
        add_goal_btn = AppleButton("Add Goal")
        add_goal_btn.clicked.connect(self.add_goal)
        goals_layout.addWidget(add_goal_btn)
        
        focus_layout.addWidget(focus_goals)
        focus_layout.addStretch()
        
        self.tabs.addTab(focus_widget, "Focus Timer")
        
        # Task Breakdown tab
        breakdown_widget = QWidget()
        breakdown_layout = QVBoxLayout(breakdown_widget)
        breakdown_layout.setContentsMargins(20, 20, 20, 20)
        
        self.task_breakdown = TaskBreakdownWidget()
        breakdown_layout.addWidget(self.task_breakdown)
        
        # Add planning tips
        tips_card = AppleCard()
        tips_layout = QVBoxLayout(tips_card)
        tips_layout.addWidget(QLabel("💡 Planning Tips"))
        
        tips_text = QLabel("""
        • Break complex tasks into 15-30 minute chunks
        • Use the 2-minute rule: if it takes less than 2 minutes, do it now
        • Schedule similar tasks together (batching)
        • Plan your most important work for your peak energy time
        • Always include buffer time for unexpected interruptions
        """)
        tips_text.setWordWrap(True)
        tips_text.setStyleSheet("font-size: 12px; color: #666666; line-height: 1.4;")
        tips_layout.addWidget(tips_text)
        
        breakdown_layout.addWidget(tips_card)
        breakdown_layout.addStretch()
        
        self.tabs.addTab(breakdown_widget, "Task Breakdown")
        
        # Progress Tracking tab
        progress_widget = QWidget()
        progress_layout = QVBoxLayout(progress_widget)
        progress_layout.setContentsMargins(20, 20, 20, 20)
        
        # Weekly progress card
        weekly_card = AppleCard()
        weekly_layout = QVBoxLayout(weekly_card)
        weekly_layout.addWidget(QLabel("📊 Weekly Progress"))
        
        # Progress stats
        stats_layout = QHBoxLayout()
        
        # Focus sessions
        sessions_widget = QWidget()
        sessions_layout = QVBoxLayout(sessions_widget)
        sessions_layout.addWidget(QLabel("Focus Sessions"))
        sessions_count = QLabel("12")
        sessions_count.setStyleSheet("font-size: 32px; font-weight: 700; color: #007AFF;")
        sessions_count.setAlignment(Qt.AlignCenter)
        sessions_layout.addWidget(sessions_count)
        sessions_layout.addWidget(QLabel("This week"))
        
        # Tasks completed
        tasks_widget = QWidget()
        tasks_layout = QVBoxLayout(tasks_widget)
        tasks_layout.addWidget(QLabel("Tasks Completed"))
        tasks_count = QLabel("28")
        tasks_count.setStyleSheet("font-size: 32px; font-weight: 700; color: #34C759;")
        tasks_count.setAlignment(Qt.AlignCenter)
        tasks_layout.addWidget(tasks_count)
        tasks_layout.addWidget(QLabel("This week"))
        
        # Streak
        streak_widget = QWidget()
        streak_layout = QVBoxLayout(streak_widget)
        streak_layout.addWidget(QLabel("Current Streak"))
        streak_count = QLabel("5")
        streak_count.setStyleSheet("font-size: 32px; font-weight: 700; color: #FF9500;")
        streak_count.setAlignment(Qt.AlignCenter)
        streak_layout.addWidget(streak_count)
        streak_layout.addWidget(QLabel("Days"))
        
        stats_layout.addWidget(sessions_widget)
        stats_layout.addWidget(tasks_widget) 
        stats_layout.addWidget(streak_widget)
        
        weekly_layout.addLayout(stats_layout)
        
        progress_layout.addWidget(weekly_card)
        progress_layout.addStretch()
        
        self.tabs.addTab(progress_widget, "Progress")
        
        layout.addWidget(self.tabs)
    
    def add_sample_goals(self):
        """Add some sample goals"""
        goals = [
            "Complete project proposal",
            "Review team feedback", 
            "Organize workspace",
            "Plan tomorrow's schedule"
        ]
        
        for goal in goals:
            item = QListWidgetItem(goal)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.goals_list.addItem(item)
    
    def add_goal(self):
        """Add a new goal"""
        # For now, add a placeholder - in real app this would open a dialog
        item = QListWidgetItem("New goal...")
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Unchecked)
        self.goals_list.addItem(item)
    
    def on_session_completed(self, session_type):
        """Handle completed focus session"""
        if session_type == "work":
            AppleNotification.show_success(
                self,
                "Great work! 🎉",
                "You completed a focus session. Take a well-deserved break!"
            )
        else:
            AppleNotification.show_info(
                self,
                "Break time over! 💪",
                "Ready to get back to focused work?"
            )