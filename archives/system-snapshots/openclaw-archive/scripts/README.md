# Scripts

Folder ini disiapkan untuk integrasi kecil yang membuat OpenClaw lebih operasional, bukan lebih rumit.

Prioritas awal yang diambil dari acuan NotebookLM lalu disesuaikan dengan workspace ini:

- `record-mic.sh`
  - rekam mic Mac lokal via `ffmpeg` + `avfoundation`
  - output default ke `scripts/output`
- `todoist_api.sh`
  - wrapper tipis ke Todoist API
  - tugasnya hanya request dasar dan handling auth
- `sync_task.sh`
  - buat / update task status dari workflow OpenClaw
  - target status utama: `In Progress`, `Waiting`, `Done`
- `add_comment.sh`
  - tambahkan progres sub-step ke task tanpa harus buka terminal log
- `google-auth.js`
  - helper auth untuk Gmail / Calendar / Drive kalau integrasi itu benar-benar dipakai harian
- `session_checkpoint_worker.py`
  - auto-checkpoint Obsidian memory tiap 20 chat per session
  - output ke `knowledge-base/wiki/sessions/` (ringkas: keputusan, fakta baru, blocker, next action)
  - merapikan konteks aktif dengan overwrite file `*-active.md` agar konteks lama yang tidak relevan terbuang

Aturan implementasi:

- Telegram tetap interface utama; script hanya jadi layer integrasi.
- Semua script harus fail fast, log secukupnya, dan jangan pernah mencetak secret.
- Jangan implementasi penuh sebelum env, token, dan use case hariannya jelas.
- Kalau script menyentuh service eksternal, dokumentasikan env yang dibutuhkan di file yang sama.
- Voice/audio transcription sengaja tidak dipakai untuk sekarang karena jalur Telegram audio REED tidak reliable.

Env yang kemungkinan dibutuhkan nanti:

- `OPENCLAW_MAC_MIC_DEVICE`
- `TODOIST_TOKEN`
- `TODOIST_PROJECT_ID`
- `TODOIST_SECTION_IN_PROGRESS`
- `TODOIST_SECTION_WAITING`
- `TODOIST_SECTION_DONE`
- credential Google OAuth yang akan diputuskan nanti
