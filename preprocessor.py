import os, subprocess, argparse

parser = argparse.ArgumentParser(description = "A preprocessor that creates webp's from png's and svg's from tikz standalone LaTeX files.")
parser.add_argument('-f', '--forceRegenerateFiles', nargs='*',
    help="Force regenerate given files. No arguments will force regenerate all files.",
    metavar="File names")
args = parser.parse_args()
rootdir = os.path.dirname(os.path.abspath(__file__)) + "/images"

def pngToWebp(pngPath, webpPath):
    subprocess.run(f"cwebp -q 100 -lossless -mt '{pngPath}' -o '{webpPath}'", shell=True)

def texToSvg(file, directory):
    dviName = file[:-3] + "dvi"
    subprocess.run(f"latex {file}", shell=True, cwd=directory)
    subprocess.run(f"dvisvgm --exact --font-format=woff {dviName}", shell=True, cwd=directory)

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if args.forceRegenerateFiles is None:
            forceRegenerate = False
        else:
            if len(args.forceRegenerateFiles) != 0:
                forceRegenerate = file in args.forceRegenerateFiles
            else:
                forceRegenerate = True

        path = os.path.join(subdir, file)
        if file.endswith("png"):
            webpPath = path[:-3] + "webp"
            if not os.path.exists(webpPath) or forceRegenerate:
                pngToWebp(path, webpPath)
        elif file.endswith("tex"):
            svgPath = path[:-3] + "svg"
            if not os.path.exists(svgPath) or forceRegenerate:
                texToSvg(file, subdir)
