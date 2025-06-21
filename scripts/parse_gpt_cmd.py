import os, re, subprocess, yaml, textwrap, pathlib

# Read the raw issue body
body = os.environ.get("CMD_BODY", "")
blocks = [b.strip() for b in body.split('---') if b.strip()]

for block in blocks:
    if block.startswith("UPDATE"):
        header, *rest = block.splitlines()
        target = header.split()[1]
        pat = rep = ""
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
            ["gh","issue","create","--title",title,*label_flags,"--body",textwrap.dedent(body_block)],
            check=True
        )
