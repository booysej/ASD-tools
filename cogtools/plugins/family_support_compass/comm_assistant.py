from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt

class CommAssistantWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Literal-to-Empathetic Translator:"))
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Type a literal request...")
        layout.addWidget(self.input_line)
        self.translate_btn = QPushButton("Suggest Softer Wording")
        self.translate_btn.setStyleSheet("background: #4caf50; color: #fff; font-weight: bold; padding: 8px; border-radius: 6px;")
        layout.addWidget(self.translate_btn)
        self.output_text = QTextEdit()
        self.output_text.setPlaceholderText("Empathetic options will appear here.")
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)
        layout.addWidget(QLabel("Templates for Tricky Conversations (coming soon)"))
        layout.addWidget(QLabel("Conversation Journal (async reflection, coming soon)"))
        self.setLayout(layout)