#!/usr/bin/python

from PIL import Image
import math
import argparse
import subprocess

#=== define ===
COLOR=['0;40','5;40','0;41','5;41','0;42','5;42','0;43','5;43','0;44','5;44','0;45','5;45','0;46','5;46','0;47','5;47']
COLOR_RGB=[[0,0,0],[85,85,85],[187,0,0],[255,85,85],[0,187,0],[85,255,85],[187,187,0],[255,255,85],[0,0,187],[85,85,255],[187,0,187],[255,85,255],[0,187,187],[85,255,255],[187,187,187],[255,255,255]]
#==============

#=== argparse ===
parser = argparse.ArgumentParser()
parser.add_argument('img',help='image file')
parser.add_argument('-s','--save',help='save file',default="")
parser.add_argument('-l','--line',help='output line',type=int,default=32)
args = parser.parse_args()
#================

SYMBOL='  '
LINE=args.line

img=Image.open(args.img)

width=img.size[0]
height=img.size[1]

if height>LINE:
	img.thumbnail((width*LINE/height,LINE))
img=img.convert('RGB')
width=img.size[0]
height=img.size[1]

code='echo -e "'

for h in xrange(height):
	prev_i=-1
	for w in xrange(width):
		#print w,h
		color_i=0
		r,g,b=img.getpixel((w,h))
		
		#choice a color
		min_d=float("inf")
		for i,RGB in enumerate(COLOR_RGB):
			d=math.sqrt((RGB[0]-r)**2 + (RGB[1]-g)**2 + (RGB[2]-b)**2)
			if math.sqrt((RGB[0]-r)**2 + (RGB[1]-g)**2 + (RGB[2]-b)**2)<min_d:
				min_d=d
				color_i=i
		
		if prev_i!=color_i:
			code += '\\e['+COLOR[color_i]+'m'+SYMBOL
		else:
			code += SYMBOL
		
		prev_i=color_i
	code += '\\e[m\\n'
code = code[:-2]+'"'

if args.save!="":
	f=file(args.save,'w')
	f.write('#!/usr/bin/zsh\n')
	f.write(code)
else:
	subprocess.call(code,shell=True)

