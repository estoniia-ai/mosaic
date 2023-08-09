from PIL import Image
import os
import random

def resize_crop(image, size):
    #

def get_target_pixels(image):
    #

def get_small_averages(path):
    #

def get_choices():
    #

def paste():
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
    #... [Your code here]

    print("Getting pixel values from large image...")
    get_target_pixels(large_image)

    print("Resizing and gathering pixel data from small images...")
    get_small_averages(small_image_folder)

    print("Calculating matches for pixels...")
    get_choices()

    print("pasting images into final image...")
    paste()

    final_image = Image.blend(large_image_alpha, new_image, .65)
    
    print("Finishing!")
    final_image.save("result.png")

if __name__ == '__main__':
    main()
