from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QTabWidget, QScrollArea, QFrame, QPushButton, 
                               QListWidget, QListWidgetItem, QTextEdit, QComboBox,
                               QGraphicsView, QGraphicsScene, QGraphicsItem,
                               QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem,
                               QDialog, QDialogButtonBox, QSlider, QSpinBox)
from PySide6.QtCore import Qt, Signal, QRectF, QPointF, QTimer
from PySide6.QtGui import (QPainter, QColor, QPen, QBrush, QFont, 
                          QLinearGradient, QPainterPath, QPolygonF)
from cogtools.core.widgets import (AppleCard, AppleButton, AppleTextField, 
                                   AppleTextArea, AppleSegmentedControl)
from cogtools.core.theme import AppleColors, AppleTheme
import json
import re

class FlowchartNode(QGraphicsRectItem):
    """A flowchart node that can be moved and connected"""
    
    def __init__(self, text, node_type="process", x=0, y=0):
        super().__init__()
        self.text = text
        self.node_type = node_type
        self.setPos(x, y)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setup_appearance()
        
    def setup_appearance(self):
        """Setup node appearance based on type"""
        self.setRect(0, 0, 120, 60)
        
        # Colors based on node type
        colors = {
            "start": AppleColors.GREEN,
            "end": AppleColors.RED, 
            "process": AppleColors.ACCENT,
            "decision": AppleColors.ORANGE,
            "input": AppleColors.PURPLE
        }
        
        color = colors.get(self.node_type, AppleColors.ACCENT)
        self.setBrush(QBrush(color))
        self.setPen(QPen(color.darker(120), 2))
        
        # Add text
        self.text_item = QGraphicsTextItem(self.text, self)
        self.text_item.setPos(10, 20)
        self.text_item.setDefaultTextColor(QColor("white"))
        font = QFont()
        font.setPointSize(10)
        font.setWeight(QFont.Bold)
        self.text_item.setFont(font)

class FlowchartEditor(QGraphicsView):
    """Visual flowchart editor"""
    
    node_selected = Signal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.node_counter = 0
        
        # Setup scene
        self.scene.setBackgroundBrush(QBrush(QColor("#F8F9FA")))
        self.scene.setSceneRect(0, 0, 800, 600)
        
    def add_node(self, node_type, text="New Node"):
        """Add a new node to the flowchart"""
        x = 50 + (self.node_counter % 5) * 150
        y = 50 + (self.node_counter // 5) * 100
        
        node = FlowchartNode(text, node_type, x, y)
        self.scene.addItem(node)
        self.node_counter += 1
        return node
    
    def clear_flowchart(self):
        """Clear all nodes from the flowchart"""
        self.scene.clear()
        self.node_counter = 0

class CodeStructureVisualizer(QWidget):
    """Visualize code structure and relationships"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the visualizer UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("📊 Code Structure Visualizer")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Code input
        layout.addWidget(QLabel("Paste your code:"))
        self.code_input = QTextEdit()
        self.code_input.setMaximumHeight(200)
        self.code_input.setPlaceholderText("def hello_world():\n    print('Hello, World!')\n    return True")
        self.code_input.setStyleSheet(f"""
            QTextEdit {{
                border: 1px solid {AppleColors.LIGHT_SEPARATOR.name()};
                border-radius: 8px;
                padding: 10px;
                font-family: 'Monaco', 'Menlo', monospace;
                font-size: 12px;
            }}
        """)
        layout.addWidget(self.code_input)
        
        # Analyze button
        analyze_btn = AppleButton("Analyze Code Structure")
        analyze_btn.clicked.connect(self.analyze_code)
        layout.addWidget(analyze_btn)
        
        # Results area
        self.results_area = QTextEdit()
        self.results_area.setReadOnly(True)
        self.results_area.setStyleSheet(f"""
            QTextEdit {{
                border: 1px solid {AppleColors.LIGHT_SEPARATOR.name()};
                border-radius: 8px;
                padding: 10px;
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                font-family: 'Monaco', 'Menlo', monospace;
                font-size: 12px;
            }}
        """)
        layout.addWidget(self.results_area)
        
    def analyze_code(self):
        """Analyze the input code and show structure"""
        code = self.code_input.toPlainText().strip()
        if not code:
            self.results_area.setText("Please enter some code to analyze.")
            return
        
        analysis = self.perform_analysis(code)
        self.results_area.setText(analysis)
    
    def perform_analysis(self, code):
        """Perform basic code analysis"""
        lines = code.split('\n')
        
        # Count various elements
        functions = len(re.findall(r'def\s+\w+', code))
        classes = len(re.findall(r'class\s+\w+', code))
        imports = len(re.findall(r'import\s+\w+|from\s+\w+\s+import', code))
        comments = len([line for line in lines if line.strip().startswith('#')])
        
        # Calculate complexity (simple heuristic)
        complexity_indicators = ['if', 'elif', 'else', 'for', 'while', 'try', 'except']
        complexity = sum(code.count(indicator) for indicator in complexity_indicators)
        
        # Indentation analysis
        max_indent = 0
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                max_indent = max(max_indent, indent)
        
        nesting_level = max_indent // 4  # Assuming 4-space indentation
        
        analysis = f"""
📈 CODE STRUCTURE ANALYSIS
{'=' * 30}

📊 STATISTICS:
• Functions: {functions}
• Classes: {classes}
• Import statements: {imports}
• Comment lines: {comments}
• Total lines: {len(lines)}
• Non-empty lines: {len([l for l in lines if l.strip()])}

🔍 COMPLEXITY:
• Control flow statements: {complexity}
• Maximum nesting level: {nesting_level}
• Complexity score: {"Low" if complexity < 5 else "Medium" if complexity < 15 else "High"}

📝 RECOMMENDATIONS:
"""
        
        # Add recommendations
        if nesting_level > 3:
            analysis += "• Consider breaking down deeply nested code into smaller functions\n"
        if complexity > 10:
            analysis += "• High complexity detected - consider refactoring for better readability\n"
        if functions == 0 and len(lines) > 10:
            analysis += "• Consider organizing code into functions for better structure\n"
        if comments == 0:
            analysis += "• Add comments to explain complex logic\n"
        
        if "• " not in analysis.split("RECOMMENDATIONS:")[-1]:
            analysis += "• Code structure looks good! Keep up the good work."
        
        return analysis

class DebuggingAid(AppleCard):
    """Visual debugging helper"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup debugging aid UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🐛 Debugging Assistant")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Error type selector
        layout.addWidget(QLabel("Common Error Types:"))
        self.error_types = QComboBox()
        self.error_types.addItems([
            "Select error type...",
            "NameError", 
            "TypeError",
            "IndexError",
            "KeyError",
            "ValueError",
            "IndentationError",
            "SyntaxError",
            "AttributeError"
        ])
        self.error_types.currentTextChanged.connect(self.show_debugging_tips)
        layout.addWidget(self.error_types)
        
        # Tips area
        self.tips_area = QTextEdit()
        self.tips_area.setReadOnly(True)
        self.tips_area.setMaximumHeight(150)
        self.tips_area.setStyleSheet(f"""
            QTextEdit {{
                border: 1px solid {AppleColors.LIGHT_SEPARATOR.name()};
                border-radius: 8px;
                padding: 10px;
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                font-size: 12px;
            }}
        """)
        layout.addWidget(self.tips_area)
        
        # Debugging checklist
        layout.addWidget(QLabel("Debugging Checklist:"))
        checklist_items = [
            "Read the error message carefully",
            "Check the line number mentioned",
            "Verify variable names and spelling",
            "Check indentation and syntax",
            "Print intermediate values",
            "Use breakpoints or debugger"
        ]
        
        self.checklist = QListWidget()
        self.checklist.setMaximumHeight(150)
        
        for item_text in checklist_items:
            item = QListWidgetItem(item_text)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.checklist.addItem(item)
        
        layout.addWidget(self.checklist)
    
    def show_debugging_tips(self, error_type):
        """Show debugging tips for selected error type"""
        tips = {
            "NameError": """
🔍 NameError: name 'variable' is not defined

Common causes:
• Typo in variable name
• Variable used before assignment
• Variable out of scope

Quick fixes:
• Check spelling of variable names
• Ensure variable is defined before use
• Check indentation and scope
            """,
            "TypeError": """
🔍 TypeError: unsupported operand type(s)

Common causes:
• Wrong data type for operation
• Calling non-callable object
• Wrong number of arguments

Quick fixes:
• Check data types with type()
• Convert types if needed (int(), str(), etc.)
• Verify function calls and arguments
            """,
            "IndexError": """
🔍 IndexError: list index out of range

Common causes:
• Accessing index beyond list length
• Empty list access
• Off-by-one errors

Quick fixes:
• Check list length with len()
• Use range(len(list)) in loops
• Add bounds checking before access
            """
        }
        
        if error_type in tips:
            self.tips_area.setText(tips[error_type])
        else:
            self.tips_area.clear()

class VisualCodingHelperWidget(QWidget):
    """Main widget for Visual Coding Helper"""
    
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
        
        title_label = QLabel("Visual Coding Helper")
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
        
        # Flowchart tab
        flowchart_widget = QWidget()
        flowchart_layout = QVBoxLayout(flowchart_widget)
        flowchart_layout.setContentsMargins(20, 20, 20, 20)
        
        # Flowchart toolbar
        toolbar_layout = QHBoxLayout()
        
        add_start_btn = AppleButton("Start", style="secondary")
        add_start_btn.clicked.connect(lambda: self.flowchart_editor.add_node("start", "Start"))
        
        add_process_btn = AppleButton("Process", style="secondary") 
        add_process_btn.clicked.connect(lambda: self.flowchart_editor.add_node("process", "Process"))
        
        add_decision_btn = AppleButton("Decision", style="secondary")
        add_decision_btn.clicked.connect(lambda: self.flowchart_editor.add_node("decision", "Decision?"))
        
        add_end_btn = AppleButton("End", style="secondary")
        add_end_btn.clicked.connect(lambda: self.flowchart_editor.add_node("end", "End"))
        
        clear_btn = AppleButton("Clear")
        clear_btn.clicked.connect(self.clear_flowchart)
        
        toolbar_layout.addWidget(QLabel("Add nodes:"))
        toolbar_layout.addWidget(add_start_btn)
        toolbar_layout.addWidget(add_process_btn)
        toolbar_layout.addWidget(add_decision_btn)
        toolbar_layout.addWidget(add_end_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(clear_btn)
        
        flowchart_layout.addLayout(toolbar_layout)
        
        # Flowchart editor
        self.flowchart_editor = FlowchartEditor()
        flowchart_layout.addWidget(self.flowchart_editor)
        
        self.tabs.addTab(flowchart_widget, "Flowchart")
        
        # Code Structure tab
        structure_widget = QWidget()
        structure_layout = QVBoxLayout(structure_widget)
        structure_layout.setContentsMargins(20, 20, 20, 20)
        
        self.code_visualizer = CodeStructureVisualizer()
        structure_layout.addWidget(self.code_visualizer)
        
        self.tabs.addTab(structure_widget, "Code Analysis")
        
        # Debugging tab
        debug_widget = QWidget()
        debug_layout = QVBoxLayout(debug_widget)
        debug_layout.setContentsMargins(20, 20, 20, 20)
        
        self.debugging_aid = DebuggingAid()
        debug_layout.addWidget(self.debugging_aid)
        
        # Add programming concepts reference
        concepts_card = AppleCard()
        concepts_layout = QVBoxLayout(concepts_card)
        concepts_layout.addWidget(QLabel("💡 Programming Concepts"))
        
        concepts_text = QLabel("""
Key Programming Concepts:

🔄 Loops: Repeat code multiple times
  • for loop: iterate over sequences
  • while loop: repeat while condition is true

🔀 Conditionals: Make decisions in code
  • if: execute code if condition is true
  • elif: check additional conditions
  • else: execute when no conditions match

📦 Functions: Reusable blocks of code
  • def function_name(): creates a function
  • return: sends value back to caller
  • Parameters: inputs to functions

📊 Data Structures:
  • Lists: ordered collections [1, 2, 3]
  • Dictionaries: key-value pairs {"name": "John"}
  • Sets: unique collections {1, 2, 3}
        """)
        concepts_text.setWordWrap(True)
        concepts_text.setStyleSheet("font-size: 11px; color: #666666; line-height: 1.3;")
        concepts_layout.addWidget(concepts_text)
        
        debug_layout.addWidget(concepts_card)
        debug_layout.addStretch()
        
        self.tabs.addTab(debug_widget, "Debug & Learn")
        
        layout.addWidget(self.tabs)
    
    def clear_flowchart(self):
        """Clear the flowchart"""
        self.flowchart_editor.clear_flowchart()