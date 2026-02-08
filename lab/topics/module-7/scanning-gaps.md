# AIRS Scanning Gaps

## Topics to Cover (in order)
1. What AIRS catches -- code execution (pickle/keras), unsafe operations, bad formats, license issues
2. What AIRS does NOT catch -- behavioral backdoors, data poisoning, performance degradation, prompt injection
3. Why the gap exists -- AIRS is a serialization security scanner, not a behavioral analyzer
4. Defense in depth -- AIRS as one layer in a multi-layer security strategy
5. The honest conversation -- how to position AIRS capabilities accurately with customers

## Key Files
- `docs/research/ml-model-security-threats-2026.md` -- comprehensive threat landscape analysis
- The poisoning demo (next topic) proves the gap concretely

## How to Explore
- Read the threat research doc: categorize each threat as "AIRS catches" or "AIRS misses"
- Think about what tool or process would catch the threats AIRS misses
- Consider: where does behavioral testing fit in the pipeline?

## Student Activities
- Create a two-column table: threats AIRS catches vs threats AIRS misses
- For each gap, propose what additional control would address it
- Discuss: if a customer asks "does AIRS protect me from data poisoning?", what is the honest answer?

## Key Insight
AIRS is a serialization security scanner -- it inspects model files for known dangerous patterns. It cannot evaluate model behavior, training data quality, or inference-time attacks. Understanding this boundary is essential for honest customer conversations and defense-in-depth architecture.
