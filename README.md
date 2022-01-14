# Concealing messages in audio files

## Table of contents
* [Idea](#idea)
* [Modules](#modules)
* [Setup](#setup)
* [Usage](#usage)

## Idea
The main idea of the project is to create a program which encrypts a message inside an audio file.

### How does it work?
When we transform a signal from the time domain to the frequency domain, we can sometimes see some patterns.
I wanted to exploit this unique feature of a human brain and cause a signal to look like a very well-known pattern to almost all people: latin alphabet.

For example, when we look at the chirp signal, we will notice that this rising in frequency signal, when
transformed to the spectrogram, looks like a diagonal line. If we transform simple sine wave, we get straight horizontal line and when we transform noise in range of some frequencies in a very short time then we get a vertical line.

Using only those shapes: vertical line, horizontal line and ascending or descending line we can create letters.
We just need to create signals of certain parameters and combine them to get a whole text.

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
