import struct

def read_bmp(file_path):
    with open(file_path, 'rb') as f:
        f.read(18)  # Skip BMP header
        width = struct.unpack('I', f.read(4))[0]
        height = struct.unpack('I', f.read(4))[0]
        f.read(28)  # Skip the rest of the header

        # Read the pixel data
        pixels = []
        for y in range(height):
            row = []
            for x in range(width):
                b = ord(f.read(1))
                g = ord(f.read(1))
                r = ord(f.read(1))
                row.append((r, g, b))
            pixels.append(row)

    return pixels, width, height

def write_bmp(file_path, pixels, width, height):
    with open(file_path, 'wb') as f:
        # BMP header
        f.write(b'BM')
        f.write(struct.pack('I', 54 + width * height * 3))  # File size
        f.write(b'\x00\x00')
        f.write(b'\x00\x00')
        f.write(struct.pack('I', 54))  # Pixel data offset

        # DIB header
        f.write(struct.pack('I', 40))  # DIB header size
        f.write(struct.pack('I', width))
        f.write(struct.pack('I', height))
        f.write(struct.pack('H', 1))  # Number of color planes
        f.write(struct.pack('H', 24))  # Bits per pixel
        f.write(struct.pack('I', 0))  # Compression method
        f.write(struct.pack('I', width * height * 3))  # Image size
        f.write(struct.pack('I', 2835))  # Horizontal resolution
        f.write(struct.pack('I', 2835))  # Vertical resolution
        f.write(struct.pack('I', 0))  # Number of colors
        f.write(struct.pack('I', 0))  # Important colors

        # Pixel data
        for row in pixels:
            for (r, g, b) in row:
                f.write(bytes([b, g, r]))

def crop_image(image, width, height, new_size):
    cropped = []
    for y in range(new_size):
        row = []
        for x in range(new_size):
            row.append(image[(height - new_size) // 2 + y][(width - new_size) // 2 + x])
        cropped.append(row)
    return cropped

def make_tileable(image_path, output):
    pixels, width, height = read_bmp(image_path)

    if width != height:
        new_size = min(width, height)
        cropped_image = crop_image(pixels, width, height, new_size)
        new_image_size = new_size * 2
        new_image = [[(0, 0, 0)] * new_image_size for _ in range(new_image_size)]

        for y in range(new_size):
            for x in range(new_size):
                new_image[y][x] = cropped_image[y][x]
                new_image[y][new_size + x] = cropped_image[y][x]
                new_image[new_size + y][x] = cropped_image[y][x]
                new_image[new_size + y][new_size + x] = cropped_image[y][x]

        final_image = [row[new_size // 2:new_size // 2 + new_size] for row in new_image[new_size // 2:new_size // 2 + new_size]]
    else:
        new_image_size = width * 2
        new_image = [[(0, 0, 0)] * new_image_size for _ in range(new_image_size)]

        for y in range(height):
            for x in range(width):
                new_image[y][x] = pixels[y][x]
                new_image[y][width + x] = pixels[y][x]
                new_image[height + y][x] = pixels[y][x]
                new_image[height + y][width + x] = pixels[y][x]

        final_image = [row[width // 2:width // 2 + width] for row in new_image[height // 2:height // 2 + height]]

    write_bmp(output, final_image, width, height)

# Usage example
make_tileable("C:\\Users\\sophi\\OneDrive\\Desktop\\TileMe\\concept.bmp", 'output_tileable_image.bmp')
