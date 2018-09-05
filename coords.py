from sys import stderr
from .file import file_wrapper

try:
    from berny import bohr # backward compatibility for berny <= 0.3.2
except ImportError:
    from berny import angstrom
    bohr = 1.0 / angstrom

def get_coords(mol, unit="Angstrom"):
    """
    convert the output of pyscf.geomopt.optimize to atomic coordinates

    mol     : input, pyscf.gto.Mole object, return of pyscf.geomopt.optimize
    unit    : opt input, def=Angstrom, other accepted: 'A', 'AA', 'B', 'Bohr'
    coords  : out, maybe numpy array? the atomic coordinates returned
    """
    if unit is None or unit in ["A", "AA", "Angstrom"]:
        multiplier = bohr
    elif unit in ["B", "Bohr"]:
        multiplier = 1.0
    else:
        print("get_coords: arg unit=", unit, 
                "is not recognized", file=stderr)
        raise ValueError
    coords = mol.atom_coords() * multiplier
    return coords

def read_coords(file, format="xyz"):
    """
    read coordinates from file

    file    : input, file object or filename
    format  : opt input, def=xyz, the only accepted format
    atom_str: out, string that could be used as param of atom
              to build pyscf.gto.Mole
    """
    if format is None or format in ["xyz"]:
        # first two line discarded
        atom_str = "".join(file_wrapper(file, "readlines")[2:]) 
    else:
        print("read_coords: arg format=", unit, 
                "is not recognized", file=stderr)
        raise ValueError
    return atom_str

def extract_coords(logfile, remark="", ofile=None, 
                   unit='Angstrom', format="xyz"):
    r"""
    generate coordinate files from a log file of a geometric optimization run

    logfile : input, file object or filename, log file of geomopt
    remark  : opt input, a short comment/explanation added to the file
              should not contain '\n'
    ofile   : opt input, file object or filename
    unit    : opt input, unit of coordinates
    format  : opt input, def=xyz, the only accepted format
    coords  : out, string that could be written as a coordinate file
    """
    log = file_wrapper(logfile, "readlines")
    for i, l in enumerate(log):
        if "New geometry" in l:
            last_idx = i + 1
    coords = ""
    natom = 0
    if format is None or format in ["xyz"]:
        for i in range(last_idx, len(log)):
            if log[i].strip() == "":
                break
            idx, coord = log[i].split(None, 1) # rm 1st word
            try:
                if int(idx) == natom + 1:
                    if unit is None or unit in ["A", "AA", "Angstrom"]:
                        elem, pos = coord.split(None, 1)
                        coords += "{:4s} {:16.12f} {:16.12f} {:16.12f}\n" \
                                .format(elem,  
                                        *[float(x) * bohr for x in pos.split()])
                    elif unit in ["B", "Bohr"]:
                        coords += coord
                    else:
                        print("extract_coords: arg unit=", unit, 
                                "is not recognized", file=stderr)
                        raise ValueError
                    natom += 1
            except:
                break
        if coords == "":
            print("No geometry found", file=stderr)
            raise RuntimeError
        coords = "{}\n{}\n{}".format(natom, remark, coords)
    else:
        print("extract_coords: arg format=", format, 
                "is not recognized", file=stderr)
        raise ValueError
    if ofile is not None:
        file_wrapper(ofile, "writelines", "w", coords)
    return coords
