from collections import defaultdict

def _zero_tuple(*args):
    return (0,0,0,0,0)

# Energies of atoms with FC. Is LUT[basis][element][FC]
atom_enes = {'def2svpd'   :{'H' : {-1 : 0.02013,
                                    0 : 0.00000,
                                    1 : 0.49928,
                                    },
                            'C' : {-4 : 1.45670,
                                   -3 : 0.66591,
                                   -2 : 0.20712,
                                   -1 :-0.07677,
                                    0 :-0.05938,
                                    1 : 0.34948,
                                    2 : 1.24107,
                                    3 : 2.98409,
                                    4 : 5.32103,
                                    },
                            'N' : {-3 : 0.90604,
                                   -2 : 0.33772,
                                   -1 :-0.02650,
                                    0 :-0.10641,
                                    1 : 0.42292,
                                    2 : 1.50554,
                                    3 : 3.24192,
                                    4 : 6.06052,
                                    5 : 9.61128,
                                    },
                            'O' : {-2 : 0.11254,
                                   -1 :-0.12968,
                                    0 :-0.08409,
                                    1 : 0.40147,
                                    2 : 1.68570,
                                    3 : 3.69651,
                                    4 : 6.52685,
                                    5 :10.67027,
                                    6 :15.68525,
                                    },
                            'F' : {-1 :-0.12113,
                                    0 : 0.00000,
                                    1 : 0.63130,
                                    2 : 1.89498,
                                    3 : 4.19052,
                                    4 : 7.38363,
                                    5 :11.55460,
                                    6 :17.27203,
                                    7 :24.00196,
                                    },
                            'P' : {-3 : 0.67413,
                                   -2 : 0.21734,
                                   -1 :-0.04018,
                                    0 :-0.06960,
                                    1 : 0.30853,
                                    2 : 1.02731,
                                    3 : 2.12335,
                                    4 : 3.99512,
                                    5 : 6.35594,
                                    },
                            'S' : {-2 : 0.03364,
                                   -1 :-0.11824,
                                    0 :-0.05233,
                                    1 : 0.30977,
                                    2 : 1.16010,
                                    3 : 2.42590,
                                    4 : 4.14584,
                                    5 : 6.78903,
                                    6 : 9.98929,
                                    },
                            'Cl': {-1 :-0.12658,
                                    0 : 0.00000,
                                    1 : 0.46359,
                                    2 : 1.31675,
                                    3 : 2.76026,
                                    4 : 4.69375,
                                    5 : 7.15408,
                                    6 :10.68369,
                                    7 :14.83826,
                                    },
                            'Br': {-1 :-0.12165,
                                    0 : 0.00000,
                                    1 : 0.42202,
                                    2 : 1.18501,
                                    3 : 2.46653,
                                    4 : 4.16950,
                                    5 : 6.32020,
                                    6 : 9.45716,
                                    7 :13.14507,
                                    },
                            },
              'def2tzvppd' :{'H' : {-1 :-0.00264,
                                     0 : 0.00000,
                                     1 : 0.49981,
                                     },
                             'C' : {-4 : 1.10560,
                                    -3 : 0.48600,
                                    -2 : 0.12642,
                                    -1 :-0.09020,
                                     0 :-0.05385,
                                     1 : 0.35759,
                                     2 : 1.24978,
                                     3 : 3.00539,
                                     4 : 5.37111,
                                     },
                             'N' : {-3 : 0.70853,
                                    -2 : 0.20738,
                                    -1 :-0.06710,
                                     0 :-0.10055,
                                     1 : 0.43125,
                                     2 : 1.51559,
                                     3 : 3.25361,
                                     4 : 6.09490,
                                     5 : 9.68634,
                                     },
                             'O' : {-2 : 0.09397,
                                    -1 :-0.12915,
                                     0 :-0.08232,
                                     1 : 0.40942,
                                     2 : 1.69748,
                                     3 : 3.71155,
                                     4 : 6.54831,
                                     5 :10.72593,
                                     6 :15.79333,
                                     },
                             'F' : {-1 :-0.11934,
                                     0 : 0.00000,
                                     1 : 0.63230,
                                     2 : 1.90703,
                                     3 : 4.20886,
                                     4 : 7.40644,
                                     5 :11.59413,
                                     6 :17.35880,
                                     7 :24.15246,
                                     },
                             'P' : {-3 : 0.47698,
                                    -2 : 0.11858,
                                    -1 :-0.07367,
                                     0 :-0.06395,
                                     1 : 0.32033,
                                     2 : 1.04397,
                                     3 : 2.14834,
                                     4 : 4.03146,
                                     5 : 6.41082,
                                     },
                             'S' : {-2 : 0.02470,
                                    -1 :-0.12008,
                                     0 :-0.05080,
                                     1 : 0.32100,
                                     2 : 1.17760,
                                     3 : 2.45359,
                                     4 : 4.18644,
                                     5 : 6.84375,
                                     6 :10.06529,
                                     },
                             'Cl': {-1 :-0.12662,
                                     0 : 0.00000,
                                     1 : 0.46802,
                                     2 : 1.33168,
                                     3 : 2.78608,
                                     4 : 4.73544,
                                     5 : 7.21469,
                                     6 :10.76125,
                                     7 :14.93864,
                                     },
                             'Br': {-1 :-0.12263,
                                     0 : 0.00000,
                                     1 : 0.42725,
                                     2 : 1.20276,
                                     3 : 2.49427,
                                     4 : 4.20793,
                                     5 : 6.36814,
                                     6 : 9.51383,
                                     7 :13.21067,
                                     },
                             },
              'def2qzvppd' :{'H' : {-1 :-0.01452,
                                     0 : 0.00000,
                                     1 : 0.49998,
                                     },
                             'C' : {-4 : 0.95401,
                                    -3 : 0.41317,
                                    -2 : 0.09491,
                                    -1 :-0.09481,
                                     0 :-0.05259,
                                     1 : 0.36032,
                                     2 : 1.25464,
                                     3 : 3.01202,
                                     4 : 5.37919,
                                     },
                             'N' : {-3 : 0.62180,
                                    -2 : 0.15774,
                                    -1 :-0.08014,
                                     0 :-0.09900,
                                     1 : 0.43459,
                                     2 : 1.52122,
                                     3 : 3.26231,
                                     4 : 6.10582,
                                     5 : 9.69901,
                                     },
                             'O' : {-2 : 0.08240,
                                    -1 :-0.13113,
                                     0 :-0.08154,
                                     1 : 0.41510,
                                     2 : 1.70556,
                                     3 : 3.72277,
                                     4 : 6.56367,
                                     5 :10.74402,
                                     6 :15.81352,
                                     },
                             'F' : {-1 :-0.12181,
                                     0 : 0.00000,
                                     1 : 0.63696,
                                     2 : 1.91760,
                                     3 : 4.22246,
                                     4 : 7.42403,
                                     5 :11.61672,
                                     6 :17.38448,
                                     7 :24.18060,
                                     },
                             'P' : {-3 : 0.38689,
                                    -2 : 0.07921,
                                    -1 :-0.08207,
                                     0 :-0.06201,
                                     1 : 0.32391,
                                     2 : 1.04906,
                                     3 : 2.15486,
                                     4 : 4.03880,
                                     5 : 6.42020,
                                     },
                             'S' : {-2 : 0.01738,
                                    -1 :-0.12302,
                                     0 :-0.04975,
                                     1 : 0.32706,
                                     2 : 1.18565,
                                     3 : 2.46357,
                                     4 : 4.19792,
                                     5 : 6.85621,
                                     6 :10.08058,
                                     },
                             'Cl': {-1 :-0.13066,
                                     0 : 0.00000,
                                     1 : 0.47338,
                                     2 : 1.34288,
                                     3 : 2.79972,
                                     4 : 4.75117,
                                     5 : 7.23181,
                                     6 :10.77961,
                                     7 :14.96077,
                                     },
                             'Br': {-1 :-0.12670,
                                     0 : 0.00000,
                                     1 : 0.43337,
                                     2 : 1.21598,
                                     3 : 2.51151,
                                     4 : 4.22996,
                                     5 : 6.39599,
                                     6 : 9.55670,
                                     7 :13.27628,
                                     },
                             },
                  }

# Neutral bond energies. Is: LUT[basis][(element,element,order)][bsse]
bond_enes = {'def2svpd'  :{('C', 'C', 1)  : (-0.15291, -0.14485),
                                ('C', 'C', 2)  : (-0.27810, -0.27090),
                                ('C', 'C', 3)  : (-0.40270, -0.39622),
                                ('C', 'H', 1)  : (-0.17404, -0.17145),
                                ('C', 'N', 1)  : (-0.14340, -0.13471),
                                ('C', 'N', 2)  : (-0.25116, -0.24229),
                                ('C', 'N', 3)  : (-0.36505, -0.35592),
                                ('C', 'O', 1)  : (-0.15198, -0.14347),
                                ('C', 'O', 2)  : (-0.27907, -0.26999),
                                ('C', 'P', 1)  : (-0.11521, -0.10658),
                                ('C', 'P', 2)  : (-0.18584, -0.17688),
                                ('C', 'P', 3)  : (-0.26547, -0.25695),
                                ('C', 'S', 1)  : (-0.11820, -0.10833),
                                ('C', 'S', 2)  : (-0.19788, -0.18802),
                                ('H', 'N', 1)  : (-0.17752, -0.17393),
                                ('H', 'O', 1)  : (-0.19299, -0.18879),
                                ('H', 'P', 1)  : (-0.13348, -0.12958),
                                ('H', 'S', 1)  : (-0.14536, -0.14091),
                                ('N', 'N', 1)  : (-0.11113, -0.10223),
                                ('N', 'N', 2)  : (-0.19335, -0.18375),
                                ('N', 'N', 3)  : (-0.33520, -0.32536),
                                ('N', 'O', 1)  : (-0.10397, -0.09553),
                                ('N', 'O', 2)  : (-0.17890, -0.16797),
                                ('N', 'P', 1)  : (-0.11862, -0.10894),
                                ('N', 'P', 2)  : (-0.15815, -0.14858),
                                ('N', 'P', 3)  : (-0.20025, -0.19063),
                                ('N', 'S', 1)  : (-0.10161, -0.09117),
                                ('N', 'S', 2)  : (-0.13377, -0.12430),
                                ('O', 'O', 1)  : (-0.07599, -0.06878),
                                ('O', 'O', 2)  : (-0.17301, -0.16589),
                                ('O', 'P', 1)  : (-0.13497, -0.12550),
                                ('O', 'P', 2)  : (-0.19210, -0.18123),
                                ('O', 'S', 1)  : (-0.10182, -0.09185),
                                ('O', 'S', 2)  : (-0.17044, -0.15843),
                                ('P', 'P', 1)  : (-0.08651, -0.07861),
                                ('P', 'P', 2)  : (-0.11807, -0.10971),
                                ('P', 'P', 3)  : (-0.15283, -0.14410),
                                ('P', 'S', 1)  : (-0.09656, -0.08769),
                                ('P', 'S', 2)  : (-0.13096, -0.12180),
                                ('S', 'S', 1)  : (-0.08676, -0.07792),
                                ('S', 'S', 2)  : (-0.13372, -0.12616),
                                ('Br', 'Br', 1): (-0.06626, -0.05798),
                                ('Br', 'Cl', 1): (-0.06827, -0.06122),
                                ('Br', 'F', 1) : (-0.08855, -0.07919),
                                ('Br', 'H', 1) : (-0.14444, -0.13761),
                                ('Br', 'N', 1) : (-0.08229, -0.07266),
                                ('Br', 'O', 1) : (-0.07551, -0.06598),
                                ('Br', 'P', 1) : (-0.09768, -0.08883),
                                ('Br', 'S', 1) : (-0.07593, -0.06746),
                                ('Br', 'C', 1) : (-0.11578, -0.10523),
                                ('C', 'Cl', 1) : (-0.13052, -0.12052),
                                ('C', 'F', 1)  : (-0.17733, -0.17000),
                                ('Cl', 'Cl', 1): (-0.06780, -0.06038),
                                ('Cl', 'F', 1) : (-0.08043, -0.07323),
                                ('Cl', 'H', 1) : (-0.16247, -0.15659),
                                ('Cl', 'N', 1) : (-0.08910, -0.07982),
                                ('Cl', 'O', 1) : (-0.07507, -0.06654),
                                ('Cl', 'P', 1) : (-0.11142, -0.10277),
                                ('Cl', 'S', 1) : (-0.08294, -0.07483),
                                ('F', 'F', 1)  : (-0.04591, -0.04068),
                                ('F', 'H', 1)  : (-0.21700, -0.21349),
                                ('F', 'N', 1)  : (-0.10916, -0.10145),
                                ('F', 'O', 1)  : (-0.06877, -0.06220),
                                ('F', 'P', 1)  : (-0.16600, -0.15731),
                                ('F', 'S', 1)  : (-0.11864, -0.10923),
                                ('H', 'H', 1)  : (-0.16613, -0.16612), 
                                },
                  'def2tzvppd':{('Br', 'Br', 1) : (-0.07774, -0.07253),
                                ('Br', 'Cl', 1) : (-0.08190, -0.07827),
                                ('Br', 'F' , 1) : (-0.09598, -0.09073),
                                ('Br', 'H' , 1) : (-0.14805, -0.14372),
                                ('Br', 'N' , 1) : (-0.08979, -0.08401),
                                ('Br', 'O' , 1) : (-0.08459, -0.07888),
                                ('Br', 'P' , 1) : (-0.10613, -0.10189),
                                ('Br', 'S' , 1) : (-0.08819, -0.08366),
                                ('Br', 'C' , 1) : (-0.12095, -0.11532),
                                ('C' , 'C' , 1) : (-0.15215, -0.15022),
                                ('C' , 'Cl', 1) : (-0.13490, -0.13227),
                                ('C' , 'F' , 1) : (-0.17778, -0.17572),
                                ('C' , 'H' , 1) : (-0.17734, -0.17646),
                                ('C' , 'N' , 1) : (-0.14225, -0.14014),
                                ('C' , 'O' , 1) : (-0.15201, -0.14967),
                                ('C' , 'P' , 1) : (-0.11819, -0.11640),
                                ('C' , 'S' , 1) : (-0.12217, -0.11951),
                                ('Cl', 'Cl', 1) : (-0.08521, -0.08290),
                                ('Cl', 'F' , 1) : (-0.09154, -0.08916),
                                ('Cl', 'H' , 1) : (-0.16769, -0.16569),
                                ('Cl', 'N' , 1) : (-0.09728, -0.09453),
                                ('Cl', 'O' , 1) : (-0.08631, -0.08340),
                                ('Cl', 'P' , 1) : (-0.12090, -0.11867),
                                ('Cl', 'S' , 1) : (-0.09746, -0.09491),
                                ('F' , 'F' , 1) : (-0.05453, -0.05322),
                                ('F' , 'H' , 1) : (-0.22120, -0.21939),
                                ('F' , 'N' , 1) : (-0.11131, -0.10913),
                                ('F' , 'O' , 1) : (-0.07488, -0.07280),
                                ('F' , 'P' , 1) : (-0.17418, -0.17200),
                                ('F' , 'S' , 1) : (-0.12760, -0.12469),
                                ('H' , 'H' , 1) : (-0.17292, -0.17291),
                                ('H' , 'N' , 1) : (-0.18088, -0.17960),
                                ('N' , 'N' , 1) : (-0.11148, -0.10899),
                                ('N' , 'O' , 1) : (-0.10592, -0.10376),
                                ('N' , 'P' , 1) : (-0.12405, -0.12181),
                                ('N' , 'S' , 1) : (-0.10817, -0.10518),
                                ('H' , 'O' , 1) : (-0.19670, -0.19492),
                                ('O' , 'O' , 1) : (-0.08106, -0.07877),
                                ('O' , 'P' , 1) : (-0.14314, -0.14082),
                                ('O' , 'S' , 1) : (-0.11114, -0.10816),
                                ('H' , 'P' , 1) : (-0.13722, -0.13608),
                                ('P' , 'P' , 1) : (-0.09212, -0.09084),
                                ('P' , 'S' , 1) : (-0.10515, -0.10308),
                                ('H' , 'S' , 1) : (-0.15018, -0.14783),
                                ('S' , 'S' , 1) : (-0.09934, -0.09677),
                                ('C' , 'C' , 2) : (-0.28395, -0.28182),
                                ('C' , 'N' , 2) : (-0.25506, -0.25265),
                                ('C' , 'O' , 2) : (-0.28278, -0.28007),
                                ('C' , 'P' , 2) : (-0.19396, -0.19184),
                                ('C' , 'S' , 2) : (-0.20642, -0.20381),
                                ('N' , 'N' , 2) : (-0.19762, -0.19511),
                                ('N' , 'O' , 2) : (-0.18440, -0.18116),
                                ('N' , 'P' , 2) : (-0.16929, -0.16692),
                                ('N' , 'S' , 2) : (-0.14599, -0.14236),
                                ('O' , 'O' , 2) : (-0.18188, -0.17967),
                                ('O' , 'P' , 2) : (-0.20883, -0.20583),
                                ('O' , 'S' , 2) : (-0.18892, -0.18580),
                                ('P' , 'P' , 2) : (-0.12907, -0.12738),
                                ('P' , 'S' , 2) : (-0.14502, -0.14290),
                                ('S' , 'S' , 2) : (-0.15312, -0.15083),
                                ('C' , 'C' , 3) : (-0.42049, -0.41714),
                                ('C' , 'N' , 3) : (-0.37818, -0.37482),
                                ('C' , 'P' , 3) : (-0.28179, -0.27955),
                                ('N' , 'N' , 3) : (-0.34742, -0.34502),
                                ('N' , 'P' , 3) : (-0.21513, -0.21302),
                                ('P' , 'P' , 3) : (-0.16920, -0.16750),
                               },
                  }

# Charged bond energies
qbnd_enes = {'def2svpd'  :{('C', 'N+', 1) : (-0.19017, -0.18183),
                                ('C', 'O-', 1) : (-0.14427, -0.13611),
                                ('H', 'N+', 1) : (-0.20642, -0.20341),
                                ('H', 'O-', 1) : (-0.17702, -0.17358),
                                ('N', 'N+', 1) : (-0.14386, -0.13539),
                                ('N+', 'O', 1) : (-0.11734, -0.10892),
                                ('N', 'O-', 1) : (-0.06923, -0.06108),
                                ('O', 'O-', 1) : (-0.19368, -0.18796),
                                ('C', 'N+', 2) : (-0.34727, -0.33935),
                                ('N', 'N+', 2) : (-0.25216, -0.23878),
                                ('N+', 'O', 2) : (-0.20950, -0.20096),
                                ('C', 'N+', 3) : (-0.51069, -0.50241),
                                ('N', 'N+', 3) : (-0.39447, -0.38508),
                                },
                  'def2tzvppd':{('C', 'N+', 1) : (-0.18982, -0.18821),
                                ('C', 'O-', 1) : (-0.14582, -0.14299),
                                ('H', 'N+', 1) : (-0.21030, -0.20950),
                                ('H', 'O-', 1) : (-0.18133, -0.17960),
                                ('N', 'N+', 1) : (-0.14518, -0.14308),
                                ('N+', 'O', 1) : (-0.12095, -0.11868),
                                ('N', 'O-', 1) : (-0.07366, -0.07082),
                                ('O', 'O-', 1) : (-0.15766, -0.15539),
                                ('C', 'N+', 2) : (-0.35210, -0.35003),
                                ('N', 'N+', 2) : (-0.25838, -0.25436),
                                ('N+', 'O', 2) : (-0.21802, -0.21572),
                                ('C', 'N+', 3) : (-0.52567, -0.52141),
                                ('N', 'N+', 3) : (-0.41002, -0.40761),
                                },
                    }

# Probability of lone pairs on atom types
lp_prob = defaultdict(_zero_tuple, 
                        {('Br', 1) : (1.00000000, 1.00000000, 1.00000000, 1.00000000, 171),
                        ('C', 1) : (1.00000000, 1.00000000, 0.00000000, 0.00000000, 5),
                        ('C', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 443),
                        ('C', 3) : (1.00000000, 0.00007922, 0.00000000, 0.00000000, 63116),
                        ('C', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 56975),
                        ('Cl', 1) : (1.00000000, 1.00000000, 1.00000000, 1.00000000, 1448),
                        ('Cl', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 2),
                        ('F', 1) : (1.00000000, 1.00000000, 1.00000000, 1.00000000, 1791),
                        ('H', 1) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 152568),
                        ('N', 1) : (1.00000000, 1.00000000, 0.05747126, 0.00000000, 261),
                        ('N', 2) : (1.00000000, 0.99366126, 0.02180527, 0.00000000, 3944),
                        ('N', 3) : (1.00000000, 0.95871401, 0.00000000, 0.00000000, 11602),
                        ('N', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 224),
                        ('O', 1) : (1.00000000, 1.00000000, 1.00000000, 0.09320832, 12692),
                        ('O', 2) : (1.00000000, 1.00000000, 0.99960213, 0.00000000, 12567),
                        ('O', 3) : (1.00000000, 1.00000000, 0.00000000, 0.00000000, 1),
                        ('P', 2) : (1.00000000, 1.00000000, 0.00000000, 0.00000000, 3),
                        ('P', 3) : (1.00000000, 0.96666667, 0.00000000, 0.00000000, 30),
                        ('P', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 318),
                        ('S', 1) : (1.00000000, 1.00000000, 1.00000000, 0.18285714, 175),
                        ('S', 2) : (1.00000000, 1.00000000, 0.99696740, 0.00000000, 1319),
                        ('S', 3) : (1.00000000, 0.98591549, 0.00000000, 0.00000000, 71),
                        ('S', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 773),
                        ('S', 6) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 1),
                        })

# Probability of higher bond order
bo_prob = defaultdict(_zero_tuple, 
                        {('Br', 1, 'C', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 134),
                        ('Br', 1, 'C', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 36),
                        ('Br', 1, 'N', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 1),
                        ('C', 1, 'N', 2) : (1.00000000, 1.00000000, 1.00000000, 0.00000000, 5),
                        ('C', 2, 'C', 2) : (1.00000000, 1.00000000, 1.00000000, 0.00000000, 97),
                        ('C', 2, 'C', 3) : (1.00000000, 0.06666667, 0.00000000, 0.00000000, 180),
                        ('C', 2, 'C', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 183),
                        ('C', 2, 'Cl', 1) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 1),
                        ('C', 2, 'H', 1) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 62),
                        ('C', 2, 'N', 1) : (1.00000000, 1.00000000, 1.00000000, 0.00000000, 241),
                        ('C', 2, 'N', 2) : (1.00000000, 0.20000000, 0.00000000, 0.00000000, 10),
                        ('C', 2, 'N', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 7),
                        ('C', 2, 'O', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 2),
                        ('C', 2, 'S', 1) : (1.00000000, 1.00000000, 0.00000000, 0.00000000, 2),
                        ('C', 2, 'S', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 4),
                        ('C', 3, 'C', 3) : (1.00000000, 0.47709975, 0.00000000, 0.00000000, 52423),
                        ('C', 3, 'C', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 15393),
                        ('C', 3, 'Cl', 1) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 1071),
                        ('C', 3, 'F', 1) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 566),
                        ('C', 3, 'H', 1) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 31044),
                        ('C', 3, 'N', 2) : (1.00000000, 0.58616647, 0.00000000, 0.00000000, 5971),
                        ('C', 3, 'N', 3) : (1.00000000, 0.01502989, 0.00000000, 0.00000000, 11710),
                        ('C', 3, 'N', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 16),
                        ('C', 3, 'O', 1) : (1.00000000, 0.94959533, 0.00000000, 0.00000000, 9761),
                        ('C', 3, 'O', 2) : (1.00000000, 0.00090023, 0.00000000, 0.00000000, 6665),
                        ('C', 3, 'O', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 1),
                        ('C', 3, 'P', 2) : (1.00000000, 1.00000000, 0.00000000, 0.00000000, 3),
                        ('C', 3, 'P', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 2),
                        ('C', 3, 'P', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 22),
                        ('C', 3, 'S', 1) : (1.00000000, 0.85401460, 0.00000000, 0.00000000, 137),
                        ('C', 3, 'S', 2) : (1.00000000, 0.00300075, 0.00000000, 0.00000000, 1333),
                        ('C', 3, 'S', 3) : (1.00000000, 0.04761905, 0.00000000, 0.00000000, 42),
                        ('C', 3, 'S', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 451),
                        ('C', 4, 'C', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 38671),
                        ('C', 4, 'C', 5) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 4),
                        ('C', 4, 'Cl', 1) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 353),
                        ('C', 4, 'F', 1) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 1212),
                        ('C', 4, 'H', 1) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 106767),
                        ('C', 4, 'N', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 217),
                        ('C', 4, 'N', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 12629),
                        ('C', 4, 'N', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 737),
                        ('C', 4, 'O', 1) : (1.00000000, 0.11111111, 0.00000000, 0.00000000, 9),
                        ('C', 4, 'O', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 11428),
                        ('C', 4, 'O', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 2),
                        ('C', 4, 'P', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 1),
                        ('C', 4, 'P', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 43),
                        ('C', 4, 'P', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 129),
                        ('C', 4, 'S', 1) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 6),
                        ('C', 4, 'S', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 1039),
                        ('C', 4, 'S', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 82),
                        ('C', 4, 'S', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 292),
                        ('C', 5, 'H', 1) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 1),
                        ('Cl', 1, 'N', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 2),
                        ('Cl', 1, 'N', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 12),
                        ('Cl', 1, 'P', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 4),
                        ('Cl', 1, 'P', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 3),
                        ('Cl', 1, 'S', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 1),
                        ('Cl', 1, 'S', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 2),
                        ('Cl', 4, 'O', 1) : (1.00000000, 0.37500000, 0.00000000, 0.00000000, 8),
                        ('F', 1, 'N', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 2),
                        ('F', 1, 'P', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 2),
                        ('F', 1, 'P', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 3),
                        ('F', 1, 'S', 6) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 6),
                        ('H', 1, 'N', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 206),
                        ('H', 1, 'N', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 8405),
                        ('H', 1, 'N', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 127),
                        ('H', 1, 'O', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 5895),
                        ('H', 1, 'O', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 3),
                        ('H', 1, 'P', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 2),
                        ('H', 1, 'P', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 9),
                        ('H', 1, 'P', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 9),
                        ('H', 1, 'S', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 37),
                        ('H', 1, 'S', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 1),
                        ('N', 1, 'N', 2) : (1.00000000, 1.00000000, 0.25000000, 0.00000000, 20),
                        ('N', 2, 'N', 2) : (1.00000000, 0.51495017, 0.00000000, 0.00000000, 301),
                        ('N', 2, 'N', 3) : (1.00000000, 0.03420523, 0.00000000, 0.00000000, 497),
                        ('N', 2, 'N', 4) : (1.00000000, 0.50000000, 0.00000000, 0.00000000, 2),
                        ('N', 2, 'O', 1) : (1.00000000, 0.65217391, 0.00000000, 0.00000000, 23),
                        ('N', 2, 'O', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 215),
                        ('N', 2, 'P', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 4),
                        ('N', 2, 'S', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 58),
                        ('N', 2, 'S', 3) : (1.00000000, 1.00000000, 0.00000000, 0.00000000, 1),
                        ('N', 2, 'S', 4) : (1.00000000, 0.07272727, 0.00000000, 0.00000000, 55),
                        ('N', 3, 'N', 3) : (1.00000000, 0.01342282, 0.00000000, 0.00000000, 149),
                        ('N', 3, 'N', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 4),
                        ('N', 3, 'O', 1) : (1.00000000, 0.47094801, 0.00000000, 0.00000000, 654),
                        ('N', 3, 'O', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 133),
                        ('N', 3, 'P', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 9),
                        ('N', 3, 'P', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 75),
                        ('N', 3, 'S', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 12),
                        ('N', 3, 'S', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 6),
                        ('N', 3, 'S', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 400),
                        ('N', 4, 'O', 1) : (1.00000000, 0.11111111, 0.00000000, 0.00000000, 9),
                        ('N', 4, 'P', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 1),
                        ('O', 1, 'P', 3) : (1.00000000, 0.66666667, 0.00000000, 0.00000000, 3),
                        ('O', 1, 'P', 4) : (1.00000000, 0.63191489, 0.00000000, 0.00000000, 470),
                        ('O', 1, 'S', 2) : (1.00000000, 1.00000000, 0.00000000, 0.00000000, 3),
                        ('O', 1, 'S', 3) : (1.00000000, 0.91780822, 0.00000000, 0.00000000, 73),
                        ('O', 1, 'S', 4) : (1.00000000, 0.91780822, 0.00000000, 0.00000000, 1679),
                        ('O', 2, 'O', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 11),
                        ('O', 2, 'P', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 6),
                        ('O', 2, 'P', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 556),
                        ('O', 2, 'S', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 2),
                        ('O', 2, 'S', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 5),
                        ('O', 2, 'S', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 207),
                        ('P', 3, 'P', 3) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 4),
                        ('P', 3, 'S', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 3),
                        ('P', 4, 'P', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 1),
                        ('P', 4, 'S', 1) : (1.00000000, 0.77777778, 0.00000000, 0.00000000, 27),
                        ('P', 4, 'S', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 16),
                        ('S', 1, 'S', 3) : (1.00000000, 1.00000000, 0.00000000, 0.00000000, 2),
                        ('S', 1, 'S', 4) : (1.00000000, 1.00000000, 0.00000000, 0.00000000, 1),
                        ('S', 2, 'S', 2) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 63),
                        ('S', 2, 'S', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 4),
                        ('S', 3, 'S', 4) : (1.00000000, 0.00000000, 0.00000000, 0.00000000, 1),
                        })
