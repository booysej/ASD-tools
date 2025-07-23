from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QTabWidget, QScrollArea, QFrame, QPushButton, 
                               QCheckBox, QSlider, QComboBox, QSpinBox,
                               QGroupBox, QButtonGroup, QRadioButton,
                               QColorDialog, QFontDialog, QMessageBox)
from PySide6.QtCore import Qt, Signal, QSettings
from PySide6.QtGui import QColor, QFont
from cogtools.core.widgets import (AppleCard, AppleButton, AppleTextField, 
                                   AppleSegmentedControl)
from cogtools.core.theme import AppleColors, AppleTheme
import json

class ThemeSettings(AppleCard):
    """Theme and appearance settings"""
    
    theme_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup theme settings UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🎨 Theme & Appearance")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Theme selection
        theme_group = QGroupBox("Color Theme")
        theme_layout = QVBoxLayout(theme_group)
        
        self.theme_buttons = QButtonGroup()
        
        light_theme = QRadioButton("Light Theme")
        light_theme.setChecked(True)  # Default
        light_theme.toggled.connect(lambda checked: self.theme_changed.emit("light") if checked else None)
        
        dark_theme = QRadioButton("Dark Theme")
        dark_theme.toggled.connect(lambda checked: self.theme_changed.emit("dark") if checked else None)
        
        auto_theme = QRadioButton("Auto (System)")
        auto_theme.toggled.connect(lambda checked: self.theme_changed.emit("auto") if checked else None)
        
        self.theme_buttons.addButton(light_theme)
        self.theme_buttons.addButton(dark_theme)
        self.theme_buttons.addButton(auto_theme)
        
        theme_layout.addWidget(light_theme)
        theme_layout.addWidget(dark_theme)
        theme_layout.addWidget(auto_theme)
        
        layout.addWidget(theme_group)
        
        # Font settings
        font_group = QGroupBox("Font Settings")
        font_layout = QVBoxLayout(font_group)
        
        # Font size
        font_size_layout = QHBoxLayout()
        font_size_layout.addWidget(QLabel("Font Size:"))
        
        self.font_size_slider = QSlider(Qt.Horizontal)
        self.font_size_slider.setRange(10, 20)
        self.font_size_slider.setValue(14)
        self.font_size_slider.valueChanged.connect(self.update_font_size)
        
        self.font_size_label = QLabel("14px")
        self.font_size_label.setMinimumWidth(40)
        
        font_size_layout.addWidget(self.font_size_slider)
        font_size_layout.addWidget(self.font_size_label)
        
        font_layout.addLayout(font_size_layout)
        
        # Font family button
        self.font_btn = AppleButton("Change Font Family")
        self.font_btn.clicked.connect(self.choose_font)
        font_layout.addWidget(self.font_btn)
        
        layout.addWidget(font_group)
        
        # Interface options
        interface_group = QGroupBox("Interface Options")
        interface_layout = QVBoxLayout(interface_group)
        
        self.animations_cb = QCheckBox("Enable animations")
        self.animations_cb.setChecked(True)
        
        self.compact_mode_cb = QCheckBox("Compact mode")
        self.compact_mode_cb.setChecked(False)
        
        self.sidebar_cb = QCheckBox("Show sidebar by default")
        self.sidebar_cb.setChecked(True)
        
        interface_layout.addWidget(self.animations_cb)
        interface_layout.addWidget(self.compact_mode_cb)
        interface_layout.addWidget(self.sidebar_cb)
        
        layout.addWidget(interface_group)
    
    def update_font_size(self, value):
        """Update font size label"""
        self.font_size_label.setText(f"{value}px")
    
    def choose_font(self):
        """Open font selection dialog"""
        font, ok = QFontDialog.getFont()
        if ok:
            self.font_btn.setText(f"Font: {font.family()}")

class AccessibilitySettings(AppleCard):
    """Accessibility and cognitive assistance settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup accessibility settings UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("♿ Accessibility & Cognitive Support")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Visual aids
        visual_group = QGroupBox("Visual Aids")
        visual_layout = QVBoxLayout(visual_group)
        
        self.high_contrast_cb = QCheckBox("High contrast mode")
        self.large_text_cb = QCheckBox("Large text mode")
        self.focus_indicators_cb = QCheckBox("Enhanced focus indicators")
        self.focus_indicators_cb.setChecked(True)
        
        visual_layout.addWidget(self.high_contrast_cb)
        visual_layout.addWidget(self.large_text_cb)
        visual_layout.addWidget(self.focus_indicators_cb)
        
        layout.addWidget(visual_group)
        
        # Cognitive assistance
        cognitive_group = QGroupBox("Cognitive Assistance")
        cognitive_layout = QVBoxLayout(cognitive_group)
        
        self.task_breakdown_cb = QCheckBox("Auto-suggest task breakdown")
        self.task_breakdown_cb.setChecked(True)
        
        self.gentle_reminders_cb = QCheckBox("Gentle reminders")
        self.gentle_reminders_cb.setChecked(True)
        
        self.progress_celebrations_cb = QCheckBox("Progress celebrations")
        self.progress_celebrations_cb.setChecked(True)
        
        cognitive_layout.addWidget(self.task_breakdown_cb)
        cognitive_layout.addWidget(self.gentle_reminders_cb)
        cognitive_layout.addWidget(self.progress_celebrations_cb)
        
        layout.addWidget(cognitive_group)
        
        # Focus assistance
        focus_group = QGroupBox("Focus Assistance")
        focus_layout = QVBoxLayout(focus_group)
        
        # Pomodoro timer defaults
        pomodoro_layout = QHBoxLayout()
        pomodoro_layout.addWidget(QLabel("Default work session:"))
        
        self.work_duration = QSpinBox()
        self.work_duration.setRange(15, 60)
        self.work_duration.setValue(25)
        self.work_duration.setSuffix(" min")
        
        pomodoro_layout.addWidget(self.work_duration)
        pomodoro_layout.addStretch()
        
        focus_layout.addLayout(pomodoro_layout)
        
        # Break duration
        break_layout = QHBoxLayout()
        break_layout.addWidget(QLabel("Default break duration:"))
        
        self.break_duration = QSpinBox()
        self.break_duration.setRange(5, 30)
        self.break_duration.setValue(5)
        self.break_duration.setSuffix(" min")
        
        break_layout.addWidget(self.break_duration)
        break_layout.addStretch()
        
        focus_layout.addLayout(break_layout)
        
        # Auto-start options
        self.auto_start_breaks_cb = QCheckBox("Auto-start break timers")
        self.auto_start_work_cb = QCheckBox("Auto-start work sessions after breaks")
        
        focus_layout.addWidget(self.auto_start_breaks_cb)
        focus_layout.addWidget(self.auto_start_work_cb)
        
        layout.addWidget(focus_group)

class NotificationSettings(AppleCard):
    """Notification and alert settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup notification settings UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🔔 Notifications & Alerts")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # General notifications
        general_group = QGroupBox("General Notifications")
        general_layout = QVBoxLayout(general_group)
        
        self.desktop_notifications_cb = QCheckBox("Desktop notifications")
        self.desktop_notifications_cb.setChecked(True)
        
        self.sound_notifications_cb = QCheckBox("Sound notifications")
        self.sound_notifications_cb.setChecked(True)
        
        self.gentle_notifications_cb = QCheckBox("Use gentle, non-intrusive notifications")
        self.gentle_notifications_cb.setChecked(True)
        
        general_layout.addWidget(self.desktop_notifications_cb)
        general_layout.addWidget(self.sound_notifications_cb)
        general_layout.addWidget(self.gentle_notifications_cb)
        
        layout.addWidget(general_group)
        
        # Reminder settings
        reminder_group = QGroupBox("Reminders")
        reminder_layout = QVBoxLayout(reminder_group)
        
        self.task_reminders_cb = QCheckBox("Task due date reminders")
        self.task_reminders_cb.setChecked(True)
        
        self.break_reminders_cb = QCheckBox("Break time reminders")
        self.break_reminders_cb.setChecked(True)
        
        self.hydration_reminders_cb = QCheckBox("Hydration reminders")
        self.hydration_reminders_cb.setChecked(False)
        
        reminder_layout.addWidget(self.task_reminders_cb)
        reminder_layout.addWidget(self.break_reminders_cb)
        reminder_layout.addWidget(self.hydration_reminders_cb)
        
        # Reminder frequency
        frequency_layout = QHBoxLayout()
        frequency_layout.addWidget(QLabel("Reminder frequency:"))
        
        self.reminder_frequency = QComboBox()
        self.reminder_frequency.addItems([
            "Every 30 minutes",
            "Every hour", 
            "Every 2 hours",
            "Twice daily",
            "Daily"
        ])
        self.reminder_frequency.setCurrentText("Every hour")
        
        frequency_layout.addWidget(self.reminder_frequency)
        frequency_layout.addStretch()
        
        reminder_layout.addLayout(frequency_layout)
        
        layout.addWidget(reminder_group)
        
        # Quiet hours
        quiet_group = QGroupBox("Quiet Hours")
        quiet_layout = QVBoxLayout(quiet_group)
        
        self.quiet_hours_cb = QCheckBox("Enable quiet hours")
        
        quiet_time_layout = QHBoxLayout()
        quiet_time_layout.addWidget(QLabel("From:"))
        
        self.quiet_start = QComboBox()
        self.quiet_start.addItems([f"{h:02d}:00" for h in range(24)])
        self.quiet_start.setCurrentText("22:00")
        
        quiet_time_layout.addWidget(self.quiet_start)
        quiet_time_layout.addWidget(QLabel("To:"))
        
        self.quiet_end = QComboBox()
        self.quiet_end.addItems([f"{h:02d}:00" for h in range(24)])
        self.quiet_end.setCurrentText("08:00")
        
        quiet_time_layout.addWidget(self.quiet_end)
        quiet_time_layout.addStretch()
        
        quiet_layout.addWidget(self.quiet_hours_cb)
        quiet_layout.addLayout(quiet_time_layout)
        
        layout.addWidget(quiet_group)

class DataSettings(AppleCard):
    """Data and privacy settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup data settings UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("💾 Data & Privacy")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        layout.addWidget(title)
        
        # Auto-save settings
        autosave_group = QGroupBox("Auto-save")
        autosave_layout = QVBoxLayout(autosave_group)
        
        self.autosave_cb = QCheckBox("Enable auto-save")
        self.autosave_cb.setChecked(True)
        
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Save interval:"))
        
        self.save_interval = QSpinBox()
        self.save_interval.setRange(1, 60)
        self.save_interval.setValue(5)
        self.save_interval.setSuffix(" minutes")
        
        interval_layout.addWidget(self.save_interval)
        interval_layout.addStretch()
        
        autosave_layout.addWidget(self.autosave_cb)
        autosave_layout.addLayout(interval_layout)
        
        layout.addWidget(autosave_group)
        
        # Backup settings
        backup_group = QGroupBox("Backup")
        backup_layout = QVBoxLayout(backup_group)
        
        self.auto_backup_cb = QCheckBox("Automatic daily backups")
        self.auto_backup_cb.setChecked(True)
        
        self.backup_location = AppleTextField("~/CogTools/backups")
        self.backup_location.setReadOnly(True)
        
        backup_btn = AppleButton("Choose Backup Location")
        backup_btn.clicked.connect(self.choose_backup_location)
        
        backup_layout.addWidget(self.auto_backup_cb)
        backup_layout.addWidget(QLabel("Backup location:"))
        backup_layout.addWidget(self.backup_location)
        backup_layout.addWidget(backup_btn)
        
        layout.addWidget(backup_group)
        
        # Data management
        data_group = QGroupBox("Data Management")
        data_layout = QVBoxLayout(data_group)
        
        export_btn = AppleButton("Export All Data")
        export_btn.clicked.connect(self.export_data)
        
        import_btn = AppleButton("Import Data", style="secondary")
        import_btn.clicked.connect(self.import_data)
        
        clear_btn = AppleButton("Clear All Data")
        clear_btn.clicked.connect(self.clear_data)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF3B30;
                color: white;
            }
            QPushButton:hover {
                background-color: #D70015;
            }
        """)
        
        data_layout.addWidget(export_btn)
        data_layout.addWidget(import_btn)
        data_layout.addWidget(clear_btn)
        
        layout.addWidget(data_group)
    
    def choose_backup_location(self):
        """Choose backup location"""
        # In a real implementation, this would open a file dialog
        QMessageBox.information(self, "Backup Location", 
                              "Backup location selection would open here.")
    
    def export_data(self):
        """Export user data"""
        QMessageBox.information(self, "Export Data", 
                              "Data export functionality would be implemented here.")
    
    def import_data(self):
        """Import user data"""
        QMessageBox.information(self, "Import Data", 
                              "Data import functionality would be implemented here.")
    
    def clear_data(self):
        """Clear all user data"""
        reply = QMessageBox.question(self, "Clear All Data",
                                   "Are you sure you want to clear all data? This cannot be undone.",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, "Data Cleared", 
                                  "All data has been cleared.")

class SettingsPanelWidget(QWidget):
    """Main widget for Settings Panel"""
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings("CogTools", "Settings")
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Setup the main UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Settings")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #1C1C1E;
        """)
        
        # Save and reset buttons
        save_btn = AppleButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        
        reset_btn = AppleButton("Reset to Defaults", style="secondary")
        reset_btn.clicked.connect(self.reset_settings)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(reset_btn)
        header_layout.addWidget(save_btn)
        
        layout.addLayout(header_layout)
        
        # Tab widget for different setting categories
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
        
        # Theme settings tab
        theme_scroll = QScrollArea()
        theme_scroll.setWidgetResizable(True)
        theme_scroll.setFrameShape(QFrame.NoFrame)
        
        self.theme_settings = ThemeSettings()
        self.theme_settings.theme_changed.connect(self.on_theme_changed)
        theme_scroll.setWidget(self.theme_settings)
        
        self.tabs.addTab(theme_scroll, "Appearance")
        
        # Accessibility settings tab
        access_scroll = QScrollArea()
        access_scroll.setWidgetResizable(True)
        access_scroll.setFrameShape(QFrame.NoFrame)
        
        self.accessibility_settings = AccessibilitySettings()
        access_scroll.setWidget(self.accessibility_settings)
        
        self.tabs.addTab(access_scroll, "Accessibility")
        
        # Notification settings tab
        notif_scroll = QScrollArea()
        notif_scroll.setWidgetResizable(True)
        notif_scroll.setFrameShape(QFrame.NoFrame)
        
        self.notification_settings = NotificationSettings()
        notif_scroll.setWidget(self.notification_settings)
        
        self.tabs.addTab(notif_scroll, "Notifications")
        
        # Data settings tab
        data_scroll = QScrollArea()
        data_scroll.setWidgetResizable(True)
        data_scroll.setFrameShape(QFrame.NoFrame)
        
        self.data_settings = DataSettings()
        data_scroll.setWidget(self.data_settings)
        
        self.tabs.addTab(data_scroll, "Data & Privacy")
        
        layout.addWidget(self.tabs)
    
    def on_theme_changed(self, theme):
        """Handle theme change"""
        # In a real implementation, this would apply the theme
        print(f"Theme changed to: {theme}")
    
    def save_settings(self):
        """Save all settings"""
        # Save theme settings
        for button in self.theme_settings.theme_buttons.buttons():
            if button.isChecked():
                self.settings.setValue("theme", button.text())
                break
        
        self.settings.setValue("font_size", self.theme_settings.font_size_slider.value())
        self.settings.setValue("animations", self.theme_settings.animations_cb.isChecked())
        
        # Save accessibility settings
        self.settings.setValue("high_contrast", self.accessibility_settings.high_contrast_cb.isChecked())
        self.settings.setValue("large_text", self.accessibility_settings.large_text_cb.isChecked())
        
        # Save notification settings
        self.settings.setValue("desktop_notifications", self.notification_settings.desktop_notifications_cb.isChecked())
        self.settings.setValue("sound_notifications", self.notification_settings.sound_notifications_cb.isChecked())
        
        # Save data settings
        self.settings.setValue("autosave", self.data_settings.autosave_cb.isChecked())
        self.settings.setValue("save_interval", self.data_settings.save_interval.value())
        
        QMessageBox.information(self, "Settings Saved", 
                              "Your settings have been saved successfully!")
    
    def load_settings(self):
        """Load saved settings"""
        # Load theme settings
        theme = self.settings.value("theme", "Light Theme")
        for button in self.theme_settings.theme_buttons.buttons():
            if button.text() == theme:
                button.setChecked(True)
                break
        
        font_size = int(self.settings.value("font_size", 14))
        self.theme_settings.font_size_slider.setValue(font_size)
        
        animations = self.settings.value("animations", True, type=bool)
        self.theme_settings.animations_cb.setChecked(animations)
        
        # Load accessibility settings
        high_contrast = self.settings.value("high_contrast", False, type=bool)
        self.accessibility_settings.high_contrast_cb.setChecked(high_contrast)
        
        # Load notification settings
        desktop_notif = self.settings.value("desktop_notifications", True, type=bool)
        self.notification_settings.desktop_notifications_cb.setChecked(desktop_notif)
        
        # Load data settings
        autosave = self.settings.value("autosave", True, type=bool)
        self.data_settings.autosave_cb.setChecked(autosave)
    
    def reset_settings(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(self, "Reset Settings",
                                   "Are you sure you want to reset all settings to defaults?",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.settings.clear()
            self.load_settings()
            QMessageBox.information(self, "Settings Reset", 
                                  "All settings have been reset to defaults.")