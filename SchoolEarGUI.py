import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import QTimer, QTime, QDate, Qt
from PySide6.QtGui import QFont, QPixmap

class SoundAlertUI(QWidget):
    def __init__(self):
        super().__init__()

        # UI Style
        self.setStyleSheet("""
        QWidget {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(20, 30, 48, 255), stop:1 rgba(36, 59, 85, 255));
            border-radius: 0px;
            color: white;
        }
        QLabel {
            color: white;
            font-family: 'sans-serif';
            background: transparent;
        }
        """)

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Main Labels
        self.time_label = QLabel(self)
        self.time_label.setFont(QFont("sans-serif", 50, QFont.Bold))
        self.layout.addWidget(self.time_label, alignment=Qt.AlignHCenter)

        self.date_label = QLabel(self)
        self.date_label.setFont(QFont("sans-serif", 18, QFont.Bold))
        self.layout.addWidget(self.date_label, alignment=Qt.AlignHCenter)

        # Alert Display
        self.alert_label = QLabel(self)
        self.alert_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.alert_label)

        # Timers
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

        self.alert_check_timer = QTimer(self)
        self.alert_check_timer.timeout.connect(self.check_for_alert)
        self.alert_check_timer.start(500) 

        self.listening_timer = QTimer(self)
        self.listening_timer.setSingleShot(True)
        self.listening_timer.timeout.connect(self.show_alert)

        self.current_alert = None
        self.update_clock()

    def update_clock(self):
        """Update time and date labels when no alert is active."""
        if not self.current_alert:
            current_time = QTime.currentTime().toString("hh:mm AP")
            current_date = QDate.currentDate().toString("dddd, MMMM d")
            self.time_label.setText(current_time)
            self.date_label.setText(current_date)
            self.alert_label.clear()  

    def check_for_alert(self):
        """Check for incoming sound alerts (replace with real input method)."""
        try:
            with open("alert.txt", "r") as file:
                alert = file.read().strip()
                if alert and alert != self.current_alert:
                    self.start_listening_phase(alert)
        except FileNotFoundError:
            pass

    def start_listening_phase(self, alert_type):
        """Display 'Listening...' before showing the actual alert."""
        self.time_label.setText("Listening...")
        self.date_label.clear()
        self.alert_label.clear()
        self.current_alert = alert_type
        self.listening_timer.start(2000)  

    def show_alert(self):
        """Update UI with sound alert after 'Listening...' phase."""
        icon_map = {
            "fire_alarm": "fire_truck.png",
            "earthquake": "earthquake.png",
            "flag_ceremony": "flag.png",
            "door_knock": "door.png",
            "car_horn": "car.png",
            "ambulance_siren": "ambulance.png",
            "police_siren": "police.png",
            "dog_bark": "dog.png",
            "loud_voice": "voice.png"
        }

        if self.current_alert in icon_map:
            icon_path = icon_map[self.current_alert]
            pixmap = QPixmap(icon_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.alert_label.setPixmap(pixmap)
            self.time_label.setText(f"Alert: {self.current_alert.replace('_', ' ').title()}")
            self.date_label.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = SoundAlertUI()
    ui.resize(500, 300)
    ui.show()
    sys.exit(app.exec())
