# polysome_mef  

Python scripts for ribosome nearest neighbor distance measurements used in 

Fedry et al., [Visualization of translation reorganization upon persistent collision stress in mammalian cells](https://doi.org/10.1101/2023.03.23.533914)

## Dependencies

Please make sure the following Python3 packages are present:

  * [NumPy](https://numpy.org/)  
  * [eulerangles](https://github.com/alisterburt/eulerangles)
  * [Matplotlib](https://matplotlib.org/)

## Quick start

From the top folder of this repository, execute

    gunzip ./data/untreated_ref120.star.gz
    python3 split_star.py ./data/untreated_ref120.star
    python3 compute_data.py ./data/*.tomostar.star
    python3 distances.py

This produces the plot of the nearest neighbor distances 

    ./data/Untreated.png

for the control dataset.

## Usage

First, unpack the star file

    gunzip ./data/untreated_ref120.star.gz

File `./data/untreated_ref120.star` is Relion refine star file with coordinates and angles of all ribosomes in the control dataset.

Next, split the star file into star files per tomogram

    python3 split_star.py ./data/untreated_ref120.star

This generates files `./data/*.tomostar.star` for each tomogram in the dataset.

For each tomogram, compute the data of interest by

    python3 compute_data.py ./data/*.tomostar.star

This generates json files `./data/*.json`.  
The json file is a list of dictionaries, where each dictionary corresponds to a single ribosome, for example:

    { "starfile_row": "...", 
      "xyz": [1459.0, 812.0, 758.0], 
      "rot": -13.40005, 
      "tilt": 72.359731, 
      "psi": 177.817038, 
      "x0y0z0": [0.9149096774193549, -8.739467741935485, 0.6061539170506912], 
      "xyz_entry": [1455.1453325112989, 819.5896008702275, 770.0695129367426], 
      "xyz_exit": [1465.2255310348175, 808.8411191417952, 757.66496787213], 
      "index": 0, 
      "dmin_next": 35.60744083483111, 
      "dmin_next_index": 124, 
      "dmin_prev": 30.79511464048548, 
      "dmin_prev_index": 127, 
      "dmin": 30.79511464048548, 
      "dmin_index": 127 
    }

Here, `xyz_entry` and `xyz_exit` are coordinates in pixels in the original map of the ribosome entry and exit sites, `index` is the index of the ribosome in a tomogram, `dmin` is a distance in pixels to the nearest neighbor, and `dmin_index` is the index of the nearest neighbor ribosome. Similarly, `dmin_next` and `dmin_prev` are distances to the next and previous ribosome in the polysome.

Finally, we plot the distribution of all nearest neighbor distances `dmin` in the dataset by

    python3 distances.py

  
