
import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# define some image sizes
size = 20
params = {'legend.fontsize': size*0.75,
#          'figure.figsize': (20,8),
          'axes.labelsize': size,
          'axes.titlesize': size,
          'axes.linewidth': 2,
          'xtick.major.width': 1.5,
          'xtick.major.size': 5,
          'xtick.minor.width': 1.5,
          'xtick.minor.size': 4,
          'ytick.major.width': 1.5,
          'ytick.major.size': 5,
          'ytick.minor.width': 1.5,
          'ytick.minor.size': 3,
          'xtick.labelsize': size*1.,
          'ytick.labelsize': size*1.,
          'axes.titlepad': 25}
plt.rcParams.update(params)

# pixel size in Angstroms, in tomograms
PIXEL_SIZE = 4.34

def plot_hist_all(json_files):

  # distances in nm
  dist = []

  for j_file in json_files:
    with open(j_file, 'r') as f:
      json_data = json.load(f)
    distances = [PIXEL_SIZE / 10.0 * d['dmin'] for d in json_data]
    dist.extend(distances)

  nbins = 130
  # xmax in nm
  xmax = 12.01
  n, bins, patches = plt.hist(dist, nbins, range=(0, xmax), density=False, facecolor='b', alpha=0.75)

  ax = plt.gca()
  ax.spines[['right', 'top']].set_visible(False)
  ax.legend(['n='+str(int(sum(n)))])

  plot_name = 'Untreated'
  plt.title(plot_name, fontsize=23, weight='bold')
  plt.ylabel('Count')
  plt.xlim(0, xmax)

  # x-axis in nm
  plt.xlabel('Distance (nm)')
  ax.xaxis.set_major_locator(MultipleLocator(2))
  ax.xaxis.set_minor_locator(AutoMinorLocator(2))
  ax.yaxis.set_major_locator(MultipleLocator(100))
  ax.yaxis.set_minor_locator(AutoMinorLocator(5))

  plot_name_fullpath = os.path.join('./data/', plot_name + '.png')
  plt.savefig(plot_name_fullpath, dpi=300, bbox_inches='tight')
  plt.close('all')
  print('plot saved:', plot_name_fullpath)
  print()

def main():
  if len(sys.argv) > 1:
    print('ERROR: This script takes no arguments')
    sys.exit(1)

  json_files = [os.path.join('./data/', f) for f in os.listdir('./data/') if f.endswith('.json')]
  plot_hist_all(json_files=json_files)

if __name__ == '__main__':
  main()
