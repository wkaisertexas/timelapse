# TimeLapse - Record your camera or screen

<p align="center">
    <img src="https://img.shields.io/github/last-commit/wkaisertexas/timelapse">
</p>

Uses FFMPEG to take continual screenshots of your screen to make great time lapses. Originally intended for programming / creative projects to show what is required.

## Making the project

![TimeLapse of Me Creating This Project](https://img.youtube.com/vi/hjKidbt-Ad4/0.jpg)

#### [Click here to Watch](https://www.youtube.com/watch?v=hjKidbt-Ad4)

## Installation

### Install the required dependencies
```sh
pip install -r requirements.txt
```

### Install the application
```sh
python setup.py py2app
```

### Run the application bundle
```sh
./dist/Timelapse.app
```

## Tips

As a general rule, the greater the motion in your image, the slower your video should be. If you are doing a highly dynamic task such as playing a video game, you would want to be at maximum 25x faster whereas if you are doing a simple task such as editing text, you could get away with 100x faster. 

## Project TODOs

1. [ ] Converting the project to Swift may be a worthwhile endevor, I would just have to work with some of the more baremetal video conversion stuff -> this would allow me to skip the whole troubleshooting recipes for py2app stuff. 
    - I think I am going to end up waiting until I figure out more of the features people want before doing this
2. [ ] Set the GitHub thumbnail for the project

## References

> For my personal reference

1. [Menu Bar Applications in Python](https://camillovisini.com/article/create-macos-menu-bar-app-pomodoro/)
2. [FFMpeg Video Writer](https://stackoverflow.com/questions/34167691/pipe-opencv-images-to-ffmpeg-using-python) -> I did try this a little earlier and it was throwing errors intially, will try again with the new h264_nvec codec
3. [Offical Rumps Documentation](https://github.com/jaredks/rumps) -> the syntax has changed a bit to make it more pythonic recently
4. Perhaps the better way to do this would be to use something like cjkcodecs which has better support with py2app and is likely much smaller
