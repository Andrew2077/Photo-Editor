import os 
os.chdir(os.getcwd())

import streamlit as st
from utils import *
from utils.filters import *
from utils.style import *

st.set_page_config(
    page_title="Image Editor",
    page_icon=Image.open("imgs/logo.ico"),
    layout="wide",
    initial_sidebar_state="auto",
)

image = Image.open("imgs/logo.png")
col1, col2 = st.columns([0.8, 0.2])

with col1:
    st.markdown(font, unsafe_allow_html=True)
    st.markdown(main_header, unsafe_allow_html=True)

with col2:
    st.image(
        image,
        width=150,
    )

apply_denoise = False
st.sidebar.markdown(sidebar_header, unsafe_allow_html=True)
st.info('larger images will take longer to process specially if you apply :red[denoise]')
uploaded_file = st.file_uploader(
    ":blue[Upload an Image] ", type=["jpg", "png", "jpeg"], label_visibility="visible"
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    col1, col2 = st.columns([0.5, 0.5], gap='small')

    with col1:
        st.markdown(f'<p{block_header}">Original Image</p>', unsafe_allow_html=True)
        st.image(image, use_column_width=True)

    with col2:
        st.markdown(f'<p{block_header}">Edited Image</p>', unsafe_allow_html=True)
        filter = st.sidebar.radio(
            "select a filter", 
            (
                "None",
                "gray Scale",
                "Black & White",
                "Blur Effect",
                # "Edge", TODO: add edge filter
                # "Resize" TODO: add resing feature
                "Pencil Sketch",
                'denoise',
                "Custom Filter",
                
            ),
        )

        if filter == "gray Scale":
            edited_image = gray_scale_filer(image)

        elif filter == "Black & White":
            intensity = st.sidebar.slider("Intensity", 1, 255, 127, step=1)
            edited_image = black_white_filter(image, intensity)

        elif filter == "Pencil Sketch":
            intensity = st.sidebar.slider("Intensity", 1, 255, 125, step=2)
            edited_image = sktech_filter(image, intensity)

        elif filter == "Blur Effect":
            # gray_scale_image = gray_scale_filer(image)
            image = np.array(image.convert("RGB"))
            slider = st.sidebar.slider("Intensity", 1, 99, 33, step=2)
            converted_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            edited_image = blur_filter(converted_image, slider)
            #st.image(edited_image, channels="RGB")

        elif filter == "Custom Filter":
            color = st.sidebar.slider(
                "Adjust Color", 0.0, 2.0, 1.0, step=0.1, key=1
            )
            contrast = st.sidebar.slider(
                "Adjust Contrast", 0.1, 3.0, 1.0, step=0.1, key=2
            )
            brightness = st.sidebar.slider(
                "Adjust Brightness", 0.1, 2.0, 1.0, step=0.1, key=3
            )
            sharpness = st.sidebar.slider(
                "Adjust Sharpness", 0.0, 10.0, 1.0, step=0.1, key=4
            )
            effect_1 = st.sidebar.radio('Gary modes', ('None', 'Gray Scale', 'Black & White', 'Sketch'), horizontal=True)
            apply_denoise = st.sidebar.checkbox('Apply Denoise')

            # use PIL.ImageEnhance._Enhance
            image = ImageEnhance.Brightness(image).enhance(color)
            image = ImageEnhance.Contrast(image).enhance(contrast)
            image = ImageEnhance.Brightness(image).enhance(brightness)
            image = ImageEnhance.Sharpness(image).enhance(sharpness)
            if effect_1 == 'Gray Scale':
                edited_image = gray_scale_filer(image)
            
            elif effect_1 == 'Black & White':
                threshold = st.sidebar.slider("Intensity", 1, 255, 127, step=1)
                image = black_white_filter(image, threshold)
                edited_image = image
            #st.image(image, width='max')
            
            elif effect_1 == 'Sketch':
                threshold = st.sidebar.slider("Intensity", 1, 255, 125, step=2)
                edited_image = sktech_filter(image, threshold)
                # st.write(type(edited_image))
                
            else:
                edited_image = image
                
            if apply_denoise:
                h_filter_stregth = st.sidebar.slider("Iuminance Filter Strength", 0, 25, 0, step=1)
                h_color_filter_stregth = st.sidebar.slider("Color Filter Strength", 0, 25, 0, step=1)
                # try :
                    # img = np.array(edited_image)
                img = edited_image

                try :
                    print(img.mode)

                except:
                    print(type(img))
                    img = Image.fromarray(img)
                #     img = edited_image
                # st.write(type(img), img.mode)
                if img.mode == 'RGB':
                    edited_image = cv2.fastNlMeansDenoisingColored(np.array(edited_image),None,h_filter_stregth,h_color_filter_stregth,7,21) 
                elif img.mode == 'L':
                    edited_image = cv2.fastNlMeansDenoising(edited_image,None,h_filter_stregth,7,21)
                
                else:
                    st.error(f'image mode {img.mode} is not supported')
                st.image(edited_image, use_column_width=True)
                
                
        elif filter == 'denoise' :
            h_filter_stregth = st.sidebar.slider("Iuminance Filter Strength", 0, 25, 0, step=1)
            h_color_filter_stregth = st.sidebar.slider("Color Filter Strength", 0, 25, 0, step=1)
            edited_image = cv2.fastNlMeansDenoisingColored(np.array(image),None,h_filter_stregth,h_color_filter_stregth,7,21) 
            
        else:
            # TODO: change the header with streamlit state
            # with col2:
            #     st.markdown(f'<p{block_header}">Edited Image</p>',unsafe_allow_html=True)
            edited_image = image
            
        if apply_denoise == False:
            st.image(edited_image, use_column_width=True)
    st.write(f'the Photo Resolution is', np.array(image).shape, )
    # st.write(type(edited_image))
    # st.write(apply_denoise)
    if type(edited_image) == np.ndarray:
        edited_image = Image.fromarray(edited_image)
    edited_image.save('enhanced_image.jpg')
    with open("enhanced_image.jpg", "rb") as f:
        btn = st.sidebar.download_button(
            label="Download",
            data=f,
            file_name="enhanced_image.jpg",
            mime="image/jpg",
        )

with st.sidebar:
    st.write('Upload image first')
# with st.sidebar.expander("About"):
#     st.write("""
# this app was designed by :red[[Andrew2077](https://github.com/Andrew2077)]
# you can find Source Code [here](https://github.com/Andrew2077/Photo-editing-app-streamlit)""")