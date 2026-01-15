---
name: edit-presentation
description: Edit academic presentations (Beamer LaTeX) for conference talks. Acts as presentation editor ensuring slides are clear, concise (one idea per slide), visually balanced, and fit time constraints. Targets 15-20 slides for 15-20 minute talks with engaging, scannable content.
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Bash
user-invocable: true
---

# Edit Presentation

## Overview

Act as a conference presentation editor to review and improve Beamer LaTeX slides for academic talks. Ensures slides follow best practices: one idea per slide, visual clarity, minimal text, and appropriate pacing for time constraints.

**Target audience**: Conference attendees with limited attention span
**Style**: Conversational, visual-first, clear takeaways
**Common use**: 15-20 minute conference talks (typically 15-20 slides)

## Prerequisites

**Required**:
- Beamer LaTeX presentation files (`.tex`) in `presentations/` directory
- Presentation uses standard Beamer structure (frames, sections)

**Recommended**:
- Compiled PDF available for visual review
- Clear target duration (e.g., "15-minute talk")
- `/compile-latex` skill available for validation

## When to Use This Skill

- User says: "Edit my presentation" or "Review my slides"
- User says: "My talk is too long" or "Condense my presentation"
- User says: "Make slides more visual" or "Improve slide clarity"
- Presentation exceeds time limit (too many slides)
- Slides are text-heavy (>5 bullets per slide)
- Need to enforce "one idea per slide" principle
- Preparing for conference presentation submission

## Editing Levels

Choose editing intensity based on needs and time constraints:

### Level 1: Light Polish (10-15 minutes)
**What it includes**:
- Fix obvious clarity issues
- Improve slide titles (make action-oriented)
- Remove excessive text bullets
- No condensing or restructuring

**Use when**: Quick polish before practice talk

### Level 2: Standard Edit (20-40 minutes)
**What it includes**:
- Full clarity review
- Light condensing (10-20% slide reduction)
- Improve narrative flow
- Polish bullet points and titles
- No major restructuring

**Use when**: Standard conference submission preparation

### Level 3: Heavy Edit (40-90 minutes)
**What it includes**:
- Significant condensing to meet target
- Restructure sections as needed
- Split/merge slides for "one idea per slide"
- Enhance visual clarity
- Add transition slides

**Use when**: Presentation significantly exceeds time limit

### Level 4: Complete Overhaul (90+ minutes)
**What it includes**:
- Major restructuring
- Aggressive condensing (30%+ reduction)
- Complete visual redesign recommendations
- Full narrative rebuild
- Backup slides for details

**Use when**: Major revision required for submission

## Workflow

### Step 1: Analyze Presentation

**Gather requirements via `AskUserQuestion`**:
- Which presentation to edit? (path to presentation directory)
- Target duration (10 / 15 / 20 minutes)
- Current vs target slide count (e.g., "30 slides → 20 slides")
- Editing level (Light / Standard / Heavy / Complete)
- Audience level (experts / general researchers / students)
- Key messages that must be preserved

**Read presentation files**:
```bash
# Find all .tex files in presentation directory
find presentations/edge_weighted_bisection/ -name "*.tex"

# Read main presentation file
```

**Analyze structure**:
- Slide count by section (Intro: 3, Methods: 8, Results: 12, Conclusion: 2)
- Text density per slide (count bullets, estimate word count)
- Figure/diagram usage (visual vs text ratio)
- Bullet point depth (avoid 3+ levels of nesting)
- Transition quality between slides/sections
- Calculate: slides per minute (target: ~1 slide/minute)

**Time estimation heuristics**:
- Title/intro slides: ~30 seconds
- Dense technical slides: ~90-120 seconds
- Simple diagram slides: ~45 seconds
- Standard content slides: ~60 seconds
- **Target**: 10 min talk = 10-12 slides, 15 min talk = 15-18 slides, 20 min talk = 20-24 slides

### Step 2: Review Content

**Check presentation structure**:
- **Opening** (10%): Clear motivation, roadmap slide
- **Background** (15%): Context without excessive detail
- **Methodology** (25%): Core approach, algorithm overview
- **Results** (30%): Key findings, visual evidence
- **Conclusion** (10%): Takeaways, next steps
- **Q&A placeholder**: Final slide

**Review slide-level content**:
- **One idea per slide?** Each slide has single main point
- **Title reflects content?** "Compactness improves 52.8%" not "Results"
- **Text minimal?** 3-5 bullets max, phrases not sentences
- **Bullets concise?** 5-10 words per bullet, not full sentences
- **Visual elements?** Figures/diagrams support text
- **Builds appropriately?** Use `\pause` for progressive disclosure

**Identify issues**:
- **Dense slides**: >5 bullets or >50 words total
- **Multi-idea slides**: Covering 2+ unrelated concepts
- **Poor transitions**: Slides don't flow logically
- **Generic titles**: "Introduction" instead of "Why redistricting matters"
- **Missing visuals**: All text, no diagrams/figures
- **Deep nesting**: 3+ bullet levels (hard to read)

### Step 3: Apply Edits

**Condensing strategies**:
- **Merge related slides**: Two slides on same topic → One combined slide
- **Split multi-idea slides**: One slide, two concepts → Two focused slides
- **Remove tangential content**: Nice-to-have → Delete or move to backup
- **Simplify explanations**: Detailed derivation → High-level overview
- **Move to backup slides**: Technical details → Backup for Q&A

**Example slide improvements**:

**Before** (dense, multi-idea):
```latex
\begin{frame}{Results}
\begin{itemize}
  \item We ran experiments on 10 states and found that the edge-weighted algorithm significantly improves compactness
  \item The Polsby-Popper score increased from 0.34 to 0.52
  \item This represents a 52.8\% improvement over the baseline
  \item The algorithm also reduces perimeter length by 22.2\%
  \item Runtime increased by only 2x despite better results
  \item All states showed consistent improvements
\end{itemize}
\end{frame}
```

**After** (clear, one idea, action title):
```latex
\begin{frame}{Edge Weights Improve Compactness by 53\%}
\begin{itemize}
  \item Polsby-Popper: 0.34 $\rightarrow$ 0.52 (+53\%)
  \item Perimeter reduction: 22\%
  \item Runtime: 2x slower (acceptable)
\end{itemize}

\begin{figure}
  \includegraphics[width=0.6\textwidth]{figures/compactness_comparison.png}
\end{figure}
\end{frame}
```

**Improve slide titles**:
- ❌ "Results" → ✅ "Compactness improves 53%"
- ❌ "Methodology" → ✅ "METIS partitions graphs recursively"
- ❌ "Background" → ✅ "Gerrymandering is a national problem"
- ❌ "Analysis" → ✅ "Three key algorithm advantages"

**Polish bullet points**:
- **Parallel structure**: All bullets use same grammatical form
- **Action verbs**: Start with verbs when describing processes
- **Short phrases**: 5-10 words, not complete sentences
- **2 levels max**: Main bullets and sub-bullets only

**Before**: Mixed structure, verbose
```latex
\begin{itemize}
  \item The algorithm uses METIS for graph partitioning
  \item Recursive bisection repeatedly splits the graph
  \item We apply edge weights to encourage compact districts
  \item Population balance is maintained within 0.5%
\end{itemize}
```

**After**: Parallel structure, concise
```latex
\begin{itemize}
  \item METIS graph partitioning
  \item Recursive bisection splits
  \item Edge weights for compactness
  \item Population balance: $\pm$0.5\%
\end{itemize}
```

**Visual balance recommendations**:
- **50/50 rule**: Aim for 50% text, 50% visual (figure/diagram/whitespace)
- **Font size**: Never below 20pt for body text
- **Bullet depth**: 2 levels max (main + sub-bullets)
- **Whitespace**: Don't fill every inch of slide

**Use `Edit` tool to apply changes**:
- Edit one frame (slide) at a time
- Preserve Beamer commands (`\pause`, `\only`, etc.)
- Maintain figure/citation references
- Keep section structure intact

### Step 4: Verify Quality

**Consistency checks**:
- Terminology: Same terms throughout ("census tract" not mixed with "tract")
- Notation: Consistent mathematical notation (always $G = (V, E)$)
- Visual style: Figures use consistent color schemes
- Title format: Parallel structure across similar slides

**Clarity checks**:
- Each slide has clear main point
- Slide titles convey key message
- Bullets are scannable (not full sentences)
- Transitions exist between sections
- No jargon without definition

**Beamer-specific validation**:
```bash
# Compile to check for Beamer errors
/compile-latex presentations/edge_weighted_bisection/
```

**Check for**:
- `\pause` commands working correctly
- `\only<>` overlay specifications valid
- No Beamer compilation errors
- PDF renders correctly

**Before/after metrics**:
- Slide count: X slides → Y slides (Z% reduction)
- Average bullets per slide: A → B
- Text density reduction: Verbose slides reduced by N
- Estimated duration: M minutes (at 1 min/slide)

### Step 5: Generate Summary

**Create edit summary** (`presentations/{name}/EDIT_SUMMARY.md`):

```markdown
# Edit Summary: [Presentation Name]

**Date**: [Today's date]
**Editing Level**: [Light/Standard/Heavy/Complete]
**Target**: Reduce from X slides to Y slides for Z-minute talk

## Changes Made

### Condensing (N slides removed)
- Merged Introduction slides 1-2 into single motivating slide
- Removed detailed methodology (moved to backup slides)
- Combined Results slides 8-10 into comparative overview

### Clarity Improvements (M slides improved)
- Split dense Algorithm slide into 3 focused slides
- Improved all titles to be action-oriented
- Reduced bullets from 7-8 per slide to 3-5 per slide
- Added build animations for complex concepts

### Visual Enhancements
- Suggested: Replace text description with algorithm flowchart (slide 6)
- Suggested: Add compactness comparison figure (slide 12)
- Improved: Whitespace balance on 8 slides

### Title Improvements (K slides)
- "Results" → "Compactness improves 53%"
- "Methodology" → "METIS partitions graphs recursively"
- "Background" → "Gerrymandering threatens fair representation"

## Statistics

- **Slide count**: 28 → 18 slides (-36%)
- **Est. duration**: 28 min → 18 min (on target for 15-20 min talk)
- **Avg bullets/slide**: 6.5 → 4.2
- **Dense slides** (>5 bullets): 12 → 2
- **Total edits**: 85 (32 condensing, 28 clarity, 25 titles)

## Slides Requiring Author Review

- **Slide 6**: Algorithm description simplified, verify accuracy
- **Slide 12**: Results condensed significantly, ensure key findings preserved
- **Slides 20-22**: Moved to backup, confirm acceptable

## Visual Suggestions (Require New Figures)

- Slide 6: Replace text with flowchart showing recursive bisection
- Slide 14: Add bar chart comparing compactness metrics
- Slide 16: Show example district map (before/after)

## Suggested Follow-Up

- Create flowchart for slide 6 (algorithm overview)
- Practice talk to verify 15-minute target
- Consider adding one transition slide before Results section
```

**Report to user**:
- Summary of changes
- Before/after metrics
- Slides needing author review
- Visual improvements that require new figures
- Next steps for finalization

## Presentation Best Practices

### Key Principles

**One Idea Per Slide**:
- Each slide makes exactly one main point
- If explaining two concepts, use two slides
- Build complex ideas across multiple slides

**Visual First**:
- Prefer diagrams/figures over text descriptions
- 50/50 balance: half text, half visual
- Use images to reinforce messages

**Minimal Text**:
- 3-5 bullets maximum
- Short phrases (5-10 words), not sentences
- 2 bullet levels max (no deep nesting)

**Progressive Disclosure**:
- Use `\pause` to reveal bullets sequentially
- Build complex diagrams piece by piece
- Don't overwhelm with everything at once

**Clear Transitions**:
- Add transition slides between major sections
- Roadmap slides show progress through talk
- Each slide connects logically to next

**Action Titles**:
- Titles state the main message
- "Compactness improves 53%" not "Results"
- "METIS outperforms baselines" not "Comparison"

### Slide Title Patterns

**Action-oriented** (Preferred):
- "Edge weights improve compactness"
- "Three algorithm advantages"
- "Districts become more balanced"

**Statement** (Good):
- "Compactness increases 53%"
- "METIS handles large graphs efficiently"
- "Gerrymandering is a national problem"

**Question** (Occasionally):
- "Why do current districts fail?"
- "Can algorithms improve fairness?"

**Generic** (Avoid):
- "Results", "Analysis", "Methodology"
- "Discussion", "Findings", "Conclusions"

### Bullet Point Guidelines

**Parallel Structure**:
✅ Good (all verbs):
- Apply edge weights
- Partition recursively
- Validate population balance

✅ Good (all nouns):
- Edge-weighted partitioning
- Recursive bisection
- Population validation

❌ Bad (mixed):
- Apply edge weights
- Recursive bisection
- Populations are balanced

**Conciseness**:
✅ Good: "METIS recursive bisection"
❌ Bad: "We use the METIS algorithm which employs recursive bisection"

✅ Good: "53% compactness improvement"
❌ Bad: "Our results show that compactness improved by approximately 53%"

**Avoid Full Sentences**:
✅ Good: "Population balance: ±0.5%"
❌ Bad: "The population balance is maintained within plus or minus 0.5 percent."

### Visual Balance

**50/50 Rule**:
- Aim for roughly equal text and visual space
- Include figures, diagrams, or whitespace
- Avoid walls of text

**Font Sizing**:
- Title: 24-28pt
- Body text: 20-24pt
- Never below 18pt (unreadable from back of room)

**Bullet Depth**:
- ✅ 2 levels: Main bullets and sub-bullets
- ❌ 3+ levels: Too complex, hard to read

**Whitespace**:
- Don't fill every pixel
- Margins improve readability
- Empty space draws attention to content

### Time Targeting

**Standard pacing** (~1 minute per slide):
- 10-minute talk: 10-12 slides
- 15-minute talk: 15-18 slides
- 20-minute talk: 20-24 slides

**Slide-specific timing**:
- Title slide: ~30 seconds
- Roadmap slide: ~30 seconds
- Dense technical slide: ~90-120 seconds
- Simple concept slide: ~45-60 seconds
- Transition slide: ~15-30 seconds

**Section allocation** (percentage of slides):
- Introduction (10%): 2 slides for 20-slide talk
- Background (15%): 3 slides
- Methodology (25%): 5 slides
- Results (30%): 6 slides
- Conclusion (10%): 2 slides
- Q&A/Backup (10%): 2+ slides

## Beamer-Specific Considerations

### Commands to Preserve

**Build animations**:
```latex
\pause  % Reveal next bullet
```

**Overlay specifications**:
```latex
\only<1>{First content}
\only<2>{Second content}
\uncover<3->{Revealed on slide 3+}
```

**Highlighting**:
```latex
\alert{Important text}
\structure{Structural element}
```

**Blocks**:
```latex
\begin{block}{Title}
Content
\end{block}
```

**Multi-column**:
```latex
\begin{columns}
\column{0.5\textwidth}
Left content
\column{0.5\textwidth}
Right content
\end{columns}
```

### Commands to Use

**Frames (slides)**:
```latex
\begin{frame}{Slide Title}
Content
\end{frame}
```

**Sections** (for navigation):
```latex
\section{Methodology}
```

**Itemize** (bullet lists):
```latex
\begin{itemize}
  \item First point
  \item Second point
\end{itemize}
```

**Figures**:
```latex
\begin{figure}
  \includegraphics[width=0.6\textwidth]{figure.png}
\end{figure}
```

### Avoid

**Excessive animations**:
- Don't animate every element (distracting)
- Use `\pause` sparingly (2-3 per slide max)
- Avoid fancy transitions

**Tiny fonts**:
- Never `\tiny` or `\scriptsize` for body text
- If text doesn't fit, split into multiple slides

**Deep nesting**:
- Max 2 bullet levels
- Deeper nesting → hard to read

**Wall of text**:
- No paragraphs on slides
- Use bullets or figures instead

## Troubleshooting

**Beamer compilation errors after editing**:
```
Issue: Missing frame end or unmatched braces
Solution: Check all \begin{frame} have matching \end{frame}
         Verify all braces {} match
```

**Overlay specifications broken**:
```
Issue: \only<> or \uncover<> not working
Solution: Check overlay numbers are sequential
         Ensure no conflicting specifications
```

**Still too many slides after editing**:
```
Issue: Presentation still 5+ slides too long
Solution:
  - Move methodology details to backup slides
  - Combine similar result slides
  - Remove background material audience likely knows
  - Consider skipping less important findings
```

**Slides too sparse after condensing**:
```
Issue: Reduced too aggressively, slides now empty
Solution: Add figures/diagrams to fill space
         Split overly combined slides back apart
         Add transition slides between sections
```

**Title improvements unclear**:
```
Issue: Hard to make titles action-oriented
Solution: State the main takeaway as title
         Ask: "What should audience remember?"
         Example: "Results" → "Districts are 53% more compact"
```

## Quality Checklist

Before finalizing edits:

### Content
- [ ] One main idea per slide
- [ ] Slide titles convey key messages
- [ ] 3-5 bullets per slide (not more)
- [ ] No full sentences in bullets
- [ ] All jargon defined or removed

### Visual
- [ ] Figures support text (not redundant)
- [ ] ~50% visual space (figures/whitespace)
- [ ] Font sizes readable (≥20pt)
- [ ] Bullet depth max 2 levels
- [ ] Consistent visual style

### Structure
- [ ] Clear opening (motivation + roadmap)
- [ ] Logical flow between slides/sections
- [ ] Transition slides between major sections
- [ ] Strong conclusion (takeaways + next steps)
- [ ] Q&A slide at end

### Timing
- [ ] Slide count matches duration target
- [ ] ~1 minute per slide average
- [ ] No overly dense slides (>2 min each)
- [ ] Pacing allows for audience processing

### Technical
- [ ] Beamer compiles without errors
- [ ] No LaTeX formatting issues
- [ ] `\pause` commands work correctly
- [ ] All figures render properly
- [ ] Citations formatted correctly

## Related Skills

- `/compile-latex` - Compile Beamer after editing to verify no errors
- `/create-presentation-figures` - Generate new figures for slides
- `/edit-paper` - Similar editing workflow for academic papers
- `/update-docs` - Documentation editing patterns

## Performance Notes

**Typical editing time**:

| Level | Time | Reduction |
|-------|------|-----------|
| Light Polish | 10-15 min | 0-10% slides |
| Standard Edit | 20-40 min | 10-20% slides |
| Heavy Edit | 40-90 min | 20-30% slides |
| Complete Overhaul | 90-120 min | 30-40%+ slides |

**Factors affecting time**:
- Presentation length (more slides = more time)
- Current density (dense slides take longer to simplify)
- Visual needs (suggesting new figures takes time)
- Restructuring required (major changes slower)

## What You'll Get

After successful presentation editing:
- **Edited Beamer files**: All `.tex` files updated with improvements
- **Edit summary**: Comprehensive report of changes made
- **Before/after metrics**: Slide count, bullets per slide, duration estimate
- **Compiled PDF**: Verified presentation compiles correctly
- **Visual suggestions**: List of figures/diagrams to create
- **Slides for review**: Flagged areas needing author attention

## Next Steps

After editing:
1. **Review flagged slides**: Check areas marked for author review
2. **Create suggested visuals**: Generate new figures/diagrams as recommended
3. **Recompile presentation**: Generate final PDF to see visual result
4. **Practice talk**: Rehearse with timer to verify duration target
5. **Get feedback**: Present to colleague for flow/clarity check
6. **Submit**: If on target and quality high, submit to conference
7. **Archive version**: Save edited version with date for future reference

## Example Usage

**Scenario**: 30-slide presentation needs to be 18 slides for 15-minute conference talk

**Steps**:
1. User invokes: `/edit-presentation`
2. Skill asks:
   - Presentation: `presentations/edge_weighted_bisection/`
   - Target: 30 slides → 18 slides for 15-minute talk
   - Level: Heavy Edit
   - Audience: General researchers
   - Key messages: "Edge weights improve compactness by 53%"
3. Skill analyzes presentation structure
4. Applies edits:
   - Merges Introduction slides 1-2
   - Splits dense Algorithm slide into 3 focused slides
   - Removes detailed Background slides
   - Consolidates 6 Result slides into 3 comparative slides
   - Moves technical details to backup slides
   - Improves all titles to be action-oriented
   - Reduces bullets from 6-8 to 3-5 per slide
5. Generates summary showing 40% slide reduction
6. Compiles successfully, now 18 slides
7. Flags Algorithm and Results sections for author review
8. Suggests 3 new figures for visual improvement

**Result**: Presentation ready for conference, on time target, clear narrative flow
