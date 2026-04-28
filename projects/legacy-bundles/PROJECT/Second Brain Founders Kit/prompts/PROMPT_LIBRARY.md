# Prompt Library: Second Brain Intelligence

Gunakan prompt ini untuk memberi instruksi kepada AI (GPT-4, Claude, dll.) agar mengolah pengetahuan Anda sesuai standar pengambil keputusan.

---

## 1. Classification Prompt (The Sorter)
*Gunakan saat Anda baru saja menangkap teks atau suara mentah.*

```text
Identity: Anda adalah Strategist & Knowledge Architect handal.
Task: Klasifikasikan catatan masuk ini ke salah satu folder Obsidian berikut:
- 10 Projects (Jika ada deadline/output spesifik)
- 20 Areas (Jika terkait tanggung jawab berkelanjutan)
- 30 Resources (Jika topik minat umum/riset)
- 40 Archives (Jika informasi statis/lampau)

Input: [MASUKKAN TEKS DI SINI]

Format Output:
- Suggested Folder:
- Key Metadata:
- Action Item: (Jika ada hal yang harus dikerjakan)
```

---

## 2. Synthesis Prompt (The Authority Builder)
*Gunakan untuk mengubah riset menjadi draft konten otoritas (Day 23 Content Calendar).*

```text
Context: Saya ingin membangun otoritas sebagai Strategic Advisor di bidang [BIDANG ANDA].
Task: Berdasarkan kumpulan riset/catatan terlampir, buatlah draft artikel "Authority Architecture" yang:
1. Memiliki hook yang menantang status quo bagi para Founder.
2. Menyajikan 3 wawasan mendalam (Deep Insights) berbasis data riset.
3. Memberikan solusi strategis yang tidak pasaran.
4. Menyertakan Call to Action (CTA) untuk "Strategic Conversation".

Riset Lampiran: [PASTE ISI CATATAN DARI OBSIDIAN]
```

---

## 3. Decision Support Prompt (The Advisor)
*Gunakan saat Anda ingin meminta AI meninjau kumpulan catatan meeting.*

```text
Identity: Anda adalah Trusted Business Advisor saya.
Context: Saya sedang mempertimbangkan keputusan [DETAIL KEPUTUSAN].
Task: Tolong tinjau riwayat catatan meeting saya terkait [PROYEK/KLIEN] dan beri saya:
1. Analisis risiko berdasarkan pola komunikasi sebelumnya.
2. Keuntungan strategis yang mungkin terlewat.
3. Rekomendasi langkah selanjutnya.

Data Meeting Notes: [PASTE CATATAN MEETING]
```

---

## Tips Penggunaan
1. **Be Specific:** Semakin detail konteks bidang Anda, semakin tajam jawabannya.
2. **Citation Check:** Jika AI memberikan jawaban dari database Anda, selalu cek file asli di Obsidian untuk memastikan akurasi data angka/fakta.
3. **Iterasi:** Jangan ragu mengubah parameter prompt di atas sesuai gaya bahasa Anda.
