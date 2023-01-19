# Python Script for automatic image & annotation generation for YOLO
fork from：[Ieetenkiさん](https://github.com/leetenki/YOLO_train_data_generator)

This script that automatically generates a large number of training images and annotations** based on images taken in green background and background images.

# How to use
## 1. Prepare an image of a green background.
### 1-1.Under the object folder, prepare a folder with a **label name** and put the images there.
Example of object image

<img src="https://user-images.githubusercontent.com/1459353/212318265-0682b154-36fa-4498-bfa2-dfab8cc4af89.jpg" width="320px" >

Image by <a href="https://pixabay.com/users/oslometx-7322944/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4223871">OsloMetX</a> from <a href="https://pixabay.com//?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4223871">Pixabay</a>

## 2. Prepare a background image.
### Put the image in the background folder.
Example of background image

<img src="https://user-images.githubusercontent.com/1459353/212320624-aa5e62b3-9c8d-4485-aab0-8a76c02e0741.jpg" width="320px" >

Image by <a href="https://pixabay.com/users/12019-12019/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1751455">David Mark</a> from <a href="https://pixabay.com//?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1751455">Pixabay</a>


## 3. Run the greenback background deletion script.
> python deleteGreenback.py

The color range to be deleted can be specified with the following options. (HSV color)
|  option  |  mean  | default |
| ---- | ---- | ---- |
|  --hl  |  h lower limit  | 40 |
|  --sl  |  s lower limit  | 30 |
| --vl | v lower limit | 30 |
|  --hh  |  h upper limit  | 90 |
|  --sh  |  s upper limit  | 255 |
| --vh | v upper limit | 255 |

### 3-1. A folder with the label name will be created under the TRIMMED folder and an image with the background removed will be generated.
Image with background removed from generated object image
<img src="https://user-images.githubusercontent.com/1459353/212319114-fca78b22-9b64-4ccf-85a7-a371a93c7e07.png" width="320px" >

## 4.Runs a script for image composition.
> python generate_sample.py --loop 10

"--loop 10" option can be used to specify the number of loops for image composition.

### 4-1. You can select where to save the file at startup.
In the sample, the output folder is selected. In the output folder, two folders, images and labels, are created. images contains composite images and labels contains labels in yolo format.

Example of synthesized image

<img src="https://user-images.githubusercontent.com/1459353/212319566-a3245505-3818-4389-bf2c-459fb1424323.jpg" width="320px" >

### 4-2. Example of output label
> 0 0.34921875 0.6295427901524033 0.2125 0.2977725674091442

## 5.(Optional) You can also run the annotation confirmation script.
> python annotationTest.py --sample 3

The option "--sample 3" can be used to specify how many confirmation images to generate.

### 5-1. Images will be output to the annotated folder.
Example of an image with annotation information displayed.

<img src="https://user-images.githubusercontent.com/1459353/212320133-d1a68f17-f371-4ee3-94f1-8cbab6723952.jpg" width="320px" >

## Development Information
## Folder structure

Annotation output is in YOLO format (hash). (2023/01/12 15:54 under verification
Output destination can be selected at startup.

<pre>
├─dev：Folder in development
│  ├─background
│  │  └─：Insert a background image to be combined.
│  ├─object
│  │  ├─(Folder 1 with label name): Insert images taken in green background.
│  │  └─(Folder 2 with label name): Can have multiple label folders.
│  ├─old：Historical data storage for development.
│  ├─output：Final output destination at sample time (output folder can be selected at script runtime.)
│  │  ├─images：Output destination of the combined image.
│  │  └─labels：Output destination for generated labels.
│  └─trimmed：Where to store cropped greenback images.
</pre>

## Environment setup
I have output file "delgb.yaml" for the anaconda prompt. You can import it and use it.

