"""
Social Skills Trainer - Evidence-based social communication support for ASD
Based on Theory of Mind research, PEERS intervention, and social thinking curricula
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QComboBox, QTextEdit, QScrollArea,
                               QGroupBox, QCheckBox, QGridLayout, QFrame,
                               QButtonGroup, QRadioButton, QSlider, QTabWidget,
                               QListWidget, QListWidgetItem, QDialog, QDialogButtonBox)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from cogtools.core.widgets import AppleCard, AppleButton, AppleTextField
import json
from datetime import datetime

class SocialStoryCreator(AppleCard):
    """Create personalized social stories based on research evidence"""
    
    story_created = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_story = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup social story creator UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("📖 Social Story Creator")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Social stories help prepare for social situations by describing what will happen and how to respond appropriately.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666666; font-style: italic; margin-bottom: 15px;")
        layout.addWidget(desc)
        
        # Story type selection
        type_group = QGroupBox("📚 Story Type")
        type_layout = QVBoxLayout(type_group)
        
        self.story_type = QComboBox()
        self.story_type.addItems([
            "Select situation...",
            "Going to a restaurant",
            "Meeting new people",
            "Birthday parties",
            "Doctor's appointments",
            "School presentations",
            "Group work projects",
            "Unexpected changes in plans",
            "Dealing with frustration",
            "Making mistakes",
            "Asking for help",
            "Custom situation"
        ])
        self.story_type.currentTextChanged.connect(self.load_story_template)
        type_layout.addWidget(self.story_type)
        
        layout.addWidget(type_group)
        
        # Story elements (based on Carol Gray's Social Story formula)
        elements_group = QGroupBox("📝 Story Elements")
        elements_layout = QVBoxLayout(elements_group)
        
        # Title
        elements_layout.addWidget(QLabel("Story Title:"))
        self.story_title = AppleTextField("My Social Story")
        elements_layout.addWidget(self.story_title)
        
        # Descriptive sentences (what happens)
        elements_layout.addWidget(QLabel("What happens? (Descriptive sentences)"))
        self.descriptive_text = QTextEdit()
        self.descriptive_text.setMaximumHeight(80)
        self.descriptive_text.setPlaceholderText("Describe the situation objectively...")
        elements_layout.addWidget(self.descriptive_text)
        
        # Perspective sentences (what others think/feel)
        elements_layout.addWidget(QLabel("What do others think/feel? (Perspective sentences)"))
        self.perspective_text = QTextEdit()
        self.perspective_text.setMaximumHeight(80)
        self.perspective_text.setPlaceholderText("Explain others' thoughts and feelings...")
        elements_layout.addWidget(self.perspective_text)
        
        # Directive sentences (what to do)
        elements_layout.addWidget(QLabel("What should I do? (Directive sentences)"))
        self.directive_text = QTextEdit()
        self.directive_text.setMaximumHeight(80)
        self.directive_text.setPlaceholderText("Specific actions and responses...")
        elements_layout.addWidget(self.directive_text)
        
        # Control sentences (strategies for staying calm)
        elements_layout.addWidget(QLabel("How can I stay calm? (Control sentences)"))
        self.control_text = QTextEdit()
        self.control_text.setMaximumHeight(60)
        self.control_text.setPlaceholderText("Coping strategies and reminders...")
        elements_layout.addWidget(self.control_text)
        
        layout.addWidget(elements_group)
        
        # Generate story button
        generate_btn = AppleButton("Generate Complete Story")
        generate_btn.clicked.connect(self.generate_story)
        layout.addWidget(generate_btn)
        
        # Preview area
        preview_group = QGroupBox("👀 Story Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.story_preview = QTextEdit()
        self.story_preview.setReadOnly(True)
        self.story_preview.setMaximumHeight(200)
        self.story_preview.setPlaceholderText("Your complete social story will appear here...")
        preview_layout.addWidget(self.story_preview)
        
        # Save story button
        save_btn = AppleButton("Save Story")
        save_btn.clicked.connect(self.save_story)
        preview_layout.addWidget(save_btn)
        
        layout.addWidget(preview_group)
    
    def load_story_template(self, story_type):
        """Load template content for different story types"""
        templates = {
            "Going to a restaurant": {
                "title": "Going to a Restaurant",
                "descriptive": "When I go to a restaurant, I will sit at a table with my family. A server will come to take our order. There will be other people eating and talking around us.",
                "perspective": "The server wants to help us have a good meal. Other customers want to enjoy their food in a peaceful environment. My family wants us to have a nice time together.",
                "directive": "I will sit in my chair and speak in a quiet voice. I will say 'please' and 'thank you' to the server. I will stay at the table until everyone is finished eating.",
                "control": "If it gets too noisy, I can ask to sit in a quieter spot. I can take deep breaths if I feel overwhelmed. I can tell my family if I need a break."
            },
            "Meeting new people": {
                "title": "Meeting New People",
                "descriptive": "Sometimes I will meet people I don't know yet. This might happen at school, at family gatherings, or in my neighborhood. New people might want to talk to me.",
                "perspective": "New people are usually friendly and want to get to know me. They might be curious about my interests. They want to have a nice conversation.",
                "directive": "I can say 'Hello, my name is...' and tell them my name. I can ask them their name. I can share one thing I like to do. I can listen when they talk about themselves.",
                "control": "It's okay if I feel nervous - that's normal. I can take my time to think before I speak. If I need a break, I can politely excuse myself."
            },
            "Birthday parties": {
                "title": "Going to a Birthday Party",
                "descriptive": "At a birthday party, there will be decorations, music, and other children. We will sing 'Happy Birthday' and watch the birthday child blow out candles. There might be games and cake.",
                "perspective": "The birthday child feels special and happy. Other guests want to celebrate and have fun. The host family wants everyone to enjoy the party.",
                "directive": "I will bring or give a gift to the birthday child. I will participate in singing 'Happy Birthday.' I can join in games if I want to, or watch if I prefer.",
                "control": "If the music is too loud, I can move to a quieter area. I can take breaks if I need them. I can ask a parent for help if I feel overwhelmed."
            }
        }
        
        if story_type in templates:
            template = templates[story_type]
            self.story_title.setText(template["title"])
            self.descriptive_text.setPlainText(template["descriptive"])
            self.perspective_text.setPlainText(template["perspective"])
            self.directive_text.setPlainText(template["directive"])
            self.control_text.setPlainText(template["control"])
    
    def generate_story(self):
        """Generate the complete social story"""
        title = self.story_title.text()
        descriptive = self.descriptive_text.toPlainText()
        perspective = self.perspective_text.toPlainText()
        directive = self.directive_text.toPlainText()
        control = self.control_text.toPlainText()
        
        if not all([title, descriptive, directive]):
            self.story_preview.setText("Please fill in at least the title, descriptive, and directive sections.")
            return
        
        # Format the complete story
        story_text = f"""
🌟 {title} 🌟

📋 What happens:
{descriptive}

💭 What others think and feel:
{perspective}

✅ What I should do:
{directive}

🧘 How I can stay calm:
{control}

Remember: I can always ask for help if I need it. Every social situation is a chance to practice and learn! 🌈
        """
        
        self.story_preview.setText(story_text.strip())
        
        self.current_story = {
            'title': title,
            'descriptive': descriptive,
            'perspective': perspective,
            'directive': directive,
            'control': control,
            'full_text': story_text.strip(),
            'created_date': datetime.now().isoformat()
        }
    
    def save_story(self):
        """Save the current story"""
        if self.current_story:
            self.story_created.emit(self.current_story)
            self.story_preview.append("\n\n✅ Story saved successfully!")

class TheoryOfMindTrainer(AppleCard):
    """Theory of Mind exercises based on research by Baron-Cohen and others"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_level = 1
        self.setup_ui()
        
    def setup_ui(self):
        """Setup Theory of Mind trainer UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🧠 Theory of Mind Trainer")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Theory of Mind is understanding that other people have thoughts, feelings, and beliefs that may be different from your own.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666666; font-style: italic; margin-bottom: 15px;")
        layout.addWidget(desc)
        
        # Level selection
        level_group = QGroupBox("📚 Training Level")
        level_layout = QHBoxLayout(level_group)
        
        level_layout.addWidget(QLabel("Current Level:"))
        self.level_selector = QComboBox()
        self.level_selector.addItems([
            "Level 1: Basic Emotions",
            "Level 2: Wants and Preferences", 
            "Level 3: Beliefs and Knowledge",
            "Level 4: False Beliefs",
            "Level 5: Complex Emotions",
            "Level 6: Social Situations"
        ])
        self.level_selector.currentIndexChanged.connect(self.change_level)
        level_layout.addWidget(self.level_selector)
        level_layout.addStretch()
        
        layout.addWidget(level_group)
        
        # Exercise area
        self.exercise_group = QGroupBox("🎯 Current Exercise")
        self.exercise_layout = QVBoxLayout(self.exercise_group)
        
        self.load_level_exercises(1)
        
        layout.addWidget(self.exercise_group)
        
        # Progress tracking
        progress_group = QGroupBox("📊 Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_text = QLabel("Complete exercises to track your progress!")
        self.progress_text.setStyleSheet("color: #666666;")
        progress_layout.addWidget(self.progress_text)
        
        layout.addWidget(progress_group)
    
    def change_level(self, index):
        """Change the current training level"""
        self.current_level = index + 1
        self.load_level_exercises(self.current_level)
    
    def load_level_exercises(self, level):
        """Load exercises for the specified level"""
        # Clear existing exercises
        for i in reversed(range(self.exercise_layout.count())):
            child = self.exercise_layout.itemAt(i).widget()
            if child:
                child.deleteLater()
        
        if level == 1:  # Basic Emotions
            self.create_emotion_recognition_exercise()
        elif level == 2:  # Wants and Preferences
            self.create_wants_exercise()
        elif level == 3:  # Beliefs and Knowledge
            self.create_knowledge_exercise()
        elif level == 4:  # False Beliefs
            self.create_false_belief_exercise()
        elif level == 5:  # Complex Emotions
            self.create_complex_emotion_exercise()
        elif level == 6:  # Social Situations
            self.create_social_situation_exercise()
    
    def create_emotion_recognition_exercise(self):
        """Level 1: Basic emotion recognition"""
        self.exercise_layout.addWidget(QLabel("👀 Look at the situation and identify the emotion:"))
        
        scenario = QLabel("""
Scenario: Emma's ice cream fell on the ground.
Her ice cream is now dirty and she can't eat it.

How do you think Emma feels?
        """)
        scenario.setStyleSheet("background-color: #F9F9F9; padding: 10px; border-radius: 8px; margin: 10px 0;")
        self.exercise_layout.addWidget(scenario)
        
        # Answer choices
        self.emotion_choices = QButtonGroup()
        emotions = ["😊 Happy", "😢 Sad", "😠 Angry", "😨 Scared"]
        
        for i, emotion in enumerate(emotions):
            radio = QRadioButton(emotion)
            self.emotion_choices.addButton(radio, i)
            self.exercise_layout.addWidget(radio)
        
        check_btn = AppleButton("Check Answer")
        check_btn.clicked.connect(lambda: self.check_emotion_answer(1))  # Correct answer is Sad (index 1)
        self.exercise_layout.addWidget(check_btn)
        
        self.feedback_label = QLabel("")
        self.exercise_layout.addWidget(self.feedback_label)
    
    def create_wants_exercise(self):
        """Level 2: Understanding wants and preferences"""
        self.exercise_layout.addWidget(QLabel("🎯 Understanding what others want:"))
        
        scenario = QLabel("""
Scenario: Jake is looking at a menu at a restaurant.
He says "I really don't like spicy food. It makes my mouth hurt."
The waiter asks what he wants to order.

What do you think Jake wants?
        """)
        scenario.setStyleSheet("background-color: #F9F9F9; padding: 10px; border-radius: 8px; margin: 10px 0;")
        self.exercise_layout.addWidget(scenario)
        
        self.wants_choices = QButtonGroup()
        choices = [
            "🌶️ The spiciest dish on the menu",
            "🥗 Something mild and not spicy",
            "🍔 Whatever the waiter recommends",
            "🚫 Nothing at all"
        ]
        
        for i, choice in enumerate(choices):
            radio = QRadioButton(choice)
            self.wants_choices.addButton(radio, i)
            self.exercise_layout.addWidget(radio)
        
        check_btn = AppleButton("Check Answer")
        check_btn.clicked.connect(lambda: self.check_wants_answer(1))  # Correct answer is mild food
        self.exercise_layout.addWidget(check_btn)
        
        self.wants_feedback = QLabel("")
        self.exercise_layout.addWidget(self.wants_feedback)
    
    def create_false_belief_exercise(self):
        """Level 4: Classic false belief task (Sally-Anne type)"""
        self.exercise_layout.addWidget(QLabel("🎭 Understanding false beliefs:"))
        
        scenario = QLabel("""
Scenario: Sarah puts her sandwich in the red box for lunch.
Then Sarah goes outside to play.
While she's outside, Mom moves the sandwich to the blue box to keep it fresh.
Sarah doesn't see Mom move the sandwich.
Now Sarah comes back inside for lunch.

Where will Sarah look for her sandwich?
        """)
        scenario.setStyleSheet("background-color: #F9F9F9; padding: 10px; border-radius: 8px; margin: 10px 0;")
        self.exercise_layout.addWidget(scenario)
        
        self.belief_choices = QButtonGroup()
        choices = [
            "📦 In the red box (where she put it)",
            "📦 In the blue box (where it really is)",
            "🤷 She won't know where to look",
            "👩 She'll ask Mom where it is"
        ]
        
        for i, choice in enumerate(choices):
            radio = QRadioButton(choice)
            self.belief_choices.addButton(radio, i)
            self.exercise_layout.addWidget(radio)
        
        check_btn = AppleButton("Check Answer")
        check_btn.clicked.connect(lambda: self.check_belief_answer(0))  # Correct: red box
        self.exercise_layout.addWidget(check_btn)
        
        self.belief_feedback = QLabel("")
        self.exercise_layout.addWidget(self.belief_feedback)
    
    def create_complex_emotion_exercise(self):
        """Level 5: Complex emotions like embarrassment, pride"""
        self.exercise_layout.addWidget(QLabel("🎭 Understanding complex emotions:"))
        
        scenario = QLabel("""
Scenario: During class presentation, Alex's pants ripped when he stood up.
Everyone in the class started laughing.
Alex quickly sat back down and covered the rip with his notebook.
His face turned red and he looked down at his desk.

What is Alex most likely feeling?
        """)
        scenario.setStyleSheet("background-color: #F9F9F9; padding: 10px; border-radius: 8px; margin: 10px 0;")
        self.exercise_layout.addWidget(scenario)
        
        self.complex_choices = QButtonGroup()
        choices = [
            "😊 Proud of his presentation",
            "😳 Embarrassed about what happened",
            "😠 Angry at his classmates",
            "😴 Tired from standing up"
        ]
        
        for i, choice in enumerate(choices):
            radio = QRadioButton(choice)
            self.complex_choices.addButton(radio, i)
            self.exercise_layout.addWidget(radio)
        
        check_btn = AppleButton("Check Answer")
        check_btn.clicked.connect(lambda: self.check_complex_answer(1))  # Correct: embarrassed
        self.exercise_layout.addWidget(check_btn)
        
        self.complex_feedback = QLabel("")
        self.exercise_layout.addWidget(self.complex_feedback)
    
    def create_social_situation_exercise(self):
        """Level 6: Complex social situations"""
        self.exercise_layout.addWidget(QLabel("👥 Understanding social situations:"))
        
        scenario = QLabel("""
Scenario: Maria invited her friends to her birthday party.
She told them the party starts at 2 PM.
It's now 2:30 PM and only one friend has arrived.
Maria keeps looking out the window and checking her phone.

Why might Maria be feeling worried?
        """)
        scenario.setStyleSheet("background-color: #F9F9F9; padding: 10px; border-radius: 8px; margin: 10px 0;")
        self.exercise_layout.addWidget(scenario)
        
        self.social_choices = QButtonGroup()
        choices = [
            "🎂 She's worried the cake will get stale",
            "👥 She's worried her friends forgot or don't want to come",
            "⏰ She's worried about the time",
            "🎁 She's worried about her presents"
        ]
        
        for i, choice in enumerate(choices):
            radio = QRadioButton(choice)
            self.social_choices.addButton(radio, i)
            self.exercise_layout.addWidget(radio)
        
        check_btn = AppleButton("Check Answer")
        check_btn.clicked.connect(lambda: self.check_social_answer(1))  # Correct: friends forgot
        self.exercise_layout.addWidget(check_btn)
        
        self.social_feedback = QLabel("")
        self.exercise_layout.addWidget(self.social_feedback)
    
    def check_emotion_answer(self, correct_index):
        """Check the emotion recognition answer"""
        selected = self.emotion_choices.checkedId()
        if selected == correct_index:
            self.feedback_label.setText("✅ Correct! Emma would feel sad because she lost her ice cream.")
            self.feedback_label.setStyleSheet("color: #34C759; font-weight: 600;")
        else:
            self.feedback_label.setText("❌ Not quite. Think about how you would feel if you lost something you wanted.")
            self.feedback_label.setStyleSheet("color: #FF3B30; font-weight: 600;")
    
    def check_wants_answer(self, correct_index):
        """Check the wants/preferences answer"""
        selected = self.wants_choices.checkedId()
        if selected == correct_index:
            self.wants_feedback.setText("✅ Correct! Jake wants something mild because he doesn't like spicy food.")
            self.wants_feedback.setStyleSheet("color: #34C759; font-weight: 600;")
        else:
            self.wants_feedback.setText("❌ Remember: Jake said he doesn't like spicy food and it hurts his mouth.")
            self.wants_feedback.setStyleSheet("color: #FF3B30; font-weight: 600;")
    
    def check_belief_answer(self, correct_index):
        """Check the false belief answer"""
        selected = self.belief_choices.checkedId()
        if selected == correct_index:
            self.belief_feedback.setText("✅ Correct! Sarah will look in the red box because that's where she thinks it is.")
            self.belief_feedback.setStyleSheet("color: #34C759; font-weight: 600;")
        else:
            self.belief_feedback.setText("❌ Remember: Sarah doesn't know Mom moved it. She still thinks it's where she left it.")
            self.belief_feedback.setStyleSheet("color: #FF3B30; font-weight: 600;")
    
    def check_complex_answer(self, correct_index):
        """Check the complex emotion answer"""
        selected = self.complex_choices.checkedId()
        if selected == correct_index:
            self.complex_feedback.setText("✅ Correct! Alex feels embarrassed because everyone saw what happened.")
            self.complex_feedback.setStyleSheet("color: #34C759; font-weight: 600;")
        else:
            self.complex_feedback.setText("❌ Think about how you would feel if everyone laughed at something that happened to you.")
            self.complex_feedback.setStyleSheet("color: #FF3B30; font-weight: 600;")
    
    def check_social_answer(self, correct_index):
        """Check the social situation answer"""
        selected = self.social_choices.checkedId()
        if selected == correct_index:
            self.social_feedback.setText("✅ Correct! Maria is worried her friends might have forgotten about her party.")
            self.social_feedback.setStyleSheet("color: #34C759; font-weight: 600;")
        else:
            self.social_feedback.setText("❌ Think about why someone would keep looking out the window when friends are late.")
            self.social_feedback.setStyleSheet("color: #FF3B30; font-weight: 600;")

class ConversationPractice(AppleCard):
    """Practice conversation skills with guided scenarios"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup conversation practice UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("💬 Conversation Practice")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Scenario selection
        scenario_group = QGroupBox("🎭 Practice Scenario")
        scenario_layout = QVBoxLayout(scenario_group)
        
        self.scenario_selector = QComboBox()
        self.scenario_selector.addItems([
            "Select a scenario...",
            "Starting a conversation with a classmate",
            "Asking for help from a teacher",
            "Joining a group conversation",
            "Making plans with a friend",
            "Disagreeing politely",
            "Ending a conversation gracefully"
        ])
        self.scenario_selector.currentTextChanged.connect(self.load_scenario)
        scenario_layout.addWidget(self.scenario_selector)
        
        layout.addWidget(scenario_group)
        
        # Conversation display
        self.conversation_display = QTextEdit()
        self.conversation_display.setReadOnly(True)
        self.conversation_display.setMaximumHeight(300)
        self.conversation_display.setPlaceholderText("Select a scenario to begin practicing...")
        layout.addWidget(self.conversation_display)
        
        # Response options
        response_group = QGroupBox("💭 Your Response")
        response_layout = QVBoxLayout(response_group)
        
        self.response_buttons = QButtonGroup()
        self.response_widgets = []
        
        response_layout.addWidget(QLabel("What would you say?"))
        
        layout.addWidget(response_group)
        self.response_group = response_group
        
        # Practice tips
        tips_group = QGroupBox("💡 Conversation Tips")
        tips_layout = QVBoxLayout(tips_group)
        
        tips_text = QLabel("""
🎯 Good conversation skills:
• Make eye contact (or look near the person's face)
• Take turns talking and listening
• Ask questions to show interest
• Stay on topic or smoothly change topics
• Use appropriate volume and tone
• Give compliments when genuine
• Respect personal space
        """)
        tips_text.setStyleSheet("font-size: 12px; line-height: 1.4;")
        tips_layout.addWidget(tips_text)
        
        layout.addWidget(tips_group)
    
    def load_scenario(self, scenario_name):
        """Load a conversation scenario"""
        scenarios = {
            "Starting a conversation with a classmate": {
                "setup": "You want to talk to Sam, who sits near you in math class. Sam is putting books in their locker.",
                "conversation": "Sam: *organizing books*\n\nYou: ???",
                "responses": [
                    ("Hi Sam! How did you find today's math test?", "Good - shows interest in shared experience"),
                    ("Hey, nice backpack! Where did you get it?", "Good - genuine compliment starts conversation"),
                    ("Sam! Come here right now!", "Not good - too demanding and abrupt"),
                    ("*stare without saying anything*", "Not good - need to use words to start conversation")
                ]
            },
            "Asking for help from a teacher": {
                "setup": "You're confused about the homework assignment in English class. You need to ask your teacher, Ms. Johnson, for help.",
                "conversation": "Ms. Johnson: *grading papers at her desk*\n\nYou: ???",
                "responses": [
                    ("Excuse me, Ms. Johnson. Could you help me understand question 3?", "Excellent - polite and specific"),
                    ("Hey! I don't get this homework!", "Not good - too loud and demanding"),
                    ("Ms. Johnson, when you have a moment, could I ask about the homework?", "Good - respectful of teacher's time"),
                    ("This homework is stupid and makes no sense!", "Not good - rude and not helpful")
                ]
            },
            "Joining a group conversation": {
                "setup": "Three classmates are talking about weekend plans near your desk. You'd like to join the conversation.",
                "conversation": "Alex: I'm thinking of going to the new movie.\nJordan: Oh, which one? I love superhero movies!\nTaylor: Me too! I heard it's really good.\n\nYou: ???",
                "responses": [
                    ("Excuse me, are you talking about the new superhero movie? I'd love to see it too!", "Great - polite entry and relevant"),
                    ("That movie is terrible! You shouldn't watch it!", "Not good - negative and dismissive"),
                    ("Can I join your conversation? I like movies too.", "Good - direct and honest approach"),
                    ("*interrupt loudly* I LOVE SUPERHERO MOVIES!", "Not good - too loud and interrupts")
                ]
            }
        }
        
        if scenario_name in scenarios:
            scenario = scenarios[scenario_name]
            
            # Display scenario setup and conversation
            display_text = f"🎬 Scenario: {scenario['setup']}\n\n"
            display_text += f"💬 Conversation:\n{scenario['conversation']}"
            self.conversation_display.setText(display_text)
            
            # Clear previous response buttons
            for widget in self.response_widgets:
                widget.deleteLater()
            self.response_widgets.clear()
            
            # Add new response options
            response_layout = self.response_group.layout()
            
            for i, (response, feedback) in enumerate(scenario['responses']):
                response_widget = QFrame()
                response_widget.setStyleSheet("""
                    QFrame {
                        background-color: #F9F9F9;
                        border-radius: 8px;
                        padding: 10px;
                        margin: 2px;
                    }
                    QFrame:hover {
                        background-color: #F0F0F0;
                    }
                """)
                
                widget_layout = QVBoxLayout(response_widget)
                
                response_btn = QPushButton(f"Option {i+1}: {response}")
                response_btn.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding: 8px;
                        border: none;
                        background: transparent;
                        font-weight: 600;
                    }
                """)
                response_btn.clicked.connect(lambda checked, f=feedback: self.show_feedback(f))
                
                widget_layout.addWidget(response_btn)
                response_layout.addWidget(response_widget)
                self.response_widgets.append(response_widget)
        else:
            self.conversation_display.clear()
            # Clear response options
            for widget in self.response_widgets:
                widget.deleteLater()
            self.response_widgets.clear()
    
    def show_feedback(self, feedback):
        """Show feedback for the selected response"""
        current_text = self.conversation_display.toPlainText()
        self.conversation_display.setText(current_text + f"\n\n💡 Feedback: {feedback}")

class SocialSkillsTrainerWidget(QWidget):
    """Main social skills trainer combining all tools"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main social skills trainer UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("🤝 Social Skills Trainer")
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
        
        # Social Stories tab
        stories_scroll = QScrollArea()
        stories_scroll.setWidgetResizable(True)
        stories_scroll.setFrameShape(QFrame.NoFrame)
        
        self.social_stories = SocialStoryCreator()
        stories_scroll.setWidget(self.social_stories)
        
        self.tabs.addTab(stories_scroll, "Social Stories")
        
        # Theory of Mind tab
        tom_scroll = QScrollArea()
        tom_scroll.setWidgetResizable(True)
        tom_scroll.setFrameShape(QFrame.NoFrame)
        
        self.theory_of_mind = TheoryOfMindTrainer()
        tom_scroll.setWidget(self.theory_of_mind)
        
        self.tabs.addTab(tom_scroll, "Theory of Mind")
        
        # Conversation Practice tab
        conv_scroll = QScrollArea()
        conv_scroll.setWidgetResizable(True)
        conv_scroll.setFrameShape(QFrame.NoFrame)
        
        self.conversation_practice = ConversationPractice()
        conv_scroll.setWidget(self.conversation_practice)
        
        self.tabs.addTab(conv_scroll, "Conversation Practice")
        
        layout.addWidget(self.tabs)