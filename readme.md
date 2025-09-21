# Wildcard Text Replacement Script

A Python script that performs text replacement using wildcard patterns. Supports both exact word matching and flexible wildcard patterns with `*`.

## Features

- **Exact word matching**: Replace whole words only
- **Wildcard patterns**: Use `*` to match partial words
- **Flexible replacement**: Preserve matched prefixes/suffixes in replacements
- **File-based processing**: Read rules from file, process input file, output to file

## Usage

1. Create your rules file (`rules.txt`) with replacement patterns
2. Create your input file (`input.txt`) with text to process
3. Run the script: `python wildcard_replacement.py`
4. Check the output in `output.txt`

## Rule Format

Each rule should be on a separate line in the format: `pattern -> replacement`

### Pattern Types

| Pattern Type | Example | Description | Matches |
|--------------|---------|-------------|---------|
| Exact word | `word -> word_04` | Matches whole words only | `word` (not `sword` or `words`) |
| Prefix wildcard | `*word -> *word_02` | Matches words ending with pattern | `sword`, `password`, `111_word` |
| Suffix wildcard | `phrase* -> phrase_03*` | Matches words starting with pattern | `phrases`, `phrase_111` |
| Both wildcards | `*test* -> *test_01*` | Matches words containing pattern | `testing`, `_test_`, `contest` |

## Example

### Rules (`rules.txt`)
```
*test* -> *test_01*
*word -> *word_02
phrase* -> phrase_03*
word -> word_04
```

### Input (`input.txt`)
```
word hello phrase_111 111_word _testing 111_word end
```

### Output (`output.txt`)
```
word_04 hello phrase_03_111 111_word_02 _test_01ing 111_word_02 end
```

## How It Works

1. **Pattern Conversion**: Wildcard patterns are converted to regex:
   - `*word` becomes `\S*word\b` (any non-space chars + word + word boundary)
   - `word*` becomes `\bword\S*` (word boundary + word + any non-space chars)
   - `*word*` becomes `\S*word\S*` (any non-space chars + word + any non-space chars)
   - `word` becomes `\bword\b` (exact word with boundaries)

2. **Smart Replacement**: When wildcards are used in replacements:
   - Preserves the matched prefix/suffix from the original text
   - Replaces `*` in the replacement string with the captured parts

3. **Processing Order**: Rules are applied in the order they appear in the file

## Files

- `wildcard_replacement.py` - Main script
- `rules.txt` - Replacement rules (create this)
- `input.txt` - Input text to process (create this)
- `output.txt` - Processed output (generated)

## Requirements

- Python 3.x
- No external dependencies (uses only built-in `re` module)

## Notes

- Uses `\S*` for wildcard matching (non-whitespace characters)
- Word boundaries (`\b`) ensure exact word matching where appropriate
- Empty lines and lines without `->` in rules file are ignored
- Rules are processed sequentially - earlier rules can affect later ones
