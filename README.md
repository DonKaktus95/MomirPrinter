# MomirPrinter
## What is this?
The box does one thing: prints out a random creature from Magic: The Gathering that is given mana value (also known as "converted mana cost" or "CMC").
That is needed to play MTG format known as "Momir Basic" or "Momir Vig" in physical form, which used to be possible to play only using digital game clients, due to the fact that any of almost 20.000 creatures from MTG history may be randomly chosen to get summoned.

For rules, history and general good time I strongly recommend watching [this great video by Rhystic Studies on YouTube](https://youtu.be/UA_lhvMBj6c "
Momir Vig | Magic's Luckiest Minigame"), as going more into it is out of scope for this document.

Going forward, I assume the reader has basic understanding of how to:
- work with Raspberry Pi
- read and run Python code
- work with simple electronics

If you are completely new to some or all of the subjects, I suggest familiarising yourself with them at even the most entry level before continuing.
## How-to
### What do you need
- Raspberry Pi - my final version is using model 3B+, but for most of development I used very old B rev.1, so any should do (keep in mind newer ones will work smoother and faster)
- Thermal printer - in my case a cheap CSN-A5 from AliExpress, just make sure that it has serial port connection
- Buttons
- Screen - in my case TM1637 based 7-segment, 6-digit LED display, but even 2 digit would be enough
- Power supply - Raspberry Pi and printer work on 5V, 3A should be enough to power both 
- Some other basic electronic components to connect all of the above
- Something to keep it together - print box I designed for the build [available here on Printables](https://www.printables.com/model/1782320-printer-for-momir-basic "Printer box design on Printables"), design one yourself to better fit your components and style, or wrap it around with duct tape - we don't judge here
### Putting it together
Refer to "connection_diagram.png" and Your own common sense. I believe in You.
### What about the code?
Going file-by-file:
1. creatures_from_json.py - prepares jsonl with all the info about cards that main program then uses.
First download the ["Oracle Cards" file from Scryfall](https://scryfall.com/docs/api/bulk-data "Find and download Oracle Cards"), then change the name to "oracle-cards.jsonl". Then run the script and upload generated "creatures.jsonl" to RasPi (theoretically can be used on RasPi directly, but I encountered some issues with the script crashing in that case so I decided on generating the file on PC and then uploading - may work better for You). Repeat the process when new sets are released to keep the database up to date.
2. dl_card_art.py - downloads and formats card art for all the creatures included in database from the previous step. Definitely can be run directly on RasPi to avoid copying over 1GB of images from computer to the device. When run for the first time it took just under 2h to process everything, but when run again to add cards from updated database it skips already existing ones.
3. momir.py - main script that actually handles the printing. Basic controls are simple:
	- Use buttons to select CMC of desired creature, ranging from 0 to 16 (as for now there are no creature with higher CMC).
	- Press third button to print random creature.
	- If you hold both "+" and "-" buttons together the program will exit. Try to not do that when playing as it will probably require turning the RasPi off and on again, but can be useful for testing when messing around with the code.
### Running on startup
There are couple ways to run a Python program on startup of Raspberry Pi, with the "most correct" as far I can tell being utilising systemd service:
1. Replace placeholders in "momirprint.service" and "momir_start.sh" with correct paths to whatever file or directory they say
2. Put "momir_start.sh" anywhere really, but the same dir as all .py files makes most sense
3. Put "momirprint.service" in /etc/systemd/system/
4. Run following commands:

	`sudo systemctl daemon-reload` - updates systemd’s internal data
	
	`sudo systemctl enable momirprint` - enables the service
	
	Now the main program will start automagically when Raspberry Pi turns on.
5. (optional) Test if the service works correctly:

	`sudo systemctl start momirprint` - starts the service manually

	`systemctl status momirprint` - show info about the service - if the service fails and errors are reported act accordingly to fix
	
And that’s it. Go grab some basic lands, a buddy to play with and have fun. Or just play around printing random creatures You probably have never seen before.
## Known issues
- Transforming cards that have a non-creature in the front and creature in the back are included in generated "creatures.jsonl" (example: [Azusa's Many Journeys](https://scryfall.com/card/neo/172/azusas-many-journeys-likeness-of-the-seeker "Azusa's Many Journeys")). Those are not used in Momir Basic as for tokens only front face exists. Art for them is not downloaded and they can not be rolled to be printed using some workarounds, but it does annoy me personally.
- Cards that have 2 cards on the front only get the creature part printed. This is not an issue with cards with adventure (example: [Amethyst Dragon](https://scryfall.com/card/clb/160/amethyst-dragon-explosive-crystal "Amethyst Dragon")) as you are not able to cast the instant/sorcery part anyway. On the other hand, the new cards with "prepare" (example: [Abigale, Poet Laureate](https://scryfall.com/card/sos/170/abigale-poet-laureate-heroic-stanza "Abigale, Poet Laureate")) which spell can be cast with them on the board unfortunately require a manual Scryfall search to see what exactly they do.
## Disclaimers
I am not a programmer, have close to zero electronics knowledge, I mess around Raspberry Pies and 3D printers as a hobby. This project was quite a trip and I learned a lot along the way. I am fully aware that every aspect here may be riddled with small and big mistakes, bad optimisations or decisions - feel free to play around, correct and expand on anything and everything I have shared.

No "AI" was used when working on this project. Only documentations, similar projects, and a lot of trial and error - that’s the most fun way.

Hope any of this was useful to you, whether that was to recreate it exactly, find inspiration or just checking it out for curiosity sake.

Now go - learn stuff and build something cool. It is fun, trust me.
