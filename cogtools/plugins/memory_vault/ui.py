from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QListWidget, QListWidgetItem, QTextEdit,
                               QSplitter, QFrame, QPushButton, QMenu,
                               QLineEdit, QToolBar, QComboBox)
from PySide6.QtCore import Qt, Signal, QDateTime, QTimer
from PySide6.QtGui import QIcon, QTextCharFormat, QFont, QAction
from cogtools.core.widgets import (AppleCard, AppleButton, AppleTextField, 
                                   AppleTextArea, AppleSegmentedControl,
                                   AppleNotification)
from cogtools.core.theme import AppleColors, AppleTheme
import json
import os
from datetime import datetime

class MemoryItem(QListWidgetItem):
    """Memory vault list item"""
    
    def __init__(self, memory_data):
        super().__init__()
        self.memory_data = memory_data
        self.update_display()
        
    def update_display(self):
        """Update the item display"""
        title = self.memory_data.get('title', 'Untitled')
        date = self.memory_data.get('date', '')
        category = self.memory_data.get('category', 'General')
        
        # Format display text
        display_text = f"{title}\n{category} • {date}"
        self.setText(title)
        
        # Set data for sorting
        self.setData(Qt.UserRole, self.memory_data)

class MemoryEditor(QWidget):
    """Rich text editor for memories"""
    
    content_changed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the editor UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setStyleSheet(f"""
            QToolBar {{
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                border: none;
                border-bottom: 1px solid {AppleColors.LIGHT_SEPARATOR.name()};
                padding: 4px;
            }}
            QToolButton {{
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                margin: 0px 2px;
            }}
            QToolButton:hover {{
                background-color: rgba(0, 122, 255, 0.1);
            }}
            QToolButton:pressed {{
                background-color: rgba(0, 122, 255, 0.2);
            }}
        """)
        
        # Text formatting actions
        bold_action = QAction("B", self)
        bold_action.setCheckable(True)
        bold_action.triggered.connect(lambda: self.format_text('bold'))
        toolbar.addAction(bold_action)
        
        italic_action = QAction("I", self)
        italic_action.setCheckable(True)
        italic_action.triggered.connect(lambda: self.format_text('italic'))
        toolbar.addAction(italic_action)
        
        underline_action = QAction("U", self)
        underline_action.setCheckable(True)
        underline_action.triggered.connect(lambda: self.format_text('underline'))
        toolbar.addAction(underline_action)
        
        toolbar.addSeparator()
        
        # Font size
        self.font_size = QComboBox()
        self.font_size.addItems(['12', '14', '16', '18', '20', '24'])
        self.font_size.setCurrentText('14')
        self.font_size.currentTextChanged.connect(self.change_font_size)
        toolbar.addWidget(self.font_size)
        
        layout.addWidget(toolbar)
        
        # Text editor
        self.editor = QTextEdit()
        self.editor.setStyleSheet(f"""
            QTextEdit {{
                border: none;
                background-color: white;
                padding: 20px;
                font-size: 14px;
                line-height: 1.5;
            }}
        """)
        self.editor.textChanged.connect(self.content_changed.emit)
        
        layout.addWidget(self.editor)
    
    def format_text(self, format_type):
        """Apply text formatting"""
        cursor = self.editor.textCursor()
        format = QTextCharFormat()
        
        if format_type == 'bold':
            format.setFontWeight(QFont.Bold if not cursor.charFormat().fontWeight() == QFont.Bold else QFont.Normal)
        elif format_type == 'italic':
            format.setFontItalic(not cursor.charFormat().fontItalic())
        elif format_type == 'underline':
            format.setFontUnderline(not cursor.charFormat().fontUnderline())
        
        cursor.mergeCharFormat(format)
    
    def change_font_size(self, size):
        """Change font size"""
        self.editor.setFontPointSize(int(size))
    
    def set_content(self, html):
        """Set editor content"""
        self.editor.setHtml(html)
    
    def get_content(self):
        """Get editor content"""
        return self.editor.toHtml()
    
    def clear(self):
        """Clear editor"""
        self.editor.clear()

class MemoryVaultWidget(QWidget):
    """Main widget for Memory Vault"""
    
    def __init__(self):
        super().__init__()
        self.memories = []
        self.current_memory = None
        self.setup_ui()
        self.load_sample_memories()
        
    def setup_ui(self):
        """Setup the main UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border-bottom: 1px solid {AppleColors.LIGHT_SEPARATOR.name()};
            }}
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        title_label = QLabel("Memory Vault")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        
        # Search bar
        self.search_bar = AppleTextField("Search memories...")
        self.search_bar.setMaximumWidth(300)
        self.search_bar.textChanged.connect(self.filter_memories)
        
        # New memory button
        new_btn = AppleButton("New Memory")
        new_btn.clicked.connect(self.create_new_memory)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.search_bar)
        header_layout.addWidget(new_btn)
        
        layout.addWidget(header)
        
        # Main content splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)
        
        # Left panel - Memory list
        left_panel = QWidget()
        left_panel.setMinimumWidth(250)
        left_panel.setMaximumWidth(350)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        # Category filter
        category_container = QWidget()
        category_container.setStyleSheet(f"""
            QWidget {{
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                padding: 10px;
            }}
        """)
        category_layout = QHBoxLayout(category_container)
        category_layout.setContentsMargins(10, 5, 10, 5)
        
        category_label = QLabel("Category:")
        self.category_filter = QComboBox()
        self.category_filter.addItems(["All", "General", "Work", "Personal", "Ideas", "Learning"])
        self.category_filter.currentTextChanged.connect(self.filter_memories)
        
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_filter)
        category_layout.addStretch()
        
        left_layout.addWidget(category_container)
        
        # Memory list
        self.memory_list = QListWidget()
        self.memory_list.setFrameShape(QFrame.NoFrame)
        self.memory_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                outline: none;
            }}
            QListWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {AppleColors.LIGHT_SEPARATOR.name()};
            }}
            QListWidget::item:selected {{
                background-color: {AppleColors.ACCENT.name()};
                color: white;
            }}
            QListWidget::item:hover {{
                background-color: rgba(0, 122, 255, 0.1);
            }}
        """)
        self.memory_list.currentItemChanged.connect(self.on_memory_selected)
        
        left_layout.addWidget(self.memory_list)
        
        # Right panel - Editor
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        # Memory metadata
        self.metadata_widget = QWidget()
        self.metadata_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                padding: 15px;
                border-bottom: 1px solid {AppleColors.LIGHT_SEPARATOR.name()};
            }}
        """)
        metadata_layout = QVBoxLayout(self.metadata_widget)
        
        # Title editor
        title_container = QHBoxLayout()
        title_container.addWidget(QLabel("Title:"))
        self.title_edit = AppleTextField()
        self.title_edit.textChanged.connect(self.save_current_memory)
        title_container.addWidget(self.title_edit)
        
        # Category selector
        category_container2 = QHBoxLayout()
        category_container2.addWidget(QLabel("Category:"))
        self.category_edit = QComboBox()
        self.category_edit.addItems(["General", "Work", "Personal", "Ideas", "Learning"])
        self.category_edit.currentTextChanged.connect(self.save_current_memory)
        category_container2.addWidget(self.category_edit)
        category_container2.addStretch()
        
        metadata_layout.addLayout(title_container)
        metadata_layout.addLayout(category_container2)
        
        right_layout.addWidget(self.metadata_widget)
        
        # Editor
        self.editor = MemoryEditor()
        self.editor.content_changed.connect(self.save_current_memory)
        right_layout.addWidget(self.editor)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        
        layout.addWidget(splitter)
        
        # Auto-save timer
        self.save_timer = QTimer()
        self.save_timer.timeout.connect(self.auto_save)
        self.save_timer.start(5000)  # Save every 5 seconds
    
    def create_new_memory(self):
        """Create a new memory"""
        memory_data = {
            'id': str(datetime.now().timestamp()),
            'title': 'New Memory',
            'content': '',
            'category': 'General',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'tags': []
        }
        
        self.memories.insert(0, memory_data)
        self.refresh_memory_list()
        
        # Select the new memory
        if self.memory_list.count() > 0:
            self.memory_list.setCurrentRow(0)
    
    def filter_memories(self):
        """Filter memories based on search and category"""
        search_text = self.search_bar.text().lower()
        category = self.category_filter.currentText()
        
        for i in range(self.memory_list.count()):
            item = self.memory_list.item(i)
            memory_data = item.data(Qt.UserRole)
            
            # Check category filter
            category_match = category == "All" or memory_data.get('category') == category
            
            # Check search filter
            search_match = True
            if search_text:
                title_match = search_text in memory_data.get('title', '').lower()
                content_match = search_text in memory_data.get('content', '').lower()
                search_match = title_match or content_match
            
            # Show/hide item
            item.setHidden(not (category_match and search_match))
    
    def refresh_memory_list(self):
        """Refresh the memory list display"""
        self.memory_list.clear()
        
        for memory in self.memories:
            item = MemoryItem(memory)
            self.memory_list.addItem(item)
        
        self.filter_memories()
    
    def on_memory_selected(self, current, previous):
        """Handle memory selection"""
        if not current:
            self.editor.clear()
            self.title_edit.clear()
            return
        
        memory_data = current.data(Qt.UserRole)
        self.current_memory = memory_data
        
        # Update editor
        self.title_edit.setText(memory_data.get('title', ''))
        self.category_edit.setCurrentText(memory_data.get('category', 'General'))
        self.editor.set_content(memory_data.get('content', ''))
    
    def save_current_memory(self):
        """Save the current memory"""
        if not self.current_memory:
            return
        
        # Update memory data
        self.current_memory['title'] = self.title_edit.text()
        self.current_memory['category'] = self.category_edit.currentText()
        self.current_memory['content'] = self.editor.get_content()
        self.current_memory['date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Update list item
        current_item = self.memory_list.currentItem()
        if current_item:
            current_item.memory_data = self.current_memory
            current_item.update_display()
    
    def auto_save(self):
        """Auto-save memories to storage"""
        # TODO: Implement actual storage
        pass
    
    def load_sample_memories(self):
        """Load sample memories"""
        self.memories = [
            {
                'id': '1',
                'title': 'Project Ideas',
                'content': '<h2>App Ideas</h2><p>1. A meditation app with biofeedback</p><p>2. Smart home dashboard</p><p>3. AI-powered journal</p>',
                'category': 'Ideas',
                'date': '2024-01-10 14:30',
                'tags': ['projects', 'apps']
            },
            {
                'id': '2',
                'title': 'Meeting Notes - Q1 Planning',
                'content': '<h3>Key Points:</h3><ul><li>Focus on user experience</li><li>Improve performance</li><li>Add new features</li></ul>',
                'category': 'Work',
                'date': '2024-01-08 10:00',
                'tags': ['meetings', 'planning']
            },
            {
                'id': '3',
                'title': 'Learning Resources',
                'content': '<p><b>Python Resources:</b></p><ul><li>Real Python tutorials</li><li>Python documentation</li><li>YouTube channels</li></ul>',
                'category': 'Learning',
                'date': '2024-01-05 16:45',
                'tags': ['python', 'learning']
            }
        ]
        
        self.refresh_memory_list()
        
        # Select first memory
        if self.memory_list.count() > 0:
            self.memory_list.setCurrentRow(0)