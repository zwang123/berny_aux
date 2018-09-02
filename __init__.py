from sys import stderr

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
        try:
            # first two line discarded
            atom_str = "".join(file.readlines()[2:]) 
        except:
            with open(file, "r") as f:
                # first two line discarded
                atom_str = "".join(f.readlines()[2:]) 
    else:
        print("read_coords: arg format=", unit, 
                "is not recognized", file=stderr)
        raise ValueError
    return atom_str

#def gen_ccsd_t_energy_gradient(mol):
#    """
#    A scanner function used for pyscf.geomopt.optimize
#
#    input: pyscf.gto.Mole
#    output: energy, gradient
#    """
#    ene, gra = scf. grad_scan(mol)
#def gen_CCSD_T(mol):
#CCSD_T = berny_solver.as_pyscf_method(mol, gen_cc)
