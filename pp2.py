# -*- coding: utf-8 -*-
# @Author: yow004
# @Date:   2019-01-08 00:38:14
# @Last Modified by:   yow004
# @Last Modified time: 2019-03-09 10:27:36
#!/usr/bin/env python

"""
Simulation: RS friction  ( arcsinh version )
"""
import numpy, SORDlatest, sys
#debug = 3
#itstats=1
rundir = 'pp2'

dx = 50, 50, 50

np3 = 32,16,16

# dimensions
L = 60000., 20000., 40000.

T = 25. 
dt = dx[0] / 12500.0
nt = int( T / dt + 1.5 )

nn = (
   int( L[0] / dx[0] + 1.5 ),
   int( L[1] / dx[1] + 1.5 ),
   int( L[2] / dx[2] + 2.5 ),
)

ihypo = int((L[0]/2.-20e3)/dx[0]+1.5), int((L[1]/2.-1000)/dx[1]+1.5), int(L[2]/2./dx[2]+1.5)
#ihypo = 181, 106, 76.5
#ihypo = (373-1)*4+1,(109-1)*4+1, int(L[2]/2./dx[2]+1.5)
#ihypo = 393,118, 38
print ihypo
npml = 10
faultnormal = 3

# boundary conditions
bc1 = 10, 0,  10 
bc2 = 10, 10, 10

# material properties
hourglass = 1.0, 2.0
eplasticity = 'plastic'
tv=50./3464
_i1=10.5,nn[0]-10.5
_j2=1.5, nn[1]-10.5
_k3=10.5,nn[2]-10.5
fieldio = [
   ( '=', 'rho', [], 2670.0  ),
   ( '=', 'vp',  [], 6000.0  ),
   ( '=', 'vs',  [], 3464.0  ),
   ( '=', 'gam', [], 0.1    ),
# elastic in pml zone and no slip
   ( '=', 'mco', [], 1e10),
   ( '=', 'mco', [_i1,_j2,_k3], 3e6),
   ( '=', 'phi', [], 0.75),
] 
# initial volume stress input
ivols = 'yes'
fieldio += [
   ( '=r', 'a33', [(),(),()], 'normal3.binr'),
   ( '=r', 'a22', [(),(),()], 'normal2.binr'),
   ( '=r', 'a11', [(),(),()], 'normal1.binr'),
#   ( '=', 'a23', [],   10.e6),
   ( '=r', 'a31', [(),(),()], 'shear.binr' ),
#   ( '=R', 'a33', [(),(),ihypo[2]+0.5], 'normal3.bin'),
#   ( '=R', 'a22', [(),(),ihypo[2]+0.5], 'normal2.bin'),
#   ( '=R', 'a11', [(),(),ihypo[2]+0.5], 'normal1.bin'),
#   ( '=', 'a23', [],   10.e6),
#   ( '=R', 'a31', [(),(),ihypo[2]+0.5], 'shear.bin' ),
#
#   ( '=', 'tn',  [], -30e6 ),
#   ( '=', 'ts', [],   15e6  ),
#   ( '=', 'td', [],   -5e6 ),
]  
slipvector = (1.0, 0.0, 0.0)
# _l1 = 15000
# _l2 = 15000
# j = int(30e3/dx[0]),int(170e3/dx[0])
# k = int(20e3/dx[1]),int(60e3/dx[1])
# rate-and-state friciton parameters
friction = 'rateandstate'
fieldio += [
#  ('=',  'td', [j,k,1,1], -5e6),
#    ( '=', 'dc',  [],  0.4),
#    ( '=', 'mus', [],  0.5),
#    ( '=', 'mud', [],  0.2),
   ( '=', 'bf',  [],  0.014  ),
#   ( '=r', 'vw', [], 'vw.bin2'  ),
#   ( '=r', 'af', [], 'af'  ),
#   ( '=', 'af',  [], 0.01),
#   ( '=', 'af',  [j,k,1,1], 0.01),
   #( '=', 'vw',  [], 0.16),
   ( '=', 'v0',  [],  1.e-6  ),
   ( '=', 'f0',  [],    0.6  ),
   ( '=', 'll',  [],    0.2  ),
   ( '=', 'fw',  [],    0.3  ),

   
#   ( '=', 'vw',  [],    0.1),
   ( '=', 'v1',  [(), (), (1,int(ihypo[2])), 1],  -5e-10 ),
   ( '=', 'v1',  [(), (), (int(ihypo[2])+1,nn[2]), 1], 5e-10 ),

   ( '=r', 'af',  [], 'af.bin'),
   ( '=r', 'vw',  [], 'vwf.bin'),
#   ( '=r', 'vw',  [], 'vwf.bin'),
#   ( '=r', 'll',  [], 'llf.bin'),
#   ( '=r', 'f0',  [], 'f0f.bin'),
#   ( '=r', 'fw',  [], 'fwf.bin' ),
#   ( '=r', 'vw',  [], 'vw.bin'),



#   ( '=', 'af',  [],   0.01 ),
#   ( '=r', 'vw', [], 'vw.bin'  ),
#   ( '=r', 'af', [], 'af.bin'  ),
#   ( '=r', 'vw', [], 'vw.bin' ),
#   ( '=', 'vw',  [],  0.1 ),
#   ( '=', 'vw',  [j,k,(),()], 0.05), 

]

# Read grid
# fieldio += [
# #   ( '=r', 'x1',  [],  'x.bin'  ),
# #   ( '=r', 'x2',  [],  'y.bin'  ),
#    ( '=r', 'x3',  [],  'z.bin'  ),
# ]

#skepb = 0.0
svtol = 0.1
# nucleation
rnucl = 3000.
#psidelts = 0.9
delts = 1
tmnucl = 1.




# _xoff0 = int(0./dx[0])
# _xoff1 = int(15.e3/dx[0])
# _xoff2 = int(30.e3/dx[0])
# _yoff3 = 371



# _kkn4x = 970.556285
# _kkn4y = 308.104111

_or = 1
_ort = 100

_ox = 10
_oz = 10
_ot = 1

fieldio += [
  ( '=w', 'x1',  [(1,-1,_ox),1,(1,ihypo[2],_ox)], 'hc_x1-'  ),
  ( '=w', 'x2',  [(1,-1,_ox),1,(1,ihypo[2],_ox)], 'hc_x2-'  ),
  ( '=w', 'x3',  [(1,-1,_ox),1,(1,ihypo[2],_ox)], 'hc_x3-'  ),
  ( '=w', 'x1',  [(1,-1,_ox),1,(ihypo[2]+1,-1,_ox)], 'hc_x1+'  ),
  ( '=w', 'x2',  [(1,-1,_ox),1,(ihypo[2]+1,-1,_ox)], 'hc_x2+'  ),
  ( '=w', 'x3',  [(1,-1,_ox),1,(ihypo[2]+1,-1,_ox)], 'hc_x3+'  ),

  ( '=w', 'a1',  [(1,-1,_ox),1,(1,ihypo[2],_ox), (1,-1,_ot)], 'h_a1-'  ),
  ( '=w', 'a1',  [(1,-1,_ox),1,(ihypo[2]+1,-1,_ox),(1,-1,_ot)], 'h_a1+'  ),
  ( '=w', 'a2',  [(1,-1,_ox),1,(1,ihypo[2],_ox), (1,-1,_ot)], 'h_a2-'  ),
  ( '=w', 'a2',  [(1,-1,_ox),1,(ihypo[2]+1,-1,_ox),(1,-1,_ot)], 'h_a2+'  ),
  ( '=w', 'a3',  [(1,-1,_ox),1,(1,ihypo[2],_ox), (1,-1,_ot)], 'h_a3-'  ),
  ( '=w', 'a3',  [(1,-1,_ox),1,(ihypo[2]+1,-1,_ox),(1,-1,_ot)], 'h_a3+'  ),

  ( '=w', 'v1',  [(1,-1,_ox),1,(1,ihypo[2],_ox), (1,-1,_ot)], 'h_v1-'  ),
  ( '=w', 'v1',  [(1,-1,_ox),1,(ihypo[2]+1,-1,_ox),(1,-1,_ot)], 'h_v1+'  ),
  ( '=w', 'v2',  [(1,-1,_ox),1,(1,ihypo[2],_ox), (1,-1,_ot)], 'h_v2-'  ),
  ( '=w', 'v2',  [(1,-1,_ox),1,(ihypo[2]+1,-1,_ox),(1,-1,_ot)], 'h_v2+'  ),
  ( '=w', 'v3',  [(1,-1,_ox),1,(1,ihypo[2],_ox), (1,-1,_ot)], 'h_v3-'  ),
  ( '=w', 'v3',  [(1,-1,_ox),1,(ihypo[2]+1,-1,_ox),(1,-1,_ot)], 'h_v3+'  ),

  ( '=w', 'u1',  [(1,-1,_ox),1,(1,ihypo[2],_ox), (1,-1,_ot)], 'h_u1-'  ),
  ( '=w', 'u1',  [(1,-1,_ox),1,(ihypo[2]+1,-1,_ox),(1,-1,_ot)], 'h_u1+'  ),
  ( '=w', 'u2',  [(1,-1,_ox),1,(1,ihypo[2],_ox), (1,-1,_ot)], 'h_u2-'  ),
  ( '=w', 'u2',  [(1,-1,_ox),1,(ihypo[2]+1,-1,_ox),(1,-1,_ot)], 'h_u2+'  ),
  ( '=w', 'u3',  [(1,-1,_ox),1,(1,ihypo[2],_ox), (1,-1,_ot)], 'h_u3-'  ),
  ( '=w', 'u3',  [(1,-1,_ox),1,(ihypo[2]+1,-1,_ox),(1,-1,_ot)], 'h_u3+'  ),

#snapshots
# 
   ( '=w', 'pgv1',  [(),1,(), -1], 'pgv1'  ),
   ( '=w', 'pgv3',  [(),1,(), -1], 'pgv3'  ),
   ( '=w', 'pgvs2',  [(),1,(), -1], 'pgvs2'  ),

   ( '=w', 'x1',  [(),(1,2),(), ()], 'hc_x1'  ),
   ( '=w', 'x2',  [(),(1,2),(), ()], 'hc_x2'  ),
   ( '=w', 'x3',  [(),(1,2),(), ()], 'hc_x3'  ),
   ( '=w', 'epm', [(),1.5,(),-1],   'plstrain'),

   ( '=w', 'x1',  [(),1,(), ()], 'h_x1'  ),
   ( '=w', 'x2',  [(),1,(), ()], 'h_x2'  ),
   ( '=w', 'x3',  [(),1,(), ()], 'h_x3'  ),

   ( '=w', 'a1',  [(),1,(), (1,-1,_ort)], 'hs_a1'  ),
   ( '=w', 'a2',  [(),1,(), (1,-1,_ort)], 'hs_a2'  ),
   ( '=w', 'a3',  [(),1,(), (1,-1,_ort)], 'hs_a3'  ),

   ( '=w', 'v1',  [(),1,(), (1,-1,_ort)], 'hs_v1'  ),
   ( '=w', 'v2',  [(),1,(), (1,-1,_ort)], 'hs_v2'  ),
   ( '=w', 'v3',  [(),1,(), (1,-1,_ort)], 'hs_v3'  ),

   ( '=w', 'u1',  [(),1,(), (1,-1,_ort)], 'hs_u1'  ),
   ( '=w', 'u2',  [(),1,(), (1,-1,_ort)], 'hs_u2'  ),
   ( '=w', 'u3',  [(),1,(), (1,-1,_ort)], 'hs_u3'  ),

   ( '=w', 'x1',  [(),(),ihypo[2], ()], 'fs_x1'  ),
   ( '=w', 'x2',  [(),(),ihypo[2], ()], 'fs_x2'  ),
   ( '=w', 'x3',  [(),(),ihypo[2], ()], 'fs_x3'  ),

   ( '=w', 'tsm', [(),(),1,(1,-1,_ort)], 'tsm'),
   ( '=w', 'svm', [(),(),1,(1,-1,_ort)], 'srm'),
   ( '=w', 'tsm', [(),(),1,1], 'ts0'),
   ( '=w', 'sum', [(),(),1,-1], 'slip'),

   ( '=w', 'trup',[(),(),1,-1], 'trup'),
   ( '=w', 'tarr',[(),(),1,-1], 'tarr'),


#   ( '=w', 'af',[], 'afinput'),
#   ( '=w', 'vw',[], 'vwinput'), 
   # ( '=w', 'x1',[(),(1,2),()],'sc_x1'),
   # ( '=w', 'x2',[(),(1,2),()],'sc_x2'),
   # ( '=w', 'x3',[(),(1,2),()],'sc_x3'),
   
   # ( '=w', 'w11',[(),1.5,(),(1,-1,_ort)],'s11'),
   # ( '=w', 'w22',[(),1.5,(),(1,-1,_ort)],'s22'),
   # ( '=w', 'w33',[(),1.5,(),(1,-1,_ort)],'s33'),
   # ( '=w', 'w23',[(),1.5,(),(1,-1,_ort)],'s23'),
   # ( '=w', 'w31',[(),1.5,(),(1,-1,_ort)],'s31'),
   # ( '=w', 'w12',[(),1.5,(),(1,-1,_ort)],'s12'),
   
   # ( '=w', 'e11',[(),1.5,(),(1,-1,_ort)],'e11'),
   # ( '=w', 'e22',[(),1.5,(),(1,-1,_ort)],'e22'),
   # ( '=w', 'e33',[(),1.5,(),(1,-1,_ort)],'e33'),
   # ( '=w', 'e23',[(),1.5,(),(1,-1,_ort)],'e23'),
   # ( '=w', 'e31',[(),1.5,(),(1,-1,_ort)],'e31'),
   # ( '=w', 'e12',[(),1.5,(),(1,-1,_ort)],'e12'),

   # ('=w', 'tsm', [(),(1,3),1,(1,-1)], 'stsm'),
   # ('=w', 'tnm', [(),(1,3),1,(1,-1)], 'stnm'),
   # ('=w', 'svm', [(),(1,3),1,(1,-1)], 'ssvm'),



#('=wi','a1', [_kkn4x,_kkn4y,1,()], 'accx'),
#('=wi','a2', [_kkn4x,_kkn4y,1,()], 'accy'),
#('=wi','a3', [_kkn4x,_kkn4y,1,()], 'accz'),
#('=wi','v1', [_kkn4x,_kkn4y,1,()], 'velx'),
#('=wi','v2', [_kkn4x,_kkn4y,1,()], 'vely'),
#('=wi','v3', [_kkn4x,_kkn4y,1,()], 'kkn4z'),
#('=wi','v1', [_kkn4x,_kkn4y,1,()], 'kkn4x'),
#('=wi','v2', [_kkn4x,_kkn4y,1,()], 'kkn4y'),
#('=wi','u1', [_kkn4x,_kkn4y,1,()], 'disx'),
#('=wi','u2', [_kkn4x,_kkn4y,1,()], 'disy'),
#('=wi','u3', [_kkn4x,_kkn4y,1,()], 'disz'),


#('=w', 'v3',[(1,-1,25),(1,-1,25),1,()],'velz'),


#    ( '=w', 'sv3',  [], 'slipr_z'  ),
#    ( '=w', 'su2',  [(),(),801,-1], 'slip_y'),
#    ( '=w', 'su3',  [(),(),801,-1], 'slip_z'),
#    ( '=w', 'x1',  [], 'xx'  ),
#    ( '=w', 'x2',  [], 'yy'  ),
#    ( '=w', 'x3',  [], 'zz'  ), # final horizontal slip
#    ( '=w', 'mus', [], 'mustatic'),
#    ( '=w', 'nhat1',[ihypo[0],(),1,1], 'n_x'),
#    ( '=w', 'nhat2',[ihypo[0],(),1,1], 'n_y'),
#    ( '=w', 'nhat3',[ihypo[0],(),1,1], 'n_z'),
#    ( '=w', 'a2',  [ihypo[0],(),(ihypo[2],ihypo[2]+1),(1,-1,50)],'a2'),
#    ( '=w', 'a3',  [ihypo[0],(),(ihypo[2],ihypo[2]+1),(1,-1,50)],'a3'),
#    ( '=w', 'v2',  [ihypo[0],(),(ihypo[2],ihypo[2]+1),(1,-1,50)],'v2'),
#    ( '=w', 'v3',  [ihypo[0],(),(ihypo[2],ihypo[2]+1),(1,-1,50)],'v3'),
#    ( '=w', 'u2',  [ihypo[0],(),(ihypo[2],ihypo[2]+1),(1,-1,50)],'u2'),
#    ( '=w', 'u3',  [ihypo[0],(),(ihypo[2],ihypo[2]+1),(1,-1,50)],'u3'),
#    ( '=w', 'af',  [(1,-1,_or),(1,-1,_or),1,1], 'af'),
#    ( '=w', 'f0',  [(1,-1,_or),(1,-1,_or),1,1], 'f0'),
#    ( '=w', 'fw',  [(1,-1,_or),(1,-1,_or),1,1], 'fw'),
#    ( '=w', 'll',  [(1,-1,_or),(1,-1,_or),1,1], 'll'),
#    ( '=w', 'vw',  [(1,-1,5),(1,-1,5),1,1], 'vw'),

#    ( '=w', 'nhat1',[], 'nhat1'),
#    ( '=w', 'nhat2',[], 'nhat2'),
#    ( '=w', 'nhat3',[], 'nhat3'),
#    ( '=w', 't1', [], 't1'),
#    ( '=w', 't2', [], 't2'),
#    ( '=w', 't3', [], 't3'),
#    ( '=w', 'ts1', [], 'ts1'),
#    ( '=w', 'ts2', [], 'ts2'),
#    ( '=w', 'ts3', [], 'ts3'),
#    ( '=w', 'tnm', [(1,-1,5),(1,-1,5),1,(1,-1,1)], 'tnm'),
#    ( '=w', 'tnm', [(1,-1,5),(1,-1,5),1,1],'tnm0'), 
#    ( '=w', 'tnm', [(),(),1,-1], 'tnme'),
#    ( '=w', 'tnm', [(),(),1,1],'tnm0'),
#    ( '=w', 'tsm', [(),(),1,-1], 'tsme'),
#    ( '=w', 'tsm', [(),(),1,1],'tsm0'),
#    ( '=w', 'tnm', [(1,-1,_or),(1,-1,_or),1,(1,-1,_ort)], 'tnm'),
#   ( '=w', 'tsm', [(1,-1,_or),(1,-1,_or),1,(1,-1,_ort)], 'tsm'),
#   ( '=w', 'svm', [(1,-1,_or),(1,-1,_or),1,(1,-1,_ort)], 'srm'),
#    ( '=w', 'svm', [(1,-1,5),(1,-1,5),1,(1,-1,1)], 'radiation'),
#    ( '=w', 'ts1', [(1,-1,_or),(1,-1,_or),1,(1,-1,_ort)], 'ts1'),
#    ( '=w', 'ts2', [(1,-1,_or),(1,-1,_or),1,(1,-1,_ort)], 'ts2'),
#    ( '=w', 'ts3', [(1,-1,_or),(1,-1,_or),1,(1,-1,_ort)], 'ts3'),

#    ( '=w', 'svm', [(1,-1,5),(1,-1,5),1,(1,-1,1)], 'sliprate'),
#    ( '=w', 'sa1', [], 'sa1'),
#    ( '=w', 'sa2', [], 'sa2'),
#    ( '=w', 'sa3', [], 'sa3'),
#    ( '=w', 'sv1', [], 'sv1'),
#    ( '=w', 'sv2', [], 'sv2'),
#    ( '=w', 'sv3', [], 'sv3'),


#('=w','w11',[(),(),(ihypo[2]-1,ihypo[2]+1),(1,-1)], 'sigma_11'),
#('=w','w22',[(),(),(ihypo[2]-1,ihypo[2]+1),(1,-1)], 'sigma_22'),
#('=w','w33',[(),(),(ihypo[2]-1,ihypo[2]+1),(1,-1)], 'sigma_33'),   
#('=w','w23',[(),(),(ihypo[2]-1,ihypo[2]+1),(1,-1)], 'sigma_23'),
#('=w','w31',[(),(),(ihypo[2]-1,ihypo[2]+1),(1,-1)], 'sigma_31'),
#('=w','w12',[(),(),(ihypo[2]-1,ihypo[2]+1),(1,-1)], 'sigma_12'),

##('=w','e11',[(),(),(ihypo[2]-1,ihypo[2]+1),(1,-1)], 'eta_11'),
#('=w','e22',[(),(),(ihypo[2]-1,ihypo[2]+1),(1,-1)], 'eta_22'),
#('=w','e33',[(),(),(ihypo[2]-1,ihypo[2]+1),(1,-1)], 'eta_33'),
#('=w','e23',[(),(),(ihypo[2]-1,ihypo[2]+1),(1,-1)], 'eta_23'),
#('=w','e31',[(),(),(ihypo[2]-1,ihypo[2]+1),(1,-1)], 'eta_31'),
#('=w','e12',[(),(),(ihypo[2]-1,ihypo[2]+1),(1,-1)], 'eta_12'),
#('=w','epm',[(),(),(ihypo[2]-1,ihypo[2]+1),(1,-1)], 'epm'),
#    ( '=w', 'vw',  [], 'vw'),
#    ( '=w', 'ts1',  [], 'ts1'),
#    ( '=w', 'ts2',  [], 'ts2'),
#    ( '=w', 'ts3',  [], 'ts3'),
#    ( '=w', 'tsm', [(1,-1,5),(1,-1,5),1,(1,-1,25)], 'tsm'),
#    ( '=w', 'tnm', [(1,-1,5),(1,-1,5),1,(1,-1,25)], 'tnm'),
#    ( '=w', 'trup', [(1,-1,_or),(1,-1,_or),1,-1], 'trup'),
#    ( '=w', 'tarr', [(1,-1,_or),(1,-1,_or),1,-1], 'tarr'),
#    ( '=w', 'sl', [(1,-1,_or),(1,-1,_or),1,(1,-1,_ort)], 'slippath'),
#    ( '=w', 'sum', [(1,-1,_or),(1,-1,_or),1,(1,-1,_ort)],'sliptest'),
#    ( '=w', 'sum', [(1,-1,_or),(1,-1,_or),1,-1], 'slip'),
    # ( '=w', 'x1',  [(1,-1,_or),(1,-1,_or),ihypo[2],1],'faultx'),
    # ( '=w', 'x2',  [(1,-1,_or),(1,-1,_or),ihypo[2],1],'faulty'),
    # ( '=w', 'x3',  [(1,-1,_or),(1,-1,_or),ihypo[2],1],'faultz'),

    # ( '=w', 'mr11',[(1,-1,_or),(1,-1,_or),1,(1,-1,_ort)], 'mr11'),
    # ( '=w', 'mr22',[(1,-1,_or),(1,-1,_or),1,(1,-1,_ort)], 'mr22'),
    # ( '=w', 'mr33',[(1,-1,_or),(1,-1,_or),1,(1,-1,_ort)], 'mr33'),
    # ( '=w', 'mr12',[(1,-1,_or),(1,-1,_or),1,(1,-1,_ort)], 'mr12'),
    # ( '=w', 'mr31',[(1,-1,_or),(1,-1,_or),1,(1,-1,_ort)], 'mr31'),
    # ( '=w', 'mr23',[(1,-1,_or),(1,-1,_or),1,(1,-1,_ort)], 'mr23'),

#    ( '=w', 'mr11',[], 'mr11'),
#    ( '=w', 'mr22',[], 'mr22'),
#    ( '=w', 'mr33',[], 'mr33'),
#    ( '=w', 'mr12',[], 'mr12'),
#    ( '=w', 'mr31',[], 'mr31'),
#    ( '=w', 'mr23',[], 'mr23'),
    
#( '=w', 'svm', [(1,-1,1),(301,501,5),1,(1,-1,25)], 'svline'),
#( '=w', 'tsm', [(1,-1,1),(301,501,5),1,(1,-1,25)], 'tsline'),
#( '=w', 'tnm', [(1,-1,1),(301,501,5),1,(1,-1,25)], 'tnline'),

#    ('=w', 'x1', [(1,-1,1),(1,-1,1),(ihypo[2]-20,ihypo[2]+20,1),1],'fzx'),
#    ('=w', 'x2', [(1,-1,1),(1,-1,1),(ihypo[2]-20,ihypo[2]+20,1),1],'fzy'),
#    ('=w', 'x3', [(1,-1,1),(1,-1,1),(ihypo[2]-20,ihypo[2]+20,1),1],'fzz'),
#    ('=w', 'epm',[(1.5,-1.5,1),(1.5,-1.5,1),(ihypo[2]-20+0.5,ihypo[2]+20-0.5,1),-1],'plstrain'),
#    ('=w','strbar',[(1.5,-1.5,1),(1.5,-1.5,1),(ihypo[2]+0.5-20,ihypo[2]-0.5+20,1),-1],'strbar'),
#    ('=w','stry',[(1.5,-1.5,1),(1.5,-1.5,1),(ihypo[2]+0.5-20,ihypo[2]-0.5+20,1),-1],'stry'),
# seismic wave fields:
#('=w', 'x1',[(1,-1,1),(1,401,1),(1,ihypo[2],1),1],'wfx'),
#('=w', 'x2',[(1,-1,1),(1,401,1),(1,ihypo[2],1),1],'wfy'),
#('=w', 'x3',[(1,-1,1),(1,401,1),(1,ihypo[2],1),1],'wfz'),
#('=w', 'v1',[(1,-1,1),(1,401,1),(1,ihypo[2],1),(1,-1,25)],'v1'),
#('=w', 'v2',[(1,-1,1),(1,401,1),(1,ihypo[2],1),(1,-1,25)],'v2'),
#('=w', 'v3',[(1,-1,1),(1,401,1),(1,ihypo[2],1),(1,-1,25)],'v3'),

#('=w', 'v3',[(1,-1,1),(1,-1,1),1,(1,-1,25)],'waveatsurface_z'),

#    ( '=w', 'svm', [(),(),1,(1,-1,1)], 'sliprate'),

#    ( '=w', 'psi', [(),(),1,(1,-1,1)], 'psi'),
#    ( '=w', 'x1',  [ihypo[0]-_xoff0,(1,-1,5),(1,-1,5),1],'wavex_0'),
#    ( '=w', 'x2',  [ihypo[0]-_xoff0,(1,-1,5),(1,-1,5),1],'wavey_0'),
#    ( '=w', 'x3',  [ihypo[0]-_xoff0,(1,-1,5),(1,-1,5),1],'wavez_0'),
#    ( '=w', 'v1', [ihypo[0]-_xoff0,(1,-1,5),(1,-1,5),(1,-1,1)], 'v1_0'),
#    ( '=w', 'v2', [ihypo[0]-_xoff0,(1,-1,5),(1,-1,5),(1,-1,1)], 'v2_0'),
#    ( '=w', 'v3', [ihypo[0]-_xoff0,(1,-1,5),(1,-1,5),(1,-1,1)], 'v3_0'),    


#    ( '=w', 'x1',  [ihypo[0]-_xoff1,(1,-1,5),(1,-1,5),1],'wavex_1'),
#    ( '=w', 'x2',  [ihypo[0]-_xoff1,(1,-1,5),(1,-1,5),1],'wavey_1'),
#    ( '=w', 'x3',  [ihypo[0]-_xoff1,(1,-1,5),(1,-1,5),1],'wavez_1'),
#    ( '=w', 'v1', [ihypo[0]-_xoff1,(1,-1,5),(1,-1,5),(1,-1,1)], 'v1_1'),
#    ( '=w', 'v2', [ihypo[0]-_xoff1,(1,-1,5),(1,-1,5),(1,-1,1)], 'v2_1'),
#    ( '=w', 'v3', [ihypo[0]-_xoff1,(1,-1,5),(1,-1,5),(1,-1,1)], 'v3_1'),


#    ( '=w', 'x1',  [ihypo[0]-_xoff2,(1,-1,5),(1,-1,5),1],'wavex_2'),
#    ( '=w', 'x2',  [ihypo[0]-_xoff2,(1,-1,5),(1,-1,5),1],'wavey_2'),
#    ( '=w', 'x3',  [ihypo[0]-_xoff2,(1,-1,5),(1,-1,5),1],'wavez_2'),
#    ( '=w', 'v1', [ihypo[0]-_xoff2,(1,-1,5),(1,-1,5),(1,-1,1)], 'v1_2'),
#    ( '=w', 'v2', [ihypo[0]-_xoff2,(1,-1,5),(1,-1,5),(1,-1,1)], 'v2_2'),
#    ( '=w', 'v3', [ihypo[0]-_xoff2,(1,-1,5),(1,-1,5),(1,-1,1)], 'v3_2'),


#    ( '=w', 'x1',  [(1,-1,1),401,(1,ihypo[2],1),1],'wavexslice'),
#    ( '=w', 'x2',  [(1,-1,1),401,(1,ihypo[2],1),1],'waveyslice'),
#    ( '=w', 'x3',  [(1,-1,1),401,(1,ihypo[2],1),1],'wavezslice'),
#    ( '=w', 'v1', [(1,-1,1),401,(1,ihypo[2],1),(1,-1,25)], 'v1slice'),
#    ( '=w', 'v2', [(1,-1,1),401,(1,ihypo[2],1),(1,-1,25)], 'v2slice'),
#    ( '=w', 'v3', [(1,-1,1),401,(1,ihypo[2],1),(1,-1,25)], 'v3slice'),

#    ( '=w', 'x1',  [(),ihypo[1],(),1],'wavex_2'),
#    ( '=w', 'x2',  [(),ihypo[1],(),1],'wavey_2'),
#    ( '=w', 'x3',  [(),ihypo[1],(),1],'wavez_2'),
#    ( '=w', 'v1', [(),ihypo[1],(),(1,-1,1)], 'v1_2'),
#    ( '=w', 'v2', [(),ihypo[1],(),(1,-1,1)], 'v2_2'),
#    ( '=w', 'v3', [(),ihypo[1],(),(1,-1,1)], 'v3_2'),
]

SORDlatest.run( locals() )

