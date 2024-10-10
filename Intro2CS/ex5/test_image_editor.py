import copy
import ex5_helper
from image_editor import *


def test_separate_channels_separation():
    assert separate_channels([[[1, 2]]]) == [[[1]], [[2]]]
    image = [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
    image_lst = [[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                 [[2, 2, 2], [2, 2, 2], [2, 2, 2], [2, 2, 2]],
                 [[3, 3, 3], [3, 3, 3], [3, 3, 3], [3, 3, 3]]]
    assert separate_channels(image) == image_lst


def test_separate_channels_non_mutation():
    image = [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
    image_cpy = copy.deepcopy(image)
    separate_channels(image)
    assert image == image_cpy


def test_combine_channels_combination():
    assert combine_channels([[[1]], [[2]]]) == [[[1, 2]]]
    image_lst = [[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                 [[2, 2, 2], [2, 2, 2], [2, 2, 2], [2, 2, 2]],
                 [[3, 3, 3], [3, 3, 3], [3, 3, 3], [3, 3, 3]]]
    image = [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
    assert combine_channels(image_lst) == image


def test_combine_channels_non_mutation():
    channels = [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
    channels_cpy = copy.deepcopy(channels)
    combine_channels(channels)
    assert channels == channels_cpy


def test_combine_channels_inversion():
    image = [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
    assert image == separate_channels(combine_channels(image))


def test_pixel2grayscale():
    # Tests rounding up
    assert RGB2grayscale([[[100, 180, 240]]]) == [[163]]
    # Tests rounding down
    assert RGB2grayscale([[[200, 0, 14], [15, 6, 50]]]) == [[61, 14]]


def test_blur_kernel():
    assert blur_kernel(1) == [[1]]
    assert blur_kernel(3) == [[1/9, 1/9, 1/9],
                              [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]


def test_apply_kernel():
    assert apply_kernel([[0, 128, 255]], blur_kernel(3)) == [[14, 128, 241]]
    image = [[10, 20, 30, 40, 50],
             [8, 16, 24, 32, 40],
             [6, 12, 18, 24, 30],
             [4, 8, 12, 16, 20]]
    image_blurred = [[12, 20, 26, 34, 44],
                     [11, 17, 22, 27, 34],
                     [10, 16, 20, 24, 29],
                     [7, 11, 16, 18, 21]]

    assert apply_kernel(image, blur_kernel(5)) == image_blurred


def test_bilinear_interpolation():
    assert bilinear_interpolation([[0, 64], [128, 255]], 0, 0) == 0
    assert bilinear_interpolation([[0, 64], [128, 255]], 1, 1) == 255
    assert bilinear_interpolation([[0, 64], [128, 255]], 0.5, 0.5) == 112
    assert bilinear_interpolation([[0, 64], [128, 255]], 0.5, 1) == 160
    image = [[15, 30, 45, 60, 75],
             [90, 105, 120, 135, 150],
             [165, 180, 195, 210, 225]]
    assert bilinear_interpolation(image, 4/5, 8/3) == 115


def test_resize_corners():
    # Test corners
    image = [[1, 0, 1],
             [0, 0, 0],
             [1, 0, 1]]
    resized_img = [[1, 0, 0, 0, 1],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [1, 0, 0, 0, 1]]
    assert resize(image, 4, 5) == resized_img
    assert resize(resized_img, 3, 3) == image


def test_resize_reflexivity():
    # Test that resizing an image to the same size
    # doesn't change it
    image = [[1, 2, 3],
             [4, 5, 6]]
    assert resize(image, 2, 3) == image

# TODO: Test actual interpolation behaviour


def test_resize_non_mutation():
    image = [[200, 100, 150]]
    image_cpy = copy.deepcopy(image)
    resize(image, 4, 4)
    assert image == image_cpy


def test_rotate_90():
    image1 = [[1, 2, 3],
              [4, 5, 6]]
    image2 = [[4, 1],
              [5, 2],
              [6, 3]]
    image3 = [[3, 6],
              [2, 5],
              [1, 4]]
    assert rotate_90(image1, "R") == image2
    assert rotate_90(image1, "L") == image3
    assert rotate_90(rotate_90(image2, "L"), "L") == image3

    # Test multi channel images
    image4 = [[[1, 1], [2, 2]]]
    image5 = [[[1, 1]],
              [[2, 2]]]
    assert rotate_90(image4, "R") == image5
    assert rotate_90(image5, "L") == image4

    # From the exercise PDF
    image6 = [[[1, 2, 3], [4, 5, 6]],
              [[0, 5, 9], [255, 200, 7]]]
    image7 = [[[4, 5, 6], [255, 200, 7]],
              [[1, 2, 3], [0, 5, 9]]]
    assert rotate_90(image6, 'L') == image7


def test_rotate_90_non_mutation():
    image = [[200, 100, 150]]
    image_cpy = copy.deepcopy(image)
    rotate_90(image, "R")
    assert image == image_cpy


def test_get_edges():
    image = ex5_helper.load_image('ziggy.png', ex5_helper.GRAYSCALE_CODE)
    edge_img = ex5_helper.load_image(
        'ziggy_edges.png', ex5_helper.GRAYSCALE_CODE)
    assert get_edges(image, 3, 3, 0) == edge_img


def test_quantize():
    assert quantize([[0, 50, 100], [150, 200, 250]], 8) == [
        [0, 36, 109], [146, 219, 255]]


def test_quantize_colored_image():
    ...
