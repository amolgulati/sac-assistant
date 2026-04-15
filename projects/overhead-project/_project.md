# SG&A Forecast POC

## What We're Building

Build a SAC Planning model and workflow for SG&A forecasting that replaces the current spreadsheet-driven process with a pre-populated, parameter-driven forecast. The initial POC focuses on salary and burden forecasting, controllable-cost averaging, calculation transparency, and a simpler review workflow for cost center owners.

## Key Dimensions

- Entity: Cost Center
- Time: Month
- Version: Forecast and Actual
- Measures: Salary, Burden, Non-People Costs, Adjustments, Comments

## Current Status

- PRD captured and converted into project context
- POC scope defined for salary, burden, and controllable-cost forecasting
- Working SAC design direction established from March-April touchpoints
- Salary planning feeder model approach confirmed; merit handling partly prototyped
- Burden and non-people logic still need final implementation and fallback rules

## Conventions

- Keep the baseline forecast separate from user-entered adjustments
- Prioritize transparent calculations and auditability in model design
- Prefer month-level logic over annual averages where the PRD calls for month-level granularity
- Design access around row-level security by cost center
- Use supporting feeder models to stage calculations before writing into the final planning model
- Keep the user-facing story simple first; automate calculations behind buttons and data actions later

## Open Items

- Confirm CSV salary-load format and ingestion process
- Validate headcount logic to avoid double-counting
- Define fallback logic for missing prior-year burden data
- Define fallback hierarchy for non-people cost forecasting
- Confirm whether current SAC roles still allow creating new data actions and multi-actions
- Resolve merit lookup behavior when trying to cascade from a single loaded intersection across added dimensions

## Working Design Notes

- Reuse public dimensions sourced from Datasphere where possible instead of recreating them per model
- Salary planning should likely live in a supporting SAC model, then push into the final SG&A/OE planning model
- Merit increase is intended to be loaded once by period, then propagated through calculations instead of keyed by every cost center or profit center
- Burden can be pre-populated from prior-year actuals and optionally adjusted by users via a separate adjustment line
- For early demos, prioritize a flat, Excel-like story with filters over polished charts or dashboards
