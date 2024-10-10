#################################################################
# FILE : image_editor.py
# WRITER : Adi Amar , adi.amar1 , 315244624
# EXERCISE : intro2cs ex5 2022-2023
# DESCRIPTION: A simple program that edits images
# STUDENTS I DISCUSSED THE EXERCISE WITH: nobody
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
from ex5_helper import *
from typing import Optional
import copy
import math
import sys

##############################################################################
#                                  Functions                                 #
##############################################################################


def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    """A function that get a 3D list represent a colored image, 
        and separate it to 3 channels of one color"""
    sep_channels_list = []
    channel: int = 0
    while channel < len(image[0][0]):
        channel_list = []
        for row_index in range(len(image)):
            inner_list = []
            for column_index in range(len(image[row_index])):
                inner_list.append(image[row_index][column_index][channel])
            channel_list.append(inner_list)
        sep_channels_list.append(channel_list)
        channel += 1
    return sep_channels_list


def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    """A function that get number of channels of one color, 
        represented bt 2D list, and combines those channels to 3D 
        list represent a colored image. """
    comb_channels_list: List = []
    for column_index in range(len(channels[0])):
        channels_list = []
        for pixel_index in range(len(channels[0][0])):
            inner_list = []
            for row_index in range(len(channels)):
                inner_list.append(channels[row_index]
                                          [column_index]
                                          [pixel_index])
            channels_list.append(inner_list)
        comb_channels_list.append(channels_list)
    return comb_channels_list


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    """A function which get a colored image, returns a grayscale image. """
    grayscale_image = []
    for row in colored_image:
        pixel_list = []
        for column in row:
            grayscale_pixle_value = 0
            for RGB_index in range(len(column)):
                if RGB_index == 0:
                    grayscale_pixle_value += column[RGB_index] * 0.299
                if RGB_index == 1:
                    grayscale_pixle_value += column[RGB_index] * 0.587
                if RGB_index == 2:
                    grayscale_pixle_value += column[RGB_index] * 0.114
            grayscale_pixle_value = round(grayscale_pixle_value)
            pixel_list.append(grayscale_pixle_value)
        grayscale_image.append(pixel_list)
    return grayscale_image


def blur_kernel(size: int) -> Kernel:
    kernel_matrix = []
    for row_index in range(size):
        row_list = []
        for column_index in range(size):
            cell_value = 1 / (size ** 2)
            row_list.append(cell_value)
        kernel_matrix.append(row_list)
    return kernel_matrix


def image_relevant_part(image: SingleChannelImage, kernel: Kernel, row_index, column_index) -> SingleChannelImage:
    """ A function that get an image, a kernel and a row and column index, 
        and return a list in kernel X kernel size, contains the givven 
        indexes from the image. """
    relevant_part_list = []
    index_range = (len(kernel)-1)//2
    for i in range(row_index-index_range, row_index+index_range+1):
        new_row = []
        for j in range(column_index-index_range, column_index+index_range+1):
            if i < 0 or j < 0 or i >= len(image) or j >= len(image[0]):
                new_row.append(image[row_index][column_index])
            else:
                new_row.append(image[i][j])
        relevant_part_list.append(new_row)
    return relevant_part_list


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    """ A function that get an inage and a kernel, and blur the image by
        the value of the kernel. the function uses the 
        "image_relevant_part" function. """
    blurred_image = copy.deepcopy(image)
    for i in range(len(image)):
        for j in range(len(image[0])):
            matrix_to_calc = image_relevant_part(image, kernel, i, j)
            blurred_pixel_value = 0
            for row_index in range(len(matrix_to_calc)):
                for column_index in range(len(matrix_to_calc[0])):
                    blurred_pixel_value += (matrix_to_calc[row_index]
                                                          [column_index] *
                                            kernel[row_index]
                                                  [column_index])
            blurred_pixel_value = round(blurred_pixel_value)
            if blurred_pixel_value < 0:
                blurred_pixel_value = 0
            if blurred_pixel_value > 250:
                blurred_pixel_value = 250
            blurred_image[i][j] = blurred_pixel_value
    return blurred_image


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    """ A function that get an image and 2 floats, and represent the 
        relative location of a pixel from the destination image in the source
        image, and calculate the value of the index of the destination image
        using biliniar interpolation. """
    DEL_X = x - int(x)
    DEL_Y = y - int(y)
    if x == 0 and (y == 0 or y == len(image)-1):
        return image[int(y)][int(x)]
    elif x == len(image[0])-1 and (y == 0 or y == len(image)-1):
        return image[int(y)][int(x)]
    else:
        a_x = int(x)
        a_y = int(y)
        if x >= len(image[0])-1:
            DEL_X = 1
            a_x = int(x) - 1
        if x == 0:
            DEL_X = 0
            a_x = 0
        if y >= len(image) - 1:
            DEL_Y = 1
            a_y = int(y) - 1
        if y == 0:
            DEL_Y = 0
            a_y = 0
        a_val = image[a_y][a_x]
        b_val = image[a_y+1][a_x]
        c_val = image[a_y][a_x+1]
        d_val = image[a_y+1][a_x+1]
        new_pixel_val = (a_val*(1-DEL_X)*(1-DEL_Y) + b_val*(1-DEL_X)*DEL_Y +
                         c_val*DEL_X*(1-DEL_Y) + d_val*DEL_X*DEL_Y)
        new_pixel_val = round(new_pixel_val)
        return new_pixel_val


def destination_image(height, width):
    """ A function that get hieght and width values, and returns nested list 
        in those sizes. a list contains height lists, 
        each contains width elements. """
    destination_list = []
    for column in range(height):
        inner_list = []
        for row in range(width):
            inner_list.append(0)
        destination_list.append(inner_list)
    return destination_list


def relative_position(source_image, destination_image, dest_y, dest_x):
    """ A function that gets a source image, a destination image, 
        and the x and y values of the destination image, 
        and returns a tupple contains a coordinate the relative 
        location of the pixel from the destination 
        image in the source image. """
    dest_rel_y = dest_y / (len(destination_image)-1)
    dest_rel_x = dest_x / (len(destination_image[0])-1)
    source_rel_y = dest_rel_y * (len(source_image)-1)
    source_rel_x = dest_rel_x * (len(source_image[0])-1)
    source_coordination_tupple = (source_rel_y, source_rel_x)
    return source_coordination_tupple


def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    """ A function that gets an grayscale image, and a new height and width for a new
        destination inage, and returns a resized image. the function uses the
        "destination_image", "relative_position", 
        "bilinear_interpolation" function. """
    dest_image = destination_image(new_height, new_width)
    for y_index in range(len(dest_image)):
        for x_index in range(len(dest_image[0])):
            rel_pos = relative_position(image, dest_image, y_index, x_index)
            dest_image[y_index][x_index] = bilinear_interpolation(image,
                                                                  rel_pos[0],
                                                                  rel_pos[-1])
    return dest_image


def resize_color(image, height, width):
    image = separate_channels(image)
    for channel_index in range(len(image)):
        image[channel_index] = resize(image[channel_index], height, width)
    image = combine_channels(image)
    return image


def rotate_90(image: Image, direction: str) -> Image:
    """A function that gets an image and a direction, left or right,
    and rotate the image in 90 dgrees accordingly. """
    rotated_image = []
    if direction == "R":
        for column_index in range(len(image[0])):
            inner_list = []
            for row_index in range(len(image)-1, -1, -1):
                inner_list.append(image[row_index][column_index])
            rotated_image.append(inner_list)
    else:
        for column_index in range(len(image[0])-1, -1, -1):
            inner_list = []
            for row_index in range(len(image)):
                inner_list.append(image[row_index][column_index])
            rotated_image.append(inner_list)
    return rotated_image


def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    """ A function that gets an image, ints of blur size and block size
        and a float of c, and blur the image, then calculate whether 
        every pixel value in the list is smaller than its adaptive treshols
        or not. if yes - it's make the pixel black. if not - white.
        the treshold calculate by the average value of the pixels in the
        current pixel block size X block size area minus c. """
    blurred_image = apply_kernel(image, blur_kernel(blur_size))
    edges_image = copy.deepcopy(blurred_image)
    for row_idx in range(len(blurred_image)):
        for column_idx in range(len(blurred_image[0])):
            adaptive_treshold = 0
            curr_pixel_val = blurred_image[row_idx][column_idx]
            area_pix_val = 0
            for i in range(row_idx-(block_size//2),
                           row_idx+(block_size//2)+1):
                for j in range(column_idx-(block_size//2),
                               column_idx+(block_size//2)+1):
                    if (i < 0 or j < 0 or i > len(blurred_image)-1
                            or j > len(blurred_image[0])-1):
                        area_pix_val += curr_pixel_val
                    else:
                        area_pix_val += blurred_image[i][j]
            adaptive_treshold = (area_pix_val / (blur_size**2)) - c
            if curr_pixel_val < adaptive_treshold:
                edges_image[row_idx][column_idx] = 0
            else:
                edges_image[row_idx][column_idx] = 255
    return edges_image


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    """ A function that get a grayscale image, 
        and returns a quantized image. """
    quantized_image = copy.deepcopy(image)
    for row_index in range(len(image)):
        for column_index in range(len(image[0])):
            curr_pixel_val = image[row_index][column_index]
            q_pix = round(int(curr_pixel_val * (N/256)) * (255/(N-1)))
            quantized_image[row_index][column_index] = q_pix
    return quantized_image


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    """ A function that get a colorede image, 
        and returns a quantized image. the function 
        first separte the colored channels to quantize each one color channel
        on its own, then combine the quantized channels 
        into one colored image and returns it. the function uses the 
        "separate_channels", "quantize" and "combine_channels" function. """
    quantized_image = copy.deepcopy(image)
    sep_quan_image = separate_channels(quantized_image)
    new_sep_quan = []
    for channel_index in range(len(sep_quan_image)):
        quantized_channel = quantize(sep_quan_image[channel_index], N)
        new_sep_quan.append(quantized_channel)
    quantized_combined_image = combine_channels(new_sep_quan)
    return quantized_combined_image


def check_float(string):
    """ A function checks whether a givven string is a float or not. """
    try:
        float(string)
        return True
    except ValueError:
        return False


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Invalid arguments number")
        exit()

    input_image = load_image(sys.argv[1])
    message_to_user = """Choose an action to comitt: 
    1. Convert to grascale image.
    2. Blur the image. 
    3. Resize.
    4. Rotate.
    5. Get edges.
    6. Quantize.
    7. Show the image.
    8. Quit program. 
    Reply with a number: """
    chosen_act = input(message_to_user)
    while chosen_act != "8":
        while chosen_act not in "1234567":
            chosen_act = input("Invalid input. Choose a valid one: ")

        if chosen_act == "1":
            if type(input_image[0][0]) != list:
                print("The image is already grayscaled.")
            else:
                input_image = RGB2grayscale(input_image)
            chosen_act = input("Choose a number of a new action: ")
            while chosen_act not in "12345678":
                chosen_act = input("Invalid input. Choose a valid one: ")

        if chosen_act == "2":
            kernel_size = input("Insert a positive odd number as a kernel: ")
            while not kernel_size.isdigit():
                kernel_size = input("Invalid kernel. Insert another one: ")
            while int(kernel_size) % 2 == 0:
                kernel_size = input("Invalid kernel. Insert another one: ")
                while not kernel_size.isdigit():
                    kernel_size = input("""Invalid kernel. 
Insert another one: """)
            kernel_size = int(kernel_size)
            if type(input_image[0][0]) == list:
                input_image = separate_channels(input_image)
                for sep_chan_idx in range(len(input_image)):
                    input_image[sep_chan_idx] = apply_kernel(input_image
                                                             [sep_chan_idx],
                                                             blur_kernel
                                                             (kernel_size))
                input_image = combine_channels(input_image)
            else:
                input_image = apply_kernel(input_image, blur_kernel
                                           (kernel_size))
            chosen_act = input("Choose a number of a new action: ")
            while chosen_act not in "12345678":
                chosen_act = input("Invalid input. Choose a valid one: ")

        if chosen_act == "3":
            new_image_sizes = input("""Insert positive integers of height 
and width separated by a comma: """)
            while "," not in new_image_sizes:
                new_image_sizes = input("Insert sizes separated by a comma: ")
            sizes_list = new_image_sizes.split(",")
            while (not sizes_list[0].isdigit() or
                   not sizes_list[-1].isdigit()):
                new_image_sizes = input("Insert a valid integers: ")
                while "," not in new_image_sizes:
                    new_image_sizes = input(
                        "Insert sizes separated by a comma: ")
                sizes_list = new_image_sizes.split(",")
            while int(sizes_list[0]) <= 1 or int(sizes_list[-1]) <= 1:
                new_image_sizes = input("Insert integers greater than 1: ")
                while "," not in new_image_sizes:
                    new_image_sizes = input(
                        "Insert sizes separated by a comma: ")
                sizes_list = new_image_sizes.split(",")
                while (not sizes_list[0].isdigit()
                       or not sizes_list[-1].isdigit()):
                    new_image_sizes = input("Insert a valid integers: ")
                    while "," not in new_image_sizes:
                        new_image_sizes = input(
                            "Insert sizes separated by a comma: ")
                    sizes_list = new_image_sizes.split(",")
            new_height = int(sizes_list[0])
            new_width = int(sizes_list[-1])
            if type(input_image[0][0]) == list:
                input_image = resize_color(input_image, new_height, new_width)
            else:
                input_image = resize(input_image, new_height, new_width)
            chosen_act = input("Choose a number of a new action: ")
            while chosen_act not in "12345678":
                chosen_act = input("Invalid input. Choose a valid one: ")

        if chosen_act == "4":
            rotation_side = input(
                "Insert 'R' to rotate right, 'L' to rotate left: ")
            while rotation_side != "R" and rotation_side != "L":
                rotation_side = input("Insert a valid input: ")
            input_image = rotate_90(input_image, rotation_side)
            chosen_act = input("Choose a number of a new action: ")
            while chosen_act not in "1234567":
                chosen_act = input("Invalid input. Choose a valid one: ")

        if chosen_act == "5":
            values_input = input("""Insert a blur size, a block size and 
value for c separated by a commas: """)
            while values_input.count(",") != 2:
                values_input = input("Insert two commas: ")
            val_list = values_input.split(",")
            while (not val_list[0].isdigit() or not val_list[1].isdigit()
                   and (not val_list[-1].isdigit and
                        not check_float(val_list[-1]))):
                values_input = input("Insert a valid numbers: ")
                while values_input.count(",") != 2:
                    values_input = input("Insert two commas: ")
                val_list = values_input.split(",")
            while (int(val_list[0]) <= 0 or int(val_list[0]) % 2 == 0
                   or int(val_list[1]) <= 0 or int(val_list[1]) % 2 == 0
                   or float(val_list[-1]) < 0):
                values_input = input("Insert a valid numbers: ")
                while values_input.count(",") != 2:
                    values_input = input("Insert two commas: ")
                val_list = values_input.split(",")
                while (not val_list[0].isdigit() or not val_list[1].isdigit()
                       or (not val_list[-1].isdigit and
                       not check_float(val_list[-1]))):
                    values_input = input("Insert a valid numbers: ")
                    while values_input.count(",") != 2:
                        values_input = input("Insert two commas input: ")
                    val_list = values_input.split(",")
            blur_size = int(val_list[0])
            block_size = int(val_list[1])
            c = float(val_list[-1])
            if type(input_image[0][0]) == list:
                input_image = RGB2grayscale(input_image)
            input_image = get_edges(input_image, blur_size, block_size, c)
            chosen_act = input("Choose a number of a new action: ")
            while chosen_act not in "12345678":
                chosen_act = input("Invalid input. Choose a valid one: ")

        if chosen_act == "6":
            quantize_val = input("""Insert an integer value greater 
than 1 for the quantize: """)
            while not quantize_val.isdigit() or int(quantize_val) <= 1:
                quantize_val = input("Insert a valid input: ")
            quantize_val = int(quantize_val)
            if type(input_image[0][0]) == list:
                input_image = quantize_colored_image(input_image,
                                                     quantize_val)
            else:
                input_image = quantize(input_image, quantize_val)
            chosen_act = input("Choose a number of a new action: ")
            while chosen_act not in "12345678":
                chosen_act = input("Invalid input. Choose a valid one: ")

        if chosen_act == "7":
            show_image(input_image)
            chosen_act = input("Choose a number of a new action: ")
            while chosen_act not in "12345678":
                chosen_act = input("Invalid input. Choose a valid one: ")

    path_to_save = input("Insert a path to save the image: ")
    save_image(input_image, path_to_save)
    exit()
