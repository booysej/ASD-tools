"""
Sensory Toolkit - Evidence-based sensory processing support for ASD
Based on Sensory Processing Theory (Ayres) and current ASD research
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QSlider, QPushButton, QComboBox, QTextEdit,
                               QProgressBar, QGroupBox, QCheckBox, QGridLayout,
                               QScrollArea, QFrame, QButtonGroup, QRadioButton,
                               QSpinBox, QTimeEdit, QTabWidget)
from PySide6.QtCore import Qt, Signal, QTimer, QTime
from PySide6.QtGui import QColor, QFont, QPixmap, QPainter
from cogtools.core.widgets import AppleCard, AppleButton, AppleTextField
from datetime import datetime, timedelta
import json

class SensoryProfileWidget(AppleCard):
    """Individual sensory profile assessment and tracking"""
    
    profile_updated = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sensory_data = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup sensory profile UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🎭 Sensory Profile Assessment")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Based on Dunn's Sensory Profile categories
        sensory_systems = {
            "Auditory": {
                "description": "How you process sounds",
                "items": [
                    "Sudden loud noises",
                    "Background noise (TV, music)",
                    "Multiple people talking",
                    "High-pitched sounds",
                    "Specific textures of sound"
                ]
            },
            "Visual": {
                "description": "How you process what you see",
                "items": [
                    "Bright lights",
                    "Fluorescent lighting", 
                    "Busy visual environments",
                    "Moving objects",
                    "Certain colors or patterns"
                ]
            },
            "Tactile": {
                "description": "How you process touch",
                "items": [
                    "Light touch",
                    "Clothing textures",
                    "Food textures",
                    "Getting hands dirty",
                    "Unexpected touch"
                ]
            },
            "Vestibular": {
                "description": "How you process movement and balance",
                "items": [
                    "Swinging or spinning",
                    "Heights or falling",
                    "Quick movements",
                    "Being upside down",
                    "Uneven surfaces"
                ]
            },
            "Proprioceptive": {
                "description": "How you sense your body position",
                "items": [
                    "Need for deep pressure",
                    "Heavy work activities",
                    "Joint compression",
                    "Tight spaces",
                    "Physical boundaries"
                ]
            }
        }
        
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        self.system_ratings = {}
        
        for system_name, system_info in sensory_systems.items():
            system_group = QGroupBox(f"{system_name} Processing")
            system_layout = QVBoxLayout(system_group)
            
            # Description
            desc_label = QLabel(system_info["description"])
            desc_label.setStyleSheet("font-style: italic; color: #666666; margin-bottom: 10px;")
            system_layout.addWidget(desc_label)
            
            self.system_ratings[system_name] = {}
            
            for item in system_info["items"]:
                item_layout = QHBoxLayout()
                
                item_label = QLabel(item)
                item_label.setMinimumWidth(200)
                item_layout.addWidget(item_label)
                
                # Rating scale: 1 (Very Sensitive) to 5 (Very Seeking)
                slider = QSlider(Qt.Horizontal)
                slider.setRange(1, 5)
                slider.setValue(3)  # Neutral
                slider.valueChanged.connect(lambda v, s=system_name, i=item: self.update_rating(s, i, v))
                
                rating_label = QLabel("Neutral")
                rating_label.setMinimumWidth(80)
                slider.valueChanged.connect(lambda v, l=rating_label: l.setText(self.get_rating_text(v)))
                
                item_layout.addWidget(slider)
                item_layout.addWidget(rating_label)
                
                self.system_ratings[system_name][item] = slider
                system_layout.addLayout(item_layout)
            
            scroll_layout.addWidget(system_group)
        
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        # Generate recommendations button
        generate_btn = AppleButton("Generate Sensory Recommendations")
        generate_btn.clicked.connect(self.generate_recommendations)
        layout.addWidget(generate_btn)
        
        # Recommendations display
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setReadOnly(True)
        self.recommendations_text.setMaximumHeight(150)
        self.recommendations_text.setPlaceholderText("Complete the assessment to see personalized sensory strategies...")
        layout.addWidget(self.recommendations_text)
    
    def get_rating_text(self, value):
        """Convert rating value to descriptive text"""
        ratings = {
            1: "Very Sensitive",
            2: "Sensitive", 
            3: "Neutral",
            4: "Seeking",
            5: "Very Seeking"
        }
        return ratings.get(value, "Neutral")
    
    def update_rating(self, system, item, value):
        """Update rating for a sensory item"""
        if system not in self.sensory_data:
            self.sensory_data[system] = {}
        self.sensory_data[system][item] = value
    
    def generate_recommendations(self):
        """Generate personalized sensory recommendations based on profile"""
        if not self.sensory_data:
            self.recommendations_text.setText("Please complete the sensory assessment first.")
            return
        
        recommendations = []
        
        # Analyze each system
        for system, items in self.sensory_data.items():
            avg_rating = sum(items.values()) / len(items) if items else 3
            
            if system == "Auditory":
                if avg_rating <= 2:  # Sensitive
                    recommendations.extend([
                        "🎧 Use noise-canceling headphones in busy environments",
                        "🔇 Create quiet spaces at home with soft furnishings",
                        "⏰ Use visual timers instead of auditory alarms",
                        "🎵 Try white noise or brown noise for focus"
                    ])
                elif avg_rating >= 4:  # Seeking
                    recommendations.extend([
                        "🎵 Incorporate music into daily routines",
                        "🔊 Use upbeat music for transitions",
                        "🎤 Try humming or singing for self-regulation",
                        "🎼 Explore different types of music for different moods"
                    ])
            
            elif system == "Visual":
                if avg_rating <= 2:  # Sensitive
                    recommendations.extend([
                        "💡 Use soft, warm lighting instead of fluorescents",
                        "🕶️ Wear sunglasses in bright environments",
                        "🎨 Choose calming, muted colors for personal spaces",
                        "📱 Reduce screen brightness and use dark modes"
                    ])
                elif avg_rating >= 4:  # Seeking
                    recommendations.extend([
                        "🌈 Use colorful visual schedules and reminders",
                        "✨ Incorporate interesting visual patterns",
                        "🎭 Try visual fidgets like kaleidoscopes",
                        "🎨 Engage in visually stimulating art activities"
                    ])
            
            elif system == "Tactile":
                if avg_rating <= 2:  # Sensitive
                    recommendations.extend([
                        "👕 Choose soft, seamless clothing fabrics",
                        "🧤 Use gloves for messy activities when needed",
                        "🚿 Gradually introduce new textures",
                        "🤚 Practice deep pressure touch for comfort"
                    ])
                elif avg_rating >= 4:  # Seeking
                    recommendations.extend([
                        "🧸 Use textured fidgets and stress balls",
                        "🎨 Try clay, playdough, or kinetic sand",
                        "🛁 Explore different bath textures safely",
                        "👐 Incorporate texture exploration into daily activities"
                    ])
            
            elif system == "Vestibular":
                if avg_rating <= 2:  # Sensitive
                    recommendations.extend([
                        "🪑 Use stable seating with good support",
                        "🚶 Take movement breaks slowly and controlled",
                        "🧘 Try gentle yoga or stretching",
                        "⚖️ Focus on balance exercises on solid ground"
                    ])
                elif avg_rating >= 4:  # Seeking
                    recommendations.extend([
                        "🪀 Use a therapy ball or wobble cushion",
                        "🏃 Incorporate running or jumping activities",
                        "🎠 Try swinging or spinning (safely supervised)",
                        "🤸 Consider gymnastics or dance activities"
                    ])
            
            elif system == "Proprioceptive":
                if avg_rating <= 2:  # Sensitive to pressure
                    recommendations.extend([
                        "🤗 Use light, gentle pressure activities",
                        "🧘 Try progressive muscle relaxation",
                        "👕 Choose loose, comfortable clothing",
                        "🛏️ Use lighter blankets and bedding"
                    ])
                elif avg_rating >= 4:  # Seeking pressure
                    recommendations.extend([
                        "🏋️ Try heavy work activities (carrying, pushing)",
                        "🤗 Use weighted blankets or lap pads",
                        "💪 Incorporate resistance exercises",
                        "🤲 Try deep pressure massage or hugs"
                    ])
        
        # Format recommendations
        if recommendations:
            formatted_recs = "\n".join([f"• {rec}" for rec in recommendations[:12]])  # Limit to 12
            final_text = f"🎯 Personalized Sensory Strategies:\n\n{formatted_recs}\n\n💡 Remember: These are starting points. Observe what works best and adjust accordingly!"
        else:
            final_text = "Complete more of the assessment to generate specific recommendations."
        
        self.recommendations_text.setText(final_text)
        self.profile_updated.emit(self.sensory_data)

class SensoryDietPlanner(AppleCard):
    """Evidence-based sensory diet planning tool"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup sensory diet planner UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🍽️ Sensory Diet Planner")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("A 'sensory diet' is a planned schedule of sensory activities throughout the day to help maintain optimal arousal and attention.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666666; font-style: italic; margin-bottom: 15px;")
        layout.addWidget(desc)
        
        # Time-based sensory activities
        self.daily_schedule = {}
        
        # Morning routine
        morning_group = QGroupBox("🌅 Morning Routine (6-10 AM)")
        morning_layout = QVBoxLayout(morning_group)
        
        morning_activities = [
            ("Heavy Work", "Carrying laundry, making bed with firm pressure", "proprioceptive"),
            ("Deep Pressure", "Tight hugs, weighted blanket for 10 minutes", "tactile"),
            ("Organizing", "Sort items by color/size for visual input", "visual"),
            ("Calming Music", "Soft instrumental music during breakfast", "auditory")
        ]
        
        for activity, description, system in morning_activities:
            activity_widget = self.create_activity_widget(activity, description, system)
            morning_layout.addWidget(activity_widget)
        
        layout.addWidget(morning_group)
        
        # Midday routine
        midday_group = QGroupBox("☀️ Midday Routine (10 AM-2 PM)")
        midday_layout = QVBoxLayout(midday_group)
        
        midday_activities = [
            ("Movement Breaks", "5-minute walks or jumping jacks every hour", "vestibular"),
            ("Fidget Tools", "Stress ball or fidget toy during focused work", "tactile"),
            ("Visual Breaks", "Look out window or at calming pictures", "visual"),
            ("Alerting Activities", "Crunchy snacks or cold drinks", "oral")
        ]
        
        for activity, description, system in midday_activities:
            activity_widget = self.create_activity_widget(activity, description, system)
            midday_layout.addWidget(activity_widget)
        
        layout.addWidget(midday_group)
        
        # Evening routine
        evening_group = QGroupBox("🌙 Evening Routine (6-9 PM)")
        evening_layout = QVBoxLayout(evening_group)
        
        evening_activities = [
            ("Calming Input", "Dim lights, soft textures, quiet activities", "multi-sensory"),
            ("Proprioceptive", "Gentle stretching or yoga poses", "proprioceptive"),
            ("Deep Breathing", "Slow, rhythmic breathing exercises", "interoceptive"),
            ("Consistent Routine", "Same order of activities each evening", "predictability")
        ]
        
        for activity, description, system in evening_activities:
            activity_widget = self.create_activity_widget(activity, description, system)
            evening_layout.addWidget(activity_widget)
        
        layout.addWidget(evening_group)
        
        # Customization section
        custom_group = QGroupBox("🎯 Customize Your Diet")
        custom_layout = QVBoxLayout(custom_group)
        
        custom_layout.addWidget(QLabel("Add your own sensory activities:"))
        
        self.custom_activity = AppleTextField("Activity name...")
        self.custom_description = AppleTextField("Description...")
        self.custom_time = QComboBox()
        self.custom_time.addItems(["Morning", "Midday", "Evening", "As Needed"])
        
        custom_form = QHBoxLayout()
        custom_form.addWidget(self.custom_activity)
        custom_form.addWidget(self.custom_description)
        custom_form.addWidget(self.custom_time)
        
        add_btn = AppleButton("Add Activity")
        add_btn.clicked.connect(self.add_custom_activity)
        custom_form.addWidget(add_btn)
        
        custom_layout.addLayout(custom_form)
        layout.addWidget(custom_group)
        
    def create_activity_widget(self, activity, description, system):
        """Create a widget for a sensory activity"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: #F9F9F9;
                border-radius: 8px;
                padding: 10px;
                margin: 2px;
            }
        """)
        
        layout = QHBoxLayout(widget)
        
        # Activity info
        info_layout = QVBoxLayout()
        
        activity_label = QLabel(activity)
        activity_label.setStyleSheet("font-weight: 600; color: #333333;")
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 12px; color: #666666;")
        desc_label.setWordWrap(True)
        
        system_label = QLabel(f"System: {system}")
        system_label.setStyleSheet("font-size: 11px; color: #007AFF; font-style: italic;")
        
        info_layout.addWidget(activity_label)
        info_layout.addWidget(desc_label)
        info_layout.addWidget(system_label)
        
        layout.addLayout(info_layout, 1)
        
        # Completion checkbox
        completed_cb = QCheckBox("Completed")
        completed_cb.setStyleSheet("margin-left: 10px;")
        layout.addWidget(completed_cb)
        
        return widget
    
    def add_custom_activity(self):
        """Add a custom sensory activity"""
        activity = self.custom_activity.text()
        description = self.custom_description.text()
        time_period = self.custom_time.currentText()
        
        if activity and description:
            # In a real implementation, this would be added to the appropriate time group
            print(f"Adding custom activity: {activity} ({time_period})")
            
            # Clear fields
            self.custom_activity.clear()
            self.custom_description.clear()

class InteroceptionTrainer(AppleCard):
    """Body awareness and emotional recognition trainer"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup interoception training UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🧘 Body Awareness Trainer")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Interoception helps you notice signals from inside your body, like hunger, thirst, tiredness, and emotions.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666666; font-style: italic; margin-bottom: 15px;")
        layout.addWidget(desc)
        
        # Body scan exercise
        scan_group = QGroupBox("🔍 Body Scan Exercise")
        scan_layout = QVBoxLayout(scan_group)
        
        scan_instructions = QLabel("""
1. Sit comfortably and close your eyes
2. Notice your breathing without changing it
3. Starting from your toes, notice how each part feels
4. Move slowly up your body
5. Notice without judging - just observe
        """)
        scan_instructions.setStyleSheet("font-size: 12px; line-height: 1.4;")
        scan_layout.addWidget(scan_instructions)
        
        scan_timer_layout = QHBoxLayout()
        scan_timer_layout.addWidget(QLabel("Duration:"))
        
        self.scan_duration = QComboBox()
        self.scan_duration.addItems(["2 minutes", "5 minutes", "10 minutes", "15 minutes"])
        scan_timer_layout.addWidget(self.scan_duration)
        
        start_scan_btn = AppleButton("Start Body Scan")
        start_scan_btn.clicked.connect(self.start_body_scan)
        scan_timer_layout.addWidget(start_scan_btn)
        
        scan_layout.addLayout(scan_timer_layout)
        layout.addWidget(scan_group)
        
        # Emotion-body connection
        emotion_group = QGroupBox("💭 Emotion-Body Connection")
        emotion_layout = QVBoxLayout(emotion_group)
        
        emotion_layout.addWidget(QLabel("When you feel each emotion, where do you notice it in your body?"))
        
        emotions = ["Happy", "Sad", "Angry", "Worried", "Excited", "Calm"]
        self.emotion_body_map = {}
        
        for emotion in emotions:
            emotion_row = QHBoxLayout()
            emotion_row.addWidget(QLabel(f"{emotion}:"))
            
            body_location = QComboBox()
            body_location.addItems([
                "Select location...", "Head/Face", "Throat", "Chest", "Stomach", 
                "Arms", "Hands", "Back", "Legs", "Whole Body", "Don't Notice"
            ])
            
            self.emotion_body_map[emotion] = body_location
            emotion_row.addWidget(body_location)
            emotion_row.addStretch()
            
            emotion_layout.addLayout(emotion_row)
        
        layout.addWidget(emotion_group)
        
        # Daily check-in
        checkin_group = QGroupBox("📝 Daily Body Check-In")
        checkin_layout = QVBoxLayout(checkin_group)
        
        checkin_questions = [
            "How hungry am I right now?",
            "How thirsty am I?",
            "How tired/energetic am I?",
            "How tense/relaxed are my muscles?",
            "How fast/slow is my breathing?",
            "What emotion am I feeling?"
        ]
        
        self.checkin_responses = {}
        
        for question in checkin_questions:
            question_layout = QHBoxLayout()
            question_layout.addWidget(QLabel(question))
            
            response_slider = QSlider(Qt.Horizontal)
            response_slider.setRange(1, 10)
            response_slider.setValue(5)
            
            response_label = QLabel("5")
            response_slider.valueChanged.connect(lambda v, l=response_label: l.setText(str(v)))
            
            self.checkin_responses[question] = response_slider
            
            question_layout.addWidget(response_slider)
            question_layout.addWidget(response_label)
            
            checkin_layout.addLayout(question_layout)
        
        save_checkin_btn = AppleButton("Save Check-In")
        save_checkin_btn.clicked.connect(self.save_checkin)
        checkin_layout.addWidget(save_checkin_btn)
        
        layout.addWidget(checkin_group)
    
    def start_body_scan(self):
        """Start guided body scan exercise"""
        duration_text = self.scan_duration.currentText()
        minutes = int(duration_text.split()[0])
        
        # In a real implementation, this would start a guided audio/visual exercise
        print(f"Starting {minutes}-minute body scan")
        
        # Could integrate with text-to-speech or pre-recorded audio
    
    def save_checkin(self):
        """Save daily check-in responses"""
        responses = {}
        for question, slider in self.checkin_responses.items():
            responses[question] = slider.value()
        
        # Save with timestamp
        checkin_data = {
            'timestamp': datetime.now().isoformat(),
            'responses': responses
        }
        
        print(f"Saved check-in: {checkin_data}")

class SensoryToolkitWidget(QWidget):
    """Main sensory toolkit widget combining all tools"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main sensory toolkit UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("🎭 Sensory Processing Toolkit")
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
        
        # Sensory Profile tab
        profile_scroll = QScrollArea()
        profile_scroll.setWidgetResizable(True)
        profile_scroll.setFrameShape(QFrame.NoFrame)
        
        self.sensory_profile = SensoryProfileWidget()
        profile_scroll.setWidget(self.sensory_profile)
        
        self.tabs.addTab(profile_scroll, "Sensory Profile")
        
        # Sensory Diet tab
        diet_scroll = QScrollArea()
        diet_scroll.setWidgetResizable(True)
        diet_scroll.setFrameShape(QFrame.NoFrame)
        
        self.sensory_diet = SensoryDietPlanner()
        diet_scroll.setWidget(self.sensory_diet)
        
        self.tabs.addTab(diet_scroll, "Sensory Diet")
        
        # Interoception tab
        intero_scroll = QScrollArea()
        intero_scroll.setWidgetResizable(True)
        intero_scroll.setFrameShape(QFrame.NoFrame)
        
        self.interoception = InteroceptionTrainer()
        intero_scroll.setWidget(self.interoception)
        
        self.tabs.addTab(intero_scroll, "Body Awareness")
        
        layout.addWidget(self.tabs)