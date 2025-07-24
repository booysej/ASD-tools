"""
CBT Toolkit for ASD - Cognitive Behavioral Therapy tools adapted for autism
Based on CBT-A (CBT for Autism) research and evidence-based practices
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QComboBox, QTextEdit, QScrollArea,
                               QGroupBox, QCheckBox, QGridLayout, QFrame,
                               QButtonGroup, QRadioButton, QSlider, QTabWidget,
                               QListWidget, QListWidgetItem, QDialog, QDialogButtonBox,
                               QSpinBox, QProgressBar)
from PySide6.QtCore import Qt, Signal, QTimer, QDate
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from cogtools.core.widgets import AppleCard, AppleButton, AppleTextField
import json
from datetime import datetime, timedelta

class ThoughtRecord(AppleCard):
    """CBT thought record adapted for ASD thinking patterns"""
    
    thought_recorded = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_record = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup thought record UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🧠 Thought Record")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("A thought record helps you notice and examine your thoughts, especially when you're feeling upset or stressed.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666666; font-style: italic; margin-bottom: 15px;")
        layout.addWidget(desc)
        
        # Situation section
        situation_group = QGroupBox("🎯 What happened? (The Situation)")
        situation_layout = QVBoxLayout(situation_group)
        
        situation_layout.addWidget(QLabel("Describe what was happening when you noticed the feeling:"))
        self.situation_text = QTextEdit()
        self.situation_text.setMaximumHeight(80)
        self.situation_text.setPlaceholderText("Where were you? Who was there? What was happening? Be specific about facts, not interpretations.")
        situation_layout.addWidget(self.situation_text)
        
        layout.addWidget(situation_group)
        
        # Emotions section
        emotions_group = QGroupBox("😊 What did you feel? (Emotions)")
        emotions_layout = QVBoxLayout(emotions_group)
        
        emotions_layout.addWidget(QLabel("Select emotions you felt (you can choose more than one):"))
        
        # Common emotions with intensity sliders
        emotions = [
            "Anxious/Worried", "Sad/Down", "Angry/Frustrated", "Scared/Afraid", 
            "Embarrassed/Ashamed", "Overwhelmed", "Confused", "Happy/Excited"
        ]
        
        self.emotion_sliders = {}
        emotions_grid = QGridLayout()
        
        for i, emotion in enumerate(emotions):
            row = i // 2
            col = (i % 2) * 3
            
            # Emotion label
            emotion_label = QLabel(emotion)
            emotions_grid.addWidget(emotion_label, row, col)
            
            # Intensity slider
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 10)
            slider.setValue(0)
            slider.setFixedWidth(100)
            emotions_grid.addWidget(slider, row, col + 1)
            
            # Intensity label
            intensity_label = QLabel("0")
            slider.valueChanged.connect(lambda v, l=intensity_label: l.setText(str(v)))
            emotions_grid.addWidget(intensity_label, row, col + 2)
            
            self.emotion_sliders[emotion] = slider
        
        emotions_layout.addLayout(emotions_grid)
        layout.addWidget(emotions_group)
        
        # Thoughts section
        thoughts_group = QGroupBox("💭 What went through your mind? (Thoughts)")
        thoughts_layout = QVBoxLayout(thoughts_group)
        
        thoughts_layout.addWidget(QLabel("What thoughts went through your mind? What were you thinking about?"))
        self.thoughts_text = QTextEdit()
        self.thoughts_text.setMaximumHeight(100)
        self.thoughts_text.setPlaceholderText("Write down your thoughts exactly as they occurred. Don't worry about whether they're 'right' or 'wrong'.")
        thoughts_layout.addWidget(self.thoughts_text)
        
        # Thought believability
        believability_layout = QHBoxLayout()
        believability_layout.addWidget(QLabel("How much do you believe this thought? (0-100%):"))
        
        self.believability_slider = QSlider(Qt.Horizontal)
        self.believability_slider.setRange(0, 100)
        self.believability_slider.setValue(50)
        
        self.believability_label = QLabel("50%")
        self.believability_slider.valueChanged.connect(lambda v: self.believability_label.setText(f"{v}%"))
        
        believability_layout.addWidget(self.believability_slider)
        believability_layout.addWidget(self.believability_label)
        
        thoughts_layout.addLayout(believability_layout)
        layout.addWidget(thoughts_group)
        
        # Evidence section
        evidence_group = QGroupBox("🔍 Evidence (Looking at the facts)")
        evidence_layout = QVBoxLayout(evidence_group)
        
        evidence_layout.addWidget(QLabel("Evidence FOR this thought:"))
        self.evidence_for = QTextEdit()
        self.evidence_for.setMaximumHeight(70)
        self.evidence_for.setPlaceholderText("What facts support this thought?")
        evidence_layout.addWidget(self.evidence_for)
        
        evidence_layout.addWidget(QLabel("Evidence AGAINST this thought:"))
        self.evidence_against = QTextEdit()
        self.evidence_against.setMaximumHeight(70)
        self.evidence_against.setPlaceholderText("What facts contradict this thought? What would you tell a friend in this situation?")
        evidence_layout.addWidget(self.evidence_against)
        
        layout.addWidget(evidence_group)
        
        # Alternative thought section
        alternative_group = QGroupBox("🌟 Alternative Thoughts")
        alternative_layout = QVBoxLayout(alternative_group)
        
        alternative_layout.addWidget(QLabel("Based on the evidence, what's a more balanced way to think about this situation?"))
        self.alternative_text = QTextEdit()
        self.alternative_text.setMaximumHeight(80)
        self.alternative_text.setPlaceholderText("Write a more balanced, realistic thought. Consider all the evidence.")
        alternative_layout.addWidget(self.alternative_text)
        
        # New believability
        new_believability_layout = QHBoxLayout()
        new_believability_layout.addWidget(QLabel("How much do you believe the ORIGINAL thought now? (0-100%):"))
        
        self.new_believability_slider = QSlider(Qt.Horizontal)
        self.new_believability_slider.setRange(0, 100)
        self.new_believability_slider.setValue(50)
        
        self.new_believability_label = QLabel("50%")
        self.new_believability_slider.valueChanged.connect(lambda v: self.new_believability_label.setText(f"{v}%"))
        
        new_believability_layout.addWidget(self.new_believability_slider)
        new_believability_layout.addWidget(self.new_believability_label)
        
        alternative_layout.addLayout(new_believability_layout)
        layout.addWidget(alternative_group)
        
        # Save button
        save_btn = AppleButton("Save Thought Record")
        save_btn.clicked.connect(self.save_thought_record)
        layout.addWidget(save_btn)
    
    def save_thought_record(self):
        """Save the current thought record"""
        emotions = {}
        for emotion, slider in self.emotion_sliders.items():
            if slider.value() > 0:
                emotions[emotion] = slider.value()
        
        self.current_record = {
            'situation': self.situation_text.toPlainText(),
            'emotions': emotions,
            'thoughts': self.thoughts_text.toPlainText(),
            'believability_before': self.believability_slider.value(),
            'evidence_for': self.evidence_for.toPlainText(),
            'evidence_against': self.evidence_against.toPlainText(),
            'alternative_thought': self.alternative_text.toPlainText(),
            'believability_after': self.new_believability_slider.value(),
            'timestamp': datetime.now().isoformat()
        }
        
        self.thought_recorded.emit(self.current_record)
        
        # Clear form for next use
        self.clear_form()
    
    def clear_form(self):
        """Clear all form fields"""
        self.situation_text.clear()
        self.thoughts_text.clear()
        self.evidence_for.clear()
        self.evidence_against.clear()
        self.alternative_text.clear()
        
        for slider in self.emotion_sliders.values():
            slider.setValue(0)
        
        self.believability_slider.setValue(50)
        self.new_believability_slider.setValue(50)

class BehaviorExperiment(AppleCard):
    """Design and track behavioral experiments"""
    
    experiment_completed = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup behavior experiment UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🧪 Behavior Experiment")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Behavior experiments help you test whether your worries or beliefs are accurate by trying something new in a safe way.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666666; font-style: italic; margin-bottom: 15px;")
        layout.addWidget(desc)
        
        # Prediction section
        prediction_group = QGroupBox("🔮 What do you predict will happen?")
        prediction_layout = QVBoxLayout(prediction_group)
        
        prediction_layout.addWidget(QLabel("Describe your worry or belief:"))
        self.belief_text = QTextEdit()
        self.belief_text.setMaximumHeight(60)
        self.belief_text.setPlaceholderText("What do you think will happen if you try this?")
        prediction_layout.addWidget(self.belief_text)
        
        # Confidence in prediction
        confidence_layout = QHBoxLayout()
        confidence_layout.addWidget(QLabel("How confident are you this will happen? (0-100%):"))
        
        self.confidence_slider = QSlider(Qt.Horizontal)
        self.confidence_slider.setRange(0, 100)
        self.confidence_slider.setValue(50)
        
        self.confidence_label = QLabel("50%")
        self.confidence_slider.valueChanged.connect(lambda v: self.confidence_label.setText(f"{v}%"))
        
        confidence_layout.addWidget(self.confidence_slider)
        confidence_layout.addWidget(self.confidence_label)
        
        prediction_layout.addLayout(confidence_layout)
        layout.addWidget(prediction_group)
        
        # Experiment design
        experiment_group = QGroupBox("🎯 Design your experiment")
        experiment_layout = QVBoxLayout(experiment_group)
        
        experiment_layout.addWidget(QLabel("What exactly will you try? (Be specific)"))
        self.experiment_text = QTextEdit()
        self.experiment_text.setMaximumHeight(80)
        self.experiment_text.setPlaceholderText("Describe exactly what you'll do, when, where, and with whom.")
        experiment_layout.addWidget(self.experiment_text)
        
        # Safety planning
        experiment_layout.addWidget(QLabel("Safety plan (What will you do if you feel overwhelmed?):"))
        self.safety_text = QTextEdit()
        self.safety_text.setMaximumHeight(60)
        self.safety_text.setPlaceholderText("How will you take care of yourself? Who can help? What's your exit strategy?")
        experiment_layout.addWidget(self.safety_text)
        
        layout.addWidget(experiment_group)
        
        # Results section
        results_group = QGroupBox("📊 What actually happened?")
        results_layout = QVBoxLayout(results_group)
        
        results_layout.addWidget(QLabel("Describe what actually happened:"))
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(80)
        self.results_text.setPlaceholderText("What actually happened? How did you feel? What did you learn?")
        results_layout.addWidget(self.results_text)
        
        # Outcome vs prediction
        outcome_layout = QHBoxLayout()
        outcome_layout.addWidget(QLabel("How much did your prediction come true? (0-100%):"))
        
        self.outcome_slider = QSlider(Qt.Horizontal)
        self.outcome_slider.setRange(0, 100)
        self.outcome_slider.setValue(0)
        
        self.outcome_label = QLabel("0%")
        self.outcome_slider.valueChanged.connect(lambda v: self.outcome_label.setText(f"{v}%"))
        
        outcome_layout.addWidget(self.outcome_slider)
        outcome_layout.addWidget(self.outcome_label)
        
        results_layout.addLayout(outcome_layout)
        layout.addWidget(results_group)
        
        # Learning section
        learning_group = QGroupBox("💡 What did you learn?")
        learning_layout = QVBoxLayout(learning_group)
        
        self.learning_text = QTextEdit()
        self.learning_text.setMaximumHeight(80)
        self.learning_text.setPlaceholderText("What did this experiment teach you? How might this change your thinking about similar situations?")
        learning_layout.addWidget(self.learning_text)
        
        layout.addWidget(learning_group)
        
        # Save button
        save_btn = AppleButton("Save Experiment")
        save_btn.clicked.connect(self.save_experiment)
        layout.addWidget(save_btn)
    
    def save_experiment(self):
        """Save the behavior experiment"""
        experiment_data = {
            'belief': self.belief_text.toPlainText(),
            'confidence_before': self.confidence_slider.value(),
            'experiment_plan': self.experiment_text.toPlainText(),
            'safety_plan': self.safety_text.toPlainText(),
            'results': self.results_text.toPlainText(),
            'prediction_accuracy': self.outcome_slider.value(),
            'learning': self.learning_text.toPlainText(),
            'timestamp': datetime.now().isoformat()
        }
        
        self.experiment_completed.emit(experiment_data)

class CopingStrategies(AppleCard):
    """ASD-specific coping strategies and tools"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup coping strategies UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🛠️ Coping Strategies Toolbox")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Strategy categories
        categories = {
            "Immediate Calming (When overwhelmed right now)": [
                "5-4-3-2-1 Grounding: Name 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste",
                "Box breathing: Breathe in for 4, hold for 4, out for 4, hold for 4",
                "Progressive muscle relaxation: Tense and release each muscle group",
                "Cold water on face or wrists",
                "Weighted blanket or tight hugs",
                "Noise-canceling headphones",
                "Fidget tools or stress ball"
            ],
            "Thinking Strategies (When thoughts are unhelpful)": [
                "Thought stopping: Say 'STOP' and redirect to something concrete",
                "Fact vs. opinion: 'Is this a fact or my interpretation?'",
                "Time perspective: 'Will this matter in 1 year?'",
                "Best friend advice: 'What would I tell my best friend?'",
                "Probability check: 'What's the actual likelihood of this?'",
                "Reframe catastrophizing: 'What's the worst, best, and most likely outcome?'"
            ],
            "Social Strategies (When social situations are hard)": [
                "Script preparation: Practice what you'll say beforehand",
                "Safe person identification: Know who you can talk to for help",
                "Exit strategy: Always have a plan for how to leave if needed",
                "Break timing: Take regular breaks from social interaction",
                "Interest sharing: Talk about your special interests when appropriate",
                "Observation first: Watch and listen before jumping into conversations"
            ],
            "Sensory Strategies (When environment is overwhelming)": [
                "Environmental modification: Change lighting, noise, or position",
                "Sensory breaks: Step away for 5-10 minutes",
                "Calming sensory input: Use preferred textures, sounds, or movements",
                "Sensory diet: Follow your planned sensory activities",
                "Pressure input: Deep pressure hugs, weighted items, or tight clothing",
                "Movement: Rock, pace, or do jumping jacks"
            ],
            "Planning Strategies (When facing change or transitions)": [
                "Visual schedules: Create pictures or lists of what will happen",
                "Transition warnings: Give yourself 5, 3, and 1-minute warnings",
                "Backup plans: Always have a Plan B (and C)",
                "Information gathering: Research new situations beforehand",
                "Gradual exposure: Start small and build up slowly",
                "Routine anchors: Maintain some familiar elements during changes"
            ]
        }
        
        for category, strategies in categories.items():
            category_group = QGroupBox(category)
            category_layout = QVBoxLayout(category_group)
            
            for strategy in strategies:
                strategy_widget = QFrame()
                strategy_widget.setStyleSheet("""
                    QFrame {
                        background-color: #F9F9F9;
                        border-radius: 8px;
                        padding: 8px;
                        margin: 2px;
                    }
                """)
                
                strategy_layout = QHBoxLayout(strategy_widget)
                
                # Strategy text
                strategy_label = QLabel(f"• {strategy}")
                strategy_label.setWordWrap(True)
                strategy_label.setStyleSheet("color: #333333; font-size: 12px;")
                
                # "Tried it" checkbox
                tried_cb = QCheckBox("Used")
                tried_cb.setStyleSheet("margin-left: 10px;")
                
                strategy_layout.addWidget(strategy_label, 1)
                strategy_layout.addWidget(tried_cb)
                
                category_layout.addWidget(strategy_widget)
            
            layout.addWidget(category_group)
        
        # Personal strategies
        personal_group = QGroupBox("📝 My Personal Strategies")
        personal_layout = QVBoxLayout(personal_group)
        
        personal_layout.addWidget(QLabel("Add strategies that work specifically for you:"))
        
        add_strategy_layout = QHBoxLayout()
        self.new_strategy = AppleTextField("My coping strategy...")
        add_btn = AppleButton("Add")
        add_btn.clicked.connect(self.add_personal_strategy)
        
        add_strategy_layout.addWidget(self.new_strategy)
        add_strategy_layout.addWidget(add_btn)
        
        personal_layout.addLayout(add_strategy_layout)
        
        self.personal_strategies_list = QListWidget()
        self.personal_strategies_list.setMaximumHeight(100)
        personal_layout.addWidget(self.personal_strategies_list)
        
        layout.addWidget(personal_group)
    
    def add_personal_strategy(self):
        """Add a personal coping strategy"""
        strategy = self.new_strategy.text().strip()
        if strategy:
            self.personal_strategies_list.addItem(f"• {strategy}")
            self.new_strategy.clear()

class MoodTracker(AppleCard):
    """Simple mood and anxiety tracking"""
    
    mood_logged = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup mood tracker UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("📊 Daily Mood & Anxiety Tracker")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Current mood
        mood_group = QGroupBox("😊 How are you feeling right now?")
        mood_layout = QVBoxLayout(mood_group)
        
        # Mood scale
        mood_scale_layout = QHBoxLayout()
        mood_scale_layout.addWidget(QLabel("Overall mood (1=very bad, 10=very good):"))
        
        self.mood_slider = QSlider(Qt.Horizontal)
        self.mood_slider.setRange(1, 10)
        self.mood_slider.setValue(5)
        
        self.mood_label = QLabel("5")
        self.mood_slider.valueChanged.connect(lambda v: self.mood_label.setText(str(v)))
        
        mood_scale_layout.addWidget(self.mood_slider)
        mood_scale_layout.addWidget(self.mood_label)
        
        mood_layout.addLayout(mood_scale_layout)
        
        # Anxiety scale
        anxiety_scale_layout = QHBoxLayout()
        anxiety_scale_layout.addWidget(QLabel("Anxiety level (1=very calm, 10=very anxious):"))
        
        self.anxiety_slider = QSlider(Qt.Horizontal)
        self.anxiety_slider.setRange(1, 10)
        self.anxiety_slider.setValue(5)
        
        self.anxiety_label = QLabel("5")
        self.anxiety_slider.valueChanged.connect(lambda v: self.anxiety_label.setText(str(v)))
        
        anxiety_scale_layout.addWidget(self.anxiety_slider)
        anxiety_scale_layout.addWidget(self.anxiety_label)
        
        mood_layout.addLayout(anxiety_scale_layout)
        
        layout.addWidget(mood_group)
        
        # Contributing factors
        factors_group = QGroupBox("🎯 What's affecting your mood today?")
        factors_layout = QVBoxLayout(factors_group)
        
        factors = [
            "Sleep quality", "Social interactions", "Sensory environment",
            "Routine changes", "Work/school stress", "Physical health",
            "Special interests", "Exercise", "Weather", "Other"
        ]
        
        self.factor_checkboxes = {}
        factors_grid = QGridLayout()
        
        for i, factor in enumerate(factors):
            row = i // 2
            col = i % 2
            
            cb = QCheckBox(factor)
            factors_grid.addWidget(cb, row, col)
            self.factor_checkboxes[factor] = cb
        
        factors_layout.addLayout(factors_grid)
        layout.addWidget(factors_group)
        
        # Notes
        notes_group = QGroupBox("📝 Notes")
        notes_layout = QVBoxLayout(notes_group)
        
        self.notes_text = QTextEdit()
        self.notes_text.setMaximumHeight(80)
        self.notes_text.setPlaceholderText("Any additional notes about your day, thoughts, or feelings...")
        notes_layout.addWidget(self.notes_text)
        
        layout.addWidget(notes_group)
        
        # Log mood button
        log_btn = AppleButton("Log Today's Mood")
        log_btn.clicked.connect(self.log_mood)
        layout.addWidget(log_btn)
        
        # Recent entries
        recent_group = QGroupBox("📈 Recent Entries")
        recent_layout = QVBoxLayout(recent_group)
        
        self.recent_list = QListWidget()
        self.recent_list.setMaximumHeight(120)
        recent_layout.addWidget(self.recent_list)
        
        layout.addWidget(recent_group)
        
        self.load_recent_entries()
    
    def log_mood(self):
        """Log the current mood entry"""
        factors = [factor for factor, cb in self.factor_checkboxes.items() if cb.isChecked()]
        
        mood_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M'),
            'mood': self.mood_slider.value(),
            'anxiety': self.anxiety_slider.value(),
            'factors': factors,
            'notes': self.notes_text.toPlainText(),
            'timestamp': datetime.now().isoformat()
        }
        
        self.mood_logged.emit(mood_entry)
        
        # Add to recent entries
        entry_text = f"{mood_entry['date']} - Mood: {mood_entry['mood']}/10, Anxiety: {mood_entry['anxiety']}/10"
        self.recent_list.insertItem(0, entry_text)
        
        # Keep only last 10 entries
        while self.recent_list.count() > 10:
            self.recent_list.takeItem(self.recent_list.count() - 1)
        
        # Clear form
        self.notes_text.clear()
        for cb in self.factor_checkboxes.values():
            cb.setChecked(False)
    
    def load_recent_entries(self):
        """Load recent mood entries"""
        # Sample entries for demonstration
        sample_entries = [
            "2024-01-15 - Mood: 7/10, Anxiety: 4/10",
            "2024-01-14 - Mood: 5/10, Anxiety: 7/10",
            "2024-01-13 - Mood: 8/10, Anxiety: 3/10"
        ]
        
        for entry in sample_entries:
            self.recent_list.addItem(entry)

class CBTToolkitWidget(QWidget):
    """Main CBT toolkit combining all tools"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main CBT toolkit UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("🧠 CBT Toolkit for ASD")
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
        
        # Thought Records tab
        thought_scroll = QScrollArea()
        thought_scroll.setWidgetResizable(True)
        thought_scroll.setFrameShape(QFrame.NoFrame)
        
        self.thought_record = ThoughtRecord()
        thought_scroll.setWidget(self.thought_record)
        
        self.tabs.addTab(thought_scroll, "Thought Records")
        
        # Behavior Experiments tab
        experiment_scroll = QScrollArea()
        experiment_scroll.setWidgetResizable(True)
        experiment_scroll.setFrameShape(QFrame.NoFrame)
        
        self.behavior_experiment = BehaviorExperiment()
        experiment_scroll.setWidget(self.behavior_experiment)
        
        self.tabs.addTab(experiment_scroll, "Experiments")
        
        # Coping Strategies tab
        coping_scroll = QScrollArea()
        coping_scroll.setWidgetResizable(True)
        coping_scroll.setFrameShape(QFrame.NoFrame)
        
        self.coping_strategies = CopingStrategies()
        coping_scroll.setWidget(self.coping_strategies)
        
        self.tabs.addTab(coping_scroll, "Coping Tools")
        
        # Mood Tracker tab
        mood_scroll = QScrollArea()
        mood_scroll.setWidgetResizable(True)
        mood_scroll.setFrameShape(QFrame.NoFrame)
        
        self.mood_tracker = MoodTracker()
        mood_scroll.setWidget(self.mood_tracker)
        
        self.tabs.addTab(mood_scroll, "Mood Tracker")
        
        layout.addWidget(self.tabs)