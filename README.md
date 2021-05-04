# Knowledge Package - deployment demo

[![DOI](https://zenodo.org/badge/364314508.svg)](https://zenodo.org/badge/latestdoi/364314508)

This repository contains a [Python 3 script](./demo-archivarius.py) that demonstrates the logic of deployment for so called 'Knowledge Package' in accordance to the concept described in the following documents (WIP):
- [Presentation](https://docs.google.com/presentation/d/1jJix6emQyPVbTTxr5HTc0jiB-Nf3lPnujJ-cMa6BCNo/edit?usp=sharing)
- [Scope/Concept Description](https://docs.google.com/document/d/1z92rN3sRDd-mjKkCIo8RZxG1vFkXSnsvvD1xCKL2kiM/edit?usp=sharing)

## Workflow description
The script loads the video recorded during demonstration of the [presentation](https://docs.google.com/presentation/d/1jJix6emQyPVbTTxr5HTc0jiB-Nf3lPnujJ-cMa6BCNo/edit?usp=sharing) into the directory. Procedures of creating directory and downloading of the persistently-identified data are cosidered as deployment operations for different knowledge packages. The identification is artificial: in fact only the video file itself is persistently identified using IPFS, the directory creation is verified via encoding of the name into `base64` system.

## Running
To run the demo, just dive into the cloned directory and run via Python 3:
```sh
python3 demo-archivarius.py
```
After successful execution (Internet connection is required) in the script's directory the new subdirectory called `packages` will be created. Inside the another subdirectory containing the video will be placed.

### Dependencies
- POSIX-compatible operating system
- Python 3.2 or later
- [`yaml`](https://github.com/yaml/pyyaml)
- `binascii`
- `base64`
