from pyscf import gto, dft, scf, cc, lib
from pyscf.dft.libxc import VV10_XC
from berny_aux import read_coords
from berny_aux.timer import Timer
from sys import stderr

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
        mf.nlc = 'VV10' if xc in VV10_XC else ''
        t = Timer(mf.xc).start()
        mf.kernel()
        print(t)
    return mol

def run_ccsd(mol, chkfile):
    """
    run CCSD

    mol     : input/output, a pyscf.gto.Mole object
    """
    t = Timer('CCSD').start()
    mf = scf.RHF(mol).set(chkfile=chkfile).run()
    mycc = cc.CCSD(mf).run()
    print(t)
    if chkfile:
        t = Timer('savechk').start()
        lib.chkfile.save(chkfile, 'cc/t1', mycc.t1)
        lib.chkfile.save(chkfile, 'cc/t2', mycc.t2)
        print(t)
    return mycc

def run_ccsd_t(mol):
    """
    run CCSD(T)

    mol     : input/output, a pyscf.gto.Mole object
    """
    t = Timer('CCSD(T)').start()
    mf = scf.RHF(mol).run()
    mycc = cc.CCSD(mf).run()
    et = mycc.ccsd_t()
    print(t)
    print('CCSD(T) correlation energy', mycc.e_corr + et)
    return mol

def benchmark(xyzname, charge, 
        xclist = ["SCAN", "REVSCAN", 
                  "SCAN_VV10", "SCAN_RVV10", "REVSCAN_VV10"], 
        basis='augccpvtz', verbose=9, 
        perturbative_t=True, chkfile=None, 
        **kwargs):
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

    if perturbative_t:
        run_ccsd_t(mol)
    else:
        run_ccsd(mol, chkfile=chkfile)

    return mol
