# Meeting Synthesis

This file summarizes the transcript documents in this project folder into cleaner planning context for the assistant.

## Current Implementation Direction

- Build the user experience around a single SAC story first, with a flat planning-oriented layout rather than a chart-heavy dashboard.
- Use one or more supporting SAC planning models as feeder models for calculations and staged uploads.
- Push curated results from feeder models into the final SG&A / OE planning model instead of doing every calculation directly in the live user-facing model.
- Reuse public dimensions already maintained from Datasphere, especially profit center, reporting account, and cost center.

## Feeder Model Pattern

- A salary planning feeder model is the main starting point.
- The feeder model is used to load salary-related inputs from CSV files.
- The final planning model should receive mapped outputs from feeder models through data actions or multi-actions.
- This pattern keeps heavy setup logic and staging data out of the main end-user planning surface.

## Salary Planning Decisions

- Salary baseline is expected to come from a CSV-based load.
- The working direction is to map salary results into a single target wages account in the final model, rather than trying to manage many salary GL members during the first phase.
- A separate baseline salary line or locked baseline account is likely useful so users can compare system-loaded baseline versus manual adjustments.
- The initial story should allow manual entry and review even before all automation is finished.

## Merit Increase Decisions

- Merit increase should be loaded separately from salary detail.
- The intended load grain is by period only, not by every cost center or profit center.
- The merit file should use numeric values like `1` and `1.03`, not percent-formatted text.
- The business intent is that users enter or load merit once and SAC calculations cascade it through the model.
- A known issue remains: the current lookup-based prototype is not reliably propagating merit across all dimensions when extra dimensions such as reporting account are present.

## Burden Decisions

- Burden should ultimately be based on prior-year actuals by month and cost center.
- For early prototyping, a flat burden rate is acceptable.
- Longer term, burden should be pre-calculated or staged from historical actuals and loaded into the model rather than derived only from a simple fixed assumption.
- The likely user pattern is system-calculated burden plus an adjustment mechanism for overrides.

## Non-People Cost Direction

- Non-people controllable costs are expected to use trailing-12-month averages.
- These costs likely belong in a separate feeder model from salary planning.
- The target behavior is to spread the next year's plan across 12 months using historical averages and a fallback hierarchy.

## Story And UX Guidance

- Start with a responsive SAC story.
- Include filters such as profit center and cost center.
- Keep the page layout simple and spreadsheet-like for the first user review cycle.
- Calculation automation can be triggered later with story buttons that launch uploads, data actions, or multi-actions.
- Users want transparency into how calculations work, not just final numbers.

## SAC Technical Notes

- Time dimension behavior in SAC is largely driven by the built-in date dimension and chosen time range.
- Some public dimensions are already maintained via OData / Datasphere integration and should be reused.
- CSV uploads are sensitive to field typing and mapping; some numeric-looking inputs can be read as text unless data types are corrected explicitly.
- Rejected upload rows may reflect missing master data, especially missing reporting-account members.
- Data action permissions or visibility may currently be limited by role/access changes, which is an active blocker to confirm.

## Open Technical Questions

- Is current access sufficient to create new data actions and multi-actions in SAC?
- What is the cleanest formula pattern for merit propagation when additional dimensions are present?
- Should reporting account be kept in the feeder model, or should feeder models use simpler measure-based structures and only map into reporting accounts in the final model?
- What exact salary CSV template should corporate own and maintain?
- How should burden overrides be captured in the final model?

## Suggested Near-Term Build Order

1. Create or refine the single user-facing SAC story with the right filters and flat planning layout.
2. Rebuild the salary feeder model cleanly using existing public dimensions.
3. Confirm the CSV templates for salary and merit uploads.
4. Fix the merit propagation prototype or simplify the feeder model grain until it works consistently.
5. Add the push mechanism from feeder model to final planning model.
6. Add burden staging logic from prior-year actuals.
7. Add the separate non-people cost model using trailing-12-month averages.

## Databricks Side Idea

- One April touchpoint also surfaced a separate idea: using Databricks to make a management-report dataset searchable via natural language.
- The immediate recommendation was to show Jennifer a short demo and validate whether that use case is actually valuable before investing further.
