import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

from Lea_pythonScript import (
    spine_generation,
    FK_spine,
    IK_spine,
    IkFkLimb,
    FK_limb,
    IK_limb,
    IkFkLimb,
    IK_FK_switch,
    strechSquashLimbIK,
    footRoll,
    FK_foot,
    foot_switch,
    mirror_joints,
    neck,
    hand,
    scapula,
    createRibbon,
    ribbonJoints,
    k_tools,
    create_skeleton,
    create_controls
)
for mod in [
    spine_generation,
    FK_spine,
    IK_spine,
    IkFkLimb,
    FK_limb,
    IK_limb,
    IkFkLimb,
    IK_FK_switch,
    strechSquashLimbIK,
    footRoll,
    FK_foot,
    foot_switch,
    mirror_joints,
    neck,
    hand,
    scapula,
    createRibbon,
    ribbonJoints,
    k_tools,
    create_skeleton,
    create_controls
]:
    importlib.reload(mod)

# arm
'''FK_limb.fk_limb(
    [
        'L_FK_arm_1_jnt',
        'L_FK_arm_2_jnt',
        'L_FK_arm_3_jnt'
    ]
)

IK_limb.ik_limb(
    [
        'L_IK_arm_1_jnt',
        'L_IK_arm_2_jnt',
        'L_IK_arm_3_jnt'
    ],
    (
        0,
        0,
        -5
    )
)

FK_limb.fk_limb(
    [
        'R_FK_arm_1_jnt',
        'R_FK_arm_2_jnt',
        'R_FK_arm_3_jnt'
    ]
)

IK_limb.ik_limb(
    [
        'R_IK_arm_1_jnt',
        'R_IK_arm_2_jnt',
        'R_IK_arm_3_jnt'
    ],
    (
        0,
        0,
        -5
    )
)'''

# leg
'''FK_limb.fk_limb(
    [
        'L_FK_leg_1_jnt',
        'L_FK_leg_2_jnt',
        'L_FK_leg_3_jnt'
    ]
)

IK_limb.ik_limb(
    [
        'L_IK_leg_1_jnt',
        'L_IK_leg_2_jnt',
        'L_IK_leg_3_jnt'
    ],
    (
        0,
        0,
        5
    )
)

FK_limb.fk_limb(
    [
        'R_FK_leg_1_jnt',
        'R_FK_leg_2_jnt',
        'R_FK_leg_3_jnt'
    ]
)

IK_limb.ik_limb(
    [
        'R_IK_leg_1_jnt',
        'R_IK_leg_2_jnt',
        'R_IK_leg_3_jnt'
    ],
    (
        0,
        0,
        5
    )
)'''

# ribbon
r_arm_ribbon = createRibbon.createRibbon_Func(
    'R_main_arm_1_jnt',
    'R_main_arm_2_jnt',
    2,
    'R_upper_arm',
    'R_arm_switch'
)
ribbonJoints.createRibbonJoints_func(
    r_arm_ribbon,
    5,
    'R_arm_switch'
)

r_l_arm_ribbon = createRibbon.createRibbon_Func(
    'R_main_arm_2_jnt',
    'R_main_arm_3_jnt',
    2,
    'R_lower_arm',
    'R_arm_switch'
)
ribbonJoints.createRibbonJoints_func(
    r_l_arm_ribbon,
    5,
    'R_arm_switch'
)

l_arm_ribbon = createRibbon.createRibbon_Func(
    'L_main_arm_1_jnt',
    'L_main_arm_2_jnt',
    2,
    'L_upper_arm',
    'L_arm_switch'
)
ribbonJoints.createRibbonJoints_func(
    l_arm_ribbon,
    5,
    'L_arm_switch'
)

l_l_arm_ribbon = createRibbon.createRibbon_Func(
    'L_main_arm_2_jnt',
    'L_main_arm_3_jnt',
    2,
    'L_lower_arm',
    'L_arm_switch'
)
ribbonJoints.createRibbonJoints_func(
    l_l_arm_ribbon,
    5,
    'L_arm_switch'
)

r_leg_ribbon = createRibbon.createRibbon_Func(
    'R_main_leg_1_jnt',
    'R_main_leg_2_jnt',
    2,
    'R_upper_leg',
    'R_leg_switch'
)
ribbonJoints.createRibbonJoints_func(
    r_leg_ribbon,
    5,
    'R_leg_switch'
)

r_l_leg_ribbon = createRibbon.createRibbon_Func(
    'R_main_leg_2_jnt',
    'R_main_leg_3_jnt',
    2,
    'R_lower_leg',
    'R_leg_switch'
)
ribbonJoints.createRibbonJoints_func(
    r_l_leg_ribbon,
    5,
    'R_leg_switch'
)

l_leg_ribbon = createRibbon.createRibbon_Func(
    'L_main_leg_1_jnt',
    'L_main_leg_2_jnt',
    2,
    'L_upper_leg',
    'L_leg_switch'
)
ribbonJoints.createRibbonJoints_func(
    l_leg_ribbon,
    5,
    'L_leg_switch'
)

l_l_leg_ribbon = createRibbon.createRibbon_Func(
    'L_main_leg_2_jnt',
    'L_main_leg_3_jnt',
    2,
    'L_lower_leg',
    'L_leg_switch'
)
ribbonJoints.createRibbonJoints_func(
    l_l_leg_ribbon,
    5,
    'L_leg_switch'
)