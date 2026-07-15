import pandas as pd
import urllib.request
from PIL import Image
from pathlib import Path
from datetime import datetime

printer_width = 384                                 # Pixel width of printer

creatures_database = 'creatures.jsonl'              # File with cards to download images for
df = pd.read_json(creatures_database, lines=True)   # Load the JSONL file into a pandas DataFrame
df = df.reset_index()                               # Make sure index is normal

cards_to_process = len(df)
cards_processed = 0
progress = 0
errors = 0
startTime = datetime.now()

for i in range(len(df)):                           # Go over every card
    try:
        card = df.iloc[i]
        filename = "art/" + str(card.get("id")) + ".jpg"        # Images will be accessed wia card ID, so make filname out of it

        if Path(filename).exists():
            cards_processed += 1                                # Skip if image already exists
            continue

        if card['card_faces'] != None:                          # Handling DFCs
            if card['image_uris'] == None:
                card = card['card_faces'][0]
                image_uri = card['image_uris']['normal']
                if 'power' not in card or 'toughness' not in card:
                    cards_processed += 1
                    continue
            else:
                image_uri = card['image_uris']['normal']

        image_uri = card['image_uris'].get('art_crop')          # Find correct URI
        urllib.request.urlretrieve(image_uri, filename)         # Download image

        image = Image.open(filename)                            # Open for editing
        w = (printer_width / float(image.size[0]))              # Calculations to keep proportion of image
        h = int((float(image.size[1]) * float(w)))              
        image = image.resize((printer_width, h), Image.Resampling.LANCZOS).convert('1')  # Resize image and convert to B&W
        image.save(filename, "JPEG")                            # Save image
        cards_processed += 1
        if cards_processed % 20 == 0:
            progress = int((cards_processed * 100) / cards_to_process)
            print(f"Progress: {progress}%, {cards_processed}/{cards_to_process}")

    except Exception as e:
        errors += 1
        print(f"Error preparing image card: {e}")
        print(f"Error with card: {card['name']}")
        print(f"{errors} errors out of {cards_processed} cards.")
        continue

rate = 100 - ((errors * 100) / cards_processed)
print("#########################")
print("### IMAGES DOWNLOADED ###")
print("###   AND PREPARED    ###")
print("#########################")
print(f"Processing time: {datetime.now() - startTime}")
print(f"Problems with {errors} out of {cards_processed} processed cards.")
print(f"Success rate: {rate}%")
