import pandas as pd

print("Starting")

oracle_database = 'oracle-cards.jsonl'                      # "Oracle Cards" dataset from https://scryfall.com/docs/api/bulk-data
creatures_database = 'creatures.jsonl'                      # Output file containing only creature cards

print("Loading database")
df = pd.read_json(oracle_database, lines=True)              # Load the JSONL file into a pandas DataFrame
df = df.filter(
    items=["id", "name", "cmc", "mana_cost", "type_line", "power", "toughness", "oracle_text", "image_uris", "card_faces"]
    )                                                       # Filter the DataFrame to keep only the relevant columns
print("Removing noncreatures")
df = df[df['type_line'].str.contains('Creature', na=False)] # Filter the DataFrame to keep only creature cards
print("Removing tokens")
df = df[df['mana_cost'].str.len() > 0]                      # Filter the DataFrame to remove creature cards that are tokens
print("Saving file")
with open(creatures_database, 'w', encoding='utf-8') as f:  # Write the filtered DataFrame to a new JSONL file
    df.to_json(f, orient='records', lines=True)
    
print("#########################")
print("### CREATURE DATABASE ###")
print("###        READY      ###")
print("#########################")