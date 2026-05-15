<!--
Tujuan: tabel 1 halaman untuk topic Telegram workspace Hermes / Second Brain
Caller: user, main, dan operator harian
Dependensi: docs/INBOX_ROUTING.md, docs/TOPIC_WORKSPACE_INDEX.md
Main Functions: ringkas fungsi topic, trigger, dan prompt cepat dalam format tabel
Side Effects: memudahkan penggunaan harian tanpa baca dokumen panjang
-->

# Telegram Topic Table

| Topic | Fungsi | Trigger | Prompt cepat |
|---|---|---|---|
| `Command Center` | Keputusan besar, brainstorming lintas lane | butuh review banyak topik | `Bandingkan 2 opsi dan pilih yang terbaik.` |
| `INBOX` | Capture awal | pesan mentah, belum jelas lane | `Tolong route pesan ini.` |
| `tasks` | Kerja aktif, action item | task, revisi, audit, implementasi | `Buat action list dari ini.` |
| `content` | Draft output publik | post, carousel, thread, script | `Ubah ini jadi LinkedIn post.` |
| `personal-crm` | Relasi dan follow-up | orang, meeting, deal, kontak | `Buat next action untuk kontak ini.` |
| `knowledge-base` | Intake knowledge dan source | URL, PDF, referensi, insight | `Ringkas dan klasifikasikan ini.` |
| `Hormozi` | Offer, pricing, funnel, sales copy | framework bisnis Hormozi | `Analisis ini pakai lens Hormozi.` |
| `ops` | Runtime, infra, automation | debug, workflow, health check | `Diagnosa masalah ini.` |
| `updates` | Summary dan alert | laporan, progress, incident | `Buat ringkasan singkat.` |

## Routing ringkas

- mentah → `INBOX`
- belajar/simpan → `knowledge-base`
- output → `content`
- action → `tasks`
- orang → `personal-crm`
- sistem → `ops`
- keputusan besar → `Command Center`
- offer/pricing/funnel → `Hormozi`
