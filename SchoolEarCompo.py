import time
import spidev
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Setup GPIO for ePaper Display
EPD_CS = 8
EPD_DC = 25
EPD_RST = 17
EPD_BUSY = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(EPD_RST, GPIO.OUT)
GPIO.setup(EPD_DC, GPIO.OUT)
GPIO.setup(EPD_BUSY, GPIO.IN)

# SPI setup
spi = spidev.SpiDev(0, 0)
spi.max_speed_hz = 2000000

# Load font (Make sure the .ttf font file exists in the directory)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_LARGE = ImageFont.truetype(FONT_PATH, 48)
FONT_SMALL = ImageFont.truetype(FONT_PATH, 18)

# Function to update the TFT display with the current time
def display_clock():
    while True:
        # Create a new blank image (black/white)
        img = Image.new('1', (296, 128), 255)  # 2.9" Display resolution
        draw = ImageDraw.Draw(img)

        # Get current time
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")  # Format: HH:MM AM/PM
        date_str = now.strftime("%A, %B %d")  # Format: Wednesday, June 15

        # Draw time and date on the display
        draw.text((50, 30), time_str, font=FONT_LARGE, fill=0)
        draw.text((60, 90), date_str, font=FONT_SMALL, fill=0)

        # Send to ePaper display
        update_display(img)

        time.sleep(1)  # Update every second

# Function to send image data to TFT display
def update_display(image):
    """Sends the processed image to the ePaper Display."""
    # Your specific TFT update function here
    pass  # Replace with actual display driver logic

if __name__ == "__main__":
    try:
        display_clock()
    except KeyboardInterrupt:
        print("Clock mode stopped.")
