#!/usr/bin/env python3
#
# Swap the blue and red channels on a bunch of jpg image files.
#
#  Copyright (c) 2020 Brent Burton
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#----------------------------------------------------------------

import os
import os.path
import argparse
from PIL import Image

version = '1.0.0'

#----------------
if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Swap B and R channels of JPEG files')
        parser.add_argument('filenames', type=str, nargs='+',
                            help='names of images files to process')
        args = parser.parse_args()

        for name in args.filenames:
            if not os.path.exists(name):
                print('%s is an invalid name, skipping' % (name))
                continue
            img = Image.open(name)
            r,g,b = img.split()
            img = Image.merge('RGB', (b,g,r)) # swap the channels to create a new image
            img.save(name, quality=95)
            print('processed ', name)
            

    except Exception as e:
        print('Error: ', e)

