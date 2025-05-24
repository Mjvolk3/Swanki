#!/usr/bin/env python3
"""
Script to retrieve card data from Anki via AnkiConnect.
Extracts all cards from the specified deck and prints their full JSON data.
"""

import json
import requests
import sys

def anki_connect(action, **params):
    """Make a request to AnkiConnect API"""
    payload = {
        "action": action,
        "version": 6,
        "params": params
    }
    response = requests.post("http://localhost:8765", json=payload)
    try:
        return response.json()
    except json.JSONDecodeError:
        print(f"Error: Failed to decode response: {response.text}")
        sys.exit(1)

def get_notes_from_deck(deck_name):
    """Get all notes from a specific deck"""
    # Construct the query for finding notes in the specified deck
    query = f'deck:"{deck_name}"'
    
    # Find all note IDs matching the query
    response = anki_connect("findNotes", query=query)
    if not response.get("result"):
        print(f"No notes found in deck: {deck_name}")
        return []
    
    note_ids = response["result"]
    print(f"Found {len(note_ids)} notes in deck: {deck_name}")
    
    # Get detailed info for each note
    response = anki_connect("notesInfo", notes=note_ids)
    if "result" not in response:
        print(f"Error retrieving note info: {response}")
        return []
    
    return response["result"]

def main():
    # The deck we want to query
    deck_name = "swanki::radivojevicMachineLearningAutomated2020"
    
    # Get all notes in the deck
    notes = get_notes_from_deck(deck_name)
    
    # Check if AnkiConnect is running
    if not notes and not anki_connect("version")["result"]:
        print("Error: AnkiConnect not available. Ensure Anki is running with AnkiConnect addon.")
        sys.exit(1)
    
    # Save the results to a file
    output_file = "anki_cards_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)
    
    print(f"Retrieved {len(notes)} notes. Data saved to {output_file}")
    
    # Print some basic information about each note
    print("\nSummary of retrieved notes:")
    for i, note in enumerate(notes):
        model = note.get("modelName", "Unknown model")
        fields = note.get("fields", {})
        
        # For Basic model cards, get front text
        if "Front" in fields:
            front_text = fields["Front"]["value"]
            front_preview = front_text[:50] + "..." if len(front_text) > 50 else front_text
            print(f"\nNote {i+1}: {model}")
            print(f"  Front: {front_preview}")
            print(f"  Note ID: {note.get('noteId')}")
            print(f"  Tags: {note.get('tags', [])}")

if __name__ == "__main__":
    main()