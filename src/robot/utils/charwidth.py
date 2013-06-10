#  Copyright 2008-2013 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""A module to handle different character widths on the console.

Some East Asian characters have width of two on console, and combining
characters themselves take no extra space.

See issue 604 [1] for more details about East Asian characters. The issue also
contains `generate_wild_chars.py` script that was originally used to create
`_EAST_ASIAN_WILD_CHARS` mapping. An updated version of the script is attached
to issue 1096. Big thanks for xieyanbo for the script and the original patch.

Note that Python's `unicodedata` module is not used here because importing
it takes several seconds on Jython.

[1] http://code.google.com/p/robotframework/issues/detail?id=604
[2] http://code.google.com/p/robotframework/issues/detail?id=1096
"""

def get_char_width(char):
    char = ord(char)
    if _char_in_map(char, _COMBINING_CHARS):
        return 0
    if _char_in_map(char, _EAST_ASIAN_WILD_CHARS):
        return 2
    return 1

def _char_in_map(char, map):
    for begin, end in map:
        if char < begin:
            break
        if begin <= char <= end:
            return True
    return False


_COMBINING_CHARS = [(768, 879)]

_EAST_ASIAN_WILD_CHARS = [
        (888, 889), (895, 899), (907, 907), (909, 909), (930, 930),
        (1316, 1328), (1367, 1368), (1376, 1376), (1416, 1416),
        (1419, 1424), (1480, 1487), (1515, 1519), (1525, 1535),
        (1540, 1541), (1564, 1565), (1568, 1568), (1631, 1631),
        (1806, 1806), (1867, 1868), (1970, 1983), (2043, 2304),
        (2362, 2363), (2382, 2383), (2389, 2391), (2419, 2426),
        (2432, 2432), (2436, 2436), (2445, 2446), (2449, 2450),
        (2473, 2473), (2481, 2481), (2483, 2485), (2490, 2491),
        (2501, 2502), (2505, 2506), (2511, 2518), (2520, 2523),
        (2526, 2526), (2532, 2533), (2555, 2560), (2564, 2564),
        (2571, 2574), (2577, 2578), (2601, 2601), (2609, 2609),
        (2612, 2612), (2615, 2615), (2618, 2619), (2621, 2621),
        (2627, 2630), (2633, 2634), (2638, 2640), (2642, 2648),
        (2653, 2653), (2655, 2661), (2678, 2688), (2692, 2692),
        (2702, 2702), (2706, 2706), (2729, 2729), (2737, 2737),
        (2740, 2740), (2746, 2747), (2758, 2758), (2762, 2762),
        (2766, 2767), (2769, 2783), (2788, 2789), (2800, 2800),
        (2802, 2816), (2820, 2820), (2829, 2830), (2833, 2834),
        (2857, 2857), (2865, 2865), (2868, 2868), (2874, 2875),
        (2885, 2886), (2889, 2890), (2894, 2901), (2904, 2907),
        (2910, 2910), (2916, 2917), (2930, 2945), (2948, 2948),
        (2955, 2957), (2961, 2961), (2966, 2968), (2971, 2971),
        (2973, 2973), (2976, 2978), (2981, 2983), (2987, 2989),
        (3002, 3005), (3011, 3013), (3017, 3017), (3022, 3023),
        (3025, 3030), (3032, 3045), (3067, 3072), (3076, 3076),
        (3085, 3085), (3089, 3089), (3113, 3113), (3124, 3124),
        (3130, 3132), (3141, 3141), (3145, 3145), (3150, 3156),
        (3159, 3159), (3162, 3167), (3172, 3173), (3184, 3191),
        (3200, 3201), (3204, 3204), (3213, 3213), (3217, 3217),
        (3241, 3241), (3252, 3252), (3258, 3259), (3269, 3269),
        (3273, 3273), (3278, 3284), (3287, 3293), (3295, 3295),
        (3300, 3301), (3312, 3312), (3315, 3329), (3332, 3332),
        (3341, 3341), (3345, 3345), (3369, 3369), (3386, 3388),
        (3397, 3397), (3401, 3401), (3406, 3414), (3416, 3423),
        (3428, 3429), (3446, 3448), (3456, 3457), (3460, 3460),
        (3479, 3481), (3506, 3506), (3516, 3516), (3518, 3519),
        (3527, 3529), (3531, 3534), (3541, 3541), (3543, 3543),
        (3552, 3569), (3573, 3584), (3643, 3646), (3676, 3712),
        (3715, 3715), (3717, 3718), (3721, 3721), (3723, 3724),
        (3726, 3731), (3736, 3736), (3744, 3744), (3748, 3748),
        (3750, 3750), (3752, 3753), (3756, 3756), (3770, 3770),
        (3774, 3775), (3781, 3781), (3783, 3783), (3790, 3791),
        (3802, 3803), (3806, 3839), (3912, 3912), (3949, 3952),
        (3980, 3983), (3992, 3992), (4029, 4029), (4045, 4045),
        (4053, 4095), (4250, 4253), (4294, 4303), (4349, 4447),
        (4515, 4519), (4602, 4607), (4681, 4681), (4686, 4687),
        (4695, 4695), (4697, 4697), (4702, 4703), (4745, 4745),
        (4750, 4751), (4785, 4785), (4790, 4791), (4799, 4799),
        (4801, 4801), (4806, 4807), (4823, 4823), (4881, 4881),
        (4886, 4887), (4955, 4958), (4989, 4991), (5018, 5023),
        (5109, 5120), (5751, 5759), (5789, 5791), (5873, 5887),
        (5901, 5901), (5909, 5919), (5943, 5951), (5972, 5983),
        (5997, 5997), (6001, 6001), (6004, 6015), (6110, 6111),
        (6122, 6127), (6138, 6143), (6159, 6159), (6170, 6175),
        (6264, 6271), (6315, 6399), (6429, 6431), (6444, 6447),
        (6460, 6463), (6465, 6467), (6510, 6511), (6517, 6527),
        (6570, 6575), (6602, 6607), (6618, 6621), (6684, 6685),
        (6688, 6911), (6988, 6991), (7037, 7039), (7083, 7085),
        (7098, 7167), (7224, 7226), (7242, 7244), (7296, 7423),
        (7655, 7677), (7958, 7959), (7966, 7967), (8006, 8007),
        (8014, 8015), (8024, 8024), (8026, 8026), (8028, 8028),
        (8030, 8030), (8062, 8063), (8117, 8117), (8133, 8133),
        (8148, 8149), (8156, 8156), (8176, 8177), (8181, 8181),
        (8191, 8191), (8293, 8297), (8306, 8307), (8335, 8335),
        (8341, 8351), (8374, 8399), (8433, 8447), (8528, 8530),
        (8585, 8591), (9001, 9002), (9192, 9215), (9255, 9279),
        (9291, 9311), (9886, 9887), (9917, 9919), (9924, 9984),
        (9989, 9989), (9994, 9995), (10024, 10024), (10060, 10060),
        (10062, 10062), (10067, 10069), (10071, 10071), (10079, 10080),
        (10133, 10135), (10160, 10160), (10175, 10175), (10187, 10187),
        (10189, 10191), (11085, 11087), (11093, 11263), (11311, 11311),
        (11359, 11359), (11376, 11376), (11390, 11391), (11499, 11512),
        (11558, 11567), (11622, 11630), (11632, 11647), (11671, 11679),
        (11687, 11687), (11695, 11695), (11703, 11703), (11711, 11711),
        (11719, 11719), (11727, 11727), (11735, 11735), (11743, 11743),
        (11825, 12350), (12352, 19903), (19968, 42239), (42540, 42559),
        (42592, 42593), (42612, 42619), (42648, 42751), (42893, 43002),
        (43052, 43071), (43128, 43135), (43205, 43213), (43226, 43263),
        (43348, 43358), (43360, 43519), (43575, 43583), (43598, 43599),
        (43610, 43611), (43616, 55295), (63744, 64255), (64263, 64274),
        (64280, 64284), (64311, 64311), (64317, 64317), (64319, 64319),
        (64322, 64322), (64325, 64325), (64434, 64466), (64832, 64847),
        (64912, 64913), (64968, 65007), (65022, 65023), (65040, 65055),
        (65063, 65135), (65141, 65141), (65277, 65278), (65280, 65376),
        (65471, 65473), (65480, 65481), (65488, 65489), (65496, 65497),
        (65501, 65511), (65519, 65528), (65534, 65535),
        ]
