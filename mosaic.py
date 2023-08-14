from PIL import Image
import os
import random

def resize_crop(image, size):
    crop_size = 0
    if image.size[0] > image.size[1]:
        crop_size = image.size[1]
    else:
        crop_size = image.size[0]
    image = image.crop((0,0,crop_size,crop_size))
    image.thumbnail((size, size), 3)
    return image

def resize_proportionally(image, target_size):
    aspect = image.width / image.height
    if image.width > image.height:
        new_width = target_size
        new_height = int(target_size / aspect)
    else:
        new_height = target_size
        new_width = int(target_size * aspect)
    image = image.resize((new_width, new_height))
    return image

def get_target_pixels(image, target_image_pixels):
    width, height = image.size
    for x in range(0, width):
        for y in range(0, height):
            pixel = image.getpixel((x,y))
            if len(pixel) == 4:
                r, g, b, a = pixel
            else:
                r, g, b = pixel
            average = int((r+g+b)/3)
            target_image_pixels.append(average)
    return target_image_pixels

def get_source_averages(path, image_list, image_brightness_list, source_image_size):
    for file in os.listdir(path):
        source_image = Image.open("{}/{}".format(path, file))
        resized_source_image = resize_crop(source_image, source_image_size)
        image_list.append(resized_source_image)

    for image in image_list:
        width, height = image.size
        r_total, g_total, b_total, count = 0, 0, 0, 0
        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x, y))
                if len(pixel) == 4:
                    r, g, b, a = pixel
                else:
                    r, g, b = pixel
                r_total += r
                g_total += g
                b_total += b
                count += 1
        average_brightness = int((((r_total + g_total + b_total) / count) / 3))
        image_brightness_list.append(average_brightness)

    return image_list, image_brightness_list

def get_choices(target_image_pixels, image_list, image_brightness_list):
    choice_list = []
    threshold = 40
    for pixel in target_image_pixels:
        possible_matches = []
        for b in image_brightness_list:
            if abs(b - pixel) <= threshold:
                possible_matches.append(image_list[image_brightness_list.index(b)])
        
        if not possible_matches:
            possible_matches.append(random.choice(image_list))
            print("Added a random choice!")
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
    source_image_folder = input("Enter the path to the source images folder(folder should contain between 400-1,000 images for best results: ")
    final_size = int(input("Enter target height of final image (pixel values between 1,000-20,000 for best results): "))
    source_image_size = int(input("Enter the size of source images (pixel values between 50-200 for best results): "))
    
    image_list = []
    image_brightness_list = []

    # Create the new image
    new_image = Image.new('RGBA', (target_image_resized.width, target_image_resized.height))
    target_image = Image.open(target_image_path)
    target_image_alpha = Image.open(target_image_path).convert('RGBA')
    target_image_resized = resize_proportionally(target_image, final_size)

    grid_width = target_image_resized.width // source_image_size
    grid_height = target_image_resized.height // source_image_size


    target_image_pixels = []

    print("Resizing target image...")
    target_image = resize_crop(target_image, scale)
    target_image_alpha = resize_crop(target_image_alpha, final_size)
    
    print("Getting pixel values from target image...")
    target_image_pixels = get_target_pixels(target_image_resized, target_image_pixels)

    print("Resizing and gathering pixel data from source images...")
    image_list, image_brightness_list = get_source_averages(source_image_folder, image_list, image_brightness_list, source_image_size)

    print("Calculating matches for pixels...")
    choice_list = get_choices(target_image_pixels, image_list, image_brightness_list)

    print("Stitching images into final output image...")
    stitch(new_image, choice_list, source_image_size)

    # Ensure the images have the same dimensions
    print(target_image_alpha.size, target_image_alpha.mode)
    print(new_image.size, new_image.mode)
    if target_image_alpha.size != new_image.size:
        new_image = new_image.resize(target_image_alpha.size)

    # Ensure the images have the same mode
    if target_image_alpha.mode != new_image.mode:
        new_image = new_image.convert(target_image_alpha.mode)

    # Blend the images
    final_image = Image.blend(target_image_alpha, new_image, .65)
    
    print("Finished processing!")
    final_image.save("result.png")

if __name__ == '__main__':
    main()
