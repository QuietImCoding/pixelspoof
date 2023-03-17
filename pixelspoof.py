from PIL import Image
import click
import sys

# if len(sys.argv) > 4:
#     image1 = sys.argv[1]
#     image2 = sys.argv[2]
#     diff_coef = float(sys.argv[3])
#     iters = int(sys.argv[4])
# else:
#     exit("pls provide 4 args <img1> <img2> <difference coefficient> <iterations>")
# 
# print(f"image1: {image1}, image2: {image2}")

def pix_subtract(p1, p2):
    return (p1[0] - p2[0],
            p1[1] - p2[1],
            p1[2] - p2[2])
    
def spoof_pixels_cross(at_coord, img_dim, pix1, pix2, iters, skip, diff_coef = 1):
    x, y = at_coord
    w, h = img_dim
    for q in range(iters):
        frac = skip - (skip // (q + 1))
        for z in range(skip):
            cx = min((x+z), w-1)
            cy = min((y+frac+z), h-1)
            pdiff = pix_subtract(pix1[cx, cy], pix2[x, y])
            maxdist = pix_subtract(pix1[cx, cy], tuple(int(a * diff_coef) for a in pdiff))
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

def spoof_pixels_block(at_coord, img_dim, pix1, pix2, blocks=1, diff_coef = 1.2):
    x, y = at_coord
    w, h = img_dim
    for cx in range(x, min(x + (blocks * 8), w)):
        for cy in range(y, min(y+(blocks * 8), h)):
            pdiff = pix_subtract(pix1[cx, cy], pix2[x, y])
            maxdist = pix_subtract(pix1[cx, cy], tuple(int(a * diff_coef) for a in pdiff))
            pix1[cx, cy] = maxdist

@click.command()
@click.argument('image1')
@click.argument('image2')
@click.option("--mode", type=click.Choice(['BLOCK', 'CROSS']), default="BLOCK")
@click.option("--diff_coef", '-d', type=float, default=1.0)
@click.option("--block_size", '-b', type=int, default=1)
@click.option("--skip_res", type=int, default=6)
def pixelspoof(image1, image2, mode, diff_coef, skip_res, block_size):
    im1 = Image.open(image1)
    im2 = Image.open(image2)

    xsize = min(im1.width, im2.width)
    ysize = min(im1.height, im2.height)
    im1 = im1.resize((xsize, ysize))
    im2 = im2.resize((xsize, ysize))
    
    pix1 = im1.load()
    pix2 = im2.load()
    
    h, w = im1.size
    # For fixed pixel-size, set to a number, otherwise a proportion of h is better
    # skip = 80 <- rip the old pixellation method :'( 
    skip = h // skip_res
    
    for y in range(0, im1.height, skip):
        for x in range(0, im1.width, skip):
            if mode == "CROSS":
                spoof_pixels_cross((x, y), (w, h), pix1, pix2, iters, skip, diff_coef = 1)
            elif mode == "BLOCK": 
                spoof_pixels_block((x,y), (w, h), pix1, pix2, block_size, diff_coef)
            else:
                print("Incorrect mode set")
    im1.save('output.png')

    im1.close()
    im2.close()


pixelspoof()    
