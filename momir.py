# MSG to console informing program started
print("Momir Printer Starting...")

# Imports
import RPi.GPIO as GPIO                     # GPIO pin library
GPIO.setmode(GPIO.BCM)                      # Set GPIO pin numbering mode to BCM
import tm1637                               # Display library
from escpos.printer import Serial           # Printer library
import pandas as pd                         # DataFrame (json) library
import sys
from pathlib import Path
from time import sleep

creatures_database = 'creatures.jsonl' # Creature database path
cmc = 0             # Current CMC value
max_cmc = 16        # Maximum CMC value (no creatures over 16 in MTG as for 7.07.2026)
debounce_time = 0.2 # Debounce time for buttons in seconds

# Initialize stuff
df = pd.read_json(creatures_database, lines=True)   # Open database
tm = tm1637.TM1637(clk=4, dio=3)                    # Initialize display
p = Serial(
    devfile='/dev/serial0', baudrate=9600, bytesize=8,
    parity='N', stopbits=1, timeout=1.00, dsrdtr=True
    )                                               # Initialize printer

# Buttons

BUTTON_PLUS = 22
BUTTON_MINUS = 17
BUTTON_PRINT = 27

GPIO.setup(BUTTON_PLUS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_PRINT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_MINUS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Functions

# Write string to display, 6 characters max
def write(string):
    if len(string) > 6:                         # Check string length
        raise ValueError("String too long")
    while len(string) < 6:                      # Pad string with spaces if too short
        string = string + ' '

    towrite = list(string)                      # Rearrange string to match display wiring
    order = [2,1,0,5,4,3]
    towrite[:] = [towrite[i] for i in order]

    string = ''.join(towrite)                   # Encode string and write to display, do not remember
    tm.write(tm.encode_string(string))          # why "join" is needed, but it is

def write_cmc(cmc):
    str_cmc = str(cmc)
    if cmc >= 10:
        towrite = "    " + str_cmc
        write(towrite)
    else:
        towrite = "     " + str_cmc
        write(towrite)

# CMC up
def plus():
    global cmc
    if cmc < max_cmc:
        cmc += 1
    write_cmc(cmc)

# CMC down
def minus():
    global cmc
    if cmc > 0:
        cmc -= 1
    write_cmc(cmc)

# Print random card with current CMC
def print_card(cmc):
    write("Prnt")                                               # MSG to inform that card is being printed
    try:
        card = df[df['cmc'] == cmc].sample(n=1).iloc[0]         # Find random card with current CMC
        image_uri = 0
        filepath = Path("art/" + str(card.get("id")) + ".jpg")   # Get path to card image
        if card['card_faces'] != None:
            if card['image_uris'] == None:  # If card has no multiple faces, take the card itself
                card = card['card_faces'][0]                         # If card has multiple faces, take the first one
                image_uri = card['image_uris']['normal']
                if 'power' not in card or 'toughness' not in card:
                    print_card(cmc)                                  # If card has no power/toughness, try again
                    return
            else:
                image_uri = card['image_uris']['normal']
                card = card['card_faces'][0]

        p.set(align='left', font="a", bold=True)
        p.textln(card['name'])                                  # Print card name

        p.set(align='right', font="a", bold=False)
        p.textln(card['mana_cost'])                             # Print card mana cost


        if filepath.exists():
            p.image(filepath)                                   # Print card art
        else:
            if image_uri == 0:
                image_uri = card['image_uris']['normal']

            p.qr(image_uri, size=5, center=True) # Print QR code with card image URL if no art is found

        p.set(align='left', font="b", bold=True)
        p.textln(card['type_line'])                             # Print card type line

        p.set(align='center', font="b", bold=True)
        p.textln("-----------------------------------")         # Divider

        p.set(align='left', font="b", bold=False)
        p.textln(card['oracle_text'])                           # Print card oracle text

        p.set(align='right', font="a", bold=True)
        p.textln(f"{card['power']}/{card['toughness']}")        # Print card power/toughness

        p.ln(3)                                                 # Print 3 empty lines to finish the card

        write_cmc(cmc)                                         # Display CMC again
    
    except Exception as e:
        print(f"Error printing card: {e}")
        write("error")


print(
    "Momir Printer Ready. Use buttons to change CMC or print a card."
      )         # MSG to console informing program is ready
print(
    "Pres \"+\" and \"-\" together to exit program."
      )
write_cmc(cmc)  # Initialize display

# Main loop

while True:
    if GPIO.input(BUTTON_PLUS) == GPIO.HIGH:
        plus()
        sleep(debounce_time)
    if GPIO.input(BUTTON_MINUS) == GPIO.HIGH:
        minus()
        sleep(debounce_time)
    if GPIO.input(BUTTON_PRINT) == GPIO.HIGH:
        print_card(cmc)
        sleep(debounce_time)
    if GPIO.input(BUTTON_MINUS) == GPIO.HIGH & GPIO.input(BUTTON_PLUS) == GPIO.HIGH:
        write("")
        GPIO.cleanup()
        sys.exit("Bye!")
