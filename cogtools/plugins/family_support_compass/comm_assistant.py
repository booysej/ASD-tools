from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QTextEdit, QListWidget, 
                               QListWidgetItem, QTabWidget, QComboBox, QGroupBox,
                               QScrollArea, QFrame)
from PySide6.QtCore import Qt, Signal, QDateTime
from PySide6.QtGui import QFont
import json
import re

class TranslationSuggestions:
    """Predefined translation suggestions for common situations"""
    
    TRANSLATIONS = {
        # Direct -> Empathetic translations
        "clean your room": [
            "Would you mind tidying up your room when you have a chance?",
            "Your room could use some organizing - would you like help or prefer to do it yourself?",
            "I noticed your room is pretty messy. How about we work together to make it nice?"
        ],
        "do your homework": [
            "Would you like to work on your homework now, or would you prefer to take a break first?",
            "How are you feeling about your homework today? Need any help getting started?",
            "I'm here if you need help with your assignments - would you like to tackle them together?"
        ],
        "stop that": [
            "I'm feeling overwhelmed by that behavior - could you help me understand what's going on?",
            "That's making me uncomfortable. Can we talk about what you need right now?",
            "I'm having trouble with that. Can we find a different way to handle this?"
        ],
        "hurry up": [
            "We need to leave soon - how much more time do you need?",
            "I'm feeling a bit rushed. Can you help me understand your timeline?",
            "We're on a schedule today. What can I do to help you get ready?"
        ],
        "you're wrong": [
            "I see it differently. Can you help me understand your perspective?",
            "I'm not sure I agree. Could you explain your thinking?",
            "That's interesting - I hadn't thought of it that way. Tell me more."
        ],
        "don't be upset": [
            "I can see you're having big feelings right now. That's okay.",
            "Your feelings are valid. Would you like to talk about what's bothering you?",
            "I notice you're upset. How can I support you right now?"
        ],
        "calm down": [
            "Take your time. I'm here when you're ready.",
            "Would some quiet time help? I can wait with you.",
            "Big feelings are hard. What usually helps you feel better?"
        ],
        "that's not normal": [
            "Everyone does things differently, and that's okay.",
            "I'm curious about your approach - can you tell me more?",
            "We all have our own ways of handling things."
        ]
    }
    
    @classmethod
    def get_suggestions(cls, text):
        """Get empathetic suggestions for a given text"""
        text_lower = text.lower().strip()
        
        # Look for direct matches first
        if text_lower in cls.TRANSLATIONS:
            return cls.TRANSLATIONS[text_lower]
        
        # Look for partial matches
        for key, suggestions in cls.TRANSLATIONS.items():
            if key in text_lower:
                return suggestions
        
        # Generate generic suggestions based on common patterns
        if any(word in text_lower for word in ["should", "must", "have to", "need to"]):
            return [
                f"Would you be willing to {text_lower.replace('you should', '').replace('you must', '').replace('you have to', '').replace('you need to', '').strip()}?",
                f"How do you feel about {text_lower.replace('you should', '').replace('you must', '').replace('you have to', '').replace('you need to', '').strip()}?",
                f"I was thinking it might be helpful to {text_lower.replace('you should', '').replace('you must', '').replace('you have to', '').replace('you need to', '').strip()}. What do you think?"
            ]
        
        if any(word in text_lower for word in ["don't", "stop", "quit"]):
            return [
                "I'm having trouble with that behavior. Can we talk about what you need?",
                "I'd appreciate if we could try a different approach. What would work better for you?",
                "That's challenging for me. How can we solve this together?"
            ]
        
        # Default suggestions for general communication
        return [
            "Consider adding more emotional context to help them understand your feelings.",
            "Try asking about their perspective or feelings first.",
            "Maybe frame it as a request rather than a demand."
        ]

class ConversationTemplates(QWidget):
    """Widget showing conversation templates for difficult situations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup conversation templates UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("💬 Conversation Templates")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Template selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Situation:"))
        
        self.template_combo = QComboBox()
        self.template_combo.addItems([
            "Select a situation...",
            "Discussing meltdowns",
            "Setting boundaries", 
            "Talking about sensory needs",
            "Explaining social situations",
            "Planning changes/transitions",
            "Discussing therapy goals",
            "Dealing with school issues",
            "Explaining emotions"
        ])
        self.template_combo.currentTextChanged.connect(self.show_template)
        
        selector_layout.addWidget(self.template_combo)
        selector_layout.addStretch()
        
        layout.addLayout(selector_layout)
        
        # Template display
        self.template_display = QTextEdit()
        self.template_display.setReadOnly(True)
        self.template_display.setMaximumHeight(200)
        self.template_display.setStyleSheet("""
            QTextEdit {
                border: 1px solid #E5E5EA;
                border-radius: 8px;
                padding: 10px;
                background-color: #F9F9F9;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        layout.addWidget(self.template_display)
        
        # Tips
        tips_label = QLabel("💡 Tip: Adapt these templates to your family's communication style")
        tips_label.setStyleSheet("""
            font-size: 11px;
            color: #8E8E93;
            font-style: italic;
        """)
        layout.addWidget(tips_label)
        
    def show_template(self, situation):
        """Show the template for the selected situation"""
        templates = {
            "Discussing meltdowns": """
🗣️ APPROACHING MELTDOWN CONVERSATIONS:

Opening:
"I noticed you had a really hard time earlier. When you're ready, I'd love to understand what was going on for you."

Validating:
"It sounds like that was really overwhelming. Thank you for sharing that with me."

Problem-solving:
"What do you think would help if that happens again? Should we make a plan together?"

Closing:
"You're not in trouble for having big feelings. I'm proud of you for talking with me about it."
            """,
            
            "Setting boundaries": """
🚧 SETTING LOVING BOUNDARIES:

Starting point:
"I want to make sure we both feel safe and respected. Can we talk about some guidelines?"

Explaining the need:
"When [behavior], I feel [emotion] because [reason]. I need [boundary] to feel okay."

Collaborative approach:
"What would help you remember this boundary? How can we make this work for both of us?"

Follow-up:
"Let's check in about how this is working in a few days."
            """,
            
            "Talking about sensory needs": """
🎵 SENSORY NEEDS CONVERSATION:

Discovery:
"I've noticed you seem uncomfortable in [situation]. Can you tell me what you're experiencing?"

Validation:
"That sounds really intense. Thank you for explaining that to me."

Solution-seeking:
"What helps you feel better when that happens? Should we get some tools or make changes?"

Planning:
"Let's practice what you can do or say when you need sensory support."
            """,
            
            "Explaining social situations": """
👥 SOCIAL SITUATION PREP:

Setting expectations:
"We're going to [event]. Here's what usually happens there..."

Preparing for challenges:
"Sometimes people might [behavior]. That's just how they communicate - it's not about you."

Creating safety plans:
"If you feel overwhelmed, you can [exit strategy]. I'll be watching for your signal."

Post-event processing:
"How did that go for you? What worked well? What was challenging?"
            """
        }
        
        if situation in templates:
            self.template_display.setText(templates[situation])
        else:
            self.template_display.clear()

class CommAssistantWidget(QWidget):
    """Enhanced communication assistant for ASD families"""
    
    def __init__(self):
        super().__init__()
        self.conversation_history = []
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the communication assistant UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("🗣️ Communication Assistant")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #1C1C1E;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
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
        
        # Translation tab
        translation_widget = QWidget()
        translation_layout = QVBoxLayout(translation_widget)
        translation_layout.setContentsMargins(15, 15, 15, 15)
        translation_layout.setSpacing(15)
        
        # Input section
        input_group = QGroupBox("Literal-to-Empathetic Translator")
        input_layout = QVBoxLayout(input_group)
        
        input_layout.addWidget(QLabel("Enter what you want to say:"))
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("e.g., 'Clean your room' or 'Do your homework'")
        self.input_line.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #E5E5EA;
                border-radius: 6px;
                font-size: 14px;
            }
        """)
        self.input_line.returnPressed.connect(self.translate_text)
        input_layout.addWidget(self.input_line)
        
        self.translate_btn = QPushButton("Get Empathetic Suggestions")
        self.translate_btn.clicked.connect(self.translate_text)
        self.translate_btn.setStyleSheet("""
            QPushButton {
                background-color: #34C759;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #28A745;
            }
        """)
        input_layout.addWidget(self.translate_btn)
        
        translation_layout.addWidget(input_group)
        
        # Output section
        output_group = QGroupBox("Suggested Rephrasing")
        output_layout = QVBoxLayout(output_group)
        
        self.output_text = QTextEdit()
        self.output_text.setPlaceholderText("Empathetic suggestions will appear here...")
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(150)
        self.output_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #E5E5EA;
                border-radius: 6px;
                padding: 10px;
                background-color: #F9F9F9;
                font-size: 12px;
            }
        """)
        output_layout.addWidget(self.output_text)
        
        translation_layout.addWidget(output_group)
        
        # Quick examples
        examples_group = QGroupBox("Quick Examples")
        examples_layout = QVBoxLayout(examples_group)
        
        examples_list = QListWidget()
        examples_list.setMaximumHeight(120)
        examples_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #E5E5EA;
                border-radius: 6px;
                background-color: white;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #F2F2F7;
            }
            QListWidget::item:hover {
                background-color: #F2F2F7;
            }
        """)
        
        example_phrases = [
            "clean your room → Would you mind tidying up your room?",
            "hurry up → We need to leave soon - how much more time do you need?",
            "calm down → Take your time. I'm here when you're ready.",
            "stop that → I'm feeling overwhelmed - can we talk about what's going on?"
        ]
        
        for example in example_phrases:
            item = QListWidgetItem(example)
            examples_list.addItem(item)
        
        examples_list.itemClicked.connect(self.use_example)
        examples_layout.addWidget(examples_list)
        
        translation_layout.addWidget(examples_group)
        translation_layout.addStretch()
        
        self.tabs.addTab(translation_widget, "Translation")
        
        # Templates tab
        templates_scroll = QScrollArea()
        templates_scroll.setWidgetResizable(True)
        templates_scroll.setFrameShape(QFrame.NoFrame)
        
        self.templates_widget = ConversationTemplates()
        templates_scroll.setWidget(self.templates_widget)
        
        self.tabs.addTab(templates_scroll, "Templates")
        
        # Communication tips tab
        tips_widget = QWidget()
        tips_layout = QVBoxLayout(tips_widget)
        tips_layout.setContentsMargins(15, 15, 15, 15)
        
        tips_content = QTextEdit()
        tips_content.setReadOnly(True)
        tips_content.setHtml("""
        <h3>🎯 Communication Strategies for ASD Families</h3>
        
        <h4>💙 Building Connection:</h4>
        <ul>
            <li>Use "I" statements to express your feelings</li>
            <li>Validate their experience before problem-solving</li>
            <li>Ask about their perspective and listen actively</li>
            <li>Acknowledge their efforts and progress</li>
        </ul>
        
        <h4>🧠 Processing Differences:</h4>
        <ul>
            <li>Allow extra time for processing information</li>
            <li>Use concrete, specific language</li>
            <li>Break complex instructions into steps</li>
            <li>Provide visual supports when helpful</li>
        </ul>
        
        <h4>😟 During Difficult Moments:</h4>
        <ul>
            <li>Stay calm and regulate your own emotions first</li>
            <li>Reduce sensory input (lower voice, dim lights)</li>
            <li>Offer choices rather than demands</li>
            <li>Focus on safety and connection over compliance</li>
        </ul>
        
        <h4>🎉 Celebrating Success:</h4>
        <ul>
            <li>Notice and acknowledge small improvements</li>
            <li>Be specific about what they did well</li>
            <li>Celebrate effort as much as outcomes</li>
            <li>Build on their strengths and interests</li>
        </ul>
        """)
        
        tips_content.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: white;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        
        tips_layout.addWidget(tips_content)
        
        self.tabs.addTab(tips_widget, "Tips & Strategies")
        
        layout.addWidget(self.tabs)
    
    def translate_text(self):
        """Translate the input text to more empathetic versions"""
        input_text = self.input_line.text().strip()
        if not input_text:
            self.output_text.setText("Please enter some text to translate.")
            return
        
        suggestions = TranslationSuggestions.get_suggestions(input_text)
        
        # Format the output
        output = f"Original: \"{input_text}\"\n\n"
        output += "Empathetic alternatives:\n\n"
        
        for i, suggestion in enumerate(suggestions, 1):
            output += f"{i}. {suggestion}\n\n"
        
        output += "💡 Remember: Choose the approach that feels most natural for your family!"
        
        self.output_text.setText(output)
        
        # Save to conversation history
        self.conversation_history.append({
            'original': input_text,
            'suggestions': suggestions,
            'timestamp': str(QDateTime.currentDateTime().toString())
        })
    
    def use_example(self, item):
        """Use a clicked example in the input field"""
        example_text = item.text()
        original = example_text.split(" → ")[0]
        self.input_line.setText(original)
        self.translate_text()