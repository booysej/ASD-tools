"""Custom widgets with Apple-style design"""

from PySide6.QtWidgets import (QWidget, QPushButton, QLabel, QFrame, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QTextEdit, QProgressBar,
                               QCheckBox, QRadioButton, QSlider, QSpinBox,
                               QGraphicsDropShadowEffect, QScrollArea, QListWidget,
                               QListWidgetItem, QMenu, QToolButton)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QTimer, Property
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient
from .theme import AppleColors, AppleTheme

class AppleButton(QPushButton):
    """Beautiful Apple-style button with animations"""
    
    def __init__(self, text="", parent=None, style="primary"):
        super().__init__(text, parent)
        self.style = style
        self._animation = None
        self._shadow = None
        self.setup_style()
        
    def setup_style(self):
        """Apply Apple-style design"""
        self.setCursor(Qt.PointingHandCursor)
        
        if self.style == "primary":
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {AppleColors.ACCENT.name()};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-weight: 600;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {AppleColors.ACCENT.darker(110).name()};
                }}
                QPushButton:pressed {{
                    background-color: {AppleColors.ACCENT.darker(120).name()};
                }}
            """)
        elif self.style == "secondary":
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                    color: {AppleColors.ACCENT.name()};
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-weight: 600;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {AppleColors.LIGHT_TERTIARY_BACKGROUND.name()};
                }}
            """)
        
        # Add shadow
        self._shadow = AppleTheme.create_shadow_effect(QColor(0, 0, 0, 40), 8, 0, 2)
        self.setGraphicsEffect(self._shadow)
    
    def enterEvent(self, event):
        """Animate on hover"""
        super().enterEvent(event)
        if self._shadow:
            self._animate_shadow(15, 4)
    
    def leaveEvent(self, event):
        """Animate on leave"""
        super().leaveEvent(event)
        if self._shadow:
            self._animate_shadow(8, 2)
    
    def _animate_shadow(self, blur_radius, offset_y):
        """Animate shadow effect"""
        # For simplicity, just update directly
        self._shadow.setBlurRadius(blur_radius)
        self._shadow.setOffset(0, offset_y)

class AppleCard(QFrame):
    """Beautiful card component with shadow"""
    
    clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_style()
        
    def setup_style(self):
        """Apply card styling"""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        
        # Add shadow
        shadow = AppleTheme.create_shadow_effect(QColor(0, 0, 0, 30), 10, 0, 2)
        self.setGraphicsEffect(shadow)
    
    def mousePressEvent(self, event):
        """Emit clicked signal"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class AppleTextField(QLineEdit):
    """Beautiful text field with Apple styling"""
    
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setup_style()
        
    def setup_style(self):
        """Apply Apple-style design"""
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                border: 2px solid transparent;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: {AppleColors.LIGHT_TEXT.name()};
            }}
            QLineEdit:focus {{
                border-color: {AppleColors.ACCENT.name()};
                background-color: white;
            }}
            QLineEdit:hover {{
                background-color: {AppleColors.LIGHT_TERTIARY_BACKGROUND.name()};
            }}
        """)

class AppleTextArea(QTextEdit):
    """Beautiful text area with Apple styling"""
    
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setup_style()
        
    def setup_style(self):
        """Apply Apple-style design"""
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                border: 2px solid transparent;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: {AppleColors.LIGHT_TEXT.name()};
            }}
            QTextEdit:focus {{
                border-color: {AppleColors.ACCENT.name()};
                background-color: white;
            }}
        """)

class AppleProgressBar(QProgressBar):
    """Beautiful progress bar with smooth animations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_style()
        self._animation = None
        
    def setup_style(self):
        """Apply Apple-style design"""
        self.setTextVisible(False)
        self.setStyleSheet(f"""
            QProgressBar {{
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                border: none;
                border-radius: 6px;
                height: 12px;
            }}
            QProgressBar::chunk {{
                background-color: {AppleColors.ACCENT.name()};
                border-radius: 6px;
            }}
        """)
    
    def set_value_animated(self, value):
        """Set value with smooth animation"""
        if self._animation:
            self._animation.stop()
            
        self._animation = QPropertyAnimation(self, b"value")
        self._animation.setDuration(300)
        self._animation.setStartValue(self.value())
        self._animation.setEndValue(value)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        self._animation.start()

class AppleToggle(QCheckBox):
    """iOS-style toggle switch"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 28)
        self._animation = QPropertyAnimation(self, b"handle_position")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        self._handle_position = 0.0
        
    def paintEvent(self, event):
        """Custom paint for toggle switch"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        if self.isChecked():
            bg_color = AppleColors.ACCENT
        else:
            bg_color = AppleColors.LIGHT_TERTIARY_BACKGROUND
            
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 14, 14)
        
        # Handle
        handle_x = 2 + (self.width() - 26) * self._handle_position
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(int(handle_x), 2, 24, 24)
        
    def get_handle_position(self):
        return self._handle_position
        
    def set_handle_position(self, pos):
        self._handle_position = pos
        self.update()
        
    handle_position = Property(float, get_handle_position, set_handle_position)
    
    def setChecked(self, checked):
        """Override to add animation"""
        super().setChecked(checked)
        self._animation.setStartValue(self._handle_position)
        self._animation.setEndValue(1.0 if checked else 0.0)
        self._animation.start()
    
    def mousePressEvent(self, event):
        """Toggle on click"""
        if event.button() == Qt.LeftButton:
            self.setChecked(not self.isChecked())

class AppleSegmentedControl(QWidget):
    """Apple-style segmented control"""
    
    currentChanged = Signal(int)
    
    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        self.items = items or []
        self.current_index = 0
        self.buttons = []
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the segmented control"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create background
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                border-radius: 8px;
            }}
        """)
        
        for i, item in enumerate(self.items):
            btn = QPushButton(item)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, idx=i: self.set_current_index(idx))
            
            if i == 0:
                btn.setStyleSheet(self._get_button_style(True, "first"))
            elif i == len(self.items) - 1:
                btn.setStyleSheet(self._get_button_style(False, "last"))
            else:
                btn.setStyleSheet(self._get_button_style(False, "middle"))
                
            self.buttons.append(btn)
            layout.addWidget(btn)
    
    def _get_button_style(self, selected, position):
        """Get button style based on state and position"""
        base = f"""
            QPushButton {{
                background-color: {"white" if selected else "transparent"};
                color: {AppleColors.ACCENT.name() if selected else AppleColors.LIGHT_TEXT.name()};
                border: none;
                padding: 8px 16px;
                font-weight: {"600" if selected else "normal"};
            }}
            QPushButton:hover {{
                background-color: {"white" if selected else "rgba(0, 0, 0, 0.05)"};
            }}
        """
        
        if position == "first":
            base += "QPushButton { border-top-left-radius: 8px; border-bottom-left-radius: 8px; }"
        elif position == "last":
            base += "QPushButton { border-top-right-radius: 8px; border-bottom-right-radius: 8px; }"
            
        return base
    
    def set_current_index(self, index):
        """Set the current selected index"""
        if 0 <= index < len(self.buttons):
            self.current_index = index
            for i, btn in enumerate(self.buttons):
                if i == 0:
                    pos = "first"
                elif i == len(self.buttons) - 1:
                    pos = "last"
                else:
                    pos = "middle"
                btn.setStyleSheet(self._get_button_style(i == index, pos))
            self.currentChanged.emit(index)

class AppleNotification(QFrame):
    """Beautiful notification widget"""
    
    closed = Signal()
    
    # Class variable to track notifications
    _active_notifications = []
    
    def __init__(self, title, message, notification_type="info", parent=None):
        super().__init__(parent)
        self.notification_type = notification_type
        self.setup_ui(title, message)
        self.setup_animation()
        
    def setup_ui(self, title, message):
        """Setup notification UI"""
        self.setFixedHeight(80)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                border: 1px solid {AppleColors.LIGHT_SEPARATOR.name()};
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Icon
        icon_label = QLabel()
        if self.notification_type == "success":
            icon_label.setText("✅")
        elif self.notification_type == "warning":
            icon_label.setText("⚠️")
        elif self.notification_type == "error":
            icon_label.setText("❌")
        else:
            icon_label.setText("ℹ️")
        icon_label.setStyleSheet("font-size: 24px;")
        
        # Text container
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #333333;
        """)
        
        message_label = QLabel(message)
        message_label.setStyleSheet("""
            font-size: 12px;
            color: #666666;
        """)
        message_label.setWordWrap(True)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(message_label)
        
        # Close button
        close_btn = QToolButton()
        close_btn.setText("×")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close_notification)
        close_btn.setStyleSheet("""
            QToolButton {
                border: none;
                color: #999999;
                font-size: 20px;
                padding: 0px;
            }
            QToolButton:hover {
                color: #333333;
            }
        """)
        
        layout.addWidget(icon_label)
        layout.addWidget(text_container, 1)
        layout.addWidget(close_btn)
        
        # Add shadow
        shadow = AppleTheme.create_shadow_effect(QColor(0, 0, 0, 30), 15, 0, 5)
        self.setGraphicsEffect(shadow)
    
    def setup_animation(self):
        """Setup slide-in animation"""
        self._opacity_effect = QGraphicsDropShadowEffect()
        self.setGraphicsEffect(self._opacity_effect)
        
    def close_notification(self):
        """Close with animation"""
        self.closed.emit()
        if self in AppleNotification._active_notifications:
            AppleNotification._active_notifications.remove(self)
        self.deleteLater()
    
    def show_with_animation(self):
        """Show notification with slide animation"""
        # Simple fade in for now
        animation = AppleTheme.create_fade_animation(self)
        animation.start()
        
        # Auto-close after 5 seconds
        QTimer.singleShot(5000, self.close_notification)
    
    @staticmethod
    def show_notification(parent, title, message, notification_type="info"):
        """Show a notification"""
        if parent is None:
            return None
            
        notification = AppleNotification(title, message, notification_type, parent)
        
        # Position notification
        parent_rect = parent.rect()
        notification.resize(400, 80)
        
        # Position in top-right corner
        x = parent_rect.width() - notification.width() - 20
        y = 20 + len(AppleNotification._active_notifications) * 90
        
        notification.move(x, y)
        notification.show()
        notification.show_with_animation()
        
        AppleNotification._active_notifications.append(notification)
        notification.closed.connect(lambda: AppleNotification._reposition_notifications())
        
        return notification
    
    @staticmethod
    def show_success(parent, title, message=""):
        """Show success notification"""
        return AppleNotification.show_notification(parent, title, message, "success")
    
    @staticmethod
    def show_warning(parent, title, message=""):
        """Show warning notification"""
        return AppleNotification.show_notification(parent, title, message, "warning")
    
    @staticmethod
    def show_error(parent, title, message=""):
        """Show error notification"""
        return AppleNotification.show_notification(parent, title, message, "error")
    
    @staticmethod
    def show_info(parent, title, message=""):
        """Show info notification"""
        return AppleNotification.show_notification(parent, title, message, "info")
    
    @staticmethod
    def _reposition_notifications():
        """Reposition all active notifications"""
        for i, notification in enumerate(AppleNotification._active_notifications):
            if notification and notification.parent():
                parent_rect = notification.parent().rect()
                x = parent_rect.width() - notification.width() - 20
                y = 20 + i * 90
                notification.move(x, y)