# ImageWatermark

GUI application that helps you create a Text watermark or a Logo on a selected image. 

### Written in python 3.10 

## Installation on Windows:
* `git clone https://github.com/snehangsude/ImageWatermark.git`
* `cd ImageWatermark`
* `pip install -r requirements.txt`
* `python main.py`

## How to use

* Run the application using the Installation section (only on Windows, currently)

#### Image Viewer

* Open any image and view it on the GUI app before making any watermark. Use the **View Image** button, which opens up a dialogue box to select and view that in the GUI.
**NOTE: All images are shown in resized and shown as (400 x 250)**

#### Create Text watermark on an Image

* Type the watermark **Text** in the Text Box. *(Default Text: Enter watermark text here...)*
* Select the **Font Style** that you'd like your text to be in. *(Default Font: Arial)*
* Select the **Font Size** of appropriately. *(Default Size: 8)*
* Select **Rotation** if you'd require any. *(Default Rotation: -360, which is no rotation - the text is displayed as it is)*
* Select the **Opacity** of the text. *(Default Opacity: 0, which means transparent. Change it to **255** for it to be completely opaque, check [Opacity](##-Opacity))*
* Select the **Placement** of the text. *(Default Placement: Bottom right (br), check [Placements](#-Placements) for more information)*
* Select the **Color** of the text. *(Default color: 212121 (black), check [Colors](#-Colors) for more information)*
* Select the **Margin X-axis** to dynamically move the text along the x-axis based on Placement. *(Default Margin X-axis: 210)
* Select the **Margin Y-axis** to dynamically move the text along the y-axis based on Placement. *(Default Margin Y-axis: 150)
* Once all of the above has been set, click on **Add Text** to open a window to select an Image on which the watermark would be added. Opens on the current directory.
* A temporary image would be displayed above with the text watermark. 

You can manually change all the above attributes now and click on **Add Text**, select the image to adjust any of the attributes. Once you are happy, hit the **Save Image** button which will open up a dialogue box to select the location for saving the image.  

#### Create Logo watermark on an Image

* Select the **Opacity** of the text. *(Default Opacity: 0, which means opaque. Changing it to **255** would make the logo white)*
* Select the **Placement** of the text. *(Default Placement: Bottom right (br), check Placements for more information)*
* Select the **Margin X-axis** to dynamically move the text along the x-axis based on Placement. *(Default Margin X-axis: 210)
* Select the **Margin Y-axis** to dynamically move the text along the y-axis based on Placement. *(Default Margin Y-axis: 150)
* Once all of the above has been set, click on **Add Logo** to open a window which allows you to **Select the Logo** (Displayed on the Dialogue box) first.
* Once the logo has been selected, it would open the next dialogue box to **Select the Image** (Displayed on the Dialogue box) next.
* A temporary image would be displayed above with the logo watermark.

You can manually change all the above attributes now, and click on **Add Logo**, selecting both the logo & the image to adjust any of the attributes. Once you are happy, hit the **Save Image** button which will open up a dialogue box to select the location for saving the image.  

## Placements

* **Bottom Right (`br`)** : Takes the width of the image and subtracts the Margin X-axis & takes the height of the image and subtracts the Margin Y-axis for the x,y co-ordinates respectively.
* **Bottom Left (`bl`)** : Takes 150 as a fixed value & takes the height of the image and subtracts the Margin Y-axis for the x,y co-ordinates respectively.
* **Top Left (`tl`)** : Takes 150 and 50 as a fixed value for x,y co-ordinates respectively.
* **Top Right (`tr`)** : Takes the width of the image and subtracts the Margin X-axis & takes 50 as a fixed value for the x,y co-ordinates respectively.
* **Center (`center`)** : Takes the width and height divides it by 2 (rounds off to the nearest integer) for the x,y co-ordinates respectively.
* **All (`all`)** : Places in all of the above positions simultaneously.
* **Special method -  Diagonal (`diag`)** : Size, Rotation, Margin X-axis & Margin Y-axis are ignored. This measures the hypotenuse based on the image width and height. Sets the size as an rounded up value of (length of hypotenuse/ (length of text/2.3). Places the text diagonally on the image. Recommended if the ratio of width : height ~ 1 or the image is a square.

## Colors

* Only Hex Code values should be entered in the color box. Else it would prompt an error on the GUI.
* Recommended to not use `#`, though it would still work fine.
* Lenght of the Hex code should be 6 withou `#` or 7 with `#`. Anything else would be ignored or an error message would be prompted.

## Opacity

* **Text watermark** -  `0` is transparent. `255` is opaque.
* **Logo watermark** - `255` is white/transparent. `0` is opaque.
* Opacity is the Alpha(A) parament in the RGBA spectrum. 

## Tips and Error Handling 
* Recommended to dynamically change the Margin X-axis and the Margin Y-axis to adjust the text or the logo watermark, may take some tries to be appropriate.
* Margin X-axis or Margin Y-axis can't be empty but can be `0`. It would show an error on the interface.
* Once the application is closed all temporary files would be deleted. 

## Internal Working

#### Libraries Used
* Tkinter
* Pillow
* OS
* Pandas
* BS4

- Font Data is collected from [Microsoft Windows 10 Fonts](https://docs.microsoft.com/en-us/typography/fonts/windows_10_font_list), using Pandas and BS4.
- The GUI after application of adding a text or logo watermark creates a `tmp.png` file in the root directory which is used as an PIL image object which returns is used as an tkinter Image object to be displayed.
- Saving or closing the application will delete the `tmp.png` file.

### Improvements Planned
- Currently two lines of text watermark has a bug and doesn't display. Fix to be applied. 
- Rotation property to be included in the Logo watermark.
- New attribute to be added which controls the Starting location of x,y co-ordinates for `bl`, `tl`, `tr`.
- `Diag` and `center` placements to be refined.
