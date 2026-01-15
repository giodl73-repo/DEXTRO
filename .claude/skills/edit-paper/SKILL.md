---
name: edit-paper
description: Edit academic papers for journal submission. Acts as journal editor providing proofreading, condensing, copyediting, and page limit targeting. Focuses on clarity, conciseness, technical accuracy, and consistent notation for peer-reviewed publications.
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Bash
user-invocable: true
---

# Edit Paper

## Overview

Act as an academic journal editor to review and improve LaTeX papers for publication. Provides systematic proofreading, condensing, copyediting, and quality enhancement while preserving technical accuracy and meeting page constraints.

**Target audience**: Academic peer reviewers and researchers
**Style**: Formal, technical, precise, concise
**Common use**: Preparing papers for conference/journal submission (8-12 page limits)

## Prerequisites

**Required**:
- LaTeX paper files (`.tex`) in `papers/` directory
- Paper uses standard LaTeX structure (sections, figures, citations)

**Recommended**:
- Compiled PDF available for visual review
- Clear target page count (e.g., "reduce to 10 pages")
- `/compile-latex` skill available for validation

## When to Use This Skill

- User says: "Edit my paper for submission"
- User says: "Proofread the paper" or "Condense the paper"
- User says: "Help me meet the page limit"
- User needs consistent notation across sections
- User wants academic style review (avoid colloquialisms)
- Paper exceeds journal/conference page limits
- Preparing for peer review submission

## Editing Levels

Choose editing intensity based on needs and time constraints:

### Level 1: Light Proofread (5-10 minutes)
**What it includes**:
- Grammar and spelling fixes
- Remove obvious verbosity
- Fix citation formatting
- No condensing or restructuring

**Use when**: Quick polish before informal review

### Level 2: Standard Edit (15-30 minutes)
**What it includes**:
- Full proofread + copyedit
- Light condensing (10-15% reduction)
- Notation consistency checks
- Improve clarity of unclear passages
- No major restructuring

**Use when**: Standard submission preparation

### Level 3: Heavy Edit (30-60 minutes)
**What it includes**:
- Comprehensive editing
- Significant condensing (20-30% reduction)
- Restructuring sections as needed
- Quality enhancement (clarity, flow, arguments)
- Meet specific page targets

**Use when**: Paper significantly exceeds page limit

### Level 4: Complete Overhaul (60+ minutes)
**What it includes**:
- Major restructuring
- Aggressive condensing (30%+ reduction)
- Complete notation standardization
- Extensive rewriting for clarity
- Move content to appendix/supplementary

**Use when**: Major revision required

## Workflow

### Step 1: Analyze Paper

**Gather requirements via `AskUserQuestion`**:
- Which paper to edit? (path to paper directory)
- Which sections? (all, or specific sections like methodology)
- Current vs target page count (e.g., "18 pages → 12 pages")
- Editing level (Light / Standard / Heavy / Complete)
- Specific concerns (notation, clarity, length, style)

**Read paper files**:
```bash
# Find all .tex files in paper directory
find papers/03_combined_recursive_bisection/ -name "*.tex"

# Read main file and sections
```

**Analyze structure**:
- Section lengths and proportions
- Notation usage (e.g., $G = (V, E)$, $PP$ for Polsby-Popper)
- Citation patterns
- Figure/table references
- Estimated page count

### Step 2: Review Content

**Proofread each section**:
- **Grammar and spelling**: Fix typos, subject-verb agreement, punctuation
- **Academic style**: Remove colloquialisms ("pretty good" → "effective"), contractions ("don't" → "do not")
- **Verb tense**: Past for methods, present for results/conclusions
- **Citation format**: Consistent style (Author (Year) vs [1])

**Check technical accuracy**:
- **Notation consistency**: Same variable names throughout (e.g., always $G$ for graph, not $G$ then $\mathcal{G}$)
- **Algorithm accuracy**: Descriptions match actual implementation
- **Mathematical correctness**: Formulas are valid
- **Definitions**: All variables defined on first use

**Identify verbosity**:
- Redundant phrases: "in order to" → "to", "due to the fact that" → "because"
- Unnecessary qualifiers: "very", "quite", "somewhat", "rather"
- Repetitive content: Same point made in multiple places
- Complex sentences: Can one sentence become two clearer ones?

### Step 3: Apply Edits

**Condensing strategies**:
- **Simplify sentences**: Break complex sentences, remove unnecessary clauses
- **Remove redundancy**: Delete repeated information
- **Efficient phrasing**: Use active voice, concrete language
- **Consolidate**: Merge similar paragraphs

**Example condensing patterns**:
```
Before: "It is important to note that the algorithm performs well."
After: "The algorithm performs well."

Before: "We use the METIS algorithm in order to partition the graph."
After: "We use METIS to partition the graph."

Before: "As can be seen in Figure 3, the compactness improves significantly."
After: "Figure 3 shows significant compactness improvement."
```

**Restructuring (if needed)**:
- Move detailed derivations to appendix
- Consolidate similar subsections
- Reorder for logical flow
- Create subsections for long sections

**Use `Edit` tool to apply changes**:
- Edit one section at a time
- Preserve technical content
- Maintain LaTeX formatting
- Keep all figure/citation references intact

### Step 4: Verify Quality

**Consistency checks**:
- Notation: Same symbols throughout (use `Grep` to find all uses)
- Terminology: Consistent terms ("census tract" not mixed with "tract")
- Citations: All references formatted same way
- Hyphenation: "edge-weighted" consistently hyphenated

**Clarity checks**:
- Each paragraph has clear main point
- Transitions between paragraphs exist
- Jargon is defined on first use
- Examples support claims

**Technical validation**:
```bash
# Compile to check for LaTeX errors
/compile-latex papers/03_combined_recursive_bisection/
```

**Before/after metrics**:
- Word count reduction: X words → Y words (Z% reduction)
- Estimated page count: A pages → B pages
- Number of edits by type (grammar, condensing, notation, etc.)

### Step 5: Generate Summary

**Create edit summary** (`papers/{paper_name}/EDIT_SUMMARY.md`):

```markdown
# Edit Summary: [Paper Name]

**Date**: [Today's date]
**Editing Level**: [Light/Standard/Heavy/Complete]
**Target**: Reduce from X pages to Y pages

## Changes Made

### Grammar & Style (N edits)
- Fixed subject-verb agreement in Section 2
- Changed passive to active voice throughout
- Removed colloquialisms ("pretty good" → "effective")

### Condensing (M% reduction)
- Simplified complex sentences in Introduction
- Removed redundant explanations in Methodology
- Consolidated Results subsections 4.1 and 4.2

### Notation Consistency (K fixes)
- Standardized graph notation: $G = (V, E)$ throughout
- Changed $PP$ to Polsby-Popper on first use, $PP$ thereafter
- Fixed inconsistent hyphenation: "edge-weighted" everywhere

### Quality Improvements
- Added transition sentences between Sections 2 and 3
- Clarified algorithm description in Section 3.1
- Strengthened conclusions with quantitative evidence

## Statistics

- **Word count**: 6,500 → 5,200 words (-20%)
- **Est. page count**: 18 pages → 13 pages
- **Total edits**: 127 (42 grammar, 58 condensing, 27 other)

## Sections Requiring Author Review

- **Section 3.2**: Condensed significantly, verify accuracy
- **Figure 4**: May need resizing to save space
- **Appendix A**: Consider moving to supplementary materials

## Suggested Follow-Up

- Review condensed sections for technical accuracy
- Consider reducing Figure 4 from full-page to half-page
- Add 1-2 sentences to Introduction motivation (currently terse)
```

**Report to user**:
- Summary of changes
- Before/after metrics
- Sections needing author review
- Next steps

## Academic Style Guidelines

### Preferred Patterns

**Active voice**:
- ✅ "We apply METIS to partition the graph"
- ❌ "METIS is applied to partition the graph"

**Concrete over abstract**:
- ✅ "Compactness improves by 52.8%"
- ❌ "Compactness significantly improves"

**Direct statements**:
- ✅ "The algorithm fails when graphs are disconnected"
- ❌ "It appears that the algorithm might fail when graphs are disconnected"

**Specific examples**:
- ✅ "In Alabama, METIS creates 7 districts"
- ❌ "In some states, METIS creates districts"

### Avoid

**Contractions**:
- ❌ "don't", "can't", "we've"
- ✅ "do not", "cannot", "we have"

**Colloquialisms**:
- ❌ "pretty good", "a lot", "kind of"
- ✅ "effective", "many", "somewhat" (sparingly)

**Hedging words** (use sparingly):
- Avoid: "somewhat", "rather", "quite", "fairly"
- Exception: Appropriate for genuine uncertainty

**Passive voice** (when active is clearer):
- ❌ "The graph is partitioned by METIS"
- ✅ "METIS partitions the graph"

**Vague quantifiers**:
- ❌ "many", "some", "several", "numerous"
- ✅ Use specific numbers or percentages

## Common Condensing Patterns

### Phrase Replacement

| Verbose | Concise |
|---------|---------|
| in order to | to |
| due to the fact that | because |
| it is important to note that | [delete] |
| as can be seen in Figure X | Figure X shows |
| at the present time | now |
| in the event that | if |
| for the purpose of | for, to |
| a number of | several, many, N |

### Sentence Simplification

**Before**: "It is worth noting that the algorithm, which uses recursive bisection, performs well when the graph has a large number of nodes."

**After**: "The recursive bisection algorithm performs well on large graphs."

**Before**: "We utilize the METIS graph partitioning algorithm for the purpose of creating congressional districts."

**After**: "We use METIS to create congressional districts."

### Redundancy Removal

**Before**: "The algorithm recursively bisects the graph again and again until the desired number of districts is reached."

**After**: "The algorithm recursively bisects the graph until reaching the desired number of districts."

## Page Estimation Heuristics

**Typical LaTeX article class**:
- ~450-500 words per page (double column)
- ~750-800 words per page (single column)
- Figures: ~0.3-0.5 pages (small), ~0.7-1.0 pages (large)
- Tables: ~0.2-0.4 pages (typical)
- Display equations: ~0.1-0.2 pages each

**Condensing targets**:
- **10% reduction**: Remove obvious verbosity, low risk
- **20% reduction**: Significant condensing, preserve all content
- **30% reduction**: Aggressive condensing, may move content to appendix
- **40%+ reduction**: Major restructuring, supplementary materials needed

## Troubleshooting

**LaTeX compilation errors after editing**:
```
Issue: Missing $ or unmatched braces
Solution: Carefully check math mode ($...$), verify all braces match
```

**Changes altered technical meaning**:
```
Issue: Condensing changed algorithm description
Solution: Restore original, condense elsewhere, or ask author to clarify
```

**Still over page limit after editing**:
```
Issue: Paper still 2-3 pages too long
Solution:
  - Move derivations to appendix
  - Reduce figure sizes or move figures to supplementary
  - Consider two-column format if single-column
  - Suggest content for supplementary materials
```

**Notation inconsistencies persist**:
```
Issue: Multiple notations for same concept
Solution: Use Grep to find all uses, standardize globally using Edit tool
```

**Unclear what to condense**:
```
Issue: All content seems essential
Solution:
  - Focus on Introduction and Related Work (often verbose)
  - Simplify experimental setup descriptions
  - Reduce redundant explanations of results
  - Move detailed tables to supplementary
```

## Quality Checklist

Before finalizing edits:

### Technical Accuracy
- [ ] No mathematical errors introduced
- [ ] Algorithm descriptions remain correct
- [ ] All citations still properly referenced
- [ ] Figure/table numbers still match

### Consistency
- [ ] Notation used consistently throughout
- [ ] Terminology uniform (not "tract" sometimes, "census tract" others)
- [ ] Citation style consistent
- [ ] Hyphenation consistent (e.g., "edge-weighted")

### Clarity
- [ ] Each paragraph has clear main point
- [ ] Transitions exist between paragraphs/sections
- [ ] Jargon defined on first use
- [ ] No ambiguous statements remain

### Style
- [ ] Active voice used where appropriate
- [ ] Concrete language (specific numbers/examples)
- [ ] No colloquialisms or contractions
- [ ] Proper academic tone maintained

### Format
- [ ] LaTeX compiles without errors
- [ ] No formatting issues introduced
- [ ] Line breaks and spacing preserved
- [ ] Math mode used correctly

## Related Skills

- `/compile-latex` - Compile LaTeX after editing to verify no errors
- `/create-presentation-figures` - May need to regenerate figures for paper
- `/update-docs` - Similar editing workflow for documentation
- `/create-session-archive` - Archive major paper revisions

## Performance Notes

**Typical editing time**:

| Level | Time | Reduction |
|-------|------|-----------|
| Light Proofread | 5-10 min | Minimal |
| Standard Edit | 15-30 min | 10-15% |
| Heavy Edit | 30-60 min | 20-30% |
| Complete Overhaul | 60-120 min | 30-40%+ |

**Factors affecting time**:
- Paper length (longer = more time)
- Current verbosity (more verbose = more to condense)
- Technical density (highly technical = slower to verify accuracy)
- Notation inconsistencies (more issues = more fixes needed)

## What You'll Get

After successful paper editing:
- **Edited LaTeX files**: All `.tex` files updated with improvements
- **Edit summary**: Comprehensive report of changes made
- **Before/after metrics**: Word count, page count reduction
- **Compiled PDF**: Verified paper compiles correctly
- **Quality assurance**: Technical accuracy preserved
- **Sections for review**: Flagged areas needing author attention

## Next Steps

After editing:
1. **Review flagged sections**: Check areas marked for author review
2. **Recompile paper**: Generate final PDF to see visual result
3. **Read through once**: Do final pass for flow and coherence
4. **Get co-author feedback**: Share edited version with collaborators
5. **Submit**: If target page count met and quality high, submit to journal/conference
6. **Archive version**: Save edited version with date for future reference

## Example Usage

**Scenario**: 18-page paper needs to be 12 pages for conference submission

**Steps**:
1. User invokes: `/edit-paper`
2. Skill asks:
   - Paper: `papers/03_combined_recursive_bisection/`
   - Sections: All
   - Target: 18 pages → 12 pages (33% reduction)
   - Level: Heavy Edit
   - Concerns: "Too verbose in intro and methodology"
3. Skill analyzes paper structure
4. Applies edits:
   - Condenses Introduction from 3 pages to 1.5 pages
   - Simplifies Methodology explanations
   - Consolidates Results subsections
   - Moves detailed derivation to Appendix
5. Generates summary showing 35% word count reduction
6. Compiles paper successfully, now 11.5 pages
7. Flags Methodology Section 3.2 for author review

**Result**: Paper ready for submission, under page limit, technical accuracy preserved
