# KB Pre-Commit Setup (raw append-only)

## Tujuan
Mencegah perubahan tidak sengaja di `raw/` selain penambahan file baru.

## Setup (di repo knowledge-base)

1. Pastikan script sudah tersedia:
   - `openclaw/scripts/kb_pre_commit_raw_append_only.sh`
2. Di folder repo `knowledge-base/`, pasang hook pre-commit:

```bash
mkdir -p .git/hooks
ln -sf ../../openclaw/scripts/kb_pre_commit_raw_append_only.sh .git/hooks/pre-commit
```

## Behavior
- Allowed: `A raw/<new-file>`
- Blocked: modify/delete/rename file lama di `raw/`

## Emergency Bypass
Hanya untuk kasus khusus dengan approval eksplisit:

```bash
KB_ALLOW_RAW_MUTATION=1 git commit -m "kb: [update] emergency raw fix"
```
