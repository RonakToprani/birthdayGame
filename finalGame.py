import sys
import random
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF, QObject, pyqtSignal, QSize, QUrl
from PyQt6.QtGui import QPixmap, QPainter, QKeyEvent, QBrush, QColor, QFont, QPalette, QIcon
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton, QGridLayout, QMessageBox
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput



app_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else '.'


class SpaceTheme(QWidget):
    def __init__(self):
        super().__init__()
        self.background_color = QColor(0, 0, 0)
        self.stars_color = QColor(255, 255, 255)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw background
        painter.setBrush(QBrush(self.background_color))
        painter.drawRect(self.rect())

        # Draw stars
        self.draw_stars(painter)

    def draw_stars(self, painter):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.stars_color))

        for _ in range(100):
            x = random.randint(0, self.width())
            y = random.randint(0, self.height())
            painter.drawEllipse(QPointF(x, y), 1, 1)
    
    app = QApplication(sys.argv)
class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(" Tishya Birthday Gaming Fest ")
        self.setGeometry(100, 100, 400, 400)

        self.space_theme = SpaceTheme()
        self.setCentralWidget(self.space_theme)
        
        self.game1_button = QPushButton("Heart Catcher", self)
        self.game1_button.clicked.connect(self.start_game1)
        self.game1_button.setGeometry(100, 150, 200, 40)

        self.game2_button = QPushButton("Matching Plaza", self)
        self.game2_button.clicked.connect(self.start_game2)
        self.game2_button.setGeometry(100, 200, 200, 40)
        
      
         
    def start_game1(self):
       
        game1 = HeartGame()


       

        game1.show()

        
             
    def start_game2(self):
        game2 = MatchingPlaza()
        game2.return_to_menu.connect(self.show)
        game2.show()
        
    


class HeartGame(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tishya's Heart Catcher")
        self.setGeometry(100, 100, 400, 400)

        self.background_color = QColor(255, 255, 255)
        self.tishya_pixmap = QPixmap(f"{app_path}/PhotoQ.jpg")
        self.heart_pixmap = QPixmap(f"{app_path}/heart.jpg")

        self.tishya_position = QRectF(180, 300, 40, 40)
        self.heart_position = QRectF(180, 0, 40, 40)

        self.score = 0
        self.score_label = QLabel(self)
        self.update_score_label()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(7)

        self.fall_speed = 2
        self.is_alive = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw background
        painter.setBrush(QBrush(self.background_color))
        painter.drawRect(self.rect())

        # Draw Tishya or a message if she lost
        if self.is_alive:
            painter.drawPixmap(QRectF(self.tishya_position).toRect(), self.tishya_pixmap)
        else:
            pixmap_scaled = self.tishya_pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
            painter.drawPixmap(QRectF(self.tishya_position).toRect(), pixmap_scaled)

        # Draw heart
        painter.drawPixmap(QRectF(self.heart_position).toRect(), self.heart_pixmap)

    def keyPressEvent(self, event):
        if self.is_alive:
            if event.key() == Qt.Key.Key_Left:
                self.tishya_position.translate(-10, 0)
            elif event.key() == Qt.Key.Key_Right:
                self.tishya_position.translate(10, 0)
        
        self.update()

    def update_game(self):
        if self.is_alive:
            self.heart_position.translate(0, self.fall_speed)

            if self.heart_position.intersects(self.tishya_position):
                self.score += 1
                self.update_score_label()
                self.reset_heart()
                self.increase_fall_speed()

            if self.heart_position.bottom() >= self.height():
                self.is_alive = False
                self.show_loss_message()

            # Wrap the heart around the window
            if self.heart_position.right() < 0:
                self.heart_position.moveLeft(self.width())
            elif self.heart_position.left() > self.width():
                self.heart_position.moveRight(0)

            # Wrap Tishya around the window
            if self.tishya_position.right() < 0:
                self.tishya_position.moveLeft(self.width())
            elif self.tishya_position.left() > self.width():
                self.tishya_position.moveRight(0)

        self.update()

    def reset_heart(self):
        x = random.randint(0, self.width() - self.heart_pixmap.width())
        y = random.randint(-self.height(), -self.heart_pixmap.height())
        self.heart_position.moveTopLeft(QPointF(x, y))

    def increase_fall_speed(self):
        if self.score % 5 == 0:
            self.fall_speed += 0.2

    def update_score_label(self):
        self.score_label.setText(f"Score: {self.score}")
        self.score_label.setStyleSheet(
            "font-size: 24px; color: white; background-color: rgba(0, 0, 0, 0.5); padding: 5px;")
        self.score_label.adjustSize()
        self.score_label.move(10, 10)

    def show_loss_message(self):
        loss_window = QMainWindow(self)
        loss_window.setWindowTitle("Oops! You Lost")
        loss_window.setGeometry(200, 200, 400, 200)

        central_widget = QWidget()
        loss_window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        message_label = QLabel("Oops! You Lost 🤕. But try again, and I bet you'll win! ❤️", loss_window)
        message_label.setStyleSheet(
            "font-size: 18px; color: white; background-color: rgba(255, 192, 203, 0.8); padding: 20px;"
        )
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message_label)

        restart_button = QPushButton("Restart Game", loss_window)
        restart_button.clicked.connect(self.restart_game)
        layout.addWidget(restart_button)

        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, self.background_color)
        loss_window.setPalette(palette)

        loss_window.show()

    def restart_game(self):
        self.is_alive = True
        self.score = 0
        self.fall_speed = 2
        self.update_score_label()
        self.timer.start(7)
        self.reset_heart()

        # Close the loss window if it exists
        for widget in QApplication.topLevelWidgets():
            if widget.windowTitle() == "Oops! You Lost":
                widget.close()
   

class MatchingPlaza(QMainWindow):
        return_to_menu  = pyqtSignal()

        def __init__(self):
            super().__init__()

            self.setWindowTitle("matchin' plaza")
            self.setFixedSize(700, 700)  # Adjust the window size to accommodate square grid

            # Set the background color
            palette = self.palette()
            palette.setColor(QPalette.ColorRole.Window, QColor("#F9E8E2"))  # Warm tone
            self.setPalette(palette)

            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)

            self.layout = QVBoxLayout(self.central_widget)
            self.grid_layout = QGridLayout()
            self.grid_layout.setSpacing(30)  # Set spacing between cells
            self.layout.addLayout(self.grid_layout)

            self.cards = []
            self.images = [f"{app_path}/PhotoX.jpg", f"{app_path}/PhotoY.jpg", f"{app_path}/PhotoP.jpg", f"{app_path}/PhotoQ.jpg",  f"{app_path}/PhotoR.jpg",  f"{app_path}/PhotoS.jpg"] * 2  # Duplicate the images for pairs
            random.shuffle(self.images)

            self.create_cards()

            self.first_card = None
            self.locked = False
                
            # Set the font and styles for the labels
            font = QFont()
            font.setPointSize(14)
            font.setItalic(True)


            # Add a label for the game title
            self.title_label = QLabel("match-shatch mauj karo!")
            self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.title_label.setFont(font)
            self.layout.addWidget(self.title_label)

            # Add a label for the instructions
            self.instructionslabel = QLabel("Click on the cards to reveal the images and determine the matching pairs!")
            self.instructionslabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.instructionslabel.setFont(font)
            self.layout.addWidget(self.instructionslabel)

        def create_cards(self):
            grid_size = 3
            num_photos = len(self.images)
            num_pairs = num_photos // 2
            max_cards = min(grid_size * 4, num_pairs * 2)

            for i in range(max_cards):
                card = QPushButton()
                card.setFixedSize(150, 150)
                card.setStyleSheet(
                    "QPushButton { background-color: #FFDCC1; border: none; border-radius: 10px; }"
                    "QPushButton:disabled { background-color: #FADAC6; }"
                )
                icon_size = QSize(card.size().width() - 20, card.size().height() - 20)
                card.setIconSize(icon_size)
                card.clicked.connect(lambda _, row=i // 4, col=i % 4: self.card_clicked(row, col))
                self.grid_layout.addWidget(card, i // 4, i % 4)
                self.cards.append(card)

        def card_clicked(self, row, col):
            if self.locked:
                return

            card_index = row * 4 + col
            card = self.cards[card_index]

            if card.isEnabled():
                image_path = self.images[card_index]

                pixmap = QPixmap(image_path)
                icon = QIcon(pixmap.scaled(card.iconSize(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                card.setIcon(icon)
                card.setDisabled(True)

                if self.first_card is None:
                    self.first_card = (card, image_path)
                else:
                    second_card = (card, image_path)
                    self.locked = True
                    self.compare_cards(self.first_card, second_card)

        def compare_cards(self, first_card, second_card):
            if first_card[1] == second_card[1]:
                first_card[0].setDisabled(True)
                second_card[0].setDisabled(True)
                self.check_game_over()
            else:
                first_card[0].setIcon(QIcon())
                second_card[0].setIcon(QIcon())
                first_card[0].setEnabled(True)
                second_card[0].setEnabled(True)

            self.first_card = None
            self.locked = False

        def check_game_over(self):
            flipped_cards = [card for card in self.cards if not card.isEnabled()]
            if len(flipped_cards) == len(self.cards):
                # All cards are flipped, show a message box with the appropriate message
                message_box = QMessageBox()
                message_box.setWindowTitle("Game Over!")

                if self.check_winning_condition():
                    message_box.setText("OMG GURL YOU WON!")
                else:
                    message_box.setText("OOPS GURL YOU LOST :( TRY AGAIN!")

                message_box.exec()

        def check_winning_condition(self):
            # Check if all cards are matched
            for card in self.cards:
                if card.isEnabled():
                    return False
            return True



       

if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    game = HeartGame()
    game.show()
    filename = f"{app_path}/music.mp3"
    player = QMediaPlayer()
    audio_output = QAudioOutput()
    player.setAudioOutput(audio_output)
    player.setSource(QUrl.fromLocalFile(filename))
    player.play()

    app.exec()

