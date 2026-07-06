import os
import hashlib
import shutil
import sys
from collections import defaultdict

if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
    print("Usage: python3 cleanup.py <target_folder> [--execute]")
    sys.exit(1)

TARGET = os.path.abspath(sys.argv[1])
BACKUP = TARGET.rstrip("/") + "_BACKUP"
DRY_RUN = "--execute" not in sys.argv

def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def project_root(path):
    """Get the top-level project folder name (e.g. MEDALII, MEDAL_RAG)."""
    rel = os.path.relpath(path, TARGET)
    return rel.split(os.sep)[0]

def find_duplicates(files):
    by_hash = defaultdict(list)
    for f in files:
        base = os.path.basename(f)
        if base == "__init__.py" and os.path.getsize(f) == 0:
            continue
        by_hash[md5(f)].append(f)

    dup_groups = {}
    for h, paths in by_hash.items():
        if len(paths) <= 1:
            continue
        # only flag duplicates within the SAME project directory
        by_project = defaultdict(list)
        for p in paths:
            by_project[project_root(p)].append(p)
        same_project = {k: v for k, v in by_project.items() if len(v) > 1}
        if same_project:
            dup_groups[h] = same_project
    return dup_groups

def is_tmp(path):
    name = os.path.basename(path).lower()
    return (
        name.startswith("tmp")
        or name.startswith("~")
        or name.endswith("~")
        or name.endswith(".tmp")
        or name.endswith(".temp")
        or name == "text file.txt"
    )

def plan():
    all_files = []
    for root, dirs, files in os.walk(TARGET):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            path = os.path.join(root, f)
            if os.path.isfile(path):
                all_files.append(path)

    pyc_files = [f for f in all_files if f.endswith(".pyc")]
    tmp_files = [f for f in all_files if is_tmp(f)]
    non_pyc_tmp = [f for f in all_files if not f.endswith(".pyc") and not is_tmp(f)]
    dup_groups = find_duplicates(non_pyc_tmp)

    print("=" * 60)
    print("CLEANUP PLAN — PROJECTS_FOLDER")
    print("=" * 60)

    print(f"\n  Total files: {len(all_files)}")
    print(f"  Backup at:   {BACKUP}")
    print()

    actions = []

    if pyc_files:
        print(f"--- {len(pyc_files)} .pyc files to DELETE (safe — auto-regenerated) ---")
        for f in sorted(pyc_files):
            rel = os.path.relpath(f, TARGET)
            sz = os.path.getsize(f)
            actions.append(("delete", f, rel, sz))
            print(f"  DELETE  {rel}  ({sz/1024:.1f}K)")

    if tmp_files:
        print(f"\n--- {len(tmp_files)} temp files to DELETE ---")
        for f in sorted(tmp_files):
            rel = os.path.relpath(f, TARGET)
            sz = os.path.getsize(f)
            actions.append(("delete", f, rel, sz))
            print(f"  DELETE  {rel}  ({sz/1024:.1f}K)")

    # Possible redundant (pattern-based, no hardcoded paths)
    redundant = []
    for f in all_files:
        if f in [a[1] for a in actions]:
            continue
        base = os.path.basename(f)
        name_lower = base.lower()
        rel_lower = os.path.relpath(f, TARGET).lower()

        # empty files that aren't package markers
        if os.path.getsize(f) == 0 and base != "__init__.py":
            redundant.append(f)
            continue

        # session / terminal logs — date-prefixed long names or keywords
        if any(k in name_lower for k in ["session", "continued", "terminal"]):
            redundant.append(f)
            continue

        # scratch / display / structure notes
        if any(k in name_lower for k in ["knn", "display", "structure_note"]):
            redundant.append(f)
            continue

        # correction / changelog / scratch notes
        if any(name_lower.startswith(p) for p in ["correction", "scratch", "note_", "_note", "temp_note"]):
            redundant.append(f)
            continue

        # environment files — keep but flag for review
        if base == ".env":
            redundant.append(f)
            continue

        # name matches date pattern like 2026-05-15-... (likely auto-generated log)
        import re
        if re.match(r"^\d{4}-\d{2}-\d{2}-", name_lower):
            redundant.append(f)
            continue

    if redundant:
        print(f"\n--- {len(redundant)} POSSIBLE REDUNDANT (review manually) ---")
        for f in redundant:
            rel = os.path.relpath(f, TARGET)
            sz = os.path.getsize(f)
            print(f"  REVIEW  {rel}  ({sz/1024:.1f}K)")

    if dup_groups:
        print(f"\n--- Same-project duplicate files ---")
        kept_total = 0
        for h, by_project in sorted(dup_groups.items()):
            for project, paths in sorted(by_project.items()):
                paths.sort()
                keep = paths[0]
                dups = paths[1:]
                kept_total += sum(os.path.getsize(d) for d in dups)
                print(f"\n  [{project}] (md5: {h[:8]}...):")
                print(f"    KEEP    {os.path.relpath(keep, TARGET)}")
                for d in dups:
                    rel = os.path.relpath(d, TARGET)
                    sz = os.path.getsize(d)
                    actions.append(("delete_dup", d, rel, sz))
                    print(f"    DELETE  {rel}  ({sz/1024:.1f}K)")

    total_save = sum(a[3] for a in actions)
    print(f"\n  Total space to recover: {total_save/1024:.1f}K")
    print(f"  Total actions: {len(actions)}")

    if DRY_RUN:
        print(f"\n  --- DRY RUN — no files touched ---")
        print(f"  Run with: python3 cleanup.py --execute")
    else:
        print(f"\n  --- EXECUTING ---")
        confirm = input(f"  Proceed with {len(actions)} actions? (yes/no): ")
        if confirm.lower() != "yes":
            print("  Aborted.")
            return

        for action, path, rel, sz in actions:
            if action.startswith("delete"):
                os.remove(path)
                print(f"  DELETED  {rel}")

        print(f"\n  Done. {len(actions)} files removed.")

    print()

if __name__ == "__main__":
    if not os.path.exists(BACKUP):
        print(f"ERROR: Backup not found at {BACKUP}. Run backup first.")
        sys.exit(1)
    plan()
