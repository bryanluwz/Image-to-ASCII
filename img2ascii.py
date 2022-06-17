import numpy as np
import cv2
import os
import time
import cairo
from utils import bcolors


class IMG2ASCIIConverter:
    """A class for converting an image to ASCII characters."""

    def __init__(self) -> None:
        # Image stuff
        self.image_path = ""
        self.image_array = None
        self.image_ascii_chars = ""
        self.ascii_image_array = None

        # Image variables for scaling purposes
        self.original_width = -1
        self.original_height = -1
        self.image_width = -1
        self.image_height = -1

        # ASCII chars count of width / height whichever one is smaller
        self.horizontal_ascii_chars_count = 100
        self.vertical_ascii_chars_count = 100

        # Cairo stuff
        self.cairo_context = None
        self.cairo_context_surface = None
        self.CANVAS_HEIGHT_INCREASE_PERCENTAGE = 1.32
        self.LINE_HEIGHT_INCREASE_PERCENTAGE = 1.00
        self.FONTSIZE_CALC_CONSTANT = 3200
        self.CANVAS_HEIGHT_MARGIN_TOP = -2

        self.canvas_width = -1
        self.canvas_height = -1
        self.line_height = -1

        self.gscale = [
            r'$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,"^`. ',
            "@%#*+=-:. ",
        ]

    # Basic functions
    def set_image(self, image_path: str):
        """
        Sets the `self.image_array` by using cv2.imread(image_path).

        Returns True if image_array is set successfully.
        """
        # Check if file exists
        if not os.path.exists(image_path):
            print(
                f"{bcolors.WARNING}[-] Image file of path '{image_path}' does not exist 0.o {bcolors.ENDC}\n"
            )
            return False

        # Read image in grayscale
        self.image_path = image_path
        self.image_array = cv2.imread(image_path, 0)
        self.image_height, self.image_width = self.image_array.shape
        self.original_height, self.original_width = self.image_array.shape
        return True

    def set_image_by_array(self, image_array):
        """
        Sets `self.image_array` by passing an array as argument.

        Returns True is image_array is set successfully.
        """
        # Check if image is in grayscale
        if len(image_array.shape) == 3:
            print(f"{bcolors.WARNING}[!] Image is not in grayscale {bcolors.ENDC} *o*")
            print(f"{bcolors.WARNING}[!] Trying to convert image from BGR format to grayscale :/ {bcolors.ENDC}\n")

            try:
                image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            except:
                print(
                    f"{bcolors.WARNING}[-] Conversion failed but I don't know why 0.o {bcolors.ENDC}\n"
                )
                return False

        # Set image to given array
        self.image_array = image_array
        self.image_height, self.image_width = self.image_array.shape
        self.original_height, self.original_width = self.image_array.shape
        return True

    def set_ascii_chars_count(self, horizontal: int, vertical: int):
        """
        Sets the horizontal and vertical ASCII characters count.

        Final image will have either 'horizontal' amount of characters widthwise
        or 'vertical' amount of characters heightwise, whichever one depending on
        the original image's aspect ratio.
        """
        self.horizontal_ascii_chars_count, self.vertical_ascii_chars_count = horizontal, vertical

    def show_image(self):
        """
        Shows image that is currently loaded to self.
        """
        # Do nothing if no image is in yet
        if self.image_array is None:
            print(f"{bcolors.WARNING}[!] No image has been loaded yet ._. {bcolors.ENDC}\n")
            return False

        print(f"{bcolors.WARNING}[!] Press any button to continue >-< {bcolors.ENDC}\n")
        cv2.imshow("Image", self.image_array)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return True

    def scale_image_by_ratio(self, scale_ratio_x: float, scale_ratio_y: float):
        """
        Scales image by ratio, and sets image_array accordingly,
        also sets `self.image_width` and `self.image_height`,
        returns scaled image as well.
        """
        self.image_array = cv2.resize(
            self.image_array,
            (int(self.image_width * scale_ratio_x), 
            int(self.image_height * scale_ratio_y)),
            interpolation=cv2.INTER_AREA,
        )
        self.image_height, self.image_width = self.image_array.shape
        return self.image_array

    def scale_image(self):
        """
        Scales image to appropriate size before converting image to ASCII characters.

        Returns scaled image.
        """
        # Check if image_array exists
        if self.image_array is None:
            print(f"{bcolors.WARNING}[!] No image has been set yet ಥ_ಥ {bcolors.ENDC}\n")
            return

        # Scale image by `font_width_to_height_ratio` because ASCII chars are not of same width and height
        font_width_to_height_ratio = 5 / 2

        self.scale_image_by_ratio(font_width_to_height_ratio, 1)

        # Scale image to horizontal or vertical ascii chars count
        scale_ratio = min((self.horizontal_ascii_chars_count / self.image_width), 
                          (self.vertical_ascii_chars_count / self.image_height))

        self.scale_image_by_ratio(scale_ratio, scale_ratio)

        return self.image_array
        
    def create_text(self, gscale_level: int=0, max_bit_value: int=256, min_bit_value: int=0):
        """
        Set `self.image_ascii_chars` to the ASCII characters created from `self.image_array` and return it.

        @param gscale_level: For choosing which grayscale ASCII characters to use.
        """
        # Check if text exists
        if self.image_array is None:
            print(f"{bcolors.WARNING}[!] No image has been set yet :< {bcolors.ENDC}\n")
            return ""

        # Make sure the gscale_level is not out of range
        gscale = self.gscale[gscale_level % len(self.gscale)]
        gscale_length = len(gscale)

        chars = '\n'.join([''.join([gscale[int((j / (max_bit_value - min_bit_value) + min_bit_value) * gscale_length)] for j in i]) for i in self.image_array])

        self.image_ascii_chars = chars

        return chars
        
    def write_to_text_file(self, text_file_path: str=""):
        """
        Writes the ASCII characters text to the file path specified.

        If no text file path is provided, then the output path will be the original one with _ascii.txt

        Extension of file path must be .txt, otherwise it will be appended.

        Returns True if write succesful.
        """
        if text_file_path == "":
            text_file_path = os.path.splitext(self.image_path)[0] + "_ascii.txt"

        # Make sure extension is .txt
        if os.path.splitext(text_file_path)[1].lower() != '.txt':
            text_file_path += '.txt'

        # Check if there is anything to write
        if self.image_ascii_chars == "":
            print(f"{bcolors.WARNING}[!] Nothing to write when saving text file, try create text first :3 {bcolors.ENDC}\n")
            return False

        print(f"{bcolors.WARNING}[!] Writing to text file of path {text_file_path} :3 {bcolors.ENDC}\n")

        with open(text_file_path, mode='w') as f:
            f.write(self.image_ascii_chars)

        print(f"{bcolors.WARNING}[+] Finished writing to text file of path {text_file_path} ·▽· {bcolors.ENDC}\n")

        return True

    def write_to_image_file(self, image_file_path: str="", extension: str=""):
        """
        Writes the created image to the file path specified.

        If not path is provided, the output path will be the original image path name with _ascii inserted.

        If extension is given, image file path's extension will be changed to the one provided.

        Returns True if write succesful.
        """
        # Check if there is a image file path
        if image_file_path == "":
            root, ext = os.path.splitext(self.image_path)
            image_file_path = root + "_ascii" + ext

        # Add extension if given, otherwise will just use image_file_path
        if extension != "":
            image_file_path = os.path.splitext(image_file_path)[0] + "." + extension
        
        # Check if there is anything to write
        if self.ascii_image_array is None:
            print(f"{bcolors.WARNING}[!] Nothing to write when saving image, try create image first ╯︿╰ {bcolors.ENDC}\n")
            return False

        print(f"{bcolors.WARNING}[!] Writing to image file of path {image_file_path} :3 {bcolors.ENDC}\n")

        try:
            cv2.imwrite(image_file_path, self.ascii_image_array)
        except:
            print(f"{bcolors.WARNING}[-] Something went wrong when writing image, and I don't know why 𓁹‿𓁹 {bcolors.ENDC}\n")
            return False

        print(f"{bcolors.WARNING}[+] Finished writing to image file of path {image_file_path} ·▽· {bcolors.ENDC}\n")
        
        return True

    def create_image(self, upscale: int=1):
        """
        Creates image from `self.image_ascii_chars`, 
        make sure you have already called to conversion funciton first.

        Returns the created image in array form
        """
        # Check if image_ascii_chars is created
        if self.image_ascii_chars == "":
            print(f"{bcolors.WARNING}[!] Nothing to write when creating image, try create text first :3 {bcolors.ENDC}\n")
            return False

        # Set up font size, and stuff
        fontsize = self.FONTSIZE_CALC_CONSTANT // self.horizontal_ascii_chars_count * upscale
        lines = self.image_ascii_chars

        # Calculate the size that the created surface should have when running for the first time
        if self.cairo_context is None:
            temp_width, temp_height = 1000, 1000
            surface = cairo.ImageSurface(cairo.FORMAT_RGB24, temp_width, temp_height)
            cairo_context = cairo.Context(surface)
            cairo_context.rectangle(0, 0, temp_width, temp_height)
            cairo_context.set_source_rgb(1, 1, 1)
            cairo_context.fill()

            cairo_context.set_source_rgb(0, 0, 0)
            cairo_context.set_font_size(fontsize)
            cairo_context.select_font_face("Consolas", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

            self.canvas_width = int(cairo_context.text_extents(lines.split('\n')[0]).width)
            self.line_height = cairo_context.text_extents(lines).height
            self.canvas_height = int(self.CANVAS_HEIGHT_MARGIN_TOP + self.line_height * (len(lines.split('\n'))) * self.CANVAS_HEIGHT_INCREASE_PERCENTAGE)
        
        # Then create a surface that is going to be used by the function
        if self.cairo_context_surface is None:
            self.cairo_context_surface = cairo.ImageSurface(cairo.FORMAT_RGB24, self.canvas_width, self.canvas_height)
            self.cairo_context = cairo.Context(self.cairo_context_surface)
            self.cairo_context.set_font_size(fontsize)
            self.cairo_context.select_font_face("Consolas", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

        # Clear surface for writing
        self.cairo_context.rectangle(0, 0, self.canvas_width, self.canvas_height)
        self.cairo_context.set_source_rgb(1, 1, 1)
        self.cairo_context.fill()

        # Start writing line
        self.cairo_context.set_source_rgb(0, 0, 0)

        for i, line in enumerate(lines.split('\n')):
            self.cairo_context.move_to(0, self.line_height * (i + 1) * self.CANVAS_HEIGHT_INCREASE_PERCENTAGE * self.LINE_HEIGHT_INCREASE_PERCENTAGE)
            self.cairo_context.show_text(line)

        # Create array from Cairo context
        image_array = np.ndarray(shape=(self.canvas_height, self.canvas_width, 4), dtype=np.uint8, buffer=self.cairo_context_surface.get_data())
        
        # Resize it to original width and height (difference shouldn't be much, ig)
        image_array = cv2.resize(image_array, (self.original_width, self.original_height), interpolation=cv2.INTER_AREA)
        self.ascii_image_array = image_array
        return True

if __name__ == "__main__":
    t0 = time.time()

    converter = IMG2ASCIIConverter()
    # converter.set_image("ඞ.png")
    converter.set_image("test_folder/rick_astley.png")
    converter.set_ascii_chars_count(200, 200)
    converter.scale_image()
    converter.create_text()
    converter.create_image()
    converter.write_to_text_file()
    converter.write_to_image_file()
    
    print(f"Wow all that took {time.time() - t0:.3f}s")