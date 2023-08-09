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
    image.thumbnail((size, size), Image.ANTIALIAS)
    return image

def get_target_pixels(image):
    width, height = image.size
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = image.getpixel((x,y))
            average = int((r+g+b)/3)
            large_image_pixels.append(average)

def get_small_averages(path):
    #

def get_choices():
    #

def stitch():
    #

def main():
    large_image_path = input("Enter the path to the large image: ")
    small_image_folder = input("Enter the path to the small images folder(folder should contain between 400-1,000 images for best results: ")
    final_size = int(input("Enter target height of final image (pixel values between 1,000-20,000 for best results): "))
    small_image_size = int(input("Enter the size of small images (pixel values between 50-200 for best results): "))
    
    image_list = []
    image_brightness_list = []
    new_image = Image.new('RGBA', (final_size, final_size))
    large_image = Image.open(large_image_path)
    large_image_alpha = Image.open(large_image_path).convert('RGBA')
    
    scale = int(final_size/small_image_size)
    large_image_pixels = []

    print("Resizing large image...")
    #

    print("Getting pixel values from large image...")
    get_target_pixels(large_image)

    print("Resizing and gathering pixel data from small images...")
    get_small_averages(small_image_folder)

    print("Calculating matches for pixels...")
    get_choices()

    print("Stitching images into final output image...")
    stitch()

    final_image = Image.blend(large_image_alpha, new_image, .65)
    
    print("Finished processing!")
    final_image.save("result.png")

if __name__ == '__main__':
    main()
