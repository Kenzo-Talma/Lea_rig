# from json import dumps

shape_dic = {
    'circleX': {
        'p': [
            (4.7982373409884725e-17, 0.7836116248912246, -0.7836116248912245),
            (4.155062684684256e-33, 1.1081941875543877, -6.785732323110912e-17),
            (-4.7982373409884725e-17, 0.7836116248912244, 0.7836116248912245),
            (-6.785732323110915e-17, 5.74489823752483e-17, 1.1081941875543881),
            (-4.7982373409884725e-17, -0.7836116248912245, 0.7836116248912245),
            (-6.797314477808589e-33, -1.1081941875543884, 1.1100856969603225e-16),
            (4.7982373409884725e-17, -0.7836116248912244, -0.7836116248912245),
            (6.785732323110915e-17, -1.511240500779959e-16, -1.1081941875543881),
            (4.7982373409884725e-17, 0.7836116248912246, -0.7836116248912245),
            (4.155062684684256e-33, 1.1081941875543877, -6.785732323110912e-17),
            (-4.7982373409884725e-17, 0.7836116248912244, 0.7836116248912245)
        ],
        'd': 3,
        'periodic': True,
        'k': [
            -2.0,
            -1.0,
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0
        ]
    },
    'circleY': {
        'p': [
            (0.7836116248912245, 4.798237340988473e-17, -0.7836116248912246),
            (6.785732323110912e-17, 6.785732323110912e-17, -1.1081941875543877),
            (-0.7836116248912245, 4.798237340988472e-17, -0.7836116248912244),
            (-1.1081941875543881, 3.517735619006027e-33, -5.74489823752483e-17),
            (-0.7836116248912245, -4.7982373409884725e-17, 0.7836116248912245),
            (-1.1100856969603225e-16, -6.785732323110917e-17, 1.1081941875543884),
            (0.7836116248912245, -4.798237340988472e-17, 0.7836116248912244),
            (1.1081941875543881, -9.253679210110099e-33, 1.511240500779959e-16),
            (0.7836116248912245, 4.798237340988473e-17, -0.7836116248912246),
            (6.785732323110912e-17, 6.785732323110912e-17, -1.1081941875543877),
            (-0.7836116248912245, 4.798237340988472e-17, -0.7836116248912244)
        ],
        'd': 3,
        'periodic': True,
        'k': [
            -2.0,
            -1.0,
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0
        ]
    },
    'circleZ': {
        'p': [
            (0.7836116248912245, 0.7836116248912246, 0.0),
            (6.785732323110912e-17, 1.1081941875543877, 0.0),
            (-0.7836116248912245, 0.7836116248912244, 0.0),
            (-1.1081941875543881, 5.74489823752483e-17, 0.0),
            (-0.7836116248912245, -0.7836116248912245, 0.0),
            (-1.1100856969603225e-16, -1.1081941875543884, 0.0),
            (0.7836116248912245, -0.7836116248912244, 0.0),
            (1.1081941875543881, -1.511240500779959e-16, 0.0),
            (0.7836116248912245, 0.7836116248912246, 0.0),
            (6.785732323110912e-17, 1.1081941875543877, 0.0),
            (-0.7836116248912245, 0.7836116248912244, 0.0)
        ],
        'd': 3,
        'periodic': True,
        'k': [
            -2.0,
            -1.0,
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0
        ]
    },
    'squareX': {
        'p': [
            (0.0, 0.0, 1.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, -1.0),
            (0.0, -1.0, 0.0),
            (0.0, 0.0, 1.0)
        ],
        'd': 1,
        'periodic': True,
        'k': [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0
        ]
    },
    'squareY': {
        'p': [
            (0.0, 0.0, 1.0),
            (-1.0, 0.0, 0.0),
            (0.0, 0.0, -1.0),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0)
        ],
        'd': 1,
        'periodic': True,
        'k': [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0
        ]
    },
    'squareZ': {
        'p': [
            (-1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, -1.0, 0.0),
            (-1.0, 0.0, 0.0)
        ],
        'd': 1,
        'periodic': True,
        'k': [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0
        ]
    },
    'diamond': {
        'p': [
            (0.0, 0.0, 1.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, -1.0),
            (0.0, -1.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, -1.0),
            (-1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (-1.0, 0.0, 0.0),
            (0.0, -1.0, 0.0),
            (1.0, 0.0, 0.0)
        ],
        'd': 1,
        'periodic': False,
        'k': [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0
        ]
    },
    'cube': {
        'p': [
            (1.0, -1.0, 1.0),
            (1.0, -1.0, -1.0),
            (1.0, 1.0, -1.0),
            (1.0, 1.0, 1.0),
            (1.0, -1.0, 1.0),
            (-1.0, -1.0, 1.0),
            (-1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, -1.0),
            (-1.0, 1.0, -1.0),
            (-1.0, -1.0, -1.0),
            (1.0, -1.0, -1.0),
            (-1.0, -1.0, -1.0),
            (-1.0, -1.0, 1.0),
            (-1.0, 1.0, 1.0),
            (-1.0, 1.0, -1.0)
        ],
        'd': 1,
        'periodic': False,
        'k': [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0
        ]
    },
    'sphere': {
        'p': [
            (4.6064327282110513e-08, 8.981798529437616e-16, 0.9722248731482216),
            (4.606432402381257e-08, -0.37205431268203387, 0.8982186812971006),
            (4.606432178373269e-08, -0.6874667451918838, 0.6874667915288918),
            (4.6064317710860324e-08, -0.8982185892757328, 0.37205435875797704),
            (4.6064315063493205e-08, -0.9722247811268466, -6.911155372902622e-15),
            (4.606431200883897e-08, -0.8982185892757372, -0.3720543587579888),
            (4.6064310176046376e-08, -0.6874667451918881, -0.6874667915288973),
            (4.606430936147186e-08, -0.37205431268204253, -0.8982186812971082),
            (4.606431241612621e-08, -7.90940673646437e-15, -0.9722248731482216),
            (4.606431404527516e-08, 0.3720543357200017, -0.898218681297105),
            (4.606431811814756e-08, 0.6874667915288722, -0.6874667915288922),
            (4.606431934000931e-08, 0.8982185892757307, -0.372054358757982),
            (4.606432402381257e-08, 0.9722247811268466, 4.581981462697869e-16),
            (4.6064325856605157e-08, 0.898218589275735, 0.37205435875798437),
            (4.6064327893041345e-08, 0.6874667915288775, 0.6874667915288984),
            (4.6064329725833905e-08, 0.3720543357200105, 0.8982186812971059),
            (4.6064327282110513e-08, 8.981798529437616e-16, 0.9722248731482216),
            (0.3720543587579768, 2.781883343163999e-15, 0.8982186812971059),
            (0.6874667915288778, 2.934616058587261e-15, 0.6874667915289032),
            (0.8982186349600866, 1.992764313477142e-15, 0.37205435875798765),
            (0.9722248274638268, 1.992764313477142e-15, 4.225605126710257e-15),
            (0.8982186349600807, -9.091572795648433e-16, -0.3720543587579775),
            (0.6874667915288678, -3.3656084526223134e-15, -0.6874667915288871),
            (0.3720543587579624, -5.554777373689073e-15, -0.8982186812971021),
            (4.606431241612621e-08, -7.90940673646437e-15, -0.9722248731482216),
            (-0.37205431268203953, -8.825803029003945e-15, -0.8982186812971096),
            (-0.687466791528868, -1.0251308372954379e-14, -0.6874667915288984),
            (-0.8982186349600806, -9.385822985555892e-15, -0.3720543587579936),
            (-0.9722248274638268, -7.196654064489147e-15, -1.0182181028217494e-14),
            (-0.8982186349600781, -5.5929605525448905e-15, 0.372054358757974),
            (-0.6874667915288566, -3.327425273766498e-15, 0.6874667915288922),
            (-0.37205431268202527, -6.164195750035901e-16, 0.8982186812971024),
            (4.6064327282110513e-08, 8.981798529437616e-16, 0.9722248731482216),
            (0.3720543587579768, 2.781883343163999e-15, 0.8982186812971059),
            (0.6874667915288778, 2.934616058587261e-15, 0.6874667915289032),
            (0.8982186349600866, 1.992764313477142e-15, 0.37205435875798765),
            (0.9722248274638268, 1.992764313477142e-15, 4.225605126710257e-15),
            (0.6874667915288767, 0.6874667451918884, 4.70925872555059e-15),
            (4.606432402381257e-08, 0.9722247811268466, 4.581981462697869e-16),
            (-0.6874667451918727, 0.6874667915288701, -7.63663577116312e-15),
            (-0.9722248274638268, -7.196654064489147e-15, -1.0182181028217494e-14),
            (-0.687466699507519, -0.6874667451918871, -1.3185924431541647e-14),
            (4.6064315063493205e-08, -0.9722247811268466, -6.911155372902622e-15),
            (0.6874667915288698, -0.6874667451918826, -4.0728724112869973e-16),
            (0.9722248274638268, 1.992764313477142e-15, 4.225605126710257e-15)
        ],
        'd': 1,
        'periodic': False,
        'k': [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0
        ]
    },
    'pinX': {
        'p': [
            (0.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
            (3.0, -1.0, 0.0),
            (4.0, 0.0, 0.0),
            (3.0, 1.0, 0.0),
            (2.0, 0.0, 0.0)
        ],
        'd': 1,
        'periodic': False,
        'k': [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0
        ]
    },
    'pinZ': {
        'p': [
            (0.0, 0.0, 0.0),
            (0.0, 0.0, -2.0),
            (-1.0, 0.0, -3.0),
            (0.0, 0.0, -4.0),
            (1.0, 0.0, -3.0),
            (0.0, 0.0, -2.0)
        ],
        'd': 1,
        'periodic': False,
        'k': [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0
        ]
    },
    'pinY': {
        'p': [
            (0.0, 0.0, 0.0),
            (0.0, 2.0, 0.0),
            (-1.0, 3.0, 0.0),
            (0.0, 4.0, 0.0),
            (1.0, 3.0, 0.0),
            (0.0, 2.0, 0.0)
        ],
        'd': 1,
        'periodic': False,
        'k': [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0
        ]
    }
}

def return_shape(shape):
    return shape_dic[shape]

####################################################################################
# test
####################################################################################
# ctrl = return_shape('cube')
# print(dumps(ctrl, indent=4))
