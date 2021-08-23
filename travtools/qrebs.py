import numpy as np
import travtools.converters as cnv
import travtools.dice as dd

def qrebs(n, l = 0):
    """
    Generates QREBS (Quality, Reliablity, Ease of Use, Bulk/Burden, Safety), based on Traveller 5.1 generation rules.

    Takes argument n, as a seed number to ensure that the generation process is repeatable for a given value of n, and argument l, defaulting to 0, l if 1 reports QREBS in long format, otherwise short format.
    """
    np.random.seed(1000 + n)
    ## the rolls
    q = dd.dice(2) - 2
    r = dd.flux()
    e = dd.flux()
    b = dd.flux()
    s = dd.flux()
    ## the descriptions
    qua = {0:"Very Bad", 1:"Bad", 2:"Poor", 3:"Lesser", 4:"Below Average", 5:"Average", 6:"Better than same", 7:"Better than many", 8:"Very Good", 9: "Better than most", 10: "Excellent"}
    per = {0:"Minutes", 1:"Hours", 2:"Days", 3:"Weeks", 4:"Months", 5:"Six Months", 6:"One Year", 7:"Two Years", 8:"Three Years", 9: "Four Years", 10: "Ten Years"}
    rel = {-5:"Very unreliable", -4:"More unreliable", -3:"Unreliable", -2:"Somewhat unreliable", -1:"Slightly unreliable", 0:"Reliability neutral", 1:"Better than some", 2:"Better than many", 3:"Reliable", 4:"More reliable", 5:"Very reliable"}
    eas = {-5:"Very difficult to use", -4:"More difficult to use", -3:"Hard to use", -2:"Somewhat hard to use", -1:"Slightly difficult to use", 0:"Ease of use neutral", 1:"Better than some", 2:"Better than many", 3:"Easy to use", 4:"Easier to use", 5:"Very easy to use"}
    bur = {-5:"Very easy-to-carry", -4:"Easier to carry", -3:"Easy to carry/wear", -2:"Better than many", -1:"Better than some", 0:"Burden neutral", 1:"Slightly unurgonomic", 2:"Unwieldy", 3:"Hard to carry", 4:"More burdensome", 5:"Very burdensome"}
    saf = {-5:"Very hazardous", -4:"More hazardous", -3:"Hazardous", -2:"Somewhat hazardous", -1:"Slightly hazardous", 0:"Safety neutral", 1:"Better than some", 2:"Better than many", 3:"Safe to use", 4:"Safer to use", 5:"Very safe"}
    ##description of part
    quality = qua[q] 
    period = per[q]
    reliability = rel[r]
    ease = eas[e]
    burden = bur[b]
    safety = saf[s]
    ##convert to ehex
    q = cnv.ext_hex(q)
    r = cnv.neg_ehex(r, "F")
    e = cnv.neg_ehex(e, "F")
    b = cnv.neg_ehex(b, "F")
    s = cnv.neg_ehex(s, "F")
    if l == 1:
        qrebs = "QREBS for device:\n\n"
        qrebs = qrebs + "Quality: " + q + " (" + quality + ")\n"
        qrebs = qrebs + "Period: " + period + "\n"
        qrebs = qrebs + "Reliability: " + r + " (" + reliability + ")\n" 
        qrebs = qrebs + "Ease of Use: " + e + " (" + ease + ")\n" 
        qrebs = qrebs + "Bulk / Burden: " + b + " (" + burden + ")\n" 
        qrebs = qrebs + "Safety: " + s + " (" + safety + ")\n" 
        return qrebs
    elif l == 0:
        qrebs = q + r + e + b + s
        return qrebs
    else:
        return #bad choice return nothing.