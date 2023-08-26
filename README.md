# Hiding text messages in audio files

## Table of contents
* [Idea](#idea)
* [Modules](#modules)
* [Setup](#setup)
* [Usage](#usage)

## Idea
The main idea behind this project is to add on top of the input audio file a layer of signals, which when displayed on a spectrogram, reveal a hidden message.

### How does it work?
Different types of signals, when visualized using a spectrogram, show different shapes and patterns. A regular sine wave looks like a horizontal line, uniformally distributed noise resembles a vertical line, whereas a chirp signal draws a diagonal line. By combining different signals of different lengths and frequencies, we can construct shapes, such as letters. They can be used to create a text that we can hide among other sounds of the input audio file.

## Modules
This project would not work without:
* librosa: version 0.8.1
* matplotlib: version 3.4.3
* numpy: version 1.21.2
* PyYAML: version 6.0
* scipy: version 1.7.1
* SoundFile: version 0.10.3.post1

## Setup

To install this program:

1. You need to have [Python](https://www.python.org/downloads/) installed (program was written on v3.9).
2. Clone this repository.
3. Install all required dependencies
   
   ``pip install -r requirements.txt``
4. *Download an audio file that you want to apply your text into (not required).

## Usage

To use this program you need to run this command in your console:

   ``python hide_in_audio.py [parameters]``
   
All parameters are optional. If you do not specify values, default values will be applied.

List of parameters:
* -i, --input : string indicating where the input file is located
* -t, --text : string containing the text to be encrypted
* -b, --start_time : value indicating the starting time of the text (in seconds)
* -f, --start_frq : value indicating the starting frequency of the text (in Hz)
* -w, --width : value indicating the width of the text (in seconds)
* -e, --height : value indicating height of the text (in Hz)
* -m, --max_time : value indicating the maximum time of the input file to be loaded
* -o, --output_sound : if used, the audio file after calculations will be plotted
* -d, --display : if used, the spectrogram of the audio file after calculations will be calculated and plotted
* -s, --save : string indicating where the output file should be saved
* --force : if used in the situation where save path is taken, it forces the program to overwrite this file
