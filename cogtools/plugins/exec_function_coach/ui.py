from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QListWidget, QListWidgetItem, QTabWidget,
                               QTextEdit, QSlider, QSpinBox, QComboBox, QCheckBox,
                               QFrame, QGroupBox, QProgressBar, QScrollArea)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont
from cogtools.core.widgets import AppleCard, AppleButton, AppleTextField, AppleNotification
from .cbt_toolkit import CBTToolkitWidget
from datetime import datetime
import json

class PomodoroTimer(AppleCard):
    """Enhanced Pomodoro timer with psychology-informed features"""
    
    session_completed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer()
        self.time_left = 25 * 60  # 25 minutes in seconds
        self.is_running = False
        self.session_type = "work"  # "work" or "break"
        self.setup_ui()
        
    def setup_ui(self):
        """Setup enhanced pomodoro timer UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🍅 Focus Timer")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Timer display
        self.time_display = QLabel("25:00")
        self.time_display.setAlignment(Qt.AlignCenter)
        self.time_display.setStyleSheet("""
            font-size: 48px;
            font-weight: 300;
            color: #007AFF;
            padding: 20px;
            background-color: #F9F9F9;
            border-radius: 12px;
            margin: 10px 0;
        """)
        layout.addWidget(self.time_display)
        
        # Session type indicator
        self.session_label = QLabel("Work Session")
        self.session_label.setAlignment(Qt.AlignCenter)
        self.session_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #333333;
            margin-bottom: 15px;
        """)
        layout.addWidget(self.session_label)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.start_btn = AppleButton("Start")
        self.start_btn.clicked.connect(self.toggle_timer)
        
        self.reset_btn = AppleButton("Reset")
        self.reset_btn.clicked.connect(self.reset_timer)
        
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.reset_btn)
        
        layout.addLayout(controls_layout)
        
        # Timer settings
        settings_group = QGroupBox("⚙️ Timer Settings")
        settings_layout = QVBoxLayout(settings_group)
        
        # Work duration
        work_layout = QHBoxLayout()
        work_layout.addWidget(QLabel("Work duration (minutes):"))
        self.work_duration = QSpinBox()
        self.work_duration.setRange(5, 60)
        self.work_duration.setValue(25)
        work_layout.addWidget(self.work_duration)
        work_layout.addStretch()
        settings_layout.addLayout(work_layout)
        
        # Break duration
        break_layout = QHBoxLayout()
        break_layout.addWidget(QLabel("Break duration (minutes):"))
        self.break_duration = QSpinBox()
        self.break_duration.setRange(5, 30)
        self.break_duration.setValue(5)
        break_layout.addWidget(self.break_duration)
        break_layout.addStretch()
        settings_layout.addLayout(break_layout)
        
        # ASD-specific features
        asd_features = QCheckBox("Enable gentle reminders")
        asd_features.setChecked(True)
        settings_layout.addWidget(asd_features)
        
        focus_sounds = QCheckBox("Play focus sounds")
        settings_layout.addWidget(focus_sounds)
        
        layout.addWidget(settings_group)
        
        # Current task
        task_group = QGroupBox("🎯 Current Task")
        task_layout = QVBoxLayout(task_group)
        
        self.current_task = AppleTextField("What are you working on?")
        task_layout.addWidget(self.current_task)
        
        # Task complexity indicator
        complexity_layout = QHBoxLayout()
        complexity_layout.addWidget(QLabel("Task complexity:"))
        self.complexity_slider = QSlider(Qt.Horizontal)
        self.complexity_slider.setRange(1, 5)
        self.complexity_slider.setValue(3)
        self.complexity_label = QLabel("Medium")
        
        complexity_mapping = {1: "Very Easy", 2: "Easy", 3: "Medium", 4: "Hard", 5: "Very Hard"}
        self.complexity_slider.valueChanged.connect(
            lambda v: self.complexity_label.setText(complexity_mapping[v])
        )
        
        complexity_layout.addWidget(self.complexity_slider)
        complexity_layout.addWidget(self.complexity_label)
        task_layout.addLayout(complexity_layout)
        
        layout.addWidget(task_group)
        
        # Connect timer
        self.timer.timeout.connect(self.update_timer)
        
    def toggle_timer(self):
        """Start or pause the timer"""
        if self.is_running:
            self.timer.stop()
            self.start_btn.setText("Resume")
            self.is_running = False
        else:
            self.timer.start(1000)  # Update every second
            self.start_btn.setText("Pause")
            self.is_running = True
    
    def reset_timer(self):
        """Reset the timer"""
        self.timer.stop()
        self.is_running = False
        self.start_btn.setText("Start")
        
        if self.session_type == "work":
            self.time_left = self.work_duration.value() * 60
            self.session_label.setText("Work Session")
        else:
            self.time_left = self.break_duration.value() * 60
            self.session_label.setText("Break Session")
            
        self.update_display()
    
    def update_timer(self):
        """Update timer display and check for completion"""
        self.time_left -= 1
        self.update_display()
        
        if self.time_left <= 0:
            self.timer.stop()
            self.is_running = False
            self.session_completed.emit(self.session_type)
            
            # Switch session type
            if self.session_type == "work":
                self.session_type = "break"
                self.time_left = self.break_duration.value() * 60
                self.session_label.setText("Break Session")
                self.start_btn.setText("Start Break")
            else:
                self.session_type = "work"
                self.time_left = self.work_duration.value() * 60
                self.session_label.setText("Work Session")
                self.start_btn.setText("Start Work")
                
            self.update_display()
    
    def update_display(self):
        """Update the time display"""
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.time_display.setText(f"{minutes:02d}:{seconds:02d}")

class TaskBreakdownWidget(AppleCard):
    """Enhanced task breakdown with psychological insights"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup enhanced task breakdown UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🔧 Task Breakdown Assistant")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Main task input
        task_input_group = QGroupBox("📝 Main Task")
        task_input_layout = QVBoxLayout(task_input_group)
        
        self.main_task = AppleTextField("Describe your main task or goal...")
        task_input_layout.addWidget(self.main_task)
        
        # Task analysis
        analysis_layout = QHBoxLayout()
        
        # Complexity assessment
        complexity_layout = QVBoxLayout()
        complexity_layout.addWidget(QLabel("Complexity:"))
        self.complexity_combo = QComboBox()
        self.complexity_combo.addItems(["Simple", "Moderate", "Complex", "Very Complex"])
        complexity_layout.addWidget(self.complexity_combo)
        
        # Time estimate
        time_layout = QVBoxLayout()
        time_layout.addWidget(QLabel("Estimated time:"))
        self.time_combo = QComboBox()
        self.time_combo.addItems(["< 30 min", "30-60 min", "1-2 hours", "2-4 hours", "4+ hours"])
        time_layout.addWidget(self.time_combo)
        
        # Anxiety level
        anxiety_layout = QVBoxLayout()
        anxiety_layout.addWidget(QLabel("Anxiety about task:"))
        self.anxiety_slider = QSlider(Qt.Horizontal)
        self.anxiety_slider.setRange(1, 5)
        self.anxiety_slider.setValue(1)
        self.anxiety_label = QLabel("Low")
        
        anxiety_mapping = {1: "Low", 2: "Mild", 3: "Moderate", 4: "High", 5: "Very High"}
        self.anxiety_slider.valueChanged.connect(
            lambda v: self.anxiety_label.setText(anxiety_mapping[v])
        )
        
        anxiety_layout.addWidget(self.anxiety_slider)
        anxiety_layout.addWidget(self.anxiety_label)
        
        analysis_layout.addLayout(complexity_layout)
        analysis_layout.addLayout(time_layout)
        analysis_layout.addLayout(anxiety_layout)
        
        task_input_layout.addLayout(analysis_layout)
        
        layout.addWidget(task_input_group)
        
        # Generate breakdown button
        generate_btn = AppleButton("Generate Task Breakdown")
        generate_btn.clicked.connect(self.generate_breakdown)
        layout.addWidget(generate_btn)
        
        # Breakdown results
        results_group = QGroupBox("📋 Suggested Breakdown")
        results_layout = QVBoxLayout(results_group)
        
        self.breakdown_list = QListWidget()
        self.breakdown_list.setMaximumHeight(200)
        results_layout.addWidget(self.breakdown_list)
        
        # Add custom step
        custom_layout = QHBoxLayout()
        self.custom_step = AppleTextField("Add custom step...")
        add_step_btn = AppleButton("Add Step")
        add_step_btn.clicked.connect(self.add_custom_step)
        
        custom_layout.addWidget(self.custom_step)
        custom_layout.addWidget(add_step_btn)
        
        results_layout.addLayout(custom_layout)
        
        layout.addWidget(results_group)
        
        # Coping strategies for high anxiety tasks
        self.anxiety_strategies = QGroupBox("😰 Anxiety Management")
        strategies_layout = QVBoxLayout(self.anxiety_strategies)
        
        strategies_text = QLabel("""
• Start with the easiest step to build momentum
• Set a timer for just 10 minutes to begin
• Remind yourself: "I only need to start, not finish"
• Take breaks every 25-30 minutes
• Use calming techniques before starting
• Ask for help if you feel stuck
        """)
        strategies_text.setStyleSheet("font-size: 12px; line-height: 1.4;")
        strategies_layout.addWidget(strategies_text)
        
        layout.addWidget(self.anxiety_strategies)
        self.anxiety_strategies.hide()  # Show only for high-anxiety tasks
        
    def generate_breakdown(self):
        """Generate task breakdown based on complexity and type"""
        task = self.main_task.text()
        if not task:
            return
            
        complexity = self.complexity_combo.currentText()
        time_estimate = self.time_combo.currentText()
        anxiety_level = self.anxiety_slider.value()
        
        # Clear previous breakdown
        self.breakdown_list.clear()
        
        # Generate steps based on complexity
        if complexity == "Simple":
            steps = [
                "1. Gather any needed materials",
                "2. Complete the main task",
                "3. Review and finalize"
            ]
        elif complexity == "Moderate":
            steps = [
                "1. Break task into 2-3 main parts",
                "2. Gather information and resources",
                "3. Complete first part",
                "4. Take a short break",
                "5. Complete remaining parts",
                "6. Review and check quality"
            ]
        elif complexity == "Complex":
            steps = [
                "1. Research and understand requirements",
                "2. Create an outline or plan",
                "3. Break into 4-6 smaller tasks",
                "4. Complete preliminary work",
                "5. Work on main components (one at a time)",
                "6. Take regular breaks between components",
                "7. Review and integrate parts",
                "8. Final quality check"
            ]
        else:  # Very Complex
            steps = [
                "1. Analyze the full scope of the task",
                "2. Research best practices or examples",
                "3. Create detailed project plan",
                "4. Identify potential challenges",
                "5. Break into 6+ manageable chunks",
                "6. Set mini-deadlines for each chunk",
                "7. Complete chunks over multiple sessions",
                "8. Regular progress reviews",
                "9. Seek feedback if possible",
                "10. Final assembly and review"
            ]
        
        # Add ASD-specific modifications
        if anxiety_level >= 3:
            steps.insert(0, "0. Take 5 deep breaths and remind yourself of your strengths")
            steps.append("• Celebrate completion of each step")
            self.anxiety_strategies.show()
        else:
            self.anxiety_strategies.hide()
        
        # Add steps to list
        for step in steps:
            item = QListWidgetItem(step)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.breakdown_list.addItem(item)
    
    def add_custom_step(self):
        """Add a custom step to the breakdown"""
        step_text = self.custom_step.text().strip()
        if step_text:
            item = QListWidgetItem(f"• {step_text}")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.breakdown_list.addItem(item)
            self.custom_step.clear()

class ExecFunctionCoachWidget(QWidget):
    """Enhanced Executive Function Coach with psychological support"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the enhanced executive function coach UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("🧠 Executive Function Coach")
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
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E5E5EA;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #F2F2F7;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #007AFF;
            }
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
        tips_layout.addWidget(QLabel("💡 Executive Function Tips"))
        
        tips_text = QLabel("""
• Use external memory aids (lists, calendars, reminders)
• Break large tasks into smaller, specific steps
• Establish consistent routines and stick to them
• Use visual schedules and checklists
• Plan for transitions and changes in advance
• Build in regular breaks and rewards
• Practice self-compassion when things don't go as planned
        """)
        tips_text.setWordWrap(True)
        tips_text.setStyleSheet("font-size: 12px; color: #666666; line-height: 1.4;")
        tips_layout.addWidget(tips_text)
        
        breakdown_layout.addWidget(tips_card)
        breakdown_layout.addStretch()
        
        self.tabs.addTab(breakdown_widget, "Task Breakdown")
        
        # CBT Toolkit tab
        cbt_scroll = QScrollArea()
        cbt_scroll.setWidgetResizable(True)
        cbt_scroll.setFrameShape(QFrame.NoFrame)
        
        self.cbt_toolkit = CBTToolkitWidget()
        cbt_scroll.setWidget(self.cbt_toolkit)
        
        self.tabs.addTab(cbt_scroll, "CBT Tools")
        
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
        
        # CBT exercises
        cbt_widget = QWidget()
        cbt_layout = QVBoxLayout(cbt_widget)
        cbt_layout.addWidget(QLabel("CBT Exercises"))
        cbt_count = QLabel("5")
        cbt_count.setStyleSheet("font-size: 32px; font-weight: 700; color: #FF9500;")
        cbt_count.setAlignment(Qt.AlignCenter)
        cbt_layout.addWidget(cbt_count)
        cbt_layout.addWidget(QLabel("This week"))
        
        stats_layout.addWidget(sessions_widget)
        stats_layout.addWidget(tasks_widget) 
        stats_layout.addWidget(cbt_widget)
        
        weekly_layout.addLayout(stats_layout)
        
        # Mood trend
        mood_card = AppleCard()
        mood_layout = QVBoxLayout(mood_card)
        mood_layout.addWidget(QLabel("📈 Mood Trend"))
        
        mood_text = QLabel("Average mood this week: 7.2/10 ↗️\nAnxiety levels are decreasing 📉")
        mood_text.setStyleSheet("font-size: 14px; color: #34C759;")
        mood_layout.addWidget(mood_text)
        
        progress_layout.addWidget(weekly_card)
        progress_layout.addWidget(mood_card)
        progress_layout.addStretch()
        
        self.tabs.addTab(progress_widget, "Progress")
        
        layout.addWidget(self.tabs)
    
    def add_sample_goals(self):
        """Add some sample goals"""
        goals = [
            "Complete project proposal draft",
            "Review team feedback and respond", 
            "Organize workspace and files",
            "Plan tomorrow's schedule",
            "Practice one CBT exercise"
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
                "You completed a focus session. Take a well-deserved break and do something you enjoy!"
            )
        else:
            AppleNotification.show_info(
                self,
                "Break time over! 💪",
                "Ready to get back to focused work? Remember to start with something small if you're feeling overwhelmed."
            )