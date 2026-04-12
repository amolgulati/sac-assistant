# SAC Assistant - Project Plan

## Vision
Lightweight AI assistant for SAP Analytics Cloud and Datasphere development. Uses Databricks-hosted Claude to provide intelligent guidance, code generation, and troubleshooting without requiring mouse/keyboard automation.

## Core Value Proposition
- **See what you're doing:** Upload screenshots of SAC models, Datasphere views, or error messages
- **Get expert guidance:** Claude Opus provides SAC-specific advice, formulas, and SQL
- **Copy/paste solutions:** You stay in control - review and apply suggestions manually
- **No security friction:** Pure API calls, no system automation, no IT red flags

## Technical Architecture

### Model Layer
- **Provider:** Databricks AI Gateway (Oxy's internal deployment)
- **Model:** Claude Opus 4.6 (via Databricks-hosted endpoint)
- **Auth:** Databricks personal access token
- **Privacy:** All data stays within Oxy's Databricks environment

### Core Components
1. **CLI Interface** (Phase 1)
   - Simple Python script
   - Text questions + optional screenshot path
   - Markdown-formatted responses

2. **Simple Web UI** (Phase 2)
   - Lightweight Flask or Streamlit app
   - Drag-and-drop screenshot upload
   - Chat-style conversation history
   - Copy button for code snippets

3. **Context Management** (Phase 3)
   - Save SAC model context (dimensions, measures, data sources)
   - Project-specific knowledge base
   - Common patterns library

## Use Cases

### SAC Planning Models
- "I need to create a YTD calculation for this revenue measure" + screenshot
- "Why is my allocation formula not distributing correctly?" + error screenshot
- "Generate the dimension hierarchy for our cost center structure" + data sample

### Datasphere Development
- "Convert this Excel logic into a Datasphere calculated column" + screenshot
- "Optimize this SQL view for performance" + query text
- "Create a graphical view that joins these three tables" + ERD screenshot

### Troubleshooting
- Upload error message screenshot
- Get explanation + fix suggestions
- Common SAC gotchas explained

## Implementation Phases

### Phase 1: CLI MVP (Week 1)
**Goal:** Prove the concept works with minimal code

**Deliverables:**
- `sac_assistant.py` - Core script
- `config.json` - Databricks endpoint + token config
- `README.md` - Setup and usage instructions
- `examples/` - Sample screenshots and prompts

**Success criteria:**
- Can send text question to Databricks Claude
- Can include screenshot with question
- Receives formatted response with code blocks
- Token auth works securely

**Tech stack:**
- Python 3.9+
- `requests` for API calls
- `python-dotenv` for config
- `Pillow` for image handling

### Phase 2: Web Interface (Week 2-3)
**Goal:** Make it usable without command line

**Deliverables:**
- Streamlit web app
- Conversation history
- Screenshot upload UI
- Code syntax highlighting
- Export conversation to markdown

**Success criteria:**
- Runs locally on Windows laptop
- Drag-and-drop screenshot upload
- Previous questions/answers visible
- One-click copy for code snippets

### Phase 3: Context & Patterns (Week 4+)
**Goal:** Make it smarter about your specific SAC environment

**Deliverables:**
- Project context files (model structures, naming conventions)
- Common patterns library (YTD calcs, allocations, etc.)
- SAC-specific prompt templates
- Datasphere SQL optimization patterns

**Success criteria:**
- Remembers your dimension/measure names
- Suggests solutions matching your conventions
- Pre-loaded with common SAC patterns

## Repository Structure

```
sac-assistant/
├── README.md                 # Setup and usage
├── PLAN.md                   # This file
├── requirements.txt          # Python dependencies
├── .env.example              # Config template
├── .gitignore               # Don't commit tokens!
│
├── src/
│   ├── sac_assistant.py     # Phase 1: CLI script
│   ├── databricks_client.py # API wrapper
│   ├── app.py               # Phase 2: Streamlit app
│   └── context_manager.py   # Phase 3: Project context
│
├── examples/
│   ├── screenshots/         # Sample SAC/Datasphere images
│   └── prompts.md           # Effective prompt examples
│
└── docs/
    ├── SETUP.md             # Installation guide
    ├── DATABRICKS_AUTH.md   # How to get API token
    └── SAC_PATTERNS.md      # Common use case examples
```

## Security & Compliance

**Safe for corporate environment:**
- ✅ No system automation (no PyAutoGUI, no keyboard control)
- ✅ No screen capture automation (manual screenshots only)
- ✅ API calls to internal Databricks (stays within Oxy network)
- ✅ No external API calls (no Anthropic, no OpenAI)
- ✅ Token stored in `.env` file (not in code)
- ✅ Can run without admin privileges

**Potential concerns:**
- Uploading SAC model screenshots to Databricks (contains business data)
  - Mitigation: Same Claude models already used in Databricks notebooks
  - All data stays in Oxy's tenant
- Python package installation (might need IT approval)
  - Minimal dependencies: requests, pillow, python-dotenv, streamlit
  - All common, well-known packages

## Success Metrics

**Phase 1 (Proof of value):**
- 5+ real SAC questions answered successfully
- 2+ Datasphere SQL queries generated and used
- Feedback: "This saved me [X] minutes vs. searching SAP docs"

**Phase 2 (Adoption):**
- Used 3+ times per week for SAC builds
- At least one "wow that would have taken me hours" moment
- Share with Jayce or Alex for feedback

**Phase 3 (Productivity tool):**
- Standard part of SAC development workflow
- Context library has 10+ common patterns
- Measurable time savings on model builds

## Next Steps

1. ✅ Create this plan
2. ⬜ Create GitHub repository
3. ⬜ Build Phase 1 CLI MVP
4. ⬜ Test with real SAC question + screenshot
5. ⬜ Iterate based on what works

## Open Questions

- **Databricks API endpoint format:** Need to confirm exact URL structure for Oxy's deployment
- **Token permissions:** What scopes needed for Databricks API access?
- **Image size limits:** Max screenshot size for API calls?
- **Context window:** How much SAC model context can we include per request?
- **Cost tracking:** Does Databricks usage show up in any dashboard?

---

**Philosophy:** Start stupid simple. One Python script that works beats a fancy app that doesn't. Prove value first, polish later.

**Target user:** You, building SAC models on Windows laptop, wanting Claude's help without fighting IT security.

**Non-goal:** Not trying to replace SAC. Not trying to automate clicks. Just trying to make the human (you) faster and smarter.
