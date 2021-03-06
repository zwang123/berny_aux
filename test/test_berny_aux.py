from berny_aux import *
from berny_aux import opt, bench
from pyscf import gto
from sys import stdout

xyz = "data/n2.xyz"
optxyz = "data/n2.opt.xyz"
log = "data/n2.log"

print("1 Bohr =", bohr, "Angstrom")
atom_str = read_coords(xyz)
mol = gto.M(atom=atom_str)
print(get_coords(mol))
print(get_coords(mol, unit="A"))
print(get_coords(mol, unit="AA"))
print(get_coords(mol, unit="B"))
print(get_coords(mol, unit="Bohr"))
print(extract_coords(log, remark="N2", ofile=None))
extract_coords(log, remark="  N2", ofile=stdout)

opt.geometry_optimization(xyz, 0, basis='6311g', verbose=4)
bench.benchmark(optxyz, 0, basis='6311g', verbose=4)
