
import os
import sys
import json
import numpy as np
import eulerangles as ea

# Relion header matching the one in star files
#
#_rlnCoordinateX #1 
#_rlnCoordinateY #2 
#_rlnCoordinateZ #3 
#_rlnMicrographName #4 
#_rlnGroupNumber #5 
#_rlnAngleRot #6 
#_rlnAngleTilt #7 
#_rlnAnglePsi #8 
#_rlnCtfMaxResolution #9 
#_rlnImageName #10 
#_rlnCtfImage #11 
#_rlnPixelSize #12 
#_rlnOpticsGroup #13 
#_rlnOriginXAngst #14 
#_rlnOriginYAngst #15 
#_rlnOriginZAngst #16 
#_rlnClassNumber #17 
#_rlnNormCorrection #18 
#_rlnRandomSubset #19 
#_rlnLogLikeliContribution #20 
#_rlnMaxValueProbDistribution #21 
#_rlnNrOfSignificantSamples #22 

# pixel size in Angstroms, in tomograms
PIXEL_SIZE = 4.34

# box size in pixels
box_size = 128

# box center in pixels
center = np.array([1.0, 1.0, 1.0]) * (box_size // 2)

# polysome entry and exit sites in pixels
offset_entry = np.array([76.87, 62.0, 65.0]) - center
offset_exit = np.array([65.1, 76.24, 70.45]) - center

def rotation_matrix(rot, tilt, psi):
  # angles in degrees
  angles = np.array([rot, tilt, psi])
  R = ea.euler2matrix(angles, axes='zyz', 
    intrinsic=True, right_handed_rotation=True)
  return R.T

def compute_data(star_file):
  # adjust number of header lines in star file
  starfile_header_lines = 25
  starfile_data = []
  with open(star_file, 'r') as f:
    for _ in range(starfile_header_lines):
      next(f)
    for line in f:
      if line.strip():
        line1 = line.split()
        d = dict()
        d['starfile_row'] = line
        # _rlnCoordinateX #1 
        # _rlnCoordinateY #2 
        # _rlnCoordinateZ #3         
        d['xyz'] = np.array([float(line1[0]), float(line1[1]), float(line1[2])])
        #_rlnAngleRot #6 
        #_rlnAngleTilt #7 
        #_rlnAnglePsi #8 
        # angles are in degrees
        d['rot'] = float(line1[5])
        d['tilt'] = float(line1[6])
        d['psi'] = float(line1[7])
        # _rlnOriginXAngst #14 
        # _rlnOriginYAngst #15 
        # _rlnOriginZAngst #16 
        d['x0y0z0'] = np.array([float(line1[13]), float(line1[14]), float(line1[15])]) / PIXEL_SIZE
        # calculate XYZ of entry and exit sites
        R = rotation_matrix(rot=d['rot'], tilt=d['tilt'], psi=d['psi'])
        d['xyz_entry'] = d['xyz'] - d['x0y0z0'] + np.matmul(R, offset_entry)
        d['xyz_exit'] = d['xyz'] - d['x0y0z0'] + np.matmul(R, offset_exit)
        starfile_data.append(d)

  # compute distances
  n = len(starfile_data)
  for i in range(n):
    starfile_data[i]['index'] = i
    dmin = 10000.0
    dmin_next = 10000.0
    dmin_prev = 10000.0
    dmin_index = -1
    dmin_next_index = -1
    dmin_prev_index = -1
    for j in range(n):
      if i == j: continue
      dprev = np.linalg.norm(starfile_data[i]['xyz_entry'] - starfile_data[j]['xyz_exit'])
      dnext = np.linalg.norm(starfile_data[i]['xyz_exit'] - starfile_data[j]['xyz_entry'])
      if dmin_prev > dprev:
        dmin_prev = dprev
        dmin_prev_index = j
      if dmin_next > dnext:
        dmin_next = dnext
        dmin_next_index = j
    starfile_data[i]['dmin_next'] = dmin_next
    starfile_data[i]['dmin_next_index'] = dmin_next_index
    starfile_data[i]['dmin_prev'] = dmin_prev
    starfile_data[i]['dmin_prev_index'] = dmin_prev_index
    starfile_data[i]['dmin'] = dmin_next
    starfile_data[i]['dmin_index'] = dmin_next_index
    if dmin_prev < dmin_next:
      starfile_data[i]['dmin'] = dmin_prev
      starfile_data[i]['dmin_index'] = dmin_prev_index

  # convert np arrays back to lists for json export
  for d in starfile_data:
    for k in d.keys():
      if type(d[k]) == np.ndarray:
        d[k] = d[k].tolist()

  # save data
  output_file = os.path.basename(star_file).split('.')[0] + '.json'
  output_file_fullpath = os.path.join(os.path.dirname(star_file), output_file)
  with open(output_file_fullpath, 'w') as f:
    json.dump(starfile_data, f)

  print(output_file, '  N =', len(starfile_data))

def main():
  if len(sys.argv) < 2:
    print('ERROR: Tomogram star file not specified')
    sys.exit(1)

  for star_file in sys.argv[1:]:
    compute_data(star_file=star_file)

if __name__ == '__main__':
  main()
