
import os
import sys
import itertools

def main():
  if len(sys.argv) < 2:
    print('ERROR: Input star file not specified')
    sys.exit(1)
  star_file = sys.argv[1]
  star_file_dir = os.path.dirname(star_file)
  ###############################################
  # adjust the number of header lines here
  header_lines = 25
  # specify which column is MicrographName
  # note that list indexing in python starts from 0
  # hence 1 is subtracted
  # _rlnMicrographName #4
  col_rlnMicrographName = 3
  ###############################################
  starfile_header = ''
  starfile_data = []
  with open(star_file, 'r') as f:
    for n in range(header_lines):
      starfile_header += f.readline()
    for line in f:
      if line.strip(): starfile_data.append(line.split())

  starfile_data_groups = [list(g) for k, g in itertools.groupby(starfile_data, key=lambda x: x[col_rlnMicrographName])]
  for g in starfile_data_groups:
    file_name = g[0][col_rlnMicrographName] + '.star'
    file_name_fullpath = os.path.join(star_file_dir, file_name)
    print('%5d %s' % (len(g), file_name))
    with open(file_name_fullpath, 'w') as f:
      f.write(starfile_header)
      for line in g:
        f.write(' '.join(line) + '\n')

if __name__ == '__main__':
  main()
