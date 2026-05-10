# KB Data Classification

## Tujuan
Menjaga memory Bani tetap rapi, aman, dan tidak kebocoran lintas lane.

## Kelas Data

### 1) Public
- Aman untuk dibagikan ke tim/publik.
- Contoh: insight umum, framework, checklist non-sensitif.
- Boleh masuk repo knowledge umum.

### 2) Internal
- Operasional internal Secondbrain.
- Contoh: SOP, routing, workflow, planning.
- Boleh masuk repo knowledge umum, tapi tidak dipublish keluar tanpa approval.

### 3) Sensitive
- Informasi bisnis/relasi yang bisa berdampak jika tersebar.
- Contoh: status klien, negosiasi, strategi pricing, pipeline deal.
- Boleh disimpan di knowledge repo hanya jika minim data pribadi dan tidak memuat secret.

### 4) Restricted (Default Wellbeing/Personal)
- Data personal/health/mental/wellbeing dan hal privat individu.
- Default: **tidak masuk repo knowledge umum**.
- Hanya boleh dipindahkan jika ada approval eksplisit user.

## Mapping Praktis
- `knowledge-base/raw/` -> Public/Internal/Sensitive (tanpa secret)
- `knowledge-base/wiki/` -> Public/Internal/Sensitive (sudah diringkas)
- Wellbeing/personal -> simpan terpisah, jangan auto-sync ke repo umum.

## Rules
- Jangan commit token, API key, credential, nomor sensitif, atau data identitas personal yang tidak perlu.
- Jika ragu klasifikasi, treat sebagai `Restricted` sampai ada konfirmasi.
- Saat conflict, prioritaskan keamanan data, bukan kecepatan merge.
