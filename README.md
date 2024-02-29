# Obsidifred

Simple full-text search for Shimmering Obsidian via `of`.

## Installing

1. Install Obsidifred
1. Install [Shimmering Obsidian](https://github.com/chrisgrieser/shimmering-obsidian)
1. Configure Obsidifred to specify vault path (using the same as Shimmering Obsidian's)

## Behavior

If you enable [RipGrep](https://github.com/BurntSushi/ripgrep) then `rg` needs to be in your path, and we pass along the `--smart-case` flag.

Otherwise, we'll do Python-native smart case searching. If you're doing a case sensitive search we'll open the file, read its contents, convert to lowercase, and search for your term. If you're doing a case insensitive search we'll read the file via `mmap` to find your term. 
