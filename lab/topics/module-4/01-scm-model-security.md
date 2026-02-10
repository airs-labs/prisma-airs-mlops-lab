# SCM Model Security Console

## Topics to Cover (in order)

1. SCM as management plane — where security admins configure policy (vs SDK as data plane)
2. Model Security Dashboard — overview of scan activity
3. Scans view — finding scan results, per-rule details (information NOT available via SDK)
4. Security Groups view — default groups per source type, rule enforcement modes
5. UUIDs — finding security group UUIDs for use with the SDK/CLI

## How to Explore

- Navigate SCM: AI Security → AI Model Security
- Explore each section: Dashboard, Scans, Model Security Groups
- Reference: `.claude/reference/airs-tech-docs/ai-model-security.md` (sections: "Default Security Groups and Rules", "Viewing Scan Results")

## Student Activities

- Navigate to the Model Security dashboard and describe what they see
- Find the Scans view — initially may be empty, will populate after Challenge 4.3
- Find the Security Groups view — identify default groups per source type
- Record UUIDs for: Default Local, Default GCS, Default Hugging Face
- Click into a security group to explore rules and their enforcement settings
- Understand which rules are HuggingFace-specific vs universal

## Key Insight

SCM shows per-rule evaluation details that the SDK does not return. When a developer asks "why was my model blocked?", the answer is in SCM, not in the SDK response. This is a real product gap worth discussing — the SDK gives aggregate counts, SCM gives the full picture. This informs the developer experience conversation in Module 5.

## Customer Talking Point

"Security admins manage policy in SCM — security groups, rules, enforcement modes. DevOps teams consume policy through the SDK in their CI/CD pipeline. They are decoupled by design: neither team needs to touch the other's tools. This maps to how enterprises already separate security operations from engineering operations."
