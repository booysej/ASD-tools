from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QScrollArea, QFrame, QPushButton, QMenu,
                               QListWidget, QListWidgetItem, QDialog,
                               QDialogButtonBox, QComboBox, QDateEdit)
from PySide6.QtCore import Qt, Signal, QMimeData, QByteArray, QDataStream, QIODevice, QDate
from PySide6.QtGui import QDrag, QPalette, QColor
from cogtools.core.widgets import (AppleCard, AppleButton, AppleTextField, 
                                   AppleTextArea, AppleSegmentedControl)
from cogtools.core.theme import AppleColors, AppleTheme
import json
from datetime import datetime

class TaskCard(AppleCard):
    """Beautiful task card with drag support"""
    
    task_updated = Signal(dict)
    task_deleted = Signal(str)
    
    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.task_data = task_data
        self.setup_ui()
        
    def setup_ui(self):
        """Setup task card UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Title
        self.title_label = QLabel(self.task_data.get('title', 'Untitled'))
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #1C1C1E;
        """)
        layout.addWidget(self.title_label)
        
        # Description
        if self.task_data.get('description'):
            desc_label = QLabel(self.task_data['description'])
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("""
                font-size: 12px;
                color: #8E8E93;
                margin-top: 4px;
            """)
            layout.addWidget(desc_label)
        
        # Tags and metadata
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(8)
        
        # Priority
        priority = self.task_data.get('priority', 'medium')
        priority_colors = {
            'high': AppleColors.RED,
            'medium': AppleColors.ORANGE,
            'low': AppleColors.GREEN
        }
        priority_label = QLabel(f"● {priority.title()}")
        priority_label.setStyleSheet(f"""
            font-size: 11px;
            color: {priority_colors.get(priority, AppleColors.ORANGE).name()};
            font-weight: 500;
        """)
        meta_layout.addWidget(priority_label)
        
        # Due date
        if self.task_data.get('due_date'):
            due_label = QLabel(f"📅 {self.task_data['due_date']}")
            due_label.setStyleSheet("""
                font-size: 11px;
                color: #8E8E93;
            """)
            meta_layout.addWidget(due_label)
        
        meta_layout.addStretch()
        layout.addLayout(meta_layout)
        
        # Enable drag
        self.setAcceptDrops(True)
        self.setCursor(Qt.OpenHandCursor)
    
    def mousePressEvent(self, event):
        """Start drag operation"""
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
            
            # Create drag
            drag = QDrag(self)
            mime_data = QMimeData()
            
            # Store task data
            data = QByteArray()
            stream = QDataStream(data, QIODevice.WriteOnly)
            stream.writeQString(json.dumps(self.task_data))
            mime_data.setData("application/x-task", data)
            
            drag.setMimeData(mime_data)
            drag.exec_(Qt.MoveAction)
            
            self.setCursor(Qt.OpenHandCursor)
    
    def mouseDoubleClickEvent(self, event):
        """Edit task on double click"""
        dialog = TaskEditDialog(self.task_data, self)
        if dialog.exec_():
            self.task_data = dialog.get_task_data()
            self.update_display()
            self.task_updated.emit(self.task_data)
    
    def update_display(self):
        """Update the card display"""
        self.title_label.setText(self.task_data.get('title', 'Untitled'))

class KanbanColumn(QFrame):
    """Kanban column with drag and drop support"""
    
    tasks_changed = Signal()
    
    def __init__(self, title, column_id, parent=None):
        super().__init__(parent)
        self.title = title
        self.column_id = column_id
        self.tasks = []
        self.setup_ui()
        
    def setup_ui(self):
        """Setup column UI"""
        self.setAcceptDrops(True)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                border-radius: 12px;
                padding: 16px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        
        self.count_label = QLabel("0")
        self.count_label.setStyleSheet("""
            font-size: 14px;
            color: #8E8E93;
            font-weight: 500;
            background-color: white;
            padding: 2px 8px;
            border-radius: 10px;
        """)
        
        add_btn = QPushButton("+")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.add_new_task)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {AppleColors.ACCENT.name()};
                border: none;
                font-size: 20px;
                font-weight: 400;
                padding: 0px;
                width: 24px;
                height: 24px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 122, 255, 0.1);
                border-radius: 12px;
            }}
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(self.count_label)
        header_layout.addStretch()
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Task container with scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.task_container = QWidget()
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setContentsMargins(0, 0, 0, 0)
        self.task_layout.setSpacing(8)
        self.task_layout.addStretch()
        
        scroll.setWidget(self.task_container)
        layout.addWidget(scroll)
        
    def add_task(self, task_data):
        """Add a task card to the column"""
        task_card = TaskCard(task_data)
        task_card.task_updated.connect(self.on_task_updated)
        task_card.task_deleted.connect(self.on_task_deleted)
        
        # Insert before the stretch
        self.task_layout.insertWidget(self.task_layout.count() - 1, task_card)
        self.tasks.append(task_data)
        self.update_count()
        
    def add_new_task(self):
        """Show dialog to add new task"""
        dialog = TaskEditDialog(parent=self)
        if dialog.exec_():
            task_data = dialog.get_task_data()
            task_data['id'] = str(datetime.now().timestamp())
            task_data['column'] = self.column_id
            self.add_task(task_data)
            self.tasks_changed.emit()
    
    def on_task_updated(self, task_data):
        """Handle task update"""
        # Update task in list
        for i, task in enumerate(self.tasks):
            if task.get('id') == task_data.get('id'):
                self.tasks[i] = task_data
                break
        self.tasks_changed.emit()
    
    def on_task_deleted(self, task_id):
        """Handle task deletion"""
        self.tasks = [t for t in self.tasks if t.get('id') != task_id]
        self.update_count()
        self.tasks_changed.emit()
    
    def update_count(self):
        """Update task count"""
        self.count_label.setText(str(len(self.tasks)))
    
    def dragEnterEvent(self, event):
        """Handle drag enter"""
        if event.mimeData().hasFormat("application/x-task"):
            event.acceptProposedAction()
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {AppleColors.LIGHT_TERTIARY_BACKGROUND.name()};
                    border-radius: 12px;
                    padding: 16px;
                    border: 2px solid {AppleColors.ACCENT.name()};
                }}
            """)
    
    def dragLeaveEvent(self, event):
        """Handle drag leave"""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                border-radius: 12px;
                padding: 16px;
            }}
        """)
    
    def dropEvent(self, event):
        """Handle drop"""
        if event.mimeData().hasFormat("application/x-task"):
            data = event.mimeData().data("application/x-task")
            stream = QDataStream(data, QIODevice.ReadOnly)
            task_json = stream.readQString()
            task_data = json.loads(task_json)
            
            # Update task column
            task_data['column'] = self.column_id
            
            # Remove from source
            source_widget = event.source()
            if source_widget and hasattr(source_widget, 'parent'):
                source_column = source_widget.parent()
                while source_column and not isinstance(source_column, KanbanColumn):
                    source_column = source_column.parent()
                if source_column:
                    source_column.tasks = [t for t in source_column.tasks if t.get('id') != task_data.get('id')]
                    source_widget.deleteLater()
                    source_column.update_count()
            
            # Add to this column
            self.add_task(task_data)
            self.tasks_changed.emit()
            
            event.acceptProposedAction()
            
        # Reset style
        self.dragLeaveEvent(event)

class TaskEditDialog(QDialog):
    """Dialog for editing tasks"""
    
    def __init__(self, task_data=None, parent=None):
        super().__init__(parent)
        self.task_data = task_data or {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("Edit Task" if self.task_data else "New Task")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # Title field
        layout.addWidget(QLabel("Title"))
        self.title_field = AppleTextField("Enter task title...")
        self.title_field.setText(self.task_data.get('title', ''))
        layout.addWidget(self.title_field)
        
        # Description field
        layout.addWidget(QLabel("Description"))
        self.desc_field = AppleTextArea("Enter task description...")
        self.desc_field.setPlainText(self.task_data.get('description', ''))
        self.desc_field.setMaximumHeight(100)
        layout.addWidget(self.desc_field)
        
        # Priority
        layout.addWidget(QLabel("Priority"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        current_priority = self.task_data.get('priority', 'medium')
        self.priority_combo.setCurrentText(current_priority.title())
        layout.addWidget(self.priority_combo)
        
        # Due date
        layout.addWidget(QLabel("Due Date"))
        self.due_date = QDateEdit()
        self.due_date.setCalendarPopup(True)
        self.due_date.setDate(QDate.currentDate())
        if self.task_data.get('due_date'):
            try:
                date = QDate.fromString(self.task_data['due_date'], "yyyy-MM-dd")
                self.due_date.setDate(date)
            except:
                pass
        layout.addWidget(self.due_date)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = AppleButton("Cancel", style="secondary")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = AppleButton("Save")
        save_btn.clicked.connect(self.accept)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
    
    def get_task_data(self):
        """Get the task data from form"""
        return {
            'id': self.task_data.get('id', str(datetime.now().timestamp())),
            'title': self.title_field.text(),
            'description': self.desc_field.toPlainText(),
            'priority': self.priority_combo.currentText().lower(),
            'due_date': self.due_date.date().toString("yyyy-MM-dd"),
            'column': self.task_data.get('column', 'todo')
        }

class FocusTaskManagerWidget(QWidget):
    """Main widget for Focus Task Manager"""
    
    def __init__(self):
        super().__init__()
        self.columns = {}
        self.setup_ui()
        self.load_sample_data()
        
    def setup_ui(self):
        """Setup the main UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Focus Task Manager")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        
        # View switcher
        view_switcher = AppleSegmentedControl(["Board", "List", "Calendar"])
        view_switcher.setMaximumWidth(300)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(view_switcher)
        
        layout.addLayout(header_layout)
        
        # Kanban board
        board_scroll = QScrollArea()
        board_scroll.setWidgetResizable(True)
        board_scroll.setFrameShape(QFrame.NoFrame)
        board_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        board_widget = QWidget()
        self.board_layout = QHBoxLayout(board_widget)
        self.board_layout.setContentsMargins(0, 0, 0, 0)
        self.board_layout.setSpacing(16)
        
        # Create columns
        columns_config = [
            ("To Do", "todo"),
            ("In Progress", "in_progress"),
            ("Review", "review"),
            ("Done", "done")
        ]
        
        for title, column_id in columns_config:
            column = KanbanColumn(title, column_id)
            column.tasks_changed.connect(self.save_tasks)
            self.columns[column_id] = column
            self.board_layout.addWidget(column)
        
        board_scroll.setWidget(board_widget)
        layout.addWidget(board_scroll)
    
    def load_sample_data(self):
        """Load some sample tasks"""
        sample_tasks = [
            {
                'id': '1',
                'title': 'Design new homepage',
                'description': 'Create mockups for the new landing page design',
                'priority': 'high',
                'due_date': '2024-01-20',
                'column': 'todo'
            },
            {
                'id': '2',
                'title': 'Fix login bug',
                'description': 'Users unable to login with social accounts',
                'priority': 'high',
                'due_date': '2024-01-15',
                'column': 'in_progress'
            },
            {
                'id': '3',
                'title': 'Update documentation',
                'description': 'Add new API endpoints to docs',
                'priority': 'medium',
                'due_date': '2024-01-25',
                'column': 'todo'
            },
            {
                'id': '4',
                'title': 'Code review PR #123',
                'description': 'Review the new feature implementation',
                'priority': 'medium',
                'due_date': '2024-01-16',
                'column': 'review'
            },
            {
                'id': '5',
                'title': 'Deploy to production',
                'description': 'Deploy version 2.0 to production servers',
                'priority': 'low',
                'due_date': '2024-01-30',
                'column': 'done'
            }
        ]
        
        for task in sample_tasks:
            column = self.columns.get(task['column'])
            if column:
                column.add_task(task)
    
    def save_tasks(self):
        """Save tasks to storage"""
        # TODO: Implement actual storage
        pass