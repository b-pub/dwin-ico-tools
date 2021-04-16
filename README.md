# dwin-ico-tools
Tools to process DWIN LCD display .ICO files.

## What

DWIN LCD displays use a number of image and container files to
skin the UI elements on the display. These displays are used on
Creality's Ender 3 v2 and other 3d printers, and the
configuration files to support these displays is included in the
[Marlin firmware](https://github.com/MarlinFirmware/Marlin).

One file they use is "9.ICO", which is a structured file
containing the icons. This project contains two tools to help
developers manipulate these ICO files.

## The Tools

dwin-ico-tools consists of two tools: splitIco and makeIco.

### splitIco.py

"splitIco.py" reads an ICO file, and extracts the component icon
images, saving each into a new directory. Each icon is named by
its index in the ICO, and is named using symbol names from the
Marlin dwin.h header file for this display.

### makeIco.py

"makeIco.py" is the inverse: it reads the images from a
directory, and combines them to create a valid .ICO file.

## Dependencies

The dwin-ico-tools are written in Python 3, and use the
[Pillow image library](https://pillow.readthedocs.io/en/latest/index.html).

## Versioning

This is a new project and I don't forsee having a strict
versioning in the tools.

That said, the tools correspond the the DWIN image and
header files included in Marlin 2.0.7, as of 1-oct-2020.

## Credits

These tools were created by:
* Brent Burton [[@b-pub](https://github.com/b-pub)]

## License

dwin-ico-tools is published under the GPL 3 license. See
the LICENSE file for details.

# Usage

The dwin-ico-tools are simple command-line programs that
you run from a terminal. The files here do not need installation,
but there is one dependency that must be in place before they
work.

## Dependencies

The following dependencies can be installed with pip:

* python3 -m pip install pillow


## Overview

The dwin-ico-tools process the 9.ICO firmware file. The easiest
way to do this is to create a directory to isolate the changes,
and make a copy of 9.ICO there:

	$ mkdir hackicons
	$ cp 9.ICO hackicons
	$ cd hackicons

We'll use this setup for the following explanations.

## `splitIco.py` - Split the ICO archive

To edit the individual icons, the archive must be split first.
Do this with `splitIco.py`:

	$ python3 splitIco.py 9.ICO icons

The "icons" parameter is the name of a directory to create (if
missing) and store the individual JPEG icon files. While
running, this program will output each file it writes with
related information such as resolution, output file name, and
some perhaps uninteresting info about the offset and size of the
original 9.ICO content. It looks something like:

    Splitting 9.ICO into dir icons
    Splitting Entry Data...
    00: offset: 0x001000 len: 0x10a2 width: 130 height: 17
    Wrote 4258 bytes to icons/000-ICON_LOGO.jpg
    01: offset: 0x0020a2 len: 0x0eac width: 110 height: 100
    Wrote 3756 bytes to icons/001-ICON_Print_0.jpg
    02: offset: 0x002f4e len: 0x0eaa width: 110 height: 100
    Wrote 3754 bytes to icons/002-ICON_Print_1.jpg
    ...
    91: offset: 0x0345fc len: 0x0d89 width: 110 height: 100
    Wrote 3465 bytes to icons/091-ICON_Info_1.jpg

Once you have the individual JPEG files saved, you can edit
them using whatever tools or programs you want. See section 'Caveats'
below.

## `makeIco.py` - Combine JPEGs into ICO archive

After editing, the 9.ICO archive must be regenerated. This is done
by `makeIco.py`:

    $ python3 makeIco.py icons test.ICO
    Making .ico file 'test.ICO' from contents of 'icons'
    Scanning icon directory icons
    ...Scanned 91 icon files
    Scanning done. 91 icons included.
    $ ls -l *.ICO
    -rw-r--r--  1 bpub  staff  217989 Apr 15 17:35 9.ICO
    -rw-r--r--  1 bpub  staff  217989 Apr 15 18:15 test.ICO
    $
The generated output, test.ICO, is the same size in this example
and should not be a problem.

## Caveats

Since details of the DWIN internal firmware are not known (by me, at
the time of writing these scripts) the limits of file sizes are unknown.
In addition to 9.ICO, the firmware uses files 0_start.jpg, 1_English.jpg,
and 2_Chinese.jpg, which provide a startup image, and raster messages in two languages for labeling fields. It is unknown what file size limits
there are for either these files, or the individual JPEGs in 9.ICO, or the
total size of 9.ICO itself.

For example, I changed 0_start.jpg to a colorful background image, resulting
in a JPEG of 50KB (original was 28KB or 30KB). The display would not operate
properly when my 0_start.jpg file was in place. Restoring the original file
worked and the display was normal. So this hints the limit is between 30 and 50KB (maybe 32KB?) for that file.

Fortunately, it seems that problems caused by bad image files are
easily correctable by restoring the original images. However, there may be
some situation where the display unit is bricked by incompatible files.
Keep that in mind when hacking your devices' firmware, it's always a risk.

## Bonus script

The reward for reading this far is a script to programmatically swap
the blue and red channels of JPEG files. This is the script I used to
create yellow icons from the original cyan icons. Cyan (#00ffff) goes to
yellow (#ffff00) by swapping these channels.

    $ python3 swapBlueAndRed.py icons/*.jpg
    processed  000-ICON_LOGO.jpg
    processed  001-ICON_Print_0.jpg
    processed  002-ICON_Print_1.jpg
    ...
    processed  090-ICON_Info_0.jpg
    processed  091-ICON_Info_1.jpg

And then run `makeIco.py` to rebuild the ICO archive.
