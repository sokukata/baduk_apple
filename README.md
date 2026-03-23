# ⚪🍎⚫ Baduk Apple!! ⚫🍎⚪

Bad Apple!!… but on a 19×19 Go board.

I took the original video and converted each frame into a Go position using black and white stones.

---

## 🎥 Video

https://www.youtube.com/watch?v=yifpzYfplrM

---

## ⚙️ What this does

### Frames to SGF:
- takes a sequence of images (`output_0001.jpg`, …)
- converts them to black & white
- downsamples to 19×19
- turns each frame into an SGF node

### SGF to goban rendering:
- renders everything back into a video

---

## 📝 Notes

- the SGF is optimized in size, but contains a **very large number of nodes**
- most SGF editors struggle with node count more than file size
- I recommend using **Sabaki** to open the SGF  
- even then, the full file may fail to open

To make it usable:
- `output_full.sgf` → full animation (may not open)
- `output_1.sgf` and `output_2.sgf` → split versions that can be opened in Sabaki
