import imageio
from PIL import Image, ImageDraw, ImageFont
import re
import numpy as np

SIZE = 800
GRID = 19
MARGIN = 40
CELL = (SIZE - 2*MARGIN) // (GRID - 1)

def sgf_to_frames(sgf_path):
    with open(sgf_path, "r", encoding="utf-8") as f:
        content = f.read()

    nodes = content.split(";")[1:]  # skip header

    board = [[None]*19 for _ in range(19)]
    frames = []

    for node in nodes:
        # Black stones
        for block in re.findall(r'AB((?:\[[a-s]{2}\])+)', node):
            for coord in re.findall(r'\[([a-s]{2})\]', block):
                x = ord(coord[0]) - ord('a')
                y = ord(coord[1]) - ord('a')
                board[y][x] = "B"

        # White stones
        for block in re.findall(r'AW((?:\[[a-s]{2}\])+)', node):
            for coord in re.findall(r'\[([a-s]{2})\]', block):
                x = ord(coord[0]) - ord('a')
                y = ord(coord[1]) - ord('a')
                board[y][x] = "W"

        # Just in case
        for block in re.findall(r'AE((?:\[[a-s]{2}\])+)', node):
            for coord in re.findall(r'\[([a-s]{2})\]', block):
                x = ord(coord[0]) - ord('a')
                y = ord(coord[1]) - ord('a')
                board[y][x] = None

        # Draw empty node to fill all frames
        img = draw_board(board)
        frames.append(img)

    return frames


def draw_board(board):
    img = Image.new("RGB", (SIZE, SIZE), (240, 200, 120))
    draw = ImageDraw.Draw(img)

    # grid
    for i in range(GRID):
        x = MARGIN + i * CELL
        draw.line((x, MARGIN, x, SIZE - MARGIN), fill=(0,0,0))
        draw.line((MARGIN, x, SIZE - MARGIN, x), fill=(0,0,0))

    # stone
    r = CELL // 2 - 2

    for y in range(19):
        for x in range(19):
            if board[y][x]:
                cx = MARGIN + x * CELL
                cy = MARGIN + y * CELL

                if board[y][x] == "B":
                    color = (0, 0, 0)
                else:
                    color = (255, 255, 255)

                draw.ellipse(
                    (cx - r, cy - r, cx + r, cy + r),
                    fill=color,
                    outline=(0,0,0)
                )
                
  
    # coordinates

    letters = "ABCDEFGHJKLMNOPQRST" # Remove I
    font = ImageFont.truetype("arial.ttf", 16)
    
    # Letter 
    for i in range(19):
        x = MARGIN + i * CELL

        # Top
        draw.text((x - 5, MARGIN - 40), letters[i], fill=(0,0,0), font=font)

        # Bottom
        draw.text((x - 5, SIZE - MARGIN + 20), letters[i], fill=(0,0,0), font=font)

    # Number
    for i in range(19):
        y = MARGIN + i * CELL

        number = str(19 - i)  # Bottom → Top

        # Left
        draw.text((MARGIN - 40, y - 7), number, fill=(0,0,0), font=font)

        # Right
        draw.text((SIZE - MARGIN + 20, y - 7), number, fill=(0,0,0), font=font)

    return img


def save_video(frames, output="output.mp4", fps=30):
    writer = imageio.get_writer(output, fps=fps)

    for i, frame in enumerate(frames):
        writer.append_data(np.array(frame))
        print(f"Frame {i+1}/{len(frames)}")

    writer.close()


if __name__ == "__main__":
    sgf_file = r"/path/to/output_full.sgf"

    frames = sgf_to_frames(sgf_file)
    save_video(frames, "badu_apple.mp4", fps=30)
    
    input('Press ENTER to exit')