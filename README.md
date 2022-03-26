# HPCA-Assignment-1

Benchmarking with GEM5 simulation

## Important Files

- **_HPCA.pdf\:_** The assignment problem statement and specifications in PDF format.
- **_assignment/\:_** The directory containing the source code for the assignment.
    - **_config.py\:_** Configuration file for the gem5 simulation.
    - **_options.py\:_** File for arguments for the config script.
    - **_qsort4.c\:_** C implementation of the quicksort algorithm, will be used for the benchmark.
    - **_qsort4\:_** Binary file of the quicksort algorithm, will be used for the benchmark.
    - **_m5out_/\:_** Directory for the gem5 simulation output.
        - **_stats.txt\:_** File containing the gem5 simulation statistics.
        - **_config.dot\:_** File containing the gem5 configuration in dot format.
        - **_config.png\:_** File containing the gem5 configuration in png format.
        - **_config.ini\:_** File containing the gem5 configuration in ini format.
        - **_config.json\:_** File containing the gem5 configuration in json format.

## Project Structure

```
.
├── assignment
│   ├── __pycache__
│   ├── config.py
│   ├── logs.txt
│   ├── m5out
│   ├── options.py
│   ├── plot.py
│   ├── qsort4
│   ├── qsort4.c
│   ├── run.py
│   ├── runs.tar.gz
│   └── tmp.txt
├── config.py
├── logs.txt
├── m5out
│   ├── config.dot
│   ├── config.ini
│   ├── config.json
│   ├── config.png
│   └── stats.txt
├── options.py
├── plot.py
├── qsort4
├── qsort4.c
├── run.py
└── tmp.txt
```

# Getting Started

```bash
# Install gem5
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev python-dev python
git clone https://gem5.googlesource.com/public/gem5
cd gem5
python3 `which scons` build/X86/gem5.opt -j9

# Clone the repository
$ git clone https://github.com/debajyotidasgupta/HPCA-Assignment-1.git

# Change directory to the assignment directory
$ cd HPCA-Assignment-1

# Copy files from the assignment directory to the benchmark programs directory
$ cp -r assignment/ ~/gem5/configs/

# Change directory to the gem5 root directory
$ cd ~/gem5

# Run the gem5 simulation
$ build/X86/gem5.opt -d configs/assignment/m5out configs/assignment/config.py -b configs/assignment/qsort4
```
