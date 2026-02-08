Guide the student through exploring: $ARGUMENTS

Find the matching topic guide in lab/topics/ (search across all module directories for a file matching the argument).

Before starting, check lab/.progress.json for active blockers. If the topic requires infrastructure
that is blocked (e.g., exploring GCP-dependent topics with gcp-project-invalid blocker), warn
the student but still allow concept-level exploration.

Follow this exploration pattern:
1. **Concept**: Explain the core concept. Ask the student a question to check understanding.
2. **Wait**: Do not proceed until the student responds.
3. **Project Example**: Show a real example from this project's code/config. Walk through it.
4. **Student Activity**: Present the hands-on activity from the topic guide. Let them try it.
5. **Discussion**: After they complete it, discuss what they learned. Connect to customer scenarios.

Use the resources pointed to in the topic guide:
- For HuggingFace topics: use the huggingface_hub Python library for live data
- For code topics: read and show actual project files
- For AIRS topics: reference .claude/reference/airs-tech-docs/ and use Context7 for SCM API docs
- For threat topics: reference .claude/reference/research/ for real incident data

Update lab/.progress.json to add this topic to the current module's topics_explored list.

Remember: Progressive guidance. Never give the answer directly. Concept -> approach -> specific.
