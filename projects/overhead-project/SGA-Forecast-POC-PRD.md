# SG&A Forecast POC PRD

Source: converted from the Word PRD in `projects/_template/Overhead-project/SGA-Forecast-POC-PRD.docx` so the SAC Assistant can load it as project context.

## Executive Summary
Build a SAC Planning model to automate SG&A forecasting for Corporate Finance and related teams. The POC replaces manual spreadsheet workflows with a parameter-driven, pre-populated forecast that users can review and adjust. Version 1 focuses on salary and burden calculations plus trailing-12-month logic for non-people costs, with a user experience centered on transparency and auditability.

## Problem Statement

### Current State
- SG&A forecasting relies on manual spreadsheet processes.
- Recalculation after assumption changes takes 1 to 2 weeks.
- Methodology is not standardized across cost centers.
- Audit trail and version control are limited.
- Users effectively start from scratch each cycle.

### Desired State
- Automated, pre-populated forecast baseline.
- Transparent calculations that users can inspect.
- Adjustments tracked with full audit trail.
- Same-day recalculation after parameter changes.
- Cost center owners can review and provide feedback without editing the numbers directly.

## Key Features

### 1. Salary Forecast Calculation
Pre-populate salary forecast using an actuals baseline with merit increase applied.

Calculation notes:
- Data source: CSV file loaded with pre-calculated salary data from a Workday extract.
- Baseline method: 3-month average.
- Merit increase: 4% after month 3.

Open requirements:
- Confirm CSV file format and load process with Amol and Jayce.
- Validate headcount tracking to prevent double-counting.

### 2. Burden Rate Calculation
Auto-populate burden rates from prior-year actuals by month and cost center.

Requirements:
- Use prior-year actuals as the burden source.
- Preserve month-level granularity instead of an annual average.
- Build a data action to fetch and apply burden rates.
- Define fallback logic for missing prior-year data.

### 3. Non-People Cost Forecast
Forecast controllable non-salary costs using a trailing-12-month average.

Requirements:
- Averaging method: trailing 12 months.
- Distribution method: even spread.
- Build a `BUILD_AVERAGES` data action.
- Implement a fallback hierarchy.

### 4. Single-Story User Interface
All users work from a single SAC story with filtering.

UX goals:
- Eliminate multi-tab workbook management.
- Allow users to click a lead-sheet line and open a filtered cost center view.
- Show driver-loaded baseline separately from user adjustments.

### 5. Access Model
Use a tiered access model where cost center owners can view and comment but not edit values.

Security goals:
- Apply row-level security by cost center.
- Users should see only their assigned cost centers.
- Example from the PRD: Melanie sees only her 10 cost centers.

### 6. Calculation Transparency
Users should be able to see how numbers were calculated, not just the final result.

### 7. Publish Workflow
When users publish, their data writes back to the planning model.

Workflow:
1. User reviews pre-populated forecast.
2. User makes adjustments if needed.
3. User adds comments explaining changes.
4. User clicks Publish.
5. Data writes back to the planning model.
6. Changes become visible in the consolidated view.

## Technical Areas Called Out In The PRD
- SAC Planning model
- Dimensions
- Data actions
- Data load
- Dependencies
- Testing approach
- Test data
- Test users
- Acceptance criteria

These sections were listed in the source document but did not include detailed body content in the extracted text.

## Out Of Scope
The PRD references an out-of-scope section for the POC, but the extracted text did not include detailed entries.

## Related Documents
- SG&A Forecast POC Charter
- 2026 AI Roadmap
- Finance AI Operating Principles

## Working Notes
- Treat this markdown file as the assistant-readable PRD.
- Keep future project-specific notes in this folder as `.md` or `.txt` files so they are loaded automatically.