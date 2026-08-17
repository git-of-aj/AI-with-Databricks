1. Reusable process skill (step by step process)
2. Tool-based skill (get info from one tool paste to another)
3. Conventions/standards skill ( consistent tone, format, or quality—even when the underlying content changes—for example, drafting a blog post using a style guide and supporting materials.)

> A skill is a versioned bundle of files plus a SKILL.md manifest (front matter + instructions). Skills are modular instructions you can use to codify processes and conventions, from company style guides to multi-step workflows.
- This is based on [Agent SKills](https://agentskills.io/home)
- The LLM auto decides when to use skill but “use the <skill name> skill” is what guarentees skill use.
- The model decides whether to invoke a skill based on this metadata. If the model invokes a skill, it uses the path to read the full Markdown instructions from SKILL.md.
A typical SKILL.md file defines:
- What the skill does 
- Required inputs
- Step-by-step instructions (numbered steps are helpful)
- Required output format  (uploaded examples are helpful)
- Final checks before completion

> Design tip: Skills often work best as small building blocks you can mix and match, rather than one massive end-to-end skill. For complex workflows, consider splitting them into smaller skills.
