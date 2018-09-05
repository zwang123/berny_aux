from pyscf import gto, scf, cc, geomopt, lib
from berny_aux import read_coords, get_coords
from sys import argv, stderr
import time

def geometry_optimization(xyzname, charge, basis='6311++g**', dihedral=False,
                          **kwargs):
    """
    perform geometry optimization with pyberny using CCSD

    xyzname : input, xyz filename
    charge  : input, total charge of the system
    basis   : opt input, basis set
    dihedral: opt input, use dihedral as internal coordinate, might be bugged
    kwargs  : opt input, other arguments passed to pyberny

    opt_mol : out, the optimized molecule
    """

    log = lib.logger.Logger(stderr, 5)
    lib.logger.TIMER_LEVEL = 5
    
    # TODO add symmetry... but does pyberny support symmetry?
    mol = gto.M(
              atom=read_coords(xyzname, format="xyz")
            , charge=charge
            , verbose=9
            , basis=basis)
    
    # TODO replace clock with updated versions
    t0 = time.clock()
    mycc = cc.CCSD(scf.RHF(mol))
    opt_mol = geomopt.optimize(mycc, assert_convergence=True, dihedral=dihedral,
                               verbose=9, **kwargs)
    opt_coord = get_coords(opt_mol, unit="Angstrom")
    log.timer('opt CCSD', t0)
    
    print(opt_coord)

    return opt_mol
