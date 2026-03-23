import os
from PIL import Image

def downsample_to_19x19(image_path):
    img = Image.open(image_path).convert("L")  # grayscale
    img_small = img.resize((19, 19), Image.BILINEAR)
    return img_small

def image_to_stones(img):
    black_stones = []
    white_stones = []

    pixels = img.load()

    for y in range(19):
        for x in range(19):
            value = pixels[x, y]

            if value < 128:
                black_stones.append((x, y))
            else:
                white_stones.append((x, y))

    return black_stones, white_stones

def coord_to_sgf(x, y):
    # SGF: a = 0, b = 1, ...
    return chr(ord('a') + x) + chr(ord('a') + y)
    
def compute_diff(prev, current_black, current_white):
    moves = []
    
    current = [[None]*19 for _ in range(19)]
    
    black_stones = []
    white_stones = []
    
    for x, y in current_black:
        current[y][x] = 'B'
        if prev[y][x] != 'B':
            black_stones.append((x, y))
    for x, y in current_white:
        current[y][x] = 'W'
        if prev[y][x] != 'W':
            white_stones.append((x, y))
            
    return black_stones, white_stones , current

def generate_sgf_from_folder(folder_path):
    files = sorted([f for f in os.listdir(folder_path) if f.endswith(".jpg")])
    
    print("files number :", len(files))
    
    prev_board = [[None]*19 for _ in range(19)]

    sgf = "(;SZ[19]\n"

    for i, file in enumerate(files):
   
        path = os.path.join(folder_path, file)

        img = downsample_to_19x19(path)
        black, white = image_to_stones(img)
        
        black, white, prev_board = compute_diff(prev_board, black, white)

        sgf += ";"

        if black:
            sgf += "AB"
            for (x, y) in black:
                sgf += f"[{coord_to_sgf(x, y)}]"

        if white:
            sgf += "AW"
            for (x, y) in white:
                sgf += f"[{coord_to_sgf(x, y)}]"

        sgf += "\n"

        print(f"Processed {file} ({i+1}/{len(files)})")

    sgf += ")"
    return sgf


if __name__ == "__main__":
    folder = r"/path/of/frames"
    output_file = r"/path/to/output_full.sgf"

    sgf_content = generate_sgf_from_folder(folder)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(sgf_content)
    
    print("SGF généré :", output_file)
    
    input('Press ENTER to exit')