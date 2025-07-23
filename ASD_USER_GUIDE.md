# CogTools: A Practical Guide for Users with ASD Level 1

## 🧠 Understanding This Guide

This tutorial is designed specifically for users with Autism Spectrum Disorder (ASD) Level 1. It provides:
- **Clear, direct instructions** without ambiguous language
- **Visual organization** to leverage your visual-spatial strengths
- **Step-by-step processes** to compensate for working memory challenges
- **Practical tips** based on common ASD experiences

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Understanding CogTools for ASD](#understanding-cogtools-for-asd)
3. [Setting Up Your Environment](#setting-up-your-environment)
4. [Using Each Plugin Effectively](#using-each-plugin-effectively)
5. [Customization Tips](#customization-tips)
6. [Troubleshooting](#troubleshooting)
7. [Daily Routines & Best Practices](#daily-routines--best-practices)

---

## 🚀 Quick Start

### What You Need to Know First
- CogTools runs quietly in your system tray (the icon area near your clock)
- It's designed to help with executive function, memory, and task management
- Everything is customizable to reduce sensory overload

### Installation in 5 Steps

1. **Open Terminal/Command Prompt**
   ```bash
   # Windows: Press Win+R, type "cmd", press Enter
   # Mac: Press Cmd+Space, type "terminal", press Enter
   # Linux: Press Ctrl+Alt+T
   ```

2. **Navigate to the CogTools folder**
   ```bash
   cd /workspace  # Or wherever you saved CogTools
   ```

3. **Create a virtual environment** (keeps things organized)
   ```bash
   python -m venv .venv
   ```

4. **Activate the environment**
   ```bash
   # Windows:
   .venv\Scripts\activate
   
   # Mac/Linux:
   source .venv/bin/activate
   ```

5. **Install and run**
   ```bash
   pip install -r requirements.txt
   python -m cogtools
   ```

**💡 ASD Tip:** Save these commands in a text file for easy reference. Working memory challenges mean you shouldn't have to remember them.

---

## 🎯 Understanding CogTools for ASD

### Why CogTools Works Well for ASD Level 1

1. **Predictable Interface**
   - No sudden changes or surprises
   - Consistent layout across all tools
   - Clear visual hierarchy

2. **Reduces Cognitive Load**
   - Offloads memory tasks to the computer
   - Provides visual reminders
   - Breaks complex tasks into steps

3. **Customizable Sensory Experience**
   - Adjust colors and contrast
   - Disable animations
   - Control notification sounds

### Core Concepts (Direct Explanations)

- **System Tray**: The small icon that appears near your clock. Click it to access tools.
- **Plugins**: Individual tools for specific needs (tasks, memory, coding, etc.)
- **YAML Files**: Plain text files that store your data. You can edit them manually if needed.

---

## 🛠️ Using Each Plugin Effectively

### 1. Focus Task Manager

**What it does:** Helps break down tasks into manageable pieces

**Perfect for ASD because:**
- Visual Kanban board leverages your visual-spatial strengths
- Clear task states (To Do → Doing → Done)
- No ambiguous priorities

**How to use effectively:**

1. **Create specific, concrete tasks**
   ```
   ❌ Bad: "Work on project"
   ✅ Good: "Write introduction paragraph for report (300 words)"
   ```

2. **Add context to each task**
   - What exactly needs to be done
   - Any specific requirements
   - Deadline (if applicable)

3. **Use the timer feature**
   - Set specific work periods (e.g., 25 minutes)
   - Take regular breaks to prevent overwhelm

**💡 ASD Tip:** Your strong logical reasoning means you excel at breaking down complex problems. Use this strength by creating detailed subtasks.

### 2. Memory Vault

**What it does:** External memory storage for important information

**Perfect for ASD because:**
- Compensates for working memory challenges
- Searchable reference system
- Reduces anxiety about forgetting

**Effective strategies:**

1. **Create categories that make sense to YOU**
   ```
   /work/meetings/
   /work/procedures/
   /personal/routines/
   /personal/social-scripts/
   ```

2. **Store social scripts and templates**
   ```markdown
   # Email Templates
   
   ## Asking for clarification
   Subject: Clarification needed on [topic]
   
   Hi [Name],
   
   I want to make sure I understand [topic] correctly.
   Could you please clarify:
   1. [Specific question 1]
   2. [Specific question 2]
   
   Thank you,
   [Your name]
   ```

3. **Document patterns you notice**
   - Social situations and outcomes
   - Successful communication strategies
   - Task completion methods that work

**💡 ASD Tip:** Use your pattern recognition abilities to identify what works and document it for future reference.

### 3. Visual Coding Helper

**What it does:** Converts ideas into visual flowcharts and code

**Perfect for ASD because:**
- Leverages visual thinking strengths
- Provides clear, logical structure
- Reduces ambiguity in planning

**Best practices:**

1. **Start with flowcharts before coding**
   - Map out logic visually
   - Identify edge cases
   - Plan error handling

2. **Use consistent naming conventions**
   ```python
   # Clear, descriptive names
   def calculate_user_score(user_data, scoring_rules):
       # Not: def calc(u, r):
   ```

3. **Comment your reasoning**
   ```python
   # Using explicit comparison because implicit boolean
   # conversion can be ambiguous
   if user_input is not None:
       process_input(user_input)
   ```

**💡 ASD Tip:** Your superior fluid reasoning makes you excellent at logical problem-solving. Document your thought process to help when working memory fails.

### 4. Executive Function Coach

**What it does:** Helps with planning, time management, and routine building

**Perfect for ASD because:**
- Creates predictable structure
- Reduces decision fatigue
- Provides clear next steps

**Optimization strategies:**

1. **Build detailed routines**
   ```yaml
   morning_routine:
     - time: "7:00"
       task: "Wake up"
       duration: 5
     - time: "7:05"
       task: "Shower (warm, not hot)"
       duration: 10
       notes: "Use unscented soap to avoid sensory issues"
   ```

2. **Plan for transitions**
   - Add buffer time between activities
   - Include sensory breaks
   - Prepare for context switches

3. **Create contingency plans**
   ```yaml
   if_routine_disrupted:
     - Take 3 deep breaths
     - Check priority list
     - Start with smallest task
     - Message supervisor if needed
   ```

**💡 ASD Tip:** Routines reduce anxiety and cognitive load. The more detailed, the better.

### 5. Family Support Compass

**What it does:** Helps navigate family dynamics and communication

**Perfect for ASD because:**
- Provides scripts for difficult conversations
- Tracks family patterns and preferences
- Reduces social guesswork

**Practical applications:**

1. **Document family member preferences**
   ```yaml
   family_profiles:
     spouse:
       communication_style: "direct"
       preferred_contact: "text"
       triggers: "being interrupted"
       interests: "gardening, mystery novels"
   ```

2. **Plan for social events**
   - Expected duration
   - Quiet spaces available
   - Exit strategies
   - Post-event recovery time

3. **Track successful interactions**
   - What worked well
   - What caused stress
   - Adjustments for next time

---

## ⚙️ Customization Tips

### Sensory Adjustments

1. **Reduce visual stimulation**
   ```python
   # In settings_panel:
   visual_settings:
     animations: false
     transparency: 0  # Solid backgrounds
     color_scheme: "high_contrast"
   ```

2. **Control notifications**
   ```python
   notifications:
     sound: false  # Or use gentle sounds
     visual_only: true
     group_similar: true  # Reduce interruptions
   ```

3. **Simplify interface**
   - Hide unused features
   - Increase font size
   - Use consistent colors

### Workflow Optimization

1. **Create keyboard shortcuts**
   ```python
   shortcuts:
     quick_task: "Ctrl+T"
     search_memory: "Ctrl+M"
     toggle_timer: "Ctrl+Space"
   ```

2. **Automate repetitive tasks**
   - Daily report generation
   - Task archiving
   - Backup reminders

3. **Set up templates**
   - Meeting notes
   - Project structures
   - Communication formats

---

## 🔧 Troubleshooting

### Common Issues and Direct Solutions

1. **"System tray icon not appearing"**
   - **Windows**: Check notification area settings
   - **Mac**: Check menu bar space
   - **Linux**: Install system tray support for your desktop

2. **"Too many notifications"**
   ```python
   # Reduce to essentials only
   notifications:
     task_complete: false
     only_important: true
     batch_period: 30  # Group notifications every 30 min
   ```

3. **"Interface feels overwhelming"**
   - Start with one plugin at a time
   - Disable animations
   - Use keyboard navigation

4. **"Can't remember commands"**
   - Create a `commands.txt` file on your desktop
   - Use the visual interface instead
   - Set up aliases for common actions

---

## 📅 Daily Routines & Best Practices

### Morning Setup (5 minutes)
1. Open CogTools
2. Review today's tasks
3. Check memory vault for important info
4. Set first timer

### During Work
- **Every 25 minutes**: Take a sensory break
- **Before meetings**: Review relevant notes
- **After interactions**: Log what worked/didn't work

### End of Day (10 minutes)
1. Archive completed tasks
2. Plan tomorrow's first task
3. Update memory vault with new learnings
4. Close CogTools properly

### Weekly Maintenance
- Review and adjust routines
- Clean up old tasks
- Backup your data
- Update successful scripts/templates

---

## 💪 Leveraging Your ASD Strengths

### Your Advantages:
1. **Superior logical reasoning** → Design complex workflows
2. **Pattern recognition** → Identify and optimize processes
3. **Attention to detail** → Create comprehensive documentation
4. **Visual thinking** → Use flowcharts and diagrams extensively

### Compensating for Challenges:
1. **Working memory** → Write everything down immediately
2. **Processing speed** → Build in extra time, use templates
3. **Social communication** → Create and test scripts
4. **Sensory sensitivities** → Customize everything

---

## 🎯 Final Tips

1. **Be patient with yourself** - It takes time to build effective systems
2. **Iterate regularly** - What works today might need adjustment tomorrow
3. **Document everything** - Your future self will thank you
4. **Ask for specific help** - "How do I..." instead of "This doesn't work"
5. **Celebrate systematic thinking** - Your logical approach is a strength

---

## 📚 Additional Resources

- **Technical Support**: Create detailed bug reports with exact steps
- **Feature Requests**: Describe your specific use case
- **Community**: Find other ASD users who share configurations

Remember: CogTools is a tool to support you, not another source of stress. Customize it until it feels right for your unique needs.

---

*This guide is a living document. Update it with your own discoveries and optimizations.*