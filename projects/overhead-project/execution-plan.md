# Execution Plan

This file converts the PRD and meeting synthesis into a practical delivery plan for the SG&A Forecast POC.

## Planning Assumptions

- The first release is a POC, not a production-hardened enterprise solution.
- The user-facing experience should be a single SAC story.
- Supporting feeder models are acceptable and preferred for staging and calculation logic.
- Public dimensions already maintained from Datasphere should be reused wherever possible.
- The first success criterion is a working planning flow with understandable baseline logic, not perfect automation across every edge case.

## Working Owners

- Product / business alignment: Amol
- SAC design support / prior prototype context: Jayce
- Corporate finance process input: Corporate Finance stakeholders
- Access / role / platform blockers: SAC admin or platform owner
- Final owner assignments: TBD if this moves beyond POC

## Phase 0: Foundation And Access

Goal:

Remove the blockers that would prevent model iteration and data-action-based automation.

Tasks:

- Confirm current SAC permissions for creating and editing data actions and multi-actions.
- Confirm which public dimensions already exist and are reliable enough to reuse.
- Confirm the base target planning model for SG&A / OE planning.
- Confirm the minimum required versions, years, and time ranges for the POC.

Suggested Owner:

- Amol
- SAC admin for access confirmation

Dependencies:

- Access to SAC modeler and action tooling
- Visibility into existing public dimensions

Exit Criteria:

- Team knows whether data actions can be created directly or need admin support.
- Core reusable dimensions are identified.
- Time horizon and target model are confirmed.

## Phase 1: Story V1

Goal:

Create a usable first-pass planning story that behaves like a controlled, filterable spreadsheet.

Tasks:

- Build a responsive SAC story.
- Add the base planning table using the final planning model.
- Add filters for cost center, profit center, and any other must-have planning slices.
- Keep layout simple and close to how finance users think about the current workbook.
- Separate baseline values from editable adjustment lines where possible.

Suggested Owner:

- Amol

Dependencies:

- Final planning model exists and is accessible
- Core dimensions are available

Exit Criteria:

- Users can open one story and filter to relevant planning slices.
- Story supports basic manual input and review.
- Layout is good enough for business walkthroughs even before automation is complete.

## Phase 2: Salary Feeder Model

Goal:

Stand up the supporting SAC model used to load and stage salary baseline data.

Tasks:

- Create or rebuild the salary feeder model cleanly.
- Reuse public dimensions instead of duplicating them where possible.
- Set up measures or minimal structures required to hold salary inputs.
- Confirm whether the feeder model should include reporting account or stay simpler and map into accounts later.
- Load sample salary data from CSV.

Suggested Owner:

- Amol
- Jayce as design reference

Dependencies:

- Public dimensions available
- Agreed salary CSV format

Exit Criteria:

- Salary feeder model loads sample salary data successfully.
- Model grain is understood and stable enough for next-step calculations.

## Phase 3: Merit Input And Propagation

Goal:

Enable merit increase logic that is entered once by period and applied consistently through the planning flow.

Tasks:

- Define the merit CSV template with numeric values like `1` and `1.03`.
- Load merit by period into the feeder model.
- Implement or revise the lookup / calculation pattern used to cascade merit logic.
- Test whether merit propagation still works when additional dimensions are present.
- If propagation remains unstable, simplify the feeder model grain instead of forcing a brittle formula.

Suggested Owner:

- Amol
- Jayce for prototype comparison

Dependencies:

- Salary feeder model working
- Ability to create calculations and test them quickly

Exit Criteria:

- Merit can be loaded once by period.
- Merit effect is visible in the intended planning output.
- Team understands whether the current formula pattern is viable or needs simplification.

## Phase 4: Push To Final Planning Model

Goal:

Move staged feeder-model results into the final planning model in a controlled way.

Tasks:

- Build data actions or multi-actions that copy staged salary and merit outputs into the target planning model.
- Decide which target reporting account receives salary outputs for the first phase.
- Add story buttons or action starters to launch uploads and actions.
- Test version, time, and account mapping rules.
- Decide when overwrite is appropriate versus protected write-back behavior.

Suggested Owner:

- Amol
- SAC admin if action tooling is access-restricted

Dependencies:

- Phase 0 access confirmation
- Salary and merit staging logic working

Exit Criteria:

- A user can trigger a controlled push from staging to final planning model.
- Mapped values land in the expected target slice.

## Phase 5: Burden Logic

Goal:

Pre-populate burden based on prior-year actuals and allow limited adjustment where needed.

Tasks:

- Confirm burden source and exact grain: by month and cost center.
- Define how prior-year actuals are extracted or staged.
- Load calculated burden rates into model storage rather than relying only on a flat temporary factor.
- Add an adjustment mechanism if users need to override pre-populated burden.
- Define fallback handling when prior-year values are missing.

Suggested Owner:

- Amol
- Corporate Finance stakeholders for business-rule confirmation

Dependencies:

- Historical actuals available at the needed grain
- Final burden override design agreed

Exit Criteria:

- Burden baseline is pre-populated from prior-year logic.
- Missing-data behavior is defined.
- Users can distinguish system baseline from manual override.

## Phase 6: Non-People Cost Model

Goal:

Add the controllable-cost forecast flow using trailing-12-month averages.

Tasks:

- Create a separate feeder model or equivalent staging structure for non-people costs.
- Build the trailing-12-month average logic.
- Define the spread method for next-year monthly plan values.
- Implement the fallback hierarchy for sparse or missing data.
- Validate that results align with finance expectations.

Suggested Owner:

- Amol
- Corporate Finance stakeholders for validation

Dependencies:

- Historical controllable-cost data available
- Fallback hierarchy agreed

Exit Criteria:

- Non-people baseline can be generated from trailing history.
- Result can be moved into the final planning model or story flow.

## Phase 7: UAT And Review Workflow

### Goal

Validate that the POC supports the intended review, comment, and publish workflow.

### Tasks

- Test with representative finance users.
- Confirm row-level access assumptions by cost center.
- Validate comment and review behavior.
- Validate publish behavior and consolidated visibility.
- Capture gaps between POC behavior and production expectations.

### Suggested Owner

- Amol
- Corporate Finance stakeholders

### Dependencies

- Earlier phases working end to end
- Test users and scenarios available

### Exit Criteria

- Users can review baseline, make changes, and publish.
- Known gaps are documented clearly.

## Immediate Next Actions

1. Confirm whether SAC currently allows creating new data actions and multi-actions.
2. Finalize the first-pass story layout and required filters.
3. Rebuild or clean the salary feeder model using public dimensions.
4. Lock the salary and merit CSV templates.
5. Resolve or simplify the merit propagation prototype.

## Build Checklist

### Story

- Responsive story created
- Primary planning table added
- Profit center filter added
- Cost center filter added
- Baseline versus adjustment visibility designed

### Salary Feeder Model

- Public dimensions reused
- Time range configured
- Required measures created
- Salary CSV successfully loaded
- Sample outputs validated

### Merit

- Merit CSV template defined
- Merit values loaded as numeric fields
- Merit calculation created
- Propagation behavior tested across dimensions

### Push Mechanism

- Data action or multi-action created
- Source and target mapping validated
- Story button configured
- Write results tested in final model

### Burden

- Prior-year burden source confirmed
- Burden rate calculation method confirmed
- Missing-data fallback defined
- User override path defined

### Non-People Costs

- T12 source data confirmed
- Averaging logic defined
- Spread method defined
- Fallback hierarchy defined

### Validation

- Test users identified
- Test scenarios listed
- Review and publish flow tested
- Open gaps documented
