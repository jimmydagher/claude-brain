---
tags:
  - memory/technical
---
> Scope: datasets, SQL, metrics, statistics, spreadsheets, charts from data · Pairs with: [[MEMORY/VISUAL|VISUAL]] (chart design), [[MEMORY/RESEARCH|RESEARCH]], [[MEMORY/WRITING|WRITING]] (reports)

## Core Rules (non-negotiable)

### RULE#1 Define before you query
Pin down the question, metric definitions, time window, grain and filters. Ask only if a wrong guess would change the answer.

### RULE#2 Profile the data first
Check row counts, nulls, duplicates, freshness and completeness before analyzing.

### RULE#3 Show your work
State assumptions, exclusions and caveats. Include the query when asked; otherwise name the tables, filters and logic in one line.

### RULE#4 Sanity-check before sharing
Check magnitudes, subtotals against totals and time gaps; recompute key numbers a second way.

## Defaults
- Watch for join fan-out (use `COUNT(DISTINCT)`), averaged averages, shifting denominators, partial periods, timezones, Simpson's paradox and survivorship bias.
- Report effect sizes with confidence intervals; practical ≠ statistical significance; say what the sample size can't detect.
- Mean with median; percentiles for skewed data; never drop outliers silently.
- Correlation isn't causation; disclose multiple comparisons.
- Forecasts as ranges, not single points.
- Chart by question: line = trend, bar = comparison, horizontal bar = ranking, histogram = distribution, scatter = relationship.
- Chart titles state the insight ("Revenue +23% YoY"), not the topic.
- Close with recommendations and a verdict: Ready / Share with caveats / Needs revision.
- Use the harness's data skills (e.g. `data:*`, xlsx) when they match the task.

## Avoid
- 3D charts, pies with more than 6 slices, dual axes, bar axes not starting at zero, red/green-only color.
- Unexplained swings over 50% or suspiciously round numbers.
- Segments defined by the outcome being measured.

## Output
- Quick question: the answer and one line on how it was computed.
- Analysis: finding → table or chart → method → caveats.
- Formal report: summary → methodology → findings → limitations → recommendations.
