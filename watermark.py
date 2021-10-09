from PIL import Image, ImageDraw, ImageFont
import math

HEX_CODE = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12,
            'D': 13, 'E': 14, 'F': 15}


class Mark:

    def __init__(self):
        """
        Initializes the text and the margin to avoid placement errors
        """
        self.text = ""
        self.margin_x = 210
        self.margin_y = 150
        self.start_x = 150
        self.start_y = 50

    def generate_text(self, text, image, color: str, style, angle, size, place, alpha, ):
        """
        Generates a text over an image.

        :param text: The text to be used as an watermark
        :param image: The image where the watermark would be applied
        :param color: The color of the text to be used, varies if 'alpha' is altered
        :param style: The font style of the watermark text
        :param angle: The angle of rotation of the text. Rotation from -360 to 360
        :param size: The font size of the text
        :param place: The position where the logo will be applied. Has six(6) modes:
        'tl' = Top Left,
        'tr' = Top Right,
        'br' = Bottom Right,
        'bl' = Bottom Left,
        'center' = Center,
        'all' = All of the above positions
        :param alpha: The opacity of the watermark '0' is transparent '255' is opaque

        :return: Returns the location of the temporary file to be used as an Image object for tkinter
        """
        self.text = text
        with Image.open(image).convert('RGBA') as img:
            final_img = Image.new('RGBA', img.size, (0, 0, 0, 0))

            # Font
            font = ImageFont.truetype(f'{style}', size=size)
            width, height = img.size

            # Color
            rgb_tuple = self.color_formatter(color)
            fill_param = (rgb_tuple[0], rgb_tuple[1], rgb_tuple[2], alpha)

            # Watermark Generation
            text_width, text_height = font.getsize(self.text)
            text_mark = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(text_mark)
            draw.text((0, 0), self.text, fill=fill_param, font=font)
            text_mark = text_mark.rotate(angle, expand=1)

            if place == 'all':
                img.paste(text_mark, (self.start_x, self.start_y), text_mark)
                img.paste(text_mark, (width // 2, height // 2), text_mark)
                img.paste(text_mark, (width - self.margin_x, self.start_y), text_mark)
                img.paste(text_mark, (self.start_x, height - self.margin_y), text_mark)
                img.paste(text_mark, (width - self.margin_x, height - self.margin_y), text_mark)
            elif place == 'tl':
                img.paste(text_mark, (self.start_x, self.start_y), text_mark)
            elif place == 'tr':
                img.paste(text_mark, (width - self.margin_x, self.start_y), text_mark)
            elif place == 'bl':
                img.paste(text_mark, (self.start_x, height - self.margin_y), text_mark)
            elif place == 'center':
                img.paste(text_mark, (width // 2, height // 2), text_mark)
            else:
                img.paste(text_mark, (width - self.margin_x, height - self.margin_y), text_mark)

            final = Image.alpha_composite(img, final_img)
            if place == 'diag':
                diag_final = self.diagonal_text(text=text, image=image, style=style, alpha=alpha, color=color)
                diag_final.save('tmp.png')
            else:
                final.save('tmp.png')
            return 'tmp.png'

    def generate_logo(self, image, logo, place, alpha):
        """
        Generates a logo over an image.

        :param image: The image where the watermark would be applied
        :param logo: The logo which will be applied over the image
        :param place: The position where the logo will be applied. Has six(6) modes:
        'tl' = Top Left,
        'tr' = Top Right,
        'br' = Bottom Right,
        'bl' = Bottom Left,
        'center' = Center,
        'all' = All of the above positions
        :param alpha: The opacity of the watermark '0' is transparent '255' is opaque

        :return: Returns the location of the temporary file to be used as an Image object for tkinter
        """
        with Image.open(image).convert('RGBA') as img:
            with Image.open(logo).convert('RGBA') as log:
                new_log = Image.new('RGBA', log.size, (255, 255, 255, alpha))
                alpha_logo = Image.alpha_composite(log, new_log)

                final_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
                width, height = img.size

                if place == 'all':
                    img.paste(alpha_logo, (self.start_x, self.start_y), alpha_logo)
                    img.paste(alpha_logo, (width // 2, height // 2), alpha_logo)
                    img.paste(alpha_logo, (width - self.margin_x, self.start_y), alpha_logo)
                    img.paste(alpha_logo, (self.start_x, height - self.margin_y), alpha_logo)
                    img.paste(alpha_logo, (width - self.margin_x, height - self.margin_y), alpha_logo)
                elif place == 'tl':
                    img.paste(alpha_logo, (self.start_x, self.start_y), alpha_logo)
                elif place == 'tr':
                    img.paste(alpha_logo, (width - self.margin_x, self.start_y), alpha_logo)
                elif place == 'bl':
                    img.paste(alpha_logo, (self.start_x, height - self.margin_y), alpha_logo)
                elif place == 'center':
                    img.paste(alpha_logo, (width // 2, height // 2), alpha_logo)
                else:
                    img.paste(alpha_logo, (width - self.margin_x, height - self.margin_y), alpha_logo)
                final = Image.alpha_composite(img, final_img)
                final.save('tmp.png')
                return 'tmp.png'

    def diagonal_text(self, text, image, style, alpha, color: str):
        """
        Generates the text diagonally along an image based on the size (width and height) of the image
        without specifying the rotation. This a special option only for Text Watermark. Uses the 'math' library
        to do the calculations.

        :param text: The text to be used as an watermark
        :param image: The image where the watermark would be applied
        :param style: The font style of the watermark text
        :param alpha: The opacity of the watermark '0' is transparent '255' is opaque
        :param color: The color of the text to be used, varies if 'alpha' is altered

        :return: Returns a PIL Image object
        """
        self.text = text
        text_len = len(self.text)
        font_ratio = 2.3

        with Image.open(image).convert('RGBA') as img:
            final_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
            width, height = img.size

            # Color
            rgb_tuple = self.color_formatter(color)
            fill_param = (rgb_tuple[0], rgb_tuple[1], rgb_tuple[2], alpha)

            # Measurements
            hypo = int(math.sqrt(width ** 2 + height ** 2) * 0.5)
            diag_size = int(hypo / (text_len / font_ratio))
            diag_font = ImageFont.truetype(f'{style}', size=diag_size)
            diag_angle = math.degrees(math.atan(height / width))

            text_width, text_height = diag_font.getsize(self.text)
            text_mark = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(text_mark)

            # Watermark generation diagonally
            draw.text((0, 0), self.text, fill=fill_param, font=diag_font)
            text_mark = text_mark.rotate(diag_angle, expand=1)
            x, y = text_mark.size
            xx = (width - x) // 2
            yy = (height - x) // 2
            img.paste(text_mark, (xx, yy, xx + x, yy + y), text_mark)

            final = Image.alpha_composite(img, final_img)
            return final

    def color_formatter(self, hex_color):
        """
        Formats from Hex code of a color to a RGB mode. Ignores the '#' if entered.
        :param hex_color: Hex color code of an color
        :return: A list of R G B values
        """
        if hex_color[0] == '#':
            color = hex_color[1:7].upper()
        else:
            color = hex_color[:6].upper()
        R = color[:2]
        G = color[2:4]
        B = color[4:]
        list_of_colors = [R, G, B]
        final_list = []
        for item in list_of_colors:
            digit_value = HEX_CODE.get(item[0])
            partial_value = digit_value * 16
            partial_value += HEX_CODE.get(item[1])
            final_list.append(partial_value)
        return final_list
