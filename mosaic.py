from PIL import Image
import os
import random

def resize_proportionally(image, target_size):
    aspect = image.width / image.height
    if image.width > image.height:
        new_width = target_size
        new_height = int(target_size / aspect)
    else:
        new_height = target_size
        new_width = int(target_size * aspect)
    return image.resize((new_width, new_height))

def get_target_pixels(image):
    target_image_pixels = []
    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x,y))
            r, g, b = pixel[:3]
            average = int((r + g + b) / 3)
            target_image_pixels.append(average)
    return target_image_pixels

def get_source_averages(path, source_image_size):
    image_list = []
    image_brightness_list = []
    
    for file in os.listdir(path):
        source_image = Image.open(os.path.join(path, file)).convert('RGBA')
        resized_source_image = resize_proportionally(source_image, source_image_size)
        image_list.append(resized_source_image)
        total_brightness = sum(resized_source_image.resize((1, 1)).getpixel((0, 0))[:3])
        average_brightness = total_brightness // 3
        image_brightness_list.append(average_brightness)

    return image_list, image_brightness_list

def get_choices(target_image_pixels, image_list, image_brightness_list):
    choice_list = []
    threshold = 40
    for pixel in target_image_pixels:
        possible_matches = [img for img, b in zip(image_list, image_brightness_list) if abs(b - pixel) <= threshold]
        if not possible_matches:
            possible_matches = image_list
        choice_list.append(random.choice(possible_matches))
    return choice_list

def stitch(new_image, choice_list, source_image_size):
    count = 0
    for x in range(0, new_image.width, source_image_size):
        for y in range(0, new_image.height, source_image_size):
            new_image.paste(choice_list[count], (x, y))
            count += 1

def main():
    target_image_path = input("Enter the path to the target image: ")
    source_image_folder = input("Enter the path to the source images folder: ")
    final_size = int(input("Enter target height of final image: "))
    source_image_size = int(input("Enter the size of source images: "))
    
    target_image = Image.open(target_image_path).convert('RGBA')
    target_image_resized = resize_proportionally(target_image, final_size)

    new_image = Image.new('RGBA', target_image_resized.size)

    print("Getting pixel values from target image...")
    target_image_pixels = get_target_pixels(target_image_resized)

    print("Resizing and gathering pixel data from source images...")
    image_list, image_brightness_list = get_source_averages(source_image_folder, source_image_size)

    print("Calculating matches for pixels...")
    choice_list = get_choices(target_image_pixels, image_list, image_brightness_list)

    print("Stitching images into final output image...")
    stitch(new_image, choice_list, source_image_size)

    # Blend the images
    final_image = Image.blend(target_image_resized, new_image, .65)
    
    print("Finished processing!")
    final_image.save("result.png")

if __name__ == '__main__':
    main()
