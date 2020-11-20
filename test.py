import numpy as np
import pandas as pd

def get_sphere_distribution(n, dmin, Ls, maxiter=1e4, allow_wall=True):
    """Get random points in a box with given dimensions and minimum separation.
    
    Parameters:
      
    - n: number of points
    - dmin: minimum distance
    - Ls: dimensions of box, shape (3,) array 
    - maxiter: maximum number of iterations.
    - allow_wall: whether to allow points on wall; 
       (if False: points need to keep distance dmin/2 from the walls.)
        
    Return:
        
    - ps: array (n, 3) of point positions, 
      with 0 <= ps[:, i] < Ls[i]
    - n_iter: number of iterations
    - dratio: average nearest-neighbor distance, divided by dmin.
    
    Note: with a fill density (sphere volume divided by box volume) above about
    0.53, it takes very long. (Random close-packed spheres have a fill density
    of 0.64).
    
    Author: Han-Kwang Nienhuys (2020)
    Copying: BSD, GPL, LGPL, CC-BY, CC-BY-SA
    See Stackoverflow: https://stackoverflow.com/a/62895898/6228891 
    """
    Ls = np.array(Ls).reshape(3)
    if not allow_wall:
        Ls -= dmin
    
    # filling factor; 0.64 is for random close-packed spheres
    # This is an estimate because close packing is complicated near the walls.
    # It doesn't work well for small L/dmin ratios.
    sphere_vol = np.pi/6*dmin**3
    box_vol = np.prod(Ls + 0.5*dmin)
    fill_dens = n*sphere_vol/box_vol
    if fill_dens > 0.64:
        msg = f'Too many to fit in the volume, density {fill_dens:.3g}>0.64'
        raise ValueError(msg)
    
    # initial try   
    ps = np.random.uniform(size=(n, 3)) * Ls
    
    # distance-squared matrix (diagonal is self-distance, don't count)
    dsq = ((ps - ps.reshape(n, 1, 3))**2).sum(axis=2)
    dsq[np.arange(n), np.arange(n)] = np.infty

    for iter_no in range(int(maxiter)):
        # find points that have too close neighbors
        close_counts = np.sum(dsq < dmin**2, axis=1)  # shape (n,)
        n_close = np.count_nonzero(close_counts)
        if n_close == 0:
            break
        
        # Move the one with the largest number of too-close neighbors
        imv = np.argmax(close_counts)
        
        # new positions
        newp = np.random.uniform(size=3)*Ls
        ps[imv]= newp
        
        # update distance matrix
        new_dsq_row = ((ps - newp.reshape(1, 3))**2).sum(axis=-1)
        dsq[imv, :] = dsq[:, imv] = new_dsq_row
        dsq[imv, imv] = np.inf
    else:
        raise RuntimeError(f'Failed after {iter_no+1} iterations.')

    if not allow_wall:
        ps += dmin/2
    
    dratio = (np.sqrt(dsq.min(axis=1))/dmin).mean
    return ps#, iter_no+1, dratio
  
tmp = get_sphere_distribution(250, 1, [10,10,10])
print(tmp)

omega = get_sphere_distribution(500, 1, [10,10,10])
omega = pd.DataFrame(omega, columns=["x","y","z"])
omega.head()
