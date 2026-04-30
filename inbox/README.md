# Inbox — Staging Area

Folder untuk item yang belum selesai dirutekan.

Inbox adalah capture surface, bukan lane kerja aktif.

- pending/ — item baru masuk, menunggu reed-archivist process
- processed/ — item yang sudah diklasifikasi dan ditulis ke file
- unsorted/ — item yang confidence <70%, butuh keputusan user

Dikelola oleh inbox_monitor_v2.py.

Aturan perilaku:
- user kirim ke Inbox Telegram (topic 11), `main` yang classify dan route
- balasan di Inbox hanya boleh ack singkat hasil routing
- execution, recap, reminder management, dan dialog lanjutan harus pindah ke lane tujuan
- `reed-archivist` hanya owner staging folders dan ingestion hygiene, bukan owner balasan user-facing di Inbox
