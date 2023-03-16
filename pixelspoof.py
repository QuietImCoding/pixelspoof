from PIL import Image
import sys

if len(sys.argv) > 4:
    image1 = sys.argv[1]
    image2 = sys.argv[2]
    diff_coef = float(sys.argv[3])
    iters = int(sys.argv[4])
else:
    exit("pls provide 4 args <img1> <img2> <difference coefficient> <iterations>")

print(f"image1: {image1}, image2: {image2}")

with Image.open(image1) as im1, Image.open(image2) as im2:
    xsize = min(im1.width, im2.width)
    ysize = min(im1.height, im2.height)
    im1 = im1.resize((xsize, ysize))
    im2 = im2.resize((xsize, ysize))
    
    pix1 = im1.load()
    pix2 = im2.load()
    
    h, w = im1.size
    # For fixed pixel-size, set to a number, otherwise a proportion of h is better
    # skip = 80 <- rip the old pixellation method :'( 
    skip = h // 6
    
    for y in range(0, im1.height, skip):
        for x in range(0, im1.width, skip):
            for q in range(iters):
                frac = skip - (skip // (q + 1))
                for z in range(skip):
                    cx = min((x+z), w-1)
                    cy = min((y+frac+z), h-1)
                    pdiff = (pix1[cx, cy][0] - pix2[x, y][0],
                             pix1[cx, cy][1] - pix2[x, y][1],
                             pix1[cx, cy][2] - pix2[x, y][2])
                    maxdist = (pix1[cx, cy][0] - int(diff_coef * pdiff[0]),
                               pix1[cx, cy][1] - int(diff_coef * pdiff[1]),
                               pix1[cx, cy][2] - int(diff_coef * pdiff[2]))
                    pix1[cx, cy] = maxdist
                for z in range(1, skip):
                    cx = min((x+frac-z), w-1)
                    cy = min((y+z), h-1)
                    pdiff = (pix1[cx, cy][0] - pix2[x, y][0],
                             pix1[cx, cy][1] - pix2[x, y][1],
                             pix1[cx, cy][2] - pix2[x, y][2])
                    maxdist = (pix1[cx, cy][0] - int(diff_coef * pdiff[0]),
                               pix1[cx, cy][1] - int(diff_coef * pdiff[1]),
                               pix1[cx, cy][2] - int(diff_coef * pdiff[2]))
                    pix1[cx, cy] = maxdist

    im1.save('output.png')
#    print(pix1)

    
