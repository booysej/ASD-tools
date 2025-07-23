"""Data management and persistence for CogTools"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from PySide6.QtCore import QObject, Signal, QTimer
import yaml

class DataManager(QObject):
    """Centralized data management for all CogTools plugins"""
    
    data_changed = Signal(str, dict)  # plugin_name, data
    
    def __init__(self):
        super().__init__()
        self.data_dir = Path.home() / ".cogtools"
        self.data_dir.mkdir(exist_ok=True)
        
        self.plugin_data = {}
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.save_all_data)
        self.auto_save_timer.start(30000)  # Auto-save every 30 seconds
        
        self.load_all_data()
    
    def get_data_file(self, plugin_name: str) -> Path:
        """Get the data file path for a plugin"""
        return self.data_dir / f"{plugin_name}.json"
    
    def load_plugin_data(self, plugin_name: str) -> Dict:
        """Load data for a specific plugin"""
        data_file = self.get_data_file(plugin_name)
        
        if data_file.exists():
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading data for {plugin_name}: {e}")
                return {}
        
        return {}
    
    def save_plugin_data(self, plugin_name: str, data: Dict):
        """Save data for a specific plugin"""
        data_file = self.get_data_file(plugin_name)
        
        try:
            # Add metadata
            data_with_meta = {
                'data': data,
                'last_updated': datetime.now().isoformat(),
                'version': '1.0'
            }
            
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(data_with_meta, f, indent=2, ensure_ascii=False)
            
            self.plugin_data[plugin_name] = data
            self.data_changed.emit(plugin_name, data)
            
        except IOError as e:
            print(f"Error saving data for {plugin_name}: {e}")
    
    def get_plugin_data(self, plugin_name: str) -> Dict:
        """Get data for a plugin (from memory cache)"""
        if plugin_name not in self.plugin_data:
            self.plugin_data[plugin_name] = self.load_plugin_data(plugin_name).get('data', {})
        
        return self.plugin_data[plugin_name]
    
    def update_plugin_data(self, plugin_name: str, data: Dict):
        """Update data for a plugin"""
        self.plugin_data[plugin_name] = data
        # Don't save immediately, let auto-save handle it
    
    def load_all_data(self):
        """Load data for all plugins"""
        for data_file in self.data_dir.glob("*.json"):
            plugin_name = data_file.stem
            self.plugin_data[plugin_name] = self.load_plugin_data(plugin_name).get('data', {})
    
    def save_all_data(self):
        """Save all plugin data"""
        for plugin_name, data in self.plugin_data.items():
            if data:  # Only save if there's actually data
                self.save_plugin_data(plugin_name, data)
    
    def export_all_data(self, export_path: Path):
        """Export all data to a single file"""
        try:
            export_data = {
                'export_date': datetime.now().isoformat(),
                'version': '1.0',
                'plugins': {}
            }
            
            for plugin_name in self.plugin_data:
                export_data['plugins'][plugin_name] = self.get_plugin_data(plugin_name)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
    
    def import_data(self, import_path: Path):
        """Import data from a file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            if 'plugins' in import_data:
                for plugin_name, data in import_data['plugins'].items():
                    self.update_plugin_data(plugin_name, data)
                    
                self.save_all_data()
                return True
            else:
                print("Invalid import file format")
                return False
                
        except Exception as e:
            print(f"Error importing data: {e}")
            return False
    
    def clear_all_data(self):
        """Clear all data"""
        self.plugin_data.clear()
        
        # Remove all data files
        for data_file in self.data_dir.glob("*.json"):
            try:
                data_file.unlink()
            except OSError:
                pass
    
    def get_shared_data(self, key: str) -> Any:
        """Get shared data accessible to all plugins"""
        shared_data = self.get_plugin_data('_shared')
        return shared_data.get(key)
    
    def set_shared_data(self, key: str, value: Any):
        """Set shared data accessible to all plugins"""
        shared_data = self.get_plugin_data('_shared')
        shared_data[key] = value
        self.update_plugin_data('_shared', shared_data)

class WorkflowManager(QObject):
    """Manages workflows and automation between plugins"""
    
    workflow_triggered = Signal(str, dict)  # workflow_name, context
    
    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager
        self.workflows = {}
        self.load_workflows()
    
    def load_workflows(self):
        """Load predefined workflows"""
        self.workflows = {
            'focus_session_complete': {
                'triggers': ['pomodoro_finished'],
                'actions': [
                    {'type': 'update_stats', 'plugin': 'exec_function_coach'},
                    {'type': 'suggest_break', 'plugin': 'family_support_compass'},
                    {'type': 'log_achievement', 'plugin': 'memory_vault'}
                ]
            },
            'high_stress_detected': {
                'triggers': ['incident_logged_high_intensity'],
                'actions': [
                    {'type': 'suggest_coping_strategies', 'plugin': 'family_support_compass'},
                    {'type': 'start_cooldown_timer', 'plugin': 'family_support_compass'},
                    {'type': 'create_memory_note', 'plugin': 'memory_vault'}
                ]
            },
            'task_completed': {
                'triggers': ['task_marked_done'],
                'actions': [
                    {'type': 'celebrate_completion', 'plugin': 'exec_function_coach'},
                    {'type': 'update_progress', 'plugin': 'focus_task_manager'},
                    {'type': 'suggest_next_task', 'plugin': 'focus_task_manager'}
                ]
            },
            'daily_review': {
                'triggers': ['end_of_day'],
                'actions': [
                    {'type': 'generate_summary', 'plugin': 'memory_vault'},
                    {'type': 'review_incidents', 'plugin': 'family_support_compass'},
                    {'type': 'plan_tomorrow', 'plugin': 'exec_function_coach'}
                ]
            }
        }
    
    def trigger_workflow(self, trigger_name: str, context: Dict = None):
        """Trigger workflows based on events"""
        context = context or {}
        
        for workflow_name, workflow in self.workflows.items():
            if trigger_name in workflow.get('triggers', []):
                self.execute_workflow(workflow_name, workflow, context)
    
    def execute_workflow(self, workflow_name: str, workflow: Dict, context: Dict):
        """Execute a specific workflow"""
        print(f"Executing workflow: {workflow_name}")
        
        for action in workflow.get('actions', []):
            self.execute_action(action, context)
        
        self.workflow_triggered.emit(workflow_name, context)
    
    def execute_action(self, action: Dict, context: Dict):
        """Execute a single workflow action"""
        action_type = action.get('type')
        plugin = action.get('plugin')
        
        # Log the action for now - in a real implementation, 
        # this would call actual plugin methods
        print(f"Workflow action: {action_type} for plugin {plugin}")
        
        # Store workflow history
        history = self.data_manager.get_shared_data('workflow_history') or []
        history.append({
            'action': action,
            'context': context,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 100 workflow actions
        if len(history) > 100:
            history = history[-100:]
        
        self.data_manager.set_shared_data('workflow_history', history)

class AnalyticsManager:
    """Provides analytics and insights across plugins"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def get_focus_stats(self) -> Dict:
        """Get focus session statistics"""
        exec_data = self.data_manager.get_plugin_data('exec_function_coach')
        
        # Calculate stats from stored data
        sessions = exec_data.get('focus_sessions', [])
        
        return {
            'total_sessions': len(sessions),
            'total_focus_time': sum(s.get('duration', 0) for s in sessions),
            'average_session_length': sum(s.get('duration', 0) for s in sessions) / len(sessions) if sessions else 0,
            'sessions_this_week': len([s for s in sessions if self._is_this_week(s.get('date', ''))]),
            'longest_streak': self._calculate_streak(sessions)
        }
    
    def get_trigger_insights(self) -> Dict:
        """Get insights about triggers and incidents"""
        family_data = self.data_manager.get_plugin_data('family_support_compass')
        incidents = family_data.get('incidents', [])
        
        # Analyze trigger patterns
        trigger_counts = {}
        intensity_by_trigger = {}
        
        for incident in incidents:
            trigger = incident.get('trigger_type', 'Unknown')
            intensity = incident.get('intensity', 0)
            
            trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1
            
            if trigger not in intensity_by_trigger:
                intensity_by_trigger[trigger] = []
            intensity_by_trigger[trigger].append(intensity)
        
        # Calculate average intensities
        avg_intensities = {}
        for trigger, intensities in intensity_by_trigger.items():
            avg_intensities[trigger] = sum(intensities) / len(intensities)
        
        return {
            'total_incidents': len(incidents),
            'most_common_trigger': max(trigger_counts, key=trigger_counts.get) if trigger_counts else None,
            'trigger_frequencies': trigger_counts,
            'average_intensities': avg_intensities,
            'high_intensity_incidents': len([i for i in incidents if i.get('intensity', 0) >= 7])
        }
    
    def get_productivity_insights(self) -> Dict:
        """Get productivity insights from task management"""
        task_data = self.data_manager.get_plugin_data('focus_task_manager')
        tasks = task_data.get('tasks', [])
        
        completed_tasks = [t for t in tasks if t.get('status') == 'done']
        
        return {
            'total_tasks': len(tasks),
            'completed_tasks': len(completed_tasks),
            'completion_rate': len(completed_tasks) / len(tasks) if tasks else 0,
            'tasks_by_priority': self._count_by_field(tasks, 'priority'),
            'overdue_tasks': len([t for t in tasks if self._is_overdue(t)]),
            'average_completion_time': self._calculate_avg_completion_time(completed_tasks)
        }
    
    def _is_this_week(self, date_str: str) -> bool:
        """Check if date is in current week"""
        try:
            date = datetime.fromisoformat(date_str)
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
            return date >= week_start
        except:
            return False
    
    def _calculate_streak(self, sessions: List) -> int:
        """Calculate longest streak of daily sessions"""
        # Simplified streak calculation
        dates = set()
        for session in sessions:
            try:
                date = datetime.fromisoformat(session.get('date', '')).date()
                dates.add(date)
            except:
                continue
        
        if not dates:
            return 0
        
        sorted_dates = sorted(dates)
        max_streak = current_streak = 1
        
        for i in range(1, len(sorted_dates)):
            if (sorted_dates[i] - sorted_dates[i-1]).days == 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        
        return max_streak
    
    def _count_by_field(self, items: List, field: str) -> Dict:
        """Count items by a specific field"""
        counts = {}
        for item in items:
            value = item.get(field, 'Unknown')
            counts[value] = counts.get(value, 0) + 1
        return counts
    
    def _is_overdue(self, task: Dict) -> bool:
        """Check if a task is overdue"""
        try:
            due_date = datetime.fromisoformat(task.get('due_date', ''))
            return due_date < datetime.now() and task.get('status') != 'done'
        except:
            return False
    
    def _calculate_avg_completion_time(self, completed_tasks: List) -> float:
        """Calculate average time to complete tasks"""
        if not completed_tasks:
            return 0
        
        completion_times = []
        for task in completed_tasks:
            try:
                created = datetime.fromisoformat(task.get('created_date', ''))
                completed = datetime.fromisoformat(task.get('completed_date', ''))
                completion_times.append((completed - created).days)
            except:
                continue
        
        return sum(completion_times) / len(completion_times) if completion_times else 0

# Global instances
_data_manager = None
_workflow_manager = None
_analytics_manager = None

def get_data_manager() -> DataManager:
    """Get the global data manager instance"""
    global _data_manager
    if _data_manager is None:
        _data_manager = DataManager()
    return _data_manager

def get_workflow_manager() -> WorkflowManager:
    """Get the global workflow manager instance"""
    global _workflow_manager
    if _workflow_manager is None:
        _workflow_manager = WorkflowManager(get_data_manager())
    return _workflow_manager

def get_analytics_manager() -> AnalyticsManager:
    """Get the global analytics manager instance"""
    global _analytics_manager
    if _analytics_manager is None:
        _analytics_manager = AnalyticsManager(get_data_manager())
    return _analytics_manager