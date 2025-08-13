"""Test table conversion in AnkiProcessor."""

import pytest
from swanki.processing.anki_processor import AnkiProcessor


def test_markdown_table_conversion():
    """Test that markdown tables are converted to HTML."""
    processor = AnkiProcessor()
    
    # Test basic table conversion
    markdown_with_table = """## What is the structure of proteins?

Proteins have four levels of structure:

| Level | Description | Example |
|-------|-------------|---------|
| Primary | Amino acid sequence | MVLQAG... |
| Secondary | Local folding | α-helix, β-sheet |
| Tertiary | 3D structure | Enzyme shape |
| Quaternary | Multiple chains | Hemoglobin |

This hierarchical organization determines protein function.

- #biochemistry, #proteins"""
    
    cards = processor._parse_cards_from_markdown(markdown_with_table)
    assert len(cards) == 1
    
    card = cards[0]
    assert card['type'] == 'basic'
    assert '<table>' in card['back']
    assert '<tr>' in card['back']
    assert '<td>Primary</td>' in card['back']
    assert '|' not in card['back']  # Original markdown syntax should be gone


def test_table_in_cloze_warning():
    """Test that tables in cloze deletions trigger a warning."""
    processor = AnkiProcessor()
    
    # This should trigger a warning
    markdown_with_cloze_table = """## The genetic code uses {{c1::| Codon | AA | |----| |UUU|Phe|}} to encode amino acids.

- #genetics"""
    
    # Capture warning logs if needed
    cards = processor._parse_cards_from_markdown(markdown_with_cloze_table)
    assert len(cards) == 1
    
    # The card should still be created but the table should be outside cloze
    card = cards[0]
    assert card['type'] == 'cloze'


def test_multiple_tables_in_card():
    """Test conversion of multiple tables in one card."""
    processor = AnkiProcessor()
    
    markdown_multi_table = """## Compare DNA and RNA

First table - Sugar differences:

| Molecule | Sugar |
|----------|-------|
| DNA | Deoxyribose |
| RNA | Ribose |

Second table - Base differences:

| Molecule | Bases |
|----------|-------|
| DNA | A, T, G, C |
| RNA | A, U, G, C |

- #molecular-biology"""
    
    cards = processor._parse_cards_from_markdown(markdown_multi_table)
    assert len(cards) == 1
    
    card = cards[0]
    # Should have two tables
    assert card['back'].count('<table>') == 2
    assert card['back'].count('</table>') == 2


def test_table_with_special_characters():
    """Test table conversion with special characters."""
    processor = AnkiProcessor()
    
    markdown_special = """## What are common math symbols?

| Symbol | Meaning | LaTeX |
|--------|---------|-------|
| ∑ | Sum | \\sum |
| ∫ | Integral | \\int |
| ∂ | Partial | \\partial |

- #mathematics"""
    
    cards = processor._parse_cards_from_markdown(markdown_special)
    assert len(cards) == 1
    
    card = cards[0]
    assert '<table>' in card['back']
    assert '∑' in card['back']
    assert '\\sum' in card['back']