from argparse import ArgumentParser

if __name__ == '__main__':
    # Read arguments
    parser = ArgumentParser()

    # Accepts video file path, compression_speed
    parser.add_argument("-v", "--video", help="Path to video file")
    parser.add_argument("-cs", "--compression-speed", default=2, type=int, help="Compression speed when making video, a lower number means slower processing but higher compression.\nNumber ranges from 0-9")
    
    # Accepts image file path
    parser.add_argument("-i", "--image", help="Path to image file")

    # Main statements
    args = parser.parse_args()

    from vid2ascii import VID2ASCIIConverter
    from img2ascii import IMG2ASCIIConverter
    from helper import bcolors

    if args.video and args.image:
        print(f"{bcolors.WARNING}Cannot have both image and video :({bcolors.ENDC}\n")

    # If video
    elif args.video:
        converter = VID2ASCIIConverter()
        converter.set_video(args.video)
        converter.init_image_to_ascii_converter(200, 200)
        speeds = ["placebo", "veryslow", "slower", "slow", "medium", "fast", "faster", "veryfast", "superfast", "ultrafast"]
        converter.create_video(compression_speed=speeds[args.compression_speed])

    # If audio
    elif args.image:
        converter = IMG2ASCIIConverter()
        converter.set_image(args.image)
        converter.set_ascii_chars_count(200, 200)
        converter.scale_image()
        converter.create_text()
        converter.create_image()
        converter.write_to_text_file()
        converter.write_to_image_file()

    else:
        print("Nothing happened")