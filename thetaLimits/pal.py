from ROOT import *
from array import array

def set_palette(name=None, ncontours=999):
    """Set a color palette from a given RGB list
    stops, red, green and blue should all be lists of the same length
    see set_decent_colors for an example"""

    if name == "gray" or name == "grayscale":
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [1.00, 0.84, 0.61, 0.34, 0.00]
        green = [1.00, 0.84, 0.61, 0.34, 0.00]
        blue  = [1.00, 0.84, 0.61, 0.34, 0.00]
    elif name == "kBird":
        TColor.InitializeColors()
        red = array('d',[ 0.2082, 0.0592, 0.0780, 0.0232, 0.1802, 0.5301, 0.8186, 0.9956, 0.9764])
        green = array('d',[ 0.1664, 0.3599, 0.5041, 0.6419, 0.7178, 0.7492, 0.7328, 0.7862, 0.9832])
        blue = array('d',[ 0.5293, 0.8684, 0.8385, 0.7914, 0.6425, 0.4662, 0.3499, 0.1968, 0.0539])
        stops = array('d',[ 0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000])
        alpha=1
        TColor.CreateGradientColorTable(9, stops, red, green, blue, 255, alpha);
        print "kBird is the word"
    else:
        # default palette, looks cool
        stops = [0.00, 0.34, 0.61]
        red   = [0.00, 0.00, 0.87]
        green = [0.00, 0.81, 1.00]
        blue  = [0.51, 1.00, 0.12]

    s = array('d', stops)
    r = array('d', red)
    g = array('d', green)
    b = array('d', blue)

    #npoints = len(s)
    #TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
    #gStyle.SetNumberContours(ncontours)

if __name__=='__main__':
    h=TH2F("h","",9,1,10,9,1,10)
    f=TF2("f","1/(x^2+y^2)",0,10,0,10)
    h.FillRandom("f",10000)
    gStyle.SetOptStat(0)
    set_palette(name="kBird")
    #gStyle.SetPalette(57)
    c=TCanvas()
    c.SetLogz()
    h.Draw("COLZ")
    c.Modified()
    c.Update()

