var vehicleKeys = new Array( 
     /* 0 */          'code      ', 
     /* 1 */          'type                                        ', 
     /* 2 */          'TL', 
     /* 3 */          ' q',
     /* 4 */          ' vol', 
     /* 5 */          'spd', 
     /* 6 */          '  ld', 
     /* 7 */          ' AV:', 
     /* 8 */          'ca,', 
     /* 9 */          'fp,', 
     /* A */          'rp,', 
     /* B */          'sp,', 
     /* C */          'ps,', 
     /* D */          'in,', 
     /* E */          'se', 
     /* F */          '  KCr ' );

function VEL( array )
{
   return new El( vehicleKeys, array );
}

/******************************************************************

   Installations

******************************************************************/
var installation = new Array
(
   //                 code  label          tl  q  vol  spd  ld  AV ca fp rp sp ps in se  KCR
   new VEL( new Array( 'C', 'Container ',    5, 0,   5,  0,  5,  1, 1, 1, 0, 1, 0,  1, 1, 10 )),
   new VEL( new Array( 'H', 'Habitat',       5, 0,   8,  0,  8,  3, 1, 4, 0, 4, 0,  4, 4, 10 )),
   new VEL( new Array( 'M', 'Module ',       8, 0,  25,  0, 25,  5, 4, 4, 4, 4, 0, 10, 4, 100 ))
);

var in_mission = new Array
(
   //                       code  label             tl  q  vol   spd  ld   AV ca fp rp sp ps in se    KCR
   new VEL( new Array( '(std)', '(std)',        0, 0,  0,    0,   0,   0, 0, 0, 0, 0, 0, 0, 0,     0 )),
   new VEL( new Array( 'F',   'Fuel '     ,     0, 0,  0,    0,   0,   5, 5, 0, 0, 0, 0, 5, 0,   100 )),
   //new VEL( new Array( 'L',   'Life '     ,     0, 0,  0,    0,   2,   5, 5, 0, 0, 0, 0, 5, 0,    50 )),
   new VEL( new Array( 'N',   'Science '  ,     1, 0,  4,    0,  '/2',   0, 0, 0, 0, 0, 0,10, 0,  1000 )),
   new VEL( new Array( 'R',   'Repair '   ,     0, 0,  4,    0,  '/2',   0, 0, 0, 0, 0, 0, 5, 0,   500 )),
   new VEL( new Array( 'W',   'Defense '   ,    1, 0,  4,    0,  '/2',   5, 0, 0, 0, 0, 0, 5, 0,  1000 )),
   new VEL( new Array( 'X',   'Luxury '   ,     0, 0, -1,    0,  -1,   5, 0, 0, 0, 0, 0, 5, 0,   500 ))
);


function installation_printOptions()
{
   document.writeln( ''
      + printOptions( 'stage',     'installation_recalc',  vehicle_stage )
      + printOptions( 'bulk',      'installation_recalc',  vehicle_bulk ) 
      + printOptions( 'mission',   'installation_recalc',  in_mission   )
      + printOptions( 'installation',    'installation_recalc',  installation )
      + printOptions( 'opt',       'installation_recalc',  vehicle_opt )
      + printOptions( 'opt2',      'installation_recalc',  vehicle_opt )
      + printOptions( 'end',       'installation_recalc',  vehicle_endurance )
      + printOptions( 'desc',      'installation_recalc',  vehicle_descriptors )
   );
}          

function installation_recalc( form )
{
   var stage   = vehicle_stage[ form.stage.selectedIndex ];
   var bulk    = vehicle_bulk[ form.bulk.selectedIndex ];
   var mission = in_mission[ form.mission.selectedIndex ];
   var craft   = installation[ form.installation.selectedIndex ];
   var opt     = vehicle_opt[ form.opt.selectedIndex ];
   var opt2    = vehicle_opt[ form.opt2.selectedIndex ];
   var end     = vehicle_endurance[ form.end.selectedIndex ];
   var desc    = vehicle_descriptors[ form.desc.selectedIndex ];

   var out = compose( new Array(craft, mission, bulk, stage, desc, opt, opt2, end) );
   
   form.output.value = hdr(  vehicleKeys, ' ' )
                     + prln( out, ' ' )
                     + "\n"
                     + prln( out, "\n", 2 );
}
/******************************************************************

   Ground vehicles

******************************************************************/

var ground = new Array
(
   new VEL( new Array( 'C',   'Car'      ,  0,0, 2, 0, 1,   0, 0, 0, 0, 0, 0, 0, 0,   20 )),
   new VEL( new Array( 'V',   'Van'      ,  0,0, 3, 0, 2,   0, 0, 0, 0, 0, 0, 0, 0,   30 )),
   new VEL( new Array( 'T',   'Truck'    ,  0,0, 4, 0, 3,   0, 0, 0, 0, 0, 0, 0, 0,   50 )),
   new VEL( new Array( 'H',   'Vehicle'  ,  0,0, 5, 0, 3,   0, 0, 0, 0, 0, 0, 0, 0,   60 )),
   new VEL( new Array( 'M',   'Mover'    ,  0,0, 3, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0,   50 )),
   new VEL( new Array( 'R',   'Transport',  0,0, 5, 0, 4,   0, 0, 0, 0, 0, 0, 0, 0,   40 ))
);

var gr_mission = new Array
(
   new VEL( new Array( '(std)', '(std)',     0,0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0,    0 )),
   new VEL( new Array( 'P',   'Passenger ',  0,0, 0, 0, 0,   5, 0, 0, 0, 0, 0,12, 0,   10 )),
   new VEL( new Array( 'C',   'Cargo '    ,  0,0, 0, 0, 0,   5, 0, 0, 0, 0, 0, 6, 0,   10 )),
   new VEL( new Array( 'U',   'Utility '  ,  0,0, 0, 0, 0,   5, 0, 0, 0, 0, 0, 6, 0,   10 )),
   new VEL( new Array( 'E',   'Explorer ' ,  0,0, 0, 0, 0,  20,10,10,10,10, 0,20,20,  100 ))
);

var gr_motive = new Array
(
   new VEL( new Array( 'ACV', 'Air Cushion ',8,0,  2, 6, 0,  0, 0, 0, 0, 0, 0, 0, 0,  'x2.0' )),
   new VEL( new Array( 'W',   'Wheeled '    ,6,0,  0, 5, 0,  0, 0, 0, 0, 0, 0, 0, 0,    0    )),
   new VEL( new Array( 'L',   'Lift '       ,9,0,  1, 3, 0,  0, 0, 0, 0, 0, 0, 0, 0,  'x2.0' )),
   new VEL( new Array( 'G',   'Grav '      ,10,0, -1, 5, 0,  0, 0, 0, 0, 0, 0, 0, 0,  'x3.0' )),
   new VEL( new Array( 'T',   'Tracked '    ,7,0,  2, 4, 0,  0, 0, 0, 0, 0, 0, 0, 0,  'x2.0' ))
);

function ground_printOptions()
{
   document.writeln( ''
      + printOptions( 'stage',     'ground_recalc',  vehicle_stage )
      + printOptions( 'bulk',      'ground_recalc',  vehicle_bulk ) 
      + printOptions( 'mission',   'ground_recalc',  gr_mission   )
      + printOptions( 'motive',    'ground_recalc',  gr_motive    )
      + printOptions( 'ground',    'ground_recalc',  ground )
      + printOptions( 'opt',       'ground_recalc',  vehicle_opt )
      + printOptions( 'opt2',      'ground_recalc',  vehicle_opt )
      + printOptions( 'end',       'ground_recalc',  vehicle_endurance )
      + printOptions( 'desc',      'ground_recalc',  vehicle_descriptors )
   );
}

function ground_recalc( form )
{
   var stage   = vehicle_stage[ form.stage.selectedIndex ];
   var bulk    = vehicle_bulk[ form.bulk.selectedIndex ];
   var motive  = gr_motive[ form.motive.selectedIndex ];
   var mission = gr_mission[ form.mission.selectedIndex ];
   var craft   = ground[ form.ground.selectedIndex ];
   var opt     = vehicle_opt[ form.opt.selectedIndex ];
   var opt2    = vehicle_opt[ form.opt2.selectedIndex ];
   var end     = vehicle_endurance[ form.end.selectedIndex ];
   var desc    = vehicle_descriptors[ form.desc.selectedIndex ];

   var out = compose( new Array(craft, mission, motive, bulk, stage, desc, opt, opt2, end) );
   
   form.output.value = hdr(  vehicleKeys, ' ' )
                     + prln( out, ' ' )
                     + "\n"
                     + prln( out, "\n", 2 );
}
/******************************************************************

   Flyers

******************************************************************/

var flyers = new Array
(
   new VEL( new Array( '(F)', 'Flyer',       0, 0,   0,   0,    0,    0, 0,  0, 0,  0, 0,  0, 0,    0 ) ),
   new VEL( new Array( '(G)', 'Glider',      0, 0,   0,   0,    0,    0, 0,  0, 0,  0, 0,  0, 0,    0 ) ),
   new VEL( new Array( '(B)', 'Balloon',     0, 0,   0,   0,    0,    0, 0,  0, 0,  0, 0,  0, 0,    0 ) )
);

var f_mission = new Array
(
   new VEL( new Array( 'A', 'Combat ',       2, 0, 'x2.0', 1, 'x2.0', 20, 0, 20, 0, 20, 0, 10, 1, 'x3.0' )),
   new VEL( new Array( 'B', 'Bomber ',       1, 0, 'x3.0', 0, 'x3.0', 10, 0, 20, 0, 20, 0, 10, 1, 'x2.0' )),
   new VEL( new Array( 'C', 'Cargo ',        0, 0, 'x4.0', 0, 'x2.0',  5, 0, 20, 0, 20, 0, 10, 1, 'x1.0' )),
   new VEL( new Array( 'P', 'Protector ',    1, 0, 'x2.0', 1, 'x1.0', 10, 0, 20, 0, 20, 0, 10, 1, 'x3.0' )),
   new VEL( new Array( 'S', 'Scientific ',  -1, 0, 'x4.0', 0, 'x2.0',  5, 0, 20, 0, 20, 0, 10, 1, 'x2.0' )),
   new VEL( new Array( 'U', 'Utility ',      0, 0, 'x1.0', 0, 'x3.0',  0, 0, 20, 0, 20, 0, 10, 1, 'x10.0' ))
);

var f_motive = new Array
(
   new VEL( new Array( 'W',  'Winged ',   7,   0,   10, 8, 2,     0,0,0,0,0,0,0,0,    300 )), 
   new VEL( new Array( 'R',  'Rotor ',    8,   0,   10, 7, 0.5,   0,0,0,0,0,0,0,0,    400 )), 
   new VEL( new Array( 'F',  'Flapper ', 10,   0,   10, 6, 0.5,   0,0,0,0,0,0,0,0,    500 )), 
   new VEL( new Array( 'LTA','LTA ',      6,   0,   40, 5, 10,    0,0,0,0,0,0,0,0,    600 )), 
   new VEL( new Array( 'L',  'Lifter ',   9,   0,    8, 2, 1,     0,0,0,0,0,0,0,0,    600 )), 
   new VEL( new Array( 'G',  'Grav ',    10,   0,    9, 4, 3,     0,0,0,0,0,0,0,0,    700 ))  
);

function flyer_printOptions()
{
   document.writeln( ''
      + printOptions( 'stage',     'flyer_recalc',  vehicle_stage )
      + printOptions( 'bulk',      'flyer_recalc',  vehicle_bulk ) 
      + printOptions( 'mission',   'flyer_recalc',  f_mission   )
      + printOptions( 'motive',    'flyer_recalc',  f_motive    )
      + printOptions( 'flyer',     'flyer_recalc',  flyers )
      + printOptions( 'opt',       'flyer_recalc',  vehicle_opt )
      + printOptions( 'opt2',      'flyer_recalc',  vehicle_opt )
      + printOptions( 'end',       'flyer_recalc',  vehicle_endurance )
      + printOptions( 'desc',      'flyer_recalc',  vehicle_descriptors )
   );
}

function flyer_recalc( form )
{
   var stage   = vehicle_stage[ form.stage.selectedIndex ];
   var bulk    = vehicle_bulk[ form.bulk.selectedIndex ];
   var motive  = f_motive[ form.motive.selectedIndex ];
   var mission = f_mission[ form.mission.selectedIndex ];
   var craft   = flyers[ form.flyer.selectedIndex ];
   var opt     = vehicle_opt[ form.opt.selectedIndex ];
   var opt2    = vehicle_opt[ form.opt2.selectedIndex ];
   var end     = vehicle_endurance[ form.end.selectedIndex ];
   var desc    = vehicle_descriptors[ form.desc.selectedIndex ];

   var out = compose( new Array(craft, mission, motive, bulk, stage, desc, opt, opt2, end) );
   
   form.output.value = hdr(  vehicleKeys, ' ' )
                     + prln( out, ' ' )
                     + "\n"
                     + prln( out, "\n", 2 );
}


/******************************************************************

   Watercraft

******************************************************************/

var watercraft = new Array
(
   new VEL( new Array( 'Sh', 'Ship',       5, 0, 1000, 4, 600,  10, 0, 0, 0, 0, 0, 0, 0,1000 ) ), 
   new VEL( new Array( 'Sb', 'Sub',        6, 0, 100,  4,  60,  20, 0, 0, 0, 0, 0, 0,20,1000 ) ), 
   new VEL( new Array( 'Bt', 'Boat',       5, 0, 10,   4,   6,   5, 0, 0, 0, 0, 0, 0, 0,100 ) ),

   new VEL( new Array( 'GSh', 'Grav Ship',10, 0, 200,  4, 600,  10, 0, 0, 0, 0, 0, 0, 0,2000 ) ), 
   new VEL( new Array( 'GSb', 'Grav Sub', 10, 0, 20,   4,  60,  20, 0, 0, 0, 0, 0, 0,20,2000 ) ), 
   new VEL( new Array( 'GBt', 'Grav Boat',10, 0, 2,    4,   6,   5, 0, 0, 0, 0, 0, 0, 0,200 ) )
);

var w_mission = new Array
(
   new VEL( new Array( 'C', 'Cargo ',       0, 0, 0,   -1, 0,     0, 0, 0, 0, 0, 0, 0, 0, 0 ) ),
   new VEL( new Array( 'P', 'Patrol ',      2, 0, 0,   +1, 0,  'x2', 0, 0, 0, 0, 0, 0, 0, 0 ) ),
   new VEL( new Array( 'E', 'Explorer ',    2, 0, 0,    0, 0,     0, 0, 0, 0, 0, 0, 'x2', 0, 0 ) ),
   new VEL( new Array( 'T', 'Transport ',   0, 0, 0,    0, 0,     0, 0, 0, 0, 0, 0, 0, 0, 0 ) )
);

var w_motive = new Array
(
   new VEL( new Array( 'S', 'Standard',     0, 0, 0,    0, 0,     0, 0, 0, 0, 0, 0, 0, 0, 0 ) ),
   new VEL( new Array( 'U', 'Unpowered',   -3, 0, 0,    0, 0,     0, 0, 0, 0, 0, 0, 0, 0, 'x0.5' ) ),
   new VEL( new Array( 'H', 'Hovercraft',   6, 0, 'x2.0', "=5", 3,     0, 0, 0, 0, 0, 0, 0, 0, 200 ) )
);

function watercraft_printOptions()
{
   document.writeln( ''
      + printOptions( 'stage',     'watercraft_recalc',  vehicle_stage )
      + printOptions( 'bulk',      'watercraft_recalc',  vehicle_bulk ) 
      + printOptions( 'mission',   'watercraft_recalc',  w_mission    )
      + printOptions( 'motive',    'watercraft_recalc',  w_motive    )
      + printOptions( 'watercraft','watercraft_recalc',  watercraft   )
      + printOptions( 'opt',       'watercraft_recalc',  vehicle_opt )
      + printOptions( 'opt2',      'watercraft_recalc',  vehicle_opt )
      + printOptions( 'end',       'watercraft_recalc',  vehicle_endurance )
      + printOptions( 'desc',      'watercraft_recalc',  vehicle_descriptors )
   );
}

function watercraft_recalc( form )
{
   var stage   = vehicle_stage[ form.stage.selectedIndex ];
   var bulk    = vehicle_bulk[ form.bulk.selectedIndex ];
   var mission = w_mission[ form.mission.selectedIndex ];
   var motive  = w_motive[ form.motive.selectedIndex ];
   var craft   = watercraft[ form.watercraft.selectedIndex ];
   var opt     = vehicle_opt[ form.opt.selectedIndex ];
   var opt2     = vehicle_opt[ form.opt2.selectedIndex ];
   var end     = vehicle_endurance[ form.end.selectedIndex ];
   var desc    = vehicle_descriptors[ form.desc.selectedIndex ];
   
   var out = compose( new Array(craft, mission, bulk, stage, desc, opt, opt2, end) );
   
   form.output.value = hdr(  vehicleKeys, ' ' )
                     + prln( out, ' ' )
                     + "\n"
                     + prln( out, "\n", 2 );
}

/******************************************************************

   Military vehicles

******************************************************************/

var military = new Array
(
//                    code   type               TL q    v spd ld AV  cafprpsppsinse        KCr
   new VEL( new Array( 'T', 'Tank',              0,0,   5, 3, 0, 50, 10,10,10,20, 0,20,20, 700 )),
   new VEL( new Array( 'C', 'Carrier',           0,0,   4, 4, 2, 40, 10,10,10,20, 0,20,20, 500 )),
   new VEL( new Array( 'V', 'Vehicle',           0,0,   2, 5, 1, 30, 10,10,10,20, 0,20,20, 300 ))
);

var m_mission = new Array
(
//                    code   type               TL q    v spd ld AV  cafprpsppsinse        KCr
   new VEL( new Array( '(S)',  '(Standard)',     0,0,   0, 0, 0,  0,  0, 0, 0, 0, 0, 0, 0,   0 )),
   new VEL( new Array( 'W', 'Weapon ',           0,0,   2, 0, 0,  0,  0, 0, 0, 0, 0, 0, 0, 100 )),
   new VEL( new Array( 'T', 'Troop ',            0,0,   1, 0, 0,  0,  0, 0, 0, 0, 0, 0, 0,   0 )),
   new VEL( new Array( 'S', 'Supply ',           0,0,   3,-1, 1,-10,  0, 0, 0, 0, 0, 0, 0,   0 )),
   new VEL( new Array( 'R', 'Recon ',            0,0,  -1, 1, 0,-10,  0, 0, 0, 0, 0, 0, 0, 100 ))
);

var m_motive = new Array
(
//                    code    type              TL  q   v   spd   ld AV  cafprpsppsinse        KCr
   new VEL( new Array( 'W',   'Wheeled ',        6, 0,  0,  5.0,  0,  0,  0, 0, 0, 0, 0, 0, 0,  'x1.0' )),
   new VEL( new Array( 'T',   'Tracked ',        7, 0,  2,  4.0,  0,  0,  0, 0, 0, 0, 0, 0, 0,  'x2.0' )),
   new VEL( new Array( 'ACV', 'Air Cushion ',    8, 0,  2,  6.0,  0,  0,  0, 0, 0, 0, 0, 0, 0,  'x2.0' )),
   new VEL( new Array( 'Z',   'Lift ',           9, 0,  1,  3.0,  0,  0,  0, 0, 0, 0, 0, 0, 0,  'x2.0' )),
   new VEL( new Array( 'G',   'Grav ',           10,0, -1,  5.0,  0,  0,  0, 0, 0, 0, 0, 0, 0,  'x3.0' )),
   new VEL( new Array( 'L',   'Legged ',         10,0,  1,  2.0,  0,  0,  0, 0, 0, 0, 0, 0, 0,  'x1.0' ))
);

function mil_printOptions()
{
   document.writeln( ''
      + printOptions( 'stage',     'mil_recalc',  vehicle_stage )
      + printOptions( 'bulk',      'mil_recalc',  vehicle_bulk ) 
      + printOptions( 'mission',   'mil_recalc',  m_mission    )
      + printOptions( 'motive',    'mil_recalc',  m_motive    )
      + printOptions( 'military',  'mil_recalc',  military   )
      + printOptions( 'opt',       'mil_recalc',  vehicle_opt )
      + printOptions( 'opt2',      'mil_recalc',  vehicle_opt )
      + printOptions( 'end',       'mil_recalc',  vehicle_endurance )
      + printOptions( 'desc',      'mil_recalc',  vehicle_descriptors )
   );
}

function mil_recalc( form )
{
   var stage   = vehicle_stage[ form.stage.selectedIndex ];
   var bulk    = vehicle_bulk[ form.bulk.selectedIndex ];
   var mission = m_mission[ form.mission.selectedIndex ];
   var motive  = m_motive[ form.motive.selectedIndex ];
   var craft   = military[ form.military.selectedIndex ];
   var opt     = vehicle_opt[ form.opt.selectedIndex ];
   var opt2     = vehicle_opt[ form.opt2.selectedIndex ];
   var end     = vehicle_endurance[ form.end.selectedIndex ];
   var desc    = vehicle_descriptors[ form.desc.selectedIndex ];
   
   var out = compose( new Array(craft, mission, motive, bulk, stage, desc, opt, opt2, end) );
   
   form.output.value = hdr(  vehicleKeys, ' ' )
                     + prln( out, ' ' )
                     + "\n"
                     + prln( out, "\n", 2 );
}


/******************************************************************

   Smallcraft

******************************************************************/

var smallcraft = new Array
(
   // ALL of these have been re-done
//                          code  type       TL q   V  Gs  Ld  AV  Ca  Fl  Ra  So  Ps  In  Se   MCr
   new VEL( new Array( 'QP', 'Pod'    , 13,0,  5,  2,  1, 20, 10, 20, 20, 10, 00, 20, 20,  5000 )), 
   new VEL( new Array( 'QF', 'Fighter', 11,0, 10,  6,  1, 40, 10, 10, 10, 10, 00, 10, 10,  9000 )), 
   new VEL( new Array( 'QL', 'Launch' , 12,0, 20,  3, 10, 20, 10, 10, 10, 10, 00, 10, 10,  8000 )), 
   new VEL( new Array( 'QB', 'Boat'   , 12,0, 30,  5, 19, 30, 10, 10, 10, 10, 00, 10, 10,  7000 )), 
   new VEL( new Array( 'QN', 'Pinnace', 14,0, 40,  4, 25, 30, 10, 10, 10, 10, 00, 10, 10,  9000 )), 
   new VEL( new Array( 'QC', 'Cutter' , 12,0, 50,  4, 31, 40, 10, 10, 20, 10, 00, 10, 10, 13000 )), 
   new VEL( new Array( 'QD', 'Lander' , 10,0, 60,  1, 24, 20, 20, 20, 20, 10, 00, 20, 20, 10000 )), 
   new VEL( new Array( 'QS', 'Shuttle', 11,0, 70,  4, 42, 20, 10, 10, 20, 10, 00, 20, 10, 11000 )), 
   new VEL( new Array( 'QK', 'Picket' , 13,0, 80,  6, 20, 30, 10, 10, 10, 10, 00, 10, 20, 10000 )) 
);

var s_mission = new Array
(
   //  ALL of these have been re-done
//                          code  type          TL q  V      Gs     Ld  AV  Ca  Fl  Ra  So  Ps  In  Se   MCr   
   new VEL( new Array( '(std)', '(Std)',    0,0, 0,     0,     0 ,  0,  0,  0,  0,  0,  0,  0,  0,  0 )),
   new VEL( new Array( 'U',  'Utility ',   -1,0, 5,    -1,     5 ,  0,  0,  0,  0,  0,  0,  0,  0,  0 )),
   new VEL( new Array( 'Lr', 'Long Range ', 0,0, 0,     0,   -10 ,  0,  0,  0,  0,  0,  0,  0,  0,  1 )),
   new VEL( new Array( 'Li', 'Life ',      -1,0, 0,    -1,     3 ,  0,  0,  0,  0,  0,  0,  0,  0, -1 )),
   new VEL( new Array( 'F',  'Fast ',       1,0, 0,     1,    -5 ,  0,  0,  0,  0,  0,  0,  0,  0,  1 )),
   new VEL( new Array( 'S',  'Slow ',      -1,0, 0,    -2,     5 ,  0,  0,  0,  0,  0,  0,  0,  0, -1 )),
   new VEL( new Array( 'P',  'Passenger ',  0,0,20,     0,    15 ,  0,  0,  0,  0,  0,  0,  0,  0,  4 )),
   new VEL( new Array( 'C',  'Cargo ',     -1,0,25,    -1,    25 ,-10,  0,  0,  0,  0,  0,-10,  0,  5 )),
   new VEL( new Array( 'T',  'Tanker ',    -1,0,'x2',  -1,  'x2' ,-10,  0,  0,  0,  0,  0,-10,  0, 'x2.0' )),
   new VEL( new Array( 'A',  'Attack ',     1,0,10,     1,     0 , 50, 10, 10, 20, 10,  0, 10, 10, 'x4.0' )),
//   new VEL( new Array( 'D',  'Defense* ',   1,0,'x1.5', 0,     0 , 60, 10, 10, 20, 10,  0, 10, 10, 'x4.0' )),
   new VEL( new Array( 'R',  'Recon ',      1,0, 0,     1,  'x0.5', 20, 10, 10, 20, 10,  0, 10, 10, 'x2.0' ))
);

var s_drive = new Array
(
//                          code  type          TL q  V      Gs     Ld  AV  Ca  Fl  Ra  So  Ps  In  Se   MCr   
   new VEL( new Array( '(G)', '(G-drive)',  0,0, 0,     0,     0 ,  0,  0,  0,  0,  0,  0,  0,  0,  0 )),
   new VEL( new Array( 'M', '(M-drive)',  0,0, 0,     0,     5 ,  0,  0,  0,  0,  0,  0,  0,  0,  'x2.0' ))
);

function sc_printOptions()
{
   document.writeln( ''
//      + printOptions( 'stage',     'sc_recalc',  vehicle_stage )
      + printOptions( 'bulk',      'sc_recalc',  vehicle_bulk ) 
      + printOptions( 'mission',   'sc_recalc',  s_mission    )
      + printOptions( 'mission2',   'sc_recalc',  s_mission    )
      + printOptions( 'drive',     'sc_recalc',  s_drive )
      + printOptions( 'sc',        'sc_recalc',  smallcraft   )
//      + printOptions( 'opt',       'sc_recalc',  vehicle_opt )
      + printOptions( 'end',       'sc_recalc',  vehicle_endurance )
   );
}

function sc_recalc( form )
{
//   var stage   = vehicle_stage[ form.stage.selectedIndex ];
   var bulk    = vehicle_bulk[ form.bulk.selectedIndex ];
   var drive   = s_drive[ form.drive.selectedIndex ];
   var mission = s_mission[ form.mission.selectedIndex ];
   var mission2 = s_mission[ form.mission2.selectedIndex ];
   var craft   = smallcraft[ form.sc.selectedIndex ];
//   var opt     = vehicle_opt[ form.opt.selectedIndex ];
   var end     = vehicle_endurance[ form.end.selectedIndex ];
   
   var out = compose( new Array(craft, mission, mission2, drive, bulk, end) );
   
   form.output.value = hdr(  vehicleKeys, ' ' )
                     + prln( out, ' ' )
                     + "\n"
                     + prln( out, "\n", 2 );

}

/******************************************************************

   Common

******************************************************************/

var vehicle_bulk = new Array
(
//                     code        type     TL  q   vol    spd  ld      AV  cafprpsppsinse  KCr
   new VEL( new Array( '(M)',  '(Medium) ',  0, 0,  'x1',   0,  0,       0  ,0,0,0,0,0,0,0, 0 ) ),
   new VEL( new Array( 'Vl',         'Vl ', -1, 0,  'x0.33',1, -2,  'x0.33' ,0,0,0,0,0,0,0, 'x0.33' ) ),
   new VEL( new Array( 'L',          'Lt ', -1, 0,  'x0.5', 1, -1,   'x0.5' ,0,0,0,0,0,0,0, 'x0.5' ) ),
   new VEL( new Array( 'H',          'Hv ',  1, 0,  'x2',  -1,  2,   'x2.0' ,0,0,0,0,0,0,0, 'x3.0' ) ),
   new VEL( new Array( 'Vh',         'Vh ',  2, 0,  'x3',  -2,  3,   'x3.0' ,0,0,0,0,0,0,0, 'x9.0' ) )
);

var vehicle_stage = new Array
(
//                     code        type        TL  q  vol    spd  ld    AV  cafprpsppsinse  KCr
   new VEL( new Array( '(S)', '(Standard)',     0, 0,  0,      0,  0,    0,0,0,0,  0,0,0,0,  0 )),                
   new VEL( new Array( '(F)', 'Fossil ',       -2, 0,  2,      0,  0,  -10,0,0,0,-10,0,0,0,  0 )),
   new VEL( new Array( '(P)', 'PowerCell ',    -1, 0,  1,     -2, -2,   -5,0,0,0, -5,0,0,0,  10)),
   new VEL( new Array( '(R)', 'Renewable ',    -1, 0,  1,     -1, -1,    0,0,0,0,  0,0,0,0,  20)),      
// new VEL( new Array( 'Exp', 'Experimental ', -3, 0,  1,     -1, -1,    0,0,0,0,  0,0,0,0,  'x10.0')),
   new VEL( new Array( 'Pro', 'Prototype ',    -2, 0,  1,     -1, -1,    0,0,0,0,  0,0,0,0,  20)),
   new VEL( new Array( 'E',   'Early ',        -1, 0,  1,      0,  0,  -10,0,0,0,-10,0,0,0,  10)),
// new VEL( new Array( 'B',   'Basic ',         0, 0,  0,      0,  0,    0,0,0,0,  0,0,0,0,  'x0.5')),
   new VEL( new Array( 'I',   'Improved ',      1, 0, -1,      0,  0,   10,0,0,0, 10,0,0,0,  20)),
// new VEL( new Array( 'M',   'Modified ',      2, 0,  0,      1,  0,    0,0,0,0,  0,0,0,0,  'x0.5')),
   new VEL( new Array( 'A',   'Advanced ',      3, 0, -2,      1,  1,   20,0,0,0, 20,0,0,0,  40))
// new VEL( new Array( 'U',   'Ultimate',       4, 0, -2,      1,  1,   20,0,0,0, 20,0,0,0,  'x2.0'))   
);


var vehicle_opt = new Array
(
   new VEL( new Array( '(none)',   '(No options)',    0,0,  0,      0,  0,    0,0,0,0,  0,0,0,0,  0   )),
   new VEL( new Array( 'HP',       '(High Powered) ', 1,0,  1,      1, -1,    0,0,0,0,  0,0,0,0,  100 )),
   new VEL( new Array( 'Sl',       '(Slave) ',        1,0, -1,      0,  0,    0,0,0,0,  0,0,0,0,  10  )),
   new VEL( new Array( 'Re',       '(Remote) ',       1,0, -2,      0,  0,    0,0,0,0,  0,0,0,0,  20  )),
   new VEL( new Array( 'Wpn',      '(Weapon Mount) ', 0,0,  0,      0, -1,    0,0,0,0,  0,0,0,0,  0   )),
   new VEL( new Array( 'Lux',      'Luxury ',         0,0,  0,      0,  0,    0,0,0,0,  0,0,0,0,  'x2.0' )),
   new VEL( new Array( 'F',        '(Fast) ',         1,0,  1,      1, -2,    0,0,0,0,  0,0,0,0,  30  )),
   new VEL( new Array( 'P',        '(Passenger Module) ', 0,0,  0,      0, -3,    0,0,0,0,  0,0,0,0,  100  )),
   new VEL( new Array( 'C',        '(Cargo Module) ',     0,0,  1,     -1,  1,    0,0,0,0,  0,0,0,0,  20  )),
   new VEL( new Array( 'R',        '(Redundancy) ',       1,0,  1,      0,  0,    0,0,0,0,  0,0,0,0,  60  )),

   new VEL( new Array( '(go)',     '(Offroad) ',      0,0,  0,      0,  0,    0,0,0,0,  0,0,0,0,  30 )),
   new VEL( new Array( '(gm)',     '(Mole) ',         1,0, 'x3.0', "=1",  0,  0,0,0,0,  0,0,0,0,  400 )),
   new VEL( new Array( '(wh)',     '(Water - Hydrofoils) ',  1,0, 1, 1,  0,   0,0,0,0,  0,0,0,0,  30 )),

   new VEL( new Array( '(f1)',     '(Flyer - Stubs) ', 0,0,  0,  0,  0,   0,0,0,0,  0,0,0,0,  20 )),
   new VEL( new Array( 'Vtol',     '(Flyer - VTOL) ',  0,0, -1, -2,  0,   0,0,0,0,  0,0,0,0,  100 )),
   new VEL( new Array( 'Stol',     '(Flyer - STOL) ',  0,0,  0, -1,  0,   0,0,0,0,  0,0,0,0,  50 )),
   new VEL( new Array( 'Lift',     '(Flyer - Lift Body) ',  0,0,    4,  1, 'x2.0',   0,0,0,0,  0,0,0,0,  200 )),
   new VEL( new Array( '(f5)',     '(Flyer - Wings 1) ',  0,0,  'x2.0', 1,     0,    0,0,0,0,  0,0,0,0,  100 )),
   new VEL( new Array( '(f6)',     '(Flyer - Wings 2) ',  0,0,  'x3.0', 2, 'x2.0',   0,0,0,0,  0,0,0,0,  200 )),
   new VEL( new Array( '(f7)',     '(Flyer - Wings 3) ',  0,0,  'x4.0', 3, 'x3.0',   0,0,0,0,  0,0,0,0,  300 )),
   new VEL( new Array( '(f8)',     '(Flyer - Float Landers) ',  0,0,  -1, -1,   0,   0,0,0,0,  0,0,0,0,  100 )),
   new VEL( new Array( '(f9)',     '(Flyer - Fuel Nipple) ',    1,0,   0,  0,  -1,   0,0,0,0,  0,0,0,0,  100 ))
  
);

var vehicle_endurance = new Array
(
   new VEL( new Array( '(H)',   '(Hours) ',       0,0,  0,                0,  0,    0,0,0,0,  0,0,0,0,  0  )),
   new VEL( new Array( '(D)',   '(Days) ',        1,0,  '$speed x 1',     0,  0,    0,0,0,0,  0,0,0,0,  20  )),
   new VEL( new Array( '(W)',   '(Weeks) ',       2,0,  '$speed x 2',     0,  0,    0,0,0,0,  0,0,0,0,  50 )),
   new VEL( new Array( '(LR)',  '(Months) ',      3,0,  '$speed x 3',     0,  0,    0,0,0,0,  0,0,0,0,  100 )),
   new VEL( new Array( '(VLR)', '(Year) ',        4,0,  '$speed x 4',     0,  0,    0,0,0,0,  0,0,0,0,  400 ))
);

var vehicle_descriptors = new Array // environmental descriptors
(
   new VEL( new Array( 'O',   'Open ',          -2,0, 0,      0,  0,    0, 0, 0, 0,  0,0, 0, 0,  0 )),
   new VEL( new Array( 'E',   'Enclosed ',      -1,0, 0,      0,  0,    4, 0, 4, 0,  4,0,12, 0,  0 )),
   new VEL( new Array( 'S',   '(Sealed) ',       0,0, 0,      0,  0,    6, 2, 6, 0,  8,0,16,20,  2 )),
   new VEL( new Array( 'D',   '(DoubleSealed) ', 0,0, 1,      0,  0,    8, 4, 6, 0, 12,0,30,20,  5 )),
   new VEL( new Array( 'I',   '(Insulated) ',    0,0, 0,      0,  0,    8, 4, 6, 0, 12,0,30,20, 10 )), 
   new VEL( new Array( 'P',   '(Protected) ',    1,0, 1,      0,  0,   10,10,10,10, 12,0,10,20, 20 )),
   new VEL( new Array( 'A',   'Armored ',        2,0, 1,      0,  0,   20,10,10,10, 12,0,20,20, 30 )),
   new VEL( new Array( 'U',   'UpArmored ',      3,0, 2,      0,  0,   30,20,20,20, 20,0,30,20, 40 )),
   new VEL( new Array( 'Alt', 'AltArmored ',     3,0, 2,      0,  0,   60,20,30,30, 30,0,30,30, 50 ))
);
