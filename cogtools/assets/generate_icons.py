"""Generate beautiful app icons for CogTools"""

from PySide6.QtGui import QPixmap, QPainter, QBrush, QPen, QColor, QLinearGradient
from PySide6.QtCore import Qt, QPointF
import os

def create_app_icon(size=512):
    """Create a beautiful app icon"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Create gradient background
    gradient = QLinearGradient(0, 0, size, size)
    gradient.setColorAt(0, QColor(0, 122, 255))  # Apple blue
    gradient.setColorAt(1, QColor(88, 86, 214))  # Indigo
    
    # Draw rounded rectangle background
    painter.setBrush(QBrush(gradient))
    painter.setPen(Qt.NoPen)
    radius = size * 0.22  # Apple-style corner radius
    painter.drawRoundedRect(0, 0, size, size, radius, radius)
    
    # Draw the "C" logo
    painter.setPen(QPen(Qt.white, size * 0.08))
    font = painter.font()
    font.setPixelSize(int(size * 0.5))
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "C")
    
    # Add subtle inner glow
    painter.setPen(QPen(QColor(255, 255, 255, 30), size * 0.02))
    painter.setBrush(Qt.NoBrush)
    painter.drawRoundedRect(size * 0.02, size * 0.02, 
                           size * 0.96, size * 0.96, 
                           radius * 0.95, radius * 0.95)
    
    painter.end()
    return pixmap

def create_tray_icon(size=32):
    """Create a smaller tray icon"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Simple rounded rectangle with solid color
    painter.setBrush(QBrush(QColor(0, 122, 255)))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(4, 4, size-8, size-8, 8, 8)
    
    # Draw the "C"
    painter.setPen(QPen(Qt.white, 2))
    font = painter.font()
    font.setPixelSize(int(size * 0.5))
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "C")
    
    painter.end()
    return pixmap

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Create icons directory
    icons_dir = os.path.dirname(os.path.abspath(__file__)) + "/icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    # Generate app icons in various sizes
    sizes = [16, 32, 64, 128, 256, 512]
    for size in sizes:
        icon = create_app_icon(size)
        icon.save(f"{icons_dir}/app_icon_{size}.png")
        print(f"Created app_icon_{size}.png")
    
    # Generate tray icons
    tray_sizes = [16, 32, 64]
    for size in tray_sizes:
        icon = create_tray_icon(size)
        icon.save(f"{icons_dir}/tray_icon_{size}.png")
        print(f"Created tray_icon_{size}.png")
    
    print("Icons generated successfully!")