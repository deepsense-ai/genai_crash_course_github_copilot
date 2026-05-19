---
description: "Use when editing markdown files to maintain a consistent style across documentation and instructions."
name: "Markdown Style"
applyTo: "**/*.md"
---

# Markdown Style

Use these rules when creating or editing GitHub Flavored Markdown documentation or instruction files.

## Headings

- Use a single `#` heading for the document title.
- Structure content with sequential heading levels (`##`, then `###`) without skipping levels.
- Keep headings short, descriptive, and written in sentence case.
- Add a blank line before and after each heading.

## Paragraphs and line breaks

- Write concise paragraphs focused on one idea.
- Separate paragraphs with a single blank line.
- Avoid hard-wrapping lines unless the surrounding file already uses a fixed line width.
- Prefer clear, direct wording over jargon.

## Lists

- Use unordered lists (`-`) for related items where order does not matter.
- Use ordered lists (`1.`, `2.`, `3.`) for procedures or ranked steps.
- Keep list items parallel in grammar and punctuation.
- Indent nested list items by two spaces.
- Add a blank line before and after lists.

## Code and commands

- Use inline code formatting for filenames, paths, commands, package names, symbols, and literals.
- Use fenced code blocks with a language identifier when showing multi-line examples.
- Use `text` for plain output or content without a specific language.
- Keep code examples minimal and directly relevant.
- Do not include secrets, tokens, credentials, or machine-specific absolute paths unless required by the task.

## Links

- Use descriptive link text instead of bare URLs or phrases like "click here".
- Prefer relative links for files in the same repository.
- Verify that new internal links point to the correct target.
- Use reference-style links only when they improve readability in link-heavy documents.

## Tables

- Use tables only for compact, structured data that is easier to scan in columns.
- Keep table cells short.
- Include a header row and separator row.
- Prefer lists when table content becomes long or complex.

## Notes and callouts

- Use bold labels for lightweight callouts, such as `**Note:**`, `**Tip:**`, and `**Warning:**`.
- Keep callouts brief and actionable.
- Avoid overusing callouts; reserve them for information that needs emphasis.

## Formatting consistency

- Preserve the existing style of the file when editing established documents.
- Use American English unless the surrounding document uses another variant.
- Use consistent terminology throughout a document.
- Remove trailing whitespace.
- End files with a newline.

## Documentation quality

- Start with the information readers need most.
- Prefer task-oriented sections for procedures and reference sections for details.
- Avoid duplicating long content that is already documented elsewhere; link to the source instead.
- Keep instructions actionable and testable where possible.