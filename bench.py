from pyscf import gto, dft, scf, cc, lib
from pyscf.dft.libxc import VV10_XC
from berny_aux import read_coords
from sys import stderr
import time

log = lib.logger.Logger(stderr, 5)
lib.logger.TIMER_LEVEL = 5

def run_dft(mol, xclist):
    """
    run dft for xclist

    mol     : input/output, a pyscf.gto.Mole object
    xclist  : input, a list of xc functionals to be calculated
    """

    mf = dft.RKS(mol)

    for xc in xclist:
        mf.xc = xc
        # TODO not use clock()
        mf.nlc = 'VV10' if xc in VV10_XC else ''
        t0 = time.clock()
        mf.kernel()
        log.timer(mf.xc, t0)
    return mol

def run_ccsd_t(mol):
    """
    run CCSD(T)

    mol     : input/output, a pyscf.gto.Mole object
    """
    # TODO not use clock()
    t0 = time.clock()
    mf = scf.RHF(mol).run()
    mycc = cc.CCSD(mf).run()
    et = mycc.ccsd_t()
    print('CCSD(T) correlation energy', mycc.e_corr + et)
    log.timer('CCSD(T)', t0)
    return mol

def benchmark(xyzname, charge, 
        xclist = ["SCAN", "REVSCAN", 
                  "SCAN_VV10", "SCAN_RVV10", "REVSCAN_VV10"], 
        basis='augccpvtz', verbose=9, **kwargs):
    """
    benchmark a molecule

    xyzname : input, xyz filename
    charge  : input, total charge of the system
    xclist  : opt input, a list of xc functionals to be calculated
    basis   : opt input, basis set
    verbose : opt input, level of output
    kwargs  : opt input, other arguments passed to pyscf.gto.Mole.build()

    mol     : out, the calculated molecule
    """
    
    mol = gto.M(
              atom=read_coords(xyzname, format="xyz")
            , charge=charge
            , verbose=verbose
            , symmetry=True
            , basis=basis
            , **kwargs)
    
    run_dft(mol, xclist)
    run_ccsd_t(mol)
    return mol
