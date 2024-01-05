# Face Detection

[Face](https://www.youtube.com/watch?v=sz25xxF_AVE)

## MediaPipe

## OpenCV, dlib and face_recognition
[Face recognition with OpenCV, Python, and deep learning](https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/)

[Install Cuda](https://medium.com/@johnnyliao/%E5%9C%A8nvidia-mx150%E7%9A%84win10%E5%AE%89%E8%A3%9Dcuda-toolkit-cudnn-python-anaconda-and-tensorflow-91d4c447b60e)

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

[key](https://github.com/davisking/dlib/issues/2166)
### Install Cmake

    pip install cmake

### Install dlib with GPU support

    git clone https://github.com/davisking/dlib.git
    cd dlib
    mkdie build
    cd build
    cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1
    cmake --build .
    cd ..
    python setup.py install

If you can't install successful using above command, try this:

    pip install dlib==(version)

### Install face_recognition

    pip install face-recognition

### Install Firebase

    pip install firebase-admin
    pip install google-cloud-storage
