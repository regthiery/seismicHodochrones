import argparse
import sys
import os

sys.path.append("src")

from Hodochrones import Hodochrones

#-------------------------------------------------------------------------
#   Main code
#-------------------------------------------------------------------------

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Plot seismic hodochrones')
    parser.add_argument('script',  type=str, help='the script file name' )
    args = parser.parse_args()
    filename = args.script
    filename = os.path.splitext(filename)[0]
    
    print ("Process script {}".format(filename))


    hodochrones = Hodochrones()
    hodochrones.readScript (filename)
    hodochrones.analyzeData()
    hodochrones.plotData()
    
    
#     scene = Scene()
#     scene.buildFromScript(filename)
    
    
    try:
#         scene.buildAnimation()
        print("OK")
    except KeyboardInterrupt:
        print ("Program interrupted. Exiting...")    
        sys.exit(0)




