from PIL import Image


def convert_images(path, start, end):
    for i in range(start, end+1):
        image = Image.open(f"{path}/{i}.png")
        image.putalpha(255)

        pixels = image.load()

        if i == 3:
            print(pixels[0, 0])

        for x in range(image.width):
            for y in range(image.height):
                pixel = pixels[x, y]

                if pixel[:3] == (0, 0, 0):
                    pixels[x, y] = (0, 0, 0, 0)

        image.save(f"{path}/{i}.png")

convert_images("assets/images/grass", 1, 6)