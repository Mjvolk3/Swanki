"""Formatting utilities for tags and other text processing."""
import re
from typing import List


def format_tags(tags: List[str], format_type: str = "slugified") -> List[str]:
    """Format tags according to the specified format type.
    
    Args:
        tags: List of tags to format
        format_type: Type of formatting to apply
            - "slugified": Convert to lowercase, replace spaces with hyphens
            - "spaces": Keep spaces as-is
            - "raw": No formatting, return as-is
            
    Returns:
        List of formatted tags
    """
    if format_type == "raw":
        return tags
    
    formatted_tags = []
    for tag in tags:
        if format_type == "slugified":
            # Convert to lowercase and replace spaces with hyphens
            # Also remove any special characters except dots and hyphens
            formatted = tag.lower()
            formatted = re.sub(r'[^\w\s.-]', '', formatted)
            formatted = re.sub(r'\s+', '-', formatted)
            formatted = re.sub(r'-+', '-', formatted)  # Remove multiple hyphens
            formatted = formatted.strip('-')
            formatted_tags.append(formatted)
        elif format_type == "spaces":
            # Just clean up extra spaces
            formatted = ' '.join(tag.split())
            formatted_tags.append(formatted)
        else:
            # Default to raw if unknown format
            formatted_tags.append(tag)
    
    return formatted_tags


def detect_tags_from_text(text: str) -> List[str]:
    """Detect tags from text based on # and comma delimited formats.
    
    Args:
        text: Text to extract tags from
        
    Returns:
        List of detected tags
    """
    tags = []
    
    # Look for hashtag format: #tag1, #tag2 or #tag1 #tag2
    hashtag_pattern = r'#[\w.-]+'
    hashtag_matches = re.findall(hashtag_pattern, text)
    for match in hashtag_matches:
        tags.append(match[1:])  # Remove the # prefix
    
    # If no hashtags found, look for comma-delimited format at the end of lines
    if not tags:
        # Look for patterns like "Tags: tag1, tag2, tag3" or just "tag1, tag2, tag3" at line end
        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            # Check if line starts with "Tags:" or similar
            if re.match(r'^(tags?|labels?|categories?):\s*', line, re.IGNORECASE):
                tag_text = re.sub(r'^(tags?|labels?|categories?):\s*', '', line, flags=re.IGNORECASE)
                potential_tags = [t.strip() for t in tag_text.split(',')]
                tags.extend([t for t in potential_tags if t])
            # Check if line is just comma-separated values (heuristic: has commas and no periods)
            elif ',' in line and '.' not in line and len(line) < 100:
                potential_tags = [t.strip() for t in line.split(',')]
                if all(len(t) < 30 for t in potential_tags if t):  # Reasonable tag length
                    tags.extend([t for t in potential_tags if t])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_tags = []
    for tag in tags:
        if tag.lower() not in seen:
            seen.add(tag.lower())
            unique_tags.append(tag)
    
    return unique_tags


def humanize_citation_key(citation_key: str) -> str:
    """Convert a citation key to human-readable format for audio.
    
    Examples:
        luoWhenCausalInference2020 -> "Luo, When Causal Inference, 2020"
        smithMachineLearning2023 -> "Smith, Machine Learning, 2023"
        johnsonEtAl2022 -> "Johnson et al, 2022"
        oReilly2019 -> "O'Reilly, 2019"
        mcDonald2024 -> "McDonald, 2024"
        
    Args:
        citation_key: Citation key in camelCase format
        
    Returns:
        Human-readable version of the citation key
    """
    if not citation_key:
        return ""
    
    # Handle common patterns
    # First, handle "EtAl" -> "et al"
    humanized = citation_key.replace("EtAl", " et al")
    
    # Extract year at the end (if present)
    year_match = re.search(r'(\d{4})$', humanized)
    year = ""
    if year_match:
        year = year_match.group(1)
        humanized = humanized[:-4]  # Remove year from main text
    
    # Handle special name patterns before general processing
    # Common prefixes that should stay together
    name_patterns = [
        (r'^mc([A-Z])', r'Mc\1'),  # McDonald -> McDonald
        (r'^mac([A-Z])', r'Mac\1'),  # MacArthur -> MacArthur
        (r'^o([A-Z])', r"O'\1"),  # oReilly -> O'Reilly
        (r'^de([A-Z])', r'de \1'),  # deSouza -> de Souza
        (r'^van([A-Z])', r'van \1'),  # vanDijk -> van Dijk
        (r'^von([A-Z])', r'von \1'),  # vonNeumann -> von Neumann
    ]
    
    # Apply name patterns
    for pattern, replacement in name_patterns:
        humanized = re.sub(pattern, replacement, humanized)
    
    # Split camelCase into words
    # Insert space before uppercase letters that follow lowercase letters
    # But not if it's after an apostrophe (like O'Reilly)
    humanized = re.sub(r"(?<!')([a-z])([A-Z])", r'\1 \2', humanized)
    
    # Handle multiple consecutive capitals (like "USA" or "CNN")
    humanized = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', humanized)
    
    # Split into words
    words = humanized.split()
    
    if words:
        # First word is always the author name - capitalize it properly
        first_word = words[0]
        
        # Check if it's a special prefix that should stay lowercase
        if first_word.lower() in ['de', 'van', 'von']:
            # Keep lowercase, but capitalize the next word
            if len(words) > 1:
                words[1] = words[1].capitalize()
                words[1] = words[1] + ","  # Add comma after actual surname
        else:
            # Normal case - capitalize first word
            words[0] = words[0].capitalize()
            # Add comma after first word if there are more words
            if len(words) > 1 and words[1].lower() not in ['et', 'al']:
                words[0] = words[0] + ","
    
    # Rejoin words
    humanized = " ".join(words)
    
    # Add year at the end if present
    if year:
        humanized = f"{humanized}, {year}"
    
    # Clean up any double spaces
    humanized = " ".join(humanized.split())
    
    return humanized