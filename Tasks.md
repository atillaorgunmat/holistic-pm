_Example lineage: Idea → T-0007 (Open) → PR #42 → T-0007 (Done)_

PH-00  Initiation
│
├─ T-0001  Initialise repository skeleton [Done]
├─ T-0002  Configure GitHub Actions (blockers, summary, impact) [Done]
├─ T-0003  Draft Governance.md baseline [Done]
├─ T-0004  Establish Issue template & GPT-CMD pipeline [Done]
├─ T-0005  Create first snapshot generator [Open]
├─ T-0006  Clarify templates & add example [Open]
├─ T-0007  Insert Phase-Gate checklist & labels [Open]
├─ T-0008  Add Disaster-Recovery note & script [Open]
└─ T-0009  Create weekly cleanup Action [Open]

PH-01  Planning
│
├─ T-0101  Requirements breakdown [Open]
├─ T-0102  High-level architecture [Open]
└─ T-0103  Phase-gate schedule [Open]

PH-02  Build
│
└─ *(to be detailed after Planning)*

PH-03  Validation
│
└─ *(to be detailed)*

PH-04  Handover
│
└─ *(to be detailed)*
UPDATE Tasks.md
pattern: "T-0001.[Open]"
replacement: "T-0001 Initialise repository skeleton [Done]"
UPDATE Tasks.md
pattern: "T-0002.[Open]"
replacement: "T-0002 Configure GitHub Actions (blockers, summary, impact) [Done]"
UPDATE Tasks.md
pattern: "T-0003.[Open]"
replacement: "T-0003 Draft Governance.md baseline [Done]"
UPDATE Tasks.md
pattern: "T-0004.[Open]"
replacement: "T-0004 Establish Issue template & GPT-CMD pipeline [Done]"
CREATE issue
title: "[TASK] T-0005 Snapshot generator validation"
labels: ["task", "task:open"]
body: |
Task-ID: T-0005
Description: Validate that the daily summary.yml workflow writes a file to Snapshots/YYYY-MM-DD.md and commits without errors.
Effort: ≤ 6 h
Exit-Criteria: Snapshot file exists and commit is green.
CREATE issue
title: "[TASK] T-0006 Clarify templates & example"
labels: ["task", "task:open"]
body: |
Task-ID: T-0006
Description: Add an example filled-in ISSUE_TEMPLATE/task.yml in /docs/examples/ and reference it in Governance.md.
Effort: ≤ 6 h
CREATE issue
title: "[TASK] T-0007 Phase-Gate checklist & labels"
labels: ["task", "task:open"]
body: |
Task-ID: T-0007
Description: Create label set phase:pending-review, phase:approved; embed checklist table in Governance.md.
Effort: ≤ 6 h
CREATE issue
title: "[TASK] T-0008 Disaster-Recovery script"
labels: ["task", "task:open"]
body: |
Task-ID: T-0008
Description: Flesh out scripts/restore_ctx.ps1 to restore latest snapshot and reopen any risk:blocker tasks.
Effort: ≤ 6 h
CREATE issue
title: "[TASK] T-0009 Weekly cleanup Action"
labels: ["task", "task:open"]
body: |
Task-ID: T-0009
Description: Ensure cleanup.yml archives stale Work-Stream issues; test via workflow_dispatch.
Effort: ≤ 6 h
# --- 1 · ADD NEW TASK -------------------------------------------------------
UPDATE Tasks.md
pattern: "└─ T-0009.*"
multiple: false
replacement: |
  └─ T-0009  Create weekly cleanup Action [Open]
  ├─ T-0010  Implement GPT-CMD parser (auto-exec UPDATE/CREATE) [Open]

# --- 2 · CREATE PARSER SCRIPT ----------------------------------------------
CREATE file
path: scripts/parse_gpt_cmd.py
content: |
  import os, re, subprocess, yaml, textwrap, pathlib
  body = os.environ["CMD_BODY"]
  blocks = [b.strip() for b in body.split('---') if b.strip()]
  for block in blocks:
      if block.startswith("UPDATE"):
          header, *rest = block.splitlines()
          target = header.split()[1]
          pat, rep = "", ""
          for line in rest:
              if line.startswith("pattern:"):
                  pat = line.split(':',1)[1].strip().strip('"')
              elif line.startswith("replacement:"):
                  rep = line.split(':',1)[1].strip().strip('"')
          text = pathlib.Path(target).read_text(encoding='utf-8')
          text = re.sub(pat, rep, text, flags=re.M)
          pathlib.Path(target).write_text(text, encoding='utf-8')
      elif block.startswith("CREATE issue"):
          meta, _, body_block = block.partition("body:")
          meta_dict = yaml.safe_load(meta.replace("CREATE issue",""))
          title  = meta_dict["title"]
          labels = meta_dict.get("labels", [])
          label_flags = sum([["--label", l] for l in labels], [])
          subprocess.run(
            ["gh","issue","create","--title",title,*label_flags,"--body",textwrap.dedent(body_block)],
            check=True
          )

# --- 3 · PATCH WORKFLOW -----------------------------------------------------
UPDATE .github/workflows/gpt-cmd.yml
pattern: "printf '%s\\\\n' \\\"\\$CMD_BODY\\\" >> Tasks.md"
multiple: false
replacement: "python scripts/parse_gpt_cmd.py"

# --- 1 · ADD NEW TASK -------------------------------------------------------
UPDATE Tasks.md
pattern: "└─ T-0009.*"
multiple: false
replacement: |
  └─ T-0009  Create weekly cleanup Action [Open]
  ├─ T-0010  Implement GPT-CMD parser (auto-exec UPDATE/CREATE) [Open]

--- 2 · CREATE PARSER SCRIPT ----------------------------------------------
CREATE file
path: scripts/parse_gpt_cmd.py
content: |
  import os, re, subprocess, yaml, textwrap, pathlib
  
  body = os.environ.get("CMD_BODY", "")
  blocks = [b.strip() for b in body.split('---') if b.strip()]
  
  for block in blocks:
      if block.startswith("UPDATE"):
          header, *rest = block.splitlines()
          target = header.split()[1]
          pat, rep = "", ""
          for line in rest:
              stripped = line.strip()
              if stripped.startswith("pattern:"):
                  pat = stripped.split(":",1)[1].strip().strip('"')
              elif stripped.startswith("replacement:"):
                  rep = stripped.split(":",1)[1].strip().strip('"')
          if pat and rep:
              text = pathlib.Path(target).read_text(encoding="utf-8")
              text = re.sub(pat, rep, text, flags=re.M)
              pathlib.Path(target).write_text(text, encoding="utf-8")
  
      elif block.startswith("CREATE issue"):
          meta, _, body_block = block.partition("body:")
          spec = yaml.safe_load(meta.replace("CREATE issue",""))
          title  = spec["title"]
          labels = spec.get("labels", [])
          label_flags = sum([["--label", l] for l in labels], [])
          subprocess.run(
              ["gh", "issue", "create", "--title", title, *label_flags,
               "--body", textwrap.dedent(body_block)],
              check=True
          )

--- 3 · PATCH WORKFLOW -----------------------------------------------------
UPDATE .github/workflows/gpt-cmd.yml
pattern: "printf '%s\\\\n' \"\\$CMD_BODY\" >> Tasks.md"
multiple: false
replacement: "python scripts/parse_gpt_cmd.py"

