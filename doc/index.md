Detecting 'fake' FLAC files
===========================

January 5th, 2013

Maurits van der Schee

0 Abstract
----------

Sometimes people want to pretend they have high quality audio files and create lossless audio files from decoded MP3 audio files. FakeFLAC is a tool to detect the low-pass filter that is applied by MP3 encoders. MP3 encoders use a lowpass filter to filter out unaudible sound and reduce the information and thus the file size.

1 Background
------------

There are lossless codecs (encoder-decoders), like FLAC, that allow encoding and decoding of audio samples without loss of information. There are also "lossy" codecs like MP3. In lossy codecs information is lost in the process of encoding. Lossy coding formats modify and compress the audio data in ways that exploit features of human hearing to make the changes difficult to discern. It is a common fact that people can not hear frequencies above 20 Khz \[6\]. The Nyquist theory says you need to have a double sampling frequency in a discrete signal processing system (e.g. 40Khz) [\[2\]](http://en.wikipedia.org/wiki/Red_Book_%28CD_standard%29). When people get older their hearing of high frequencies gets even worse. You can test you own hearing using the video below. MP3 encoders use a lowpass filter to include "enough of the human hearing's threshold for the highest frequencies" [\[1\]](http://jthz.com/mp3/). This way MP3 codecs can achieve high audio quality with small file sizes (low bit rates). There are other tools like Spectro [\[4\]](http://spectro.enpts.com/) and Informer [\[5\]](http://www.neillcorlett.com/informer/) that claim to do the same.

2 How it works
--------------

The FLAC audio file is decoded into 16 bit samples, with 44100 samples per second (PCM16), also known as WAV file, using libsndfile [\[3\]](https://ffmpeg.org/). From these samples only the first 30 seconds are analyzed. For every second the frequency spectrum of the samples is computed by applying a Hanning Window and doing a Fast Fourier Transform. These spectrums are added, so that eventually you end up with 30 stacked spectrums. These is divided by 30 to get the average spectrum. Then the spectrum is normalized using log10. After that we applied a rolling average on the spectrum with a window size of 1/100th of the frequency, being 44100/100=441 samples. This produces a clean line as can be seen in the following images:

![](fake.png)
                                                                                                                                            
**Picture 1**: FLAC file with missing high frequencies

![](real.png)
                                                                                                                                            
**Picture 2**: FLAC file with intact high frequencies

### 2.1 Finding the cutoff

In Picture 1 you can see that there is an unnatural cutoff in the frequency spectrum around 33Khz. This cutoff is the thing we need to find. We sweep the spectrum from 44100th back to the 1st frequency, where the variable frequency is f. As soon as the magnitude at f-220 is more than 1.25 higher than the magnitude at f and the magnitude at f is no bigger than 1.1x the magnitude at 44100 we have found the cutoff point. The cutoff point is multiplied by 100 and divided by the frequency to get to the percentage of the spectrum not cut off. This is the score that is printed, example:

    maurits@pc:~/fakeflac$ ./fakeflac fake.flac 
    73
    maurits@pc:~/fakeflac$ ./fakeflac real.flac 
    100

3 Download
----------

Get the files from github: [https://github.com/mevdschee/fakeflac](https://github.com/mevdschee/fakeflac)

The package contains a Python program (fakeflac.py) and a bash script (fakeflac). The dependecies can be installed on a Debian system using the following command:

sudo apt-get install ffmpeg python-scipy
sudo apt-get install python-matplotlib

4 Bibliography
--------------

1.  [JTHZ | Creating quality audio-files using Windows, L.A.M.E., Ogg Vorbis  
    http://jthz.com/mp3/](http://jthz.com/mp3/)
2.  [Wikipedia | Red Book (CD standard)  
    http://en.wikipedia.org/wiki/Red\_Book\_%28CD\_standard%29](http://en.wikipedia.org/wiki/Red_Book_%28CD_standard%29)
3.  [FFmpeg: A complete, cross-platform solution to record, convert and stream audio and video.  
    https://ffmpeg.org/](https://ffmpeg.org/)
4.  [Spectro: a freeware audio file analyzer for windows  
    http://spectro.enpts.com/](http://spectro.enpts.com/)
5.  [Informer | Detect lossy audio!  
    http://www.neillcorlett.com/informer/](http://www.neillcorlett.com/informer/)
6.  [Wikipedia | Hearing range  
    http://en.wikipedia.org/wiki/Hearing\_range](http://en.wikipedia.org/wiki/Hearing_range)
