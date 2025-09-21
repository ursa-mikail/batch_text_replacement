import re

def load_rules(filename):
    """
    Load replacement rules from a file.
    Handles wildcard patterns (*) and exact matches.
    """
    rules = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or '->' not in line:
                continue
            pattern, replacement = line.split('->', 1)
            pattern = pattern.strip()
            replacement = replacement.strip()
            rules.append((pattern, replacement))
    return rules

def pattern_to_regex(pattern):
    """
    Convert wildcard pattern to regex.
    * matches any sequence of characters
    Exact words use word boundaries
    """
    if '*' not in pattern:
        # Exact word match
        return r'\b' + re.escape(pattern) + r'\b'
    
    # Handle wildcard patterns
    if pattern.startswith('*') and pattern.endswith('*'):
        # *word* - matches any string containing 'word'
        core = re.escape(pattern[1:-1])
        return r'\S*' + core + r'\S*'
    elif pattern.startswith('*'):
        # *word - matches any string ending with 'word'
        core = re.escape(pattern[1:])
        return r'\S*' + core + r'\b'
    elif pattern.endswith('*'):
        # word* - matches any string starting with 'word'
        core = re.escape(pattern[:-1])
        return r'\b' + core + r'\S*'
    else:
        # No wildcards, exact match
        return r'\b' + re.escape(pattern) + r'\b'

def replacement_function(pattern, replacement):
    """
    Create a replacement function that handles wildcards in the replacement string.
    """
    def replace_func(match):
        matched_text = match.group(0)
        result = replacement
        
        # Handle wildcards in replacement
        if '*' in replacement:
            if pattern.startswith('*') and pattern.endswith('*'):
                # *word* -> *word_01*
                core = pattern[1:-1]
                if core in matched_text:
                    prefix = matched_text[:matched_text.find(core)]
                    suffix = matched_text[matched_text.find(core) + len(core):]
                    result = result.replace('*', prefix, 1).replace('*', suffix)
            elif pattern.startswith('*'):
                # *word -> *word_02
                core = pattern[1:]
                if matched_text.endswith(core):
                    prefix = matched_text[:-len(core)]
                    result = result.replace('*', prefix)
            elif pattern.endswith('*'):
                # word* -> word_03*
                core = pattern[:-1]
                if matched_text.startswith(core):
                    suffix = matched_text[len(core):]
                    result = result.replace('*', suffix)
        
        return result
    
    return replace_func

def apply_replacements(text, rules):
    """
    Apply replacement rules to text, handling wildcards.
    """
    for pattern, replacement in rules:
        regex_pattern = pattern_to_regex(pattern)
        replace_func = replacement_function(pattern, replacement)
        text = re.sub(regex_pattern, replace_func, text)
    return text

# File paths
rules_file = "rules.txt"
input_file = "input.txt"
output_file = "output.txt"

# Load rules
replacement_rules = load_rules("rules.txt")

# Read input text
with open("input.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("Original text:", repr(text))
print("Rules loaded:", replacement_rules)

# Apply replacements
modified_text = apply_replacements(text, replacement_rules)

# Write output text
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(modified_text)

print("Modified text:", repr(modified_text))
print(f"Replacement complete. Check 'output.txt' for results.")

# Show what each rule would match
print("\nRule analysis:")
for pattern, replacement in replacement_rules:
    regex_pattern = pattern_to_regex(pattern)
    matches = re.findall(regex_pattern, text)
    print(f"'{pattern}' -> '{replacement}' matches: {matches}")

