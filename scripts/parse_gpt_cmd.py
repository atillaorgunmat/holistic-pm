import os, re, subprocess, yaml, textwrap, pathlib

# ---------------------------------------------------------------------
# Read the raw body of the GitHub Issue that triggered the workflow
# ---------------------------------------------------------------------
body = os.environ.get("CMD_BODY", "")
blocks = [b.strip() for b in body.split('---') if b.strip()]   # split on '---'

for block in blocks:
    # ================================================================
    # UPDATE <file>  ➜  regex replacement inside that file
    # ================================================================
    if block.startswith("UPDATE"):
        header, *rest = block.splitlines()
        target_file = header.split()[1]               # e.g. "Tasks.md"
        pattern, replacement = "", ""

        for line in rest:
            stripped = line.strip()
            if stripped.startswith("pattern:"):
                pattern = stripped.split(':', 1)[1].strip().strip('"')
            elif stripped.startswith("replacement:"):
                replacement = stripped.split(':', 1)[1].strip().strip('"')

        if pattern and replacement:
            text = pathlib.Path(target_file).read_text(encoding="utf-8")
            text = re.sub(pattern, replacement, text, flags=re.M)
            pathlib.Path(target_file).write_text(text, encoding="utf-8")

    # ================================================================
    # CREATE issue  ➜  open a new GitHub Issue via the gh CLI
    # ================================================================
    elif block.startswith("CREATE issue"):
        meta, _, body_block = block.partition("body:")
        spec = yaml.safe_load(meta.replace("CREATE issue", ""))

        title  = spec["title"]
        labels = spec.get("labels", [])
        label_flags = sum([["--label", l] for l in labels], [])  # flatten

        subprocess.run(
            [
                "gh", "issue", "create",
                "--title", title,
                *label_flags,
                "--body", textwrap.dedent(body_block)
            ],
            check=True
        )
