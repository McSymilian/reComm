import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont

class CTkGradientLabel(ctk.CTkLabel):
    def __init__(self, master, text="", font=("Arial", 40, "bold"), 
                 color1="#3b8ed0", color2="#9733ee", **kwargs):
        # Initialize with no text, we will use an image instead
        super().__init__(master, text="", **kwargs)
        
        self.gradient_text = text
        self.font_tuple = font
        self.color1 = color1
        self.color2 = color2
        
        # Draw the initial texts
        self._update_gradient_text()

    def _update_gradient_text(self):
        # 1. Determine font and size
        # Note: PIL needs a path to a .ttf file. 
        # For simplicity, we'll use a default, but in production, provide a font path.
        try:
            font_size = self.font_tuple[1]
            pil_font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            pil_font = ImageFont.load_default(font_size=font_size)

        # 2. Measure text size
        # We create a dummy image to get the text bounding box
        dummy_img = Image.new("RGBA", (1, 1))
        draw = ImageDraw.Draw(dummy_img)
        bbox = draw.textbbox((0, 0), self.gradient_text, font=pil_font, font_size=font_size)
        w, h = bbox[2], bbox[3] # Add small padding
        print(w, h)

        # 3. Create the Gradient Surface
        gradient = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(gradient)
        
        # 4. Create the text mask (White text on transparent)
        mask = Image.new("L", (w, h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.text((0, 0), self.gradient_text, font=pil_font, fill=255, font_size=font_size)

        # 5. Fill the gradient colors
        for y in range(h):
            # Interpolate between color1 and color2
            r = int(int(self.color1[1:3], 16) + (int(self.color2[1:3], 16) - int(self.color1[1:3], 16)) * (y / h))
            g = int(int(self.color1[3:5], 16) + (int(self.color2[3:5], 16) - int(self.color1[3:5], 16)) * (y / h))
            b = int(int(self.color1[5:7], 16) + (int(self.color2[5:7], 16) - int(self.color1[5:7], 16)) * (y / h))
            draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

        # 6. Apply the mask
        final_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        final_img.paste(gradient, (0, 0), mask=mask)

        # 7. Convert to CTkImage and update label
        self.ctk_img = ctk.CTkImage(light_image=final_img, dark_image=final_img, size=(w, h))
        self.configure(image=self.ctk_img)