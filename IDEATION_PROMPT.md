# SAC Assistant - Ideation Prompt for AI Collaboration

> **Note:** This is the original ideation document that kicked off the project. The actual implementation took a different path — we skipped the CLI phase and went straight to a Streamlit chat UI, then restructured the roadmap into three new phases (Core UX, Project Context, Polish). See [PLAN.md](PLAN.md) for current status and the [design spec](docs/superpowers/specs/2026-04-12-sac-assistant-v2-design.md) for the implemented architecture.

## Context

I'm building an AI assistant to help with SAP Analytics Cloud (SAC) and Datasphere development work. I work in corporate finance at an oil & gas company, and I spend significant time building planning models, forecasting solutions, and data transformations.

**My environment:**
- Windows corporate laptop (restricted - can't install arbitrary automation tools)
- Access to Databricks workspace with Claude Opus 4.6 via AI Gateway
- All data stays within company's Databricks tenant (no external API calls allowed)
- Work primarily in SAP Analytics Cloud (planning models, calculations, dimensions) and SAP Datasphere (SQL views, data modeling)

**The inspiration:**
I saw a project called "Clicky" (https://github.com/farzaa/clicky) that uses Claude with computer control to help with software development. I want similar assistance for SAC/Datasphere work, but I need a corporate-safe approach that doesn't trigger IT security concerns.

**What I decided NOT to do:**
- No mouse/keyboard automation (PyAutoGUI, Playwright) - these get blocked by corporate IT
- No screen capture automation - same security concerns
- No external API calls to Anthropic/OpenAI - must use internal Databricks

**What I'm building instead:**
A lightweight tool where I can:
1. Take screenshots manually (Win+Shift+S on Windows)
2. Send the screenshot + a question to Databricks-hosted Claude
3. Get back expert guidance, formulas, SQL queries, or step-by-step instructions
4. Copy/paste the suggestions into SAC/Datasphere (I stay in control)

## Current Plan Summary

**Phase 1: CLI MVP (Week 1)**
- Simple Python script (`sac_assistant.py`)
- Takes text question + optional screenshot path
- Sends to Databricks API
- Returns formatted response
- Goal: Prove it works with real SAC questions

**Phase 2: Web Interface (Week 2-3)**
- Streamlit app
- Drag-and-drop screenshot upload
- Conversation history
- Code syntax highlighting
- Export to markdown

**Phase 3: Context & Patterns (Week 4+)**
- Save project context (my dimension names, measure structures, naming conventions)
- Build library of common patterns (YTD calculations, allocations, hierarchies)
- Pre-loaded SAC/Datasphere knowledge

**Tech stack:**
- Python 3.9+
- `requests` (Databricks API calls)
- `Pillow` (image handling)
- `python-dotenv` (config management)
- `streamlit` (web UI in Phase 2)

## Example Use Cases

**SAC Planning:**
- "I need to create a YTD calculation for this revenue measure" + screenshot of current model
- "Why is my allocation formula not distributing correctly?" + screenshot of error
- "Generate the dimension hierarchy for our cost center structure" + data sample screenshot

**Datasphere Development:**
- "Convert this Excel logic into a Datasphere calculated column" + screenshot of Excel formula
- "Optimize this SQL view for performance" + screenshot of current query
- "Create a graphical view that joins these three tables" + ERD screenshot

**Troubleshooting:**
- Upload error message screenshot
- Get explanation + suggested fixes
- Learn about common SAC gotchas

## What I Need Help With

I want you to help me **ideate and refine this plan**. Specifically:

### 1. Architecture & Design
- Is the 3-phase approach reasonable, or should I structure it differently?
- Are there better alternatives to Streamlit for the UI that would work well on a corporate Windows laptop?
- Should I build conversation history into Phase 1, or is it okay to wait until Phase 2?
- How should I structure the code to make it easy to add features later?

### 2. User Experience
- What's the most efficient workflow for capturing screenshots and asking questions?
- Should I support multi-turn conversations (building on previous context), or keep each question independent?
- How do I make it feel natural to use during actual SAC development work (not just a separate tool I have to context-switch to)?
- Should I build keyboard shortcuts or quick commands to speed up common tasks?

### 3. Context Management (Phase 3)
- How should I store project-specific context (dimension names, measure structures, conventions)?
- What format works best - JSON, YAML, markdown, or something else?
- Should context be per-project, per-model, or global?
- How do I make it easy to update context without manually editing files?

### 4. SAC/Datasphere-Specific Features
- What domain knowledge should I bake into the system prompts?
- Should I create templates for common SAC patterns (allocations, driver-based calcs, variance analysis)?
- How can I make the tool understand SAC-specific terminology and constraints?
- Should I include SAC best practices or just focus on answering specific questions?

### 5. Security & Corporate Compliance
Current approach seems safe:
- No system automation
- No external API calls (Databricks only)
- Manual screenshot capture
- Minimal Python dependencies

**Questions:**
- Are there any red flags I'm missing that could still trigger IT security concerns?
- Should I build in any safeguards to prevent accidentally exposing sensitive data?
- How should I handle screenshots that might contain confidential financial data?

### 6. Databricks Integration
- What's the typical API structure for Databricks-hosted Claude models? (I need to research this)
- How should I handle authentication (PAT tokens) securely?
- Should I cache responses to reduce API calls and costs?
- How do I track usage/costs in a corporate environment where I might not see the billing?

### 7. Phase 1 Success Criteria
- What would "proof of value" look like in the first week?
- How many successful queries would validate this is worth building?
- Should I measure time saved, quality of responses, or something else?
- At what point do I know it's time to move to Phase 2?

### 8. Potential Pitfalls
- What could go wrong with this approach?
- What assumptions am I making that might not hold up in practice?
- Are there technical constraints I'm not considering?
- What would cause me to abandon this project after Phase 1?

### 9. Alternative Approaches
- Is there a simpler way to achieve the same outcome?
- Should I consider using Databricks notebooks instead of a standalone tool?
- Could I get similar value from a browser extension or VS Code plugin?
- Are there existing tools I should evaluate before building from scratch?

### 10. Future Expansion
If this works well, what could it evolve into?
- Integration with SAC/Datasphere APIs to actually execute changes?
- Collaboration features (share patterns with team members)?
- Learning from my corrections (when the AI suggestion was wrong, improve future responses)?
- Automated documentation of model builds?

## What I'm Looking For

**Concrete, actionable feedback** on:
1. What's good about this plan?
2. What's risky or likely to fail?
3. What am I overlooking?
4. What would you do differently?
5. What should I prioritize in Phase 1?

**Think like:**
- A product manager (is this solving the right problem?)
- A software architect (is this the right technical approach?)
- A user experience designer (will this actually be pleasant to use?)
- A corporate IT security person (what will raise red flags?)

## My Constraints

**Must have:**
- Works on Windows corporate laptop (no admin rights required)
- Uses only internal Databricks API (no external services)
- Minimal Python dependencies (easier to get IT approval)
- I control execution (AI suggests, I decide)

**Nice to have:**
- Fast to use (shouldn't slow down my work)
- Remembers my context (doesn't need re-explaining every time)
- Helps me learn SAC/Datasphere better (not just giving answers)
- Could share with teammates eventually

**Non-negotiable:**
- Cannot automate clicks/keyboard
- Cannot make external API calls
- Cannot require elevated permissions
- Cannot violate data security policies

## Success Looks Like

**Short term (Week 1-2):**
- I actually use it while building a SAC model
- It saves me time vs. searching SAP documentation
- Responses are accurate and actionable
- It feels natural to integrate into my workflow

**Medium term (Month 1-3):**
- I use it multiple times per week
- I've built up a context library of my conventions
- I've had at least one "wow, this would have taken hours manually" moment
- I've shared it with Jayce (my manager) and got positive feedback

**Long term (Month 3+):**
- It's a standard part of my SAC development workflow
- I've saved measurable time on model builds
- Pattern library has 10+ reusable solutions
- Potentially adopted by other team members

## Additional Context

**About me:**
- 12 years in oil & gas finance, prior Big 4 audit
- Comfortable with Python, SQL, SAP tools
- "Vibe coder" - prefer rapid prototyping over perfect architecture
- Time-constrained (young family) - need tools that work quickly

**My work style:**
- Time-boxed sessions (30-90 min)
- Favor working prototypes over documentation
- Iterate based on real usage, not theoretical perfection
- Document decisions, not just outcomes

**Current pain points this should solve:**
- Searching through SAP documentation wastes time
- Formulas in SAC are finicky and easy to get wrong
- Datasphere SQL optimization is trial-and-error
- Hard to remember best practices across different model types
- Context-switching between development and Stack Overflow/documentation

---

## Your Task

Based on everything above:

1. **Validate or challenge** the overall approach
2. **Identify blind spots** I'm not seeing
3. **Suggest improvements** to the plan (architecture, features, workflow)
4. **Prioritize** what matters most for Phase 1
5. **Flag risks** that could derail the project
6. **Propose alternatives** if you see a better path

Be specific. Don't just say "consider security" - tell me what specific security concern and how to address it. Don't just say "improve UX" - tell me what workflow change would make it better.

**Think critically.** If this plan is likely to fail, tell me why. If there's a simpler approach I'm missing, show me. I want this to work, but I'd rather know now if I'm headed in the wrong direction.

Ready? Let's refine this thing.
