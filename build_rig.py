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


####################################################################################
# create world, walk and cog control
####################################################################################

# world
world_grp, world_ctrl, world_jnt = k_tools.create_simple_ctrl('C_main', None, False)

# walk
walk_grp, walk_ctrl, walk_jnt = k_tools.create_simple_ctrl('C_walk', None, False)

# cog
cog_grp, cog_ctrl, cog_jnt = k_tools.create_simple_ctrl('C_COG', 'C_spine_1', False)

# parent
cmds.parent(cog_grp, walk_ctrl)
cmds.parent(walk_grp, world_ctrl)


####################################################################################
# spine
####################################################################################

# generate spine joints
spine_loc_list = [
    "C_spine_1",
    "C_spine_2",
    "C_spine_3",
    "C_spine_4",
    "C_spine_5",
    "C_spine_6",
    "C_spine_7",
    "C_spine_8",
    "C_spine_9",
    "C_spine_10",
    "C_spine_11",
    "C_spine_12"
]


main_spine_joints, \
    ik_spine_joints, \
    fk_spine_joints, \
    spine_blend_list = spine_generation.generate_spine_func(spine_loc_list)

# IK FK system
spine_ik_handle, spine_crv, spine_built_crv = IK_spine.buildIKSpine_func(ik_spine_joints, 'C_spine_6_IK_jnt')
FK_spine.buildFKSpine_func(fk_spine_joints, 'C_spine_4_FK_jnt', 'C_spine_8_FK_jnt')

# fix spine
cmds.connectAttr(
    'C_shoulder_ikSpine_ctrl.worldMatrix',
    'C_spine_12_IK_mlm.matrixIn[0]',
    f=True
)
cmds.connectAttr(
    'C_hip_ikSpine_ctrl.worldMatrix',
    'C_spine_1_blm.target[0].targetMatrix',
    f=True
)
cmds.connectAttr(
    'C_hip_ikSpine_ctrl.worldInverseMatrix',
    'C_spine_2_IK_mlm.matrixIn[1]',
    f=True
)

# all ik ctrl grp
ik_ctrl_grp = k.createNode('transform', n='C_spine_ik_ctrl_grp')
cmds.parent(
    "C_hip_ikSpine_grp",
    "C_spine_ikSpine_grp",
    "C_shoulder_ikSpine_grp",
    spine_crv,
    spine_built_crv,
    spine_ik_handle,
    ik_ctrl_grp
)

# create switch
spine_switch_grp = IK_FK_switch.IK_FK_switch_func(
    ik_ctrl_grp,
    'C_hip_fkSpine_grp',
    ik_spine_joints,
    fk_spine_joints,
    main_spine_joints,
    spine_blend_list
)

# clean outliner
spine_jnt_grp = k.createNode('transform', n='C_spine_jnt_grp')
cmds.parent(
    main_spine_joints[0],
    ik_spine_joints[0],
    fk_spine_joints[0],
    spine_jnt_grp
)

spine_ctrl_grp = k.createNode('transform', n='C_spine_ctrl_grp')
cmds.parent(
    ik_ctrl_grp,
    spine_switch_grp,
    'C_hip_fkSpine_grp',
    'C_spine_3_FK_reverse_grp',
    spine_ctrl_grp
)

spine_mod_grp = k.createNode('transform', n='C_spine_grp')
cmds.parent(
    spine_ctrl_grp,
    spine_jnt_grp,
    spine_mod_grp
)

# hide objects
for ob in [spine_built_crv, spine_crv, spine_ik_handle]:
    cmds.setAttr(ob+'.v', 0)

for ob in cmds.ls(spine_ctrl_grp, dag=True, type='joint'):
    cmds.setAttr(ob+'.v', 0)


####################################################################################
# neck
####################################################################################
neck_loc_list = [
    "C_neck_1",
    "C_neck_2",
    "C_neck_3"
]
neck_joint_list = neck.neck_built_func(neck_loc_list)

# clean outliner
neck_jnt_grp = k.createNode('transform', n='neck_jnt_grp')
neck_ctrl_grp = k.createNode('transform', n='neck_ctrl_grp')
neck_all_grp = k.createNode('transform', n='neck_grp')

cmds.parent(
    neck_joint_list[0],
    neck_jnt_grp
)
cmds.parent(
    neck_joint_list[0].replace('jnt', 'grp'),
    neck_ctrl_grp
)
cmds.parent(
    neck_ctrl_grp,
    neck_jnt_grp,
    neck_all_grp
)

####################################################################################
# head
####################################################################################
head_grp, head_ctrl, head_jnt = k_tools.create_simple_ctrl('C_head', 'C_head')

####################################################################################
# leg
####################################################################################

# generate spine joint

leg_loc_list = [
    "leg_1",
    "leg_2",
    "leg_3"
]

leg_blend_list, leg_main_list, leg_ik_list, leg_fk_list = IkFkLimb.ikFkLimbBuilder_func(leg_loc_list)

# IK FK system
FK_limb.fk_limb(leg_fk_list)
ik_leg, ik_pv = IK_limb.ik_limb(leg_ik_list, (0, 0, 25))

# Switch
leg_switch_grp = IK_FK_switch.IK_FK_switch_func(
    [ik_leg, ik_pv],
    'fk_leg_1_grp',
    leg_ik_list,
    leg_fk_list,
    leg_main_list,
    leg_blend_list
)

strechSquashLimbIK.strech_squash_limb_ik_func(
    leg_ik_list,
    'fk_leg_1_grp',
    'R_leg_ik',
    ik_leg.replace('grp', 'ikHandle'),
    leg_switch_grp.rpartition('_')[0]
)

# clean outliner
leg_ik_ctrl_grp = k.createNode('transform', n='leg_ik_ctrl_grp')
cmds.parent(ik_leg, ik_pv, leg_ik_ctrl_grp)

leg_ctrl_grp = k.createNode('transform', n='leg_ctrl_grp')
cmds.parent(leg_ik_ctrl_grp, 'fk_leg_1_grp', leg_switch_grp, leg_ctrl_grp)

leg_jnt_grp = k.createNode('transform', n='leg_jnt_grp')
cmds.parent(
    leg_main_list[0],
    leg_ik_list[0],
    leg_fk_list[0],
    leg_jnt_grp
)

leg_mod_grp = k.createNode('transform', n='leg_grp')
cmds.parent(leg_ctrl_grp, leg_jnt_grp, leg_mod_grp)

# hide objects
cmds.setAttr('ik_leg_3_ikHandle.v', 0)

# add side
for ob in cmds.ls(leg_mod_grp, dag=True):
    if cmds.objExists(ob):
        cmds.rename(ob, 'R_'+ob)

# reverse leg
leg_rev_blend_list,\
    leg_rev_main_list,\
    leg_rev_ik_list,\
    leg_rev_fk_list = mirror_joints.mirror_joint_func('R_main_leg_1_jnt')

FK_limb.fk_limb(leg_rev_fk_list)
rev_ik_leg, rev_ik_pv = IK_limb.ik_limb(leg_rev_ik_list, (0, 0, 25))

leg_rev_switch_grp = IK_FK_switch.IK_FK_switch_func(
    [rev_ik_leg, rev_ik_pv],
    'L_fk_leg_1_grp',
    leg_rev_ik_list,
    leg_rev_fk_list,
    leg_rev_main_list,
    leg_rev_blend_list
)

strechSquashLimbIK.strech_squash_limb_ik_func(
    leg_rev_ik_list,
    'L_fk_leg_1_grp',
    'L_leg_ik',
    rev_ik_leg.replace('grp', 'ikHandle'),
    leg_rev_switch_grp.rpartition('_')[0]
)

# clean outliner
leg_rev_ik_ctrl_grp = k.createNode('transform', n='L_leg_ik_ctrl_grp')
cmds.parent(rev_ik_leg, rev_ik_pv, leg_rev_ik_ctrl_grp)

leg_rev_ctrl_grp = k.createNode('transform', n='L_leg_ctrl_grp')
cmds.parent(leg_rev_ik_ctrl_grp, 'L_fk_leg_1_grp', leg_rev_switch_grp, leg_rev_ctrl_grp)

leg_rev_jnt_grp = k.createNode('transform', n='L_leg_jnt_grp')
cmds.parent(
    leg_rev_main_list[0],
    leg_rev_ik_list[0],
    leg_rev_fk_list[0],
    leg_rev_jnt_grp
)

leg_rev_mod_grp = k.createNode('transform', n='L_leg_grp')
cmds.parent(leg_rev_ctrl_grp, leg_rev_jnt_grp, leg_rev_mod_grp)

# hide
cmds.setAttr('L_ik_leg_3_ikHandle.v', 0)

# ribbons
r_upper_leg_ribbon = createRibbon.createRibbon_Func(
    'R_'+leg_main_list[0],
    'R_'+leg_main_list[1],
    2,
    'R_upperLeg',
    'R_main_leg_3_switch'
)
r_upper_leg_joint = ribbonJoints.createRibbonJoints_func(r_upper_leg_ribbon, 5, 'R_'+leg_switch_grp.rpartition('_')[0])

r_lower_leg_ribbon = createRibbon.createRibbon_Func(
    'R_'+leg_main_list[1],
    'R_'+leg_main_list[2],
    2,
    'R_lowerLeg',
    'R_main_leg_3_switch'
)
r_lower_leg_joint = ribbonJoints.createRibbonJoints_func(r_lower_leg_ribbon, 5, 'R_'+leg_switch_grp.rpartition('_')[0])

l_upper_leg_ribbon = createRibbon.createRibbon_Func(
    leg_rev_main_list[0],
    leg_rev_main_list[1],
    2,
    'L_upperLeg',
    'L_main_leg_3_switch'
)
l_upper_leg_joint = ribbonJoints.createRibbonJoints_func(l_upper_leg_ribbon, 5, leg_rev_switch_grp.rpartition('_')[0])

l_lower_leg_ribbon = createRibbon.createRibbon_Func(
    leg_rev_main_list[1],
    leg_rev_main_list[2],
    2,
    'L_lowerLeg',
    'L_main_leg_3_switch'
)
l_lower_leg_joint = ribbonJoints.createRibbonJoints_func(l_lower_leg_ribbon, 5, leg_rev_switch_grp.rpartition('_')[0])


# fix ribbon
c_leg_ribbon_ref = k.createNode('transform', n='C_leg_ribbon_ref')
cmds.connectAttr(main_spine_joints[0]+'.worldMatrix', c_leg_ribbon_ref+'.offsetParentMatrix', f=True)

r_upper_leg_ref = k.createNode('transform', n=r_upper_leg_ribbon+'_ref')
cmds.parent(r_upper_leg_ref, c_leg_ribbon_ref)
cmds.pointConstraint('R_'+leg_main_list[0], r_upper_leg_ref, mo=False)
cmds.orientConstraint('R_'+leg_main_list[0], r_upper_leg_ref, mo=False)
cmds.orientConstraint('R_'+leg_main_list[0], r_upper_leg_ref, mo=False, sk='x')

cmds.connectAttr(r_upper_leg_ref+'.worldMatrix', 'R_upperLeg_ribbon_start_grp.offsetParentMatrix', f=True)

l_upper_leg_ref = k.createNode('transform', n=l_upper_leg_ribbon+'_ref')
cmds.parent(l_upper_leg_ref, c_leg_ribbon_ref)
cmds.pointConstraint(leg_rev_main_list[0], l_upper_leg_ref, mo=False)
cmds.orientConstraint(leg_rev_main_list[0], l_upper_leg_ref, mo=False, sk='x')
cmds.xform(l_upper_leg_ref, ro=(180, 0, 0), r=True)

cmds.connectAttr(l_upper_leg_ref+'.worldMatrix', 'L_upperLeg_ribbon_start_grp.offsetParentMatrix', f=True)

# clean outliner
r_upper_leg_grp = k.createNode('transform', n='R_upperLeg_grp')
cmds.parent(
    "R_upperLeg_ribbon",
    "R_upperLeg_ribbon_start_grp",
    "R_upperLeg_ribbon_mid_grp",
    "R_upperLeg_ribbon_end_grp",
    "R_upperLeg_ribbon_ref_pos",
    "R_upperLeg_ribbon_1_jnt",
    "R_upperLeg_ribbon_2_jnt",
    "R_upperLeg_ribbon_3_jnt",
    "R_upperLeg_ribbon_4_jnt",
    "R_upperLeg_ribbon_5_jnt",
    r_upper_leg_grp
)
r_lower_leg_grp = k.createNode('transform', n='R_lowerLeg_grp')
cmds.parent(
    "R_lowerLeg_ribbon",
    "R_lowerLeg_ribbon_start_grp",
    "R_lowerLeg_ribbon_mid_grp",
    "R_lowerLeg_ribbon_end_grp",
    "R_lowerLeg_ribbon_ref_pos",
    "R_lowerLeg_ribbon_1_jnt",
    "R_lowerLeg_ribbon_2_jnt",
    "R_lowerLeg_ribbon_3_jnt",
    "R_lowerLeg_ribbon_4_jnt",
    "R_lowerLeg_ribbon_5_jnt",
    r_lower_leg_grp
)
l_upper_leg_grp = k.createNode('transform', n='L_upperLeg_grp')
cmds.parent(
    "L_upperLeg_ribbon",
    "L_upperLeg_ribbon_start_grp",
    "L_upperLeg_ribbon_mid_grp",
    "L_upperLeg_ribbon_end_grp",
    "L_upperLeg_ribbon_ref_pos",
    "L_upperLeg_ribbon_1_jnt",
    "L_upperLeg_ribbon_2_jnt",
    "L_upperLeg_ribbon_3_jnt",
    "L_upperLeg_ribbon_4_jnt",
    "L_upperLeg_ribbon_5_jnt",
    l_upper_leg_grp
)
l_lower_leg_grp = k.createNode('transform', n='L_lowerLeg_grp')
cmds.parent(
    "L_lowerLeg_ribbon",
    "L_lowerLeg_ribbon_start_grp",
    "L_lowerLeg_ribbon_mid_grp",
    "L_lowerLeg_ribbon_end_grp",
    "L_lowerLeg_ribbon_ref_pos",
    "L_lowerLeg_ribbon_1_jnt",
    "L_lowerLeg_ribbon_2_jnt",
    "L_lowerLeg_ribbon_3_jnt",
    "L_lowerLeg_ribbon_4_jnt",
    "L_lowerLeg_ribbon_5_jnt",
    l_lower_leg_grp
)

####################################################################################
# arm
####################################################################################

# generate spine joint

arm_loc_list = [
    "arm_1",
    "arm_2",
    "arm_3"
]

arm_blend_list, arm_main_list, arm_ik_list, arm_fk_list = IkFkLimb.ikFkLimbBuilder_func(arm_loc_list)

# IK FK system
FK_limb.fk_limb(arm_fk_list)
ik_hand, ik_pv = IK_limb.ik_limb(arm_ik_list, (0, 0, -25))

# Switch
arm_switch_grp = IK_FK_switch.IK_FK_switch_func(
    [ik_hand, ik_pv],
    'fk_arm_1_grp',
    arm_ik_list,
    arm_fk_list,
    arm_main_list,
    arm_blend_list
)

strechSquashLimbIK.strech_squash_limb_ik_func(
    arm_ik_list,
    'fk_arm_1_grp',
    'arm_ik',
    ik_hand.replace('grp', 'ikHandle'),
    arm_switch_grp.rpartition('_')[0]
)

# clean outliner
arm_ik_ctrl_grp = k.createNode('transform', n='arm_ik_ctrl_grp')
cmds.parent(ik_hand, ik_pv, arm_ik_ctrl_grp)

arm_ctrl_grp = k.createNode('transform', n='arm_ctrl_grp')
cmds.parent(arm_ik_ctrl_grp, 'fk_arm_1_grp', arm_switch_grp, arm_ctrl_grp)

arm_jnt_grp = k.createNode('transform', n=arm_ctrl_grp)
cmds.parent(
    arm_main_list[0],
    arm_ik_list[0],
    arm_fk_list[0],
    arm_jnt_grp
)

arm_mod_grp = k.createNode('transform', n='arm_grp')
cmds.parent(arm_ctrl_grp, arm_jnt_grp, arm_mod_grp)

# hide objects
cmds.setAttr('ik_arm_3_ikHandle.v', 0)

# add side
for ob in cmds.ls(arm_mod_grp, dag=True):
    if cmds.objExists(ob):
        cmds.rename(ob, 'R_'+ob)

# reverse arm
arm_rev_blend_list,\
    arm_rev_main_list,\
    arm_rev_ik_list,\
    arm_rev_fk_list = mirror_joints.mirror_joint_func('R_main_arm_1_jnt')

FK_limb.fk_limb(arm_rev_fk_list)
rev_ik_hand, rev_ik_pv = IK_limb.ik_limb(arm_rev_ik_list, (0, 0, -25))

arm_rev_switch_grp = IK_FK_switch.IK_FK_switch_func(
    [rev_ik_hand, rev_ik_pv],
    'L_fk_arm_1_grp',
    arm_rev_ik_list,
    arm_rev_fk_list,
    arm_rev_main_list,
    arm_rev_blend_list
)

strechSquashLimbIK.strech_squash_limb_ik_func(
    arm_rev_ik_list,
    'L_fk_arm_1_grp',
    'L_arm_ik',
    rev_ik_hand.replace('grp', 'ikHandle'),
    arm_rev_switch_grp.rpartition('_')[0]
)

# clean outliner
arm_rev_ik_ctrl_grp = k.createNode('transform', n='L_arm_ik_ctrl_grp')
cmds.parent(rev_ik_hand, rev_ik_pv, arm_rev_ik_ctrl_grp)

arm_rev_ctrl_grp = k.createNode('transform', n='L_arm_ctrl_grp')
cmds.parent(arm_rev_ik_ctrl_grp, 'L_fk_arm_1_grp', arm_rev_switch_grp, arm_rev_ctrl_grp)

arm_rev_jnt_grp = k.createNode('transform', n='L_arm_jnt_grp')
cmds.parent(
    arm_rev_main_list[0],
    arm_rev_ik_list[0],
    arm_rev_fk_list[0],
    arm_rev_jnt_grp
)

arm_rev_mod_grp = k.createNode('transform', n='L_arm_grp')
cmds.parent(arm_rev_ctrl_grp, arm_rev_jnt_grp, arm_rev_mod_grp)

# hide
cmds.setAttr('L_ik_arm_3_ikHandle.v', 0)

# ribbons
r_upper_arm_ribbon = createRibbon.createRibbon_Func(
    'R_'+arm_main_list[0],
    'R_'+arm_main_list[1],
    2,
    'R_upperArm',
    'R_main_arm_3_switch'
)
r_upper_arm_joint = ribbonJoints.createRibbonJoints_func(r_upper_arm_ribbon, 5, 'R_'+arm_switch_grp.rpartition('_')[0])

r_lower_arm_ribbon = createRibbon.createRibbon_Func(
    'R_'+arm_main_list[1],
    'R_'+arm_main_list[2],
    2,
    'R_lowerArm',
    'R_main_arm_3_switch'
)
r_lower_arm_joint = ribbonJoints.createRibbonJoints_func(r_lower_arm_ribbon, 5, 'R_'+arm_switch_grp.rpartition('_')[0])

l_upper_arm_ribbon = createRibbon.createRibbon_Func(
    arm_rev_main_list[0],
    arm_rev_main_list[1],
    2,
    'L_upperArm',
    'L_main_arm_3_switch'
)
l_upper_arm_joint = ribbonJoints.createRibbonJoints_func(l_upper_arm_ribbon, 5, arm_rev_switch_grp.rpartition('_')[0])

l_lower_arm_ribbon = createRibbon.createRibbon_Func(
    arm_rev_main_list[1],
    arm_rev_main_list[2],
    2,
    'L_lowerArm',
    'L_main_arm_3_switch'
)
l_lower_arm_joint = ribbonJoints.createRibbonJoints_func(l_lower_arm_ribbon, 5, arm_rev_switch_grp.rpartition('_')[0])

# fix ribbon
c_arm_ribbon_ref = k.createNode('transform', n='C_arm_ribbon_ref')
cmds.connectAttr(main_spine_joints[0]+'.worldMatrix', c_arm_ribbon_ref+'.offsetParentMatrix', f=True)

r_upper_arm_ref = k.createNode('transform', n=r_upper_arm_ribbon+'_ref')
cmds.parent(r_upper_arm_ref, c_arm_ribbon_ref)
cmds.pointConstraint('R_'+arm_main_list[0], r_upper_arm_ref, mo=False)
cmds.orientConstraint('R_'+arm_main_list[0], r_upper_arm_ref, mo=False)
cmds.orientConstraint('R_'+arm_main_list[0], r_upper_arm_ref, mo=False, sk='x')

cmds.connectAttr(r_upper_arm_ref+'.worldMatrix', 'R_upperArm_ribbon_start_grp.offsetParentMatrix', f=True)

l_upper_arm_ref = k.createNode('transform', n=l_upper_arm_ribbon+'_ref')
cmds.parent(l_upper_arm_ref, c_arm_ribbon_ref)
cmds.pointConstraint(arm_rev_main_list[0], l_upper_arm_ref, mo=False)
cmds.orientConstraint(arm_rev_main_list[0], l_upper_arm_ref, mo=False)
cmds.orientConstraint(arm_rev_main_list[0], l_upper_arm_ref, mo=False, sk='x')

cmds.connectAttr(l_upper_arm_ref+'.worldMatrix', 'L_upperArm_ribbon_start_grp.offsetParentMatrix', f=True)
#cmds.error()
# clean outliner
r_upper_arm_grp = k.createNode('transform', n='R_upperArm_grp')
cmds.parent(
    "R_upperArm_ribbon",
    "R_upperArm_ribbon_start_grp",
    "R_upperArm_ribbon_mid_grp",
    "R_upperArm_ribbon_end_grp",
    "R_upperArm_ribbon_ref_pos",
    "R_upperArm_ribbon_1_jnt",
    "R_upperArm_ribbon_2_jnt",
    "R_upperArm_ribbon_3_jnt",
    "R_upperArm_ribbon_4_jnt",
    "R_upperArm_ribbon_5_jnt",
    r_upper_arm_grp
)
r_lower_arm_grp = k.createNode('transform', n='R_lowerArm_grp')
cmds.parent(
    "R_lowerArm_ribbon",
    "R_lowerArm_ribbon_start_grp",
    "R_lowerArm_ribbon_mid_grp",
    "R_lowerArm_ribbon_end_grp",
    "R_lowerArm_ribbon_ref_pos",
    "R_lowerArm_ribbon_1_jnt",
    "R_lowerArm_ribbon_2_jnt",
    "R_lowerArm_ribbon_3_jnt",
    "R_lowerArm_ribbon_4_jnt",
    "R_lowerArm_ribbon_5_jnt",
    r_lower_arm_grp
)
l_upper_arm_grp = k.createNode('transform', n='L_upperArm_grp')
cmds.parent(
    "L_upperArm_ribbon",
    "L_upperArm_ribbon_start_grp",
    "L_upperArm_ribbon_mid_grp",
    "L_upperArm_ribbon_end_grp",
    "L_upperArm_ribbon_ref_pos",
    "L_upperArm_ribbon_1_jnt",
    "L_upperArm_ribbon_2_jnt",
    "L_upperArm_ribbon_3_jnt",
    "L_upperArm_ribbon_4_jnt",
    "L_upperArm_ribbon_5_jnt",
    l_upper_arm_grp
)
l_lower_arm_grp = k.createNode('transform', n='L_lowerArm_grp')
cmds.parent(
    "L_lowerArm_ribbon",
    "L_lowerArm_ribbon_start_grp",
    "L_lowerArm_ribbon_mid_grp",
    "L_lowerArm_ribbon_end_grp",
    "L_lowerArm_ribbon_ref_pos",
    "L_lowerArm_ribbon_1_jnt",
    "L_lowerArm_ribbon_2_jnt",
    "L_lowerArm_ribbon_3_jnt",
    "L_lowerArm_ribbon_4_jnt",
    "L_lowerArm_ribbon_5_jnt",
    l_lower_arm_grp
)

####################################################################################
# foot
####################################################################################

# foot roll
foot_loc_list = [
    'R_footRoll',
    'R_hellSlide',
    'R_ballSlide',
    'R_toeSlide',
    'R_sideOut',
    'R_sideIn',
    'R_hell',
    'R_toe',
    'R_ball',
    'R_ankle'
]

footRoll.builtFootRoll_func('foot', foot_loc_list, 'R')

# fk foot
FK_foot_loc_list = ['R_ankle', 'R_ball', 'R_toe']

FK_foot.fk_foot_build(FK_foot_loc_list)

# foot switch
foot_switch.foot_switch_func(
    'R_footRoll_grp',
    'R_hellSlide_grp',
    'R_ik_leg_3_ikHandle',
    'R_ankle_FK_grp',
    'R_fk_leg_3_ctrl',
    'R_main_leg_3_switch'
)

cmds.parent('R_ankle_main_jnt', 'R_'+leg_jnt_grp)

# foot roll reversed
footRoll.builtFootRoll_func('foot', foot_loc_list, 'L', True)

FK_foot.fk_foot_build(FK_foot_loc_list, True)

foot_switch.foot_switch_func(
    'L_footRoll_grp',
    'L_hellSlide_grp',
    'L_ik_leg_3_ikHandle',
    'L_ankle_FK_grp',
    'L_fk_leg_3_ctrl',
    'L_main_leg_3_switch'
)

cmds.parent('L_ankle_main_jnt', 'L_'+leg_jnt_grp)


####################################################################################
# scapula
####################################################################################
scapula_joint = scapula.built_scapula_func('scapula', 'arm_1')

scapula.reverse_scapula_func(scapula_joint)

####################################################################################
# hand
####################################################################################

# create hands
hand_joint_list = hand.build_hand_func(
    [
        "R_pinky_1",
        "R_annular_1",
        "R_middleFinger_1",
        "R_index_1",
        "R_thumb_1"
    ],
    'R_main_arm_3_jnt'
)

hand_reversed_joint_list = hand.reverse_hand_func(
    [
        "R_pinky_1",
        "R_annular_1",
        "R_middleFinger_1",
        "R_index_1",
        "R_thumb_1"
    ],
    'L_main_arm_3_jnt'
)

# clean outliner
hand_jnt_grp = k.createNode('transform', n='R_hand_jnt_grp')
hand_reversed_jnt_grp = k.createNode('transform', n='L_hand_jnt_grp')
hand_all_jnt_grp = k.createNode('transform', n='hand_jnt_grp')

cmds.parent(
    hand_jnt_grp,
    hand_reversed_jnt_grp,
    hand_all_jnt_grp
)
cmds.parent(
    "R_pinky_1_jnt",
    "R_annular_1_jnt",
    "R_middleFinger_1_jnt",
    "R_index_1_jnt",
    "R_thumb_1_jnt",
    hand_jnt_grp
)
cmds.parent(
    "L_pinky_1_jnt",
    "L_annular_1_jnt",
    "L_middleFinger_1_jnt",
    "L_index_1_jnt",
    "L_thumb_1_jnt",
    hand_reversed_jnt_grp
)

hand_ctrl_grp = k.createNode('transform', n='hand_ctrl_grp')
cmds.parent(
    "R_main_arm_3_jnt_offset_grp",
    "L_main_arm_3_jnt_offset_grp",
    hand_ctrl_grp
)

hand_all_grp = k.createNode('transform', n='hand_grp')
cmds.parent(
    hand_ctrl_grp,
    hand_all_jnt_grp,
    hand_all_grp
)


####################################################################################
# switch
####################################################################################

# spine
fk_spine_follow = k_tools.space_switch(
    'C_COG_ctrl',
    ['C_main_ctrl', 'C_walk_ctrl'],
    'C_hip_fkSpine_grp',
    'C_spine_12_main_switch',
    ['translate', 'scale', 'shear']
)
fk_spine_rev_follow = k_tools.space_switch(
    'C_COG_ctrl',
    ['C_main_ctrl', 'C_walk_ctrl'],
    'C_spine_3_FK_reverse_grp',
    'C_spine_3_FK_reverse_grp',
    ['translate', 'scale', 'shear']
)
ik_spine_follow = k_tools.space_switch(
    'C_COG_ctrl',
    ['C_main_ctrl', 'C_walk_ctrl'],
    ['C_hip_ikSpine_grp', 'C_spine_ikSpine_grp', 'C_shoulder_ikSpine_grp'],
    'C_spine_12_main_switch',
    ['translate', 'scale', 'shear']
)

# neck
neck_jnt_grp = k.createNode('transform', n='C_neck_1_jnt_grp')
cmds.xform(
    neck_jnt_grp,
    t=cmds.xform('C_neck_1_jnt', q=True, t=True, ws=True),
    ws=True
)
cmds.xform(
    neck_jnt_grp,
    ro=cmds.xform('C_neck_1_jnt', q=True, ro=True, ws=True),
    ws=True
)
cmds.xform(
    neck_jnt_grp,
    s=cmds.xform('C_neck_1_jnt', q=True, s=True, ws=True),
    ws=True
)
cmds.parent(neck_jnt_grp, cmds.listRelatives('C_neck_1_jnt', p=True)[0])
cmds.parent('C_neck_1_jnt', neck_jnt_grp)

neck_follow = k_tools.space_switch(
    'C_spine_12_main_jnt',
    ['C_main_ctrl', 'C_COG_ctrl'],
    ['C_neck_1_grp'],
    'C_neck_1_ctrl',
    ['translate', 'scale', 'shear']
)

neck_jnt_follow = k_tools.space_switch(
    'C_spine_12_main_jnt',
    ['C_main_ctrl', 'C_COG_ctrl'],
    neck_jnt_grp,
    None,
    ['translate', 'scale', 'shear']
)
cmds.connectAttr(
    'C_neck_1_ctrl.C_neck_1_grp_space',
    'C_neck_1_jnt_grp.C_neck_1_jnt_grp_space',
    f=True
)

# head
c_head_follow = k_tools.space_switch(
    'C_neck_3_jnt',
    [
        'C_walk_ctrl',
        'C_main_ctrl',
        'C_COG_ctrl',
        'C_spine_1_main_jnt',
        'C_spine_12_main_jnt'
    ],
    'C_head_grp',
    'C_head_ctrl',
    ['translate', 'scale', 'shear']
)

# L leg
l_fk_leg_follow = k_tools.space_switch(
    'C_spine_1_main_jnt',
    ['C_main_ctrl', 'C_walk_ctrl', 'C_COG_ctrl'],
    'L_fk_leg_1_grp',
    'L_main_leg_3_switch',
    ['translate', 'scale', 'shear']
)
l_ik_leg_follow = k_tools.space_switch(
    'C_walk_ctrl',
    ['C_main_ctrl', 'C_COG_ctrl', 'C_spine_1_main_jnt'],
    'L_ik_leg_3_grp',
    'L_main_leg_3_switch',
    ['scale', 'shear']
)
l_ik_leg_pv_follow = k_tools.space_switch(
    'L_ik_leg_3_ctrl',
    ['C_walk_ctrl', 'C_main_ctrl', 'C_COG_ctrl', 'C_spine_1_main_jnt'],
    'L_ik_leg_3_pvGrp',
    'L_main_leg_3_switch',
    ['scale', 'shear']
)
l_ik_leg_jnt_follow = k_tools.space_switch(
    'C_spine_1_main_jnt',
    ['C_walk_ctrl', 'C_main_ctrl', 'C_COG_ctrl'],
    'L_ik_leg_1_jnt',
    None,
    ['translate', 'scale', 'shear']
)

# R leg
r_fk_leg_follow = k_tools.space_switch(
    'C_spine_1_main_jnt',
    ['C_main_ctrl', 'C_walk_ctrl', 'C_COG_ctrl'],
    'R_fk_leg_1_grp',
    'R_main_leg_3_switch',
    ['translate', 'scale', 'shear']
)
r_ik_leg_follow = k_tools.space_switch(
    'C_walk_ctrl',
    ['C_main_ctrl', 'C_COG_ctrl', 'C_spine_1_main_jnt'],
    'R_ik_leg_3_grp',
    'R_main_leg_3_switch',
    ['scale', 'shear']
)
r_ik_leg_pv_follow = k_tools.space_switch(
    'R_ik_leg_3_ctrl',
    ['C_walk_ctrl', 'C_main_ctrl', 'C_COG_ctrl', 'C_spine_1_main_jnt'],
    'R_ik_leg_3_pvGrp',
    'R_main_leg_3_switch',
    ['scale', 'shear']
)
r_ik_leg_jnt_follow = k_tools.space_switch(
    'C_spine_1_main_jnt',
    ['C_walk_ctrl', 'C_main_ctrl', 'C_COG_ctrl'],
    'R_ik_leg_1_jnt',
    None,
    ['translate', 'scale', 'shear']
)

# R scapula
r_scapula_follow = k_tools.space_switch(
    'C_spine_12_main_jnt',
    [
        'C_main_ctrl',
        'C_walk_ctrl',
        'C_COG_ctrl',
        'C_spine_1_main_jnt'],
    'R_scapula_grp',
    'R_main_arm_3_switch',
    ['translate', 'scale', 'shear']
)

# R arm
r_fk_arm_follow = k_tools.space_switch(
    'R_scapula_jnt',
    [
        'C_main_ctrl',
        'C_walk_ctrl',
        'C_COG_ctrl',
        'C_spine_1_main_jnt',
        'C_spine_12_main_jnt'
    ],
    'R_fk_arm_1_grp',
    'R_main_arm_3_switch',
    ['translate', 'scale', 'shear']
)
r_ik_arm_follow = k_tools.space_switch(
    'C_main_ctrl',
    [
        'C_walk_ctrl',
        'C_COG_ctrl',
        'C_spine_1_main_jnt',
        'C_spine_12_main_jnt',
        'C_head_jnt'
    ],
    'R_ik_arm_3_grp',
    'R_main_arm_3_switch',
    ['scale', 'shear']
)
r_ik_arm_pv_follow = k_tools.space_switch(
    'R_ik_arm_3_ctrl',
    [
        'C_main_ctrl',
        'C_walk_ctrl',
        'C_COG_ctrl',
        'C_spine_1_main_jnt',
        'C_spine_12_main_jnt',
        'R_scapula_jnt'
    ],
    'R_ik_arm_3_pvGrp',
    'R_main_arm_3_switch',
    ['scale', 'shear']
)
r_ik_arm_jnt_follow = k_tools.space_switch(
    'R_scapula_jnt',
    [
        'C_walk_ctrl',
        'C_main_ctrl',
        'C_COG_ctrl',
        'C_spine_1_main_jnt',
        'C_spine_12_main_jnt'
    ],
    'R_ik_arm_1_jnt',
    None,
    ['translate', 'scale', 'shear']
)

# L scapula
l_scapula_follow = k_tools.space_switch(
    'C_spine_12_main_jnt',
    [
        'C_main_ctrl',
        'C_walk_ctrl',
        'C_COG_ctrl',
        'C_spine_1_main_jnt'],
    'L_scapula_grp',
    'L_main_arm_3_switch',
    ['translate', 'scale', 'shear']
)

# L arm
l_fk_arm_follow = k_tools.space_switch(
    'L_scapula_jnt',
    [
        'C_main_ctrl',
        'C_walk_ctrl',
        'C_COG_ctrl',
        'C_spine_1_main_jnt',
        'C_spine_12_main_jnt'
    ],
    'L_fk_arm_1_grp',
    'L_main_arm_3_switch',
    ['translate', 'scale', 'shear']
)
l_ik_arm_follow = k_tools.space_switch(
    'C_main_ctrl',
    [
        'C_walk_ctrl',
        'C_COG_ctrl',
        'C_spine_1_main_jnt',
        'C_spine_12_main_jnt',
        'C_head_jnt'
    ],
    'L_ik_arm_3_grp',
    'L_main_arm_3_switch',
    ['scale', 'shear']
)
l_ik_arm_pv_follow = k_tools.space_switch(
    'L_ik_arm_3_ctrl',
    [
        'C_main_ctrl',
        'C_walk_ctrl',
        'C_COG_ctrl',
        'C_spine_1_main_jnt',
        'C_spine_12_main_jnt',
        'L_scapula_jnt'
    ],
    'L_ik_arm_3_pvGrp',
    'L_main_arm_3_switch',
    ['scale', 'shear']
)
l_ik_arm_jnt_follow = k_tools.space_switch(
    'L_scapula_jnt',
    [
        'C_walk_ctrl',
        'C_main_ctrl',
        'C_COG_ctrl',
        'C_spine_1_main_jnt',
        'C_spine_12_main_jnt'
    ],
    'L_ik_arm_1_jnt',
    None,
    ['translate', 'scale', 'shear']
)

####################################################################################
# skeleton
####################################################################################
skeleton_dic = create_skeleton.create_skeleton_func()

# parent joints
cmds.parent(
    'R_upperLeg_ribbon_1_skn',
    'L_upperLeg_ribbon_1_skn',
    'C_spine_1_main_skn'
)
cmds.parent(
    'R_scapula_skn',
    'L_scapula_skn',
    'C_spine_12_main_skn'
)
cmds.parent(
    "R_thumb_1_skn",
    "R_index_1_skn",
    "R_middleFinger_1_skn",
    "R_annular_1_skn",
    "R_pinky_1_skn",
    "R_main_arm_3_skn"
)
cmds.parent(
    "L_thumb_1_skn",
    "L_index_1_skn",
    "L_middleFinger_1_skn",
    "L_annular_1_skn",
    "L_pinky_1_skn",
    "L_main_arm_3_skn"
)

# connect joint
create_skeleton.connect_skeleton(skeleton_dic)

####################################################################################
# clean outliner
####################################################################################

ref_grp = k.createNode('transform', n='ref_grp')

cmds.parent(
    "L_fk_arm_1_grp_ref",
    "L_scapula_jnt_ref",
    "L_ik_arm_3_grp_ref",
    "L_ik_arm_3_pvGrp_ref",
    "L_ik_arm_3_ctrl_ref",
    "L_ik_arm_1_jnt_ref",
    "L_scapula_grp_ref",
    "R_ik_arm_1_jnt_ref",
    "R_ik_arm_3_ctrl_ref",
    "R_ik_arm_3_pvGrp_ref",
    "C_head_jnt_ref",
    "R_ik_arm_3_grp_ref",
    "R_scapula_jnt_ref",
    "R_fk_arm_1_grp_ref",
    "C_neck_3_jnt_ref",
    "C_spine_1_main_jnt_ref",
    "L_fk_leg_1_grp_ref",
    "L_ik_leg_3_grp_ref",
    "L_ik_leg_3_pvGrp_ref",
    "L_ik_leg_3_ctrl_ref",
    "L_ik_leg_1_jnt_ref",
    "R_fk_leg_1_grp_ref",
    "R_ik_leg_3_grp_ref",
    "R_ik_leg_3_pvGrp_ref",
    "R_ik_leg_3_ctrl_ref",
    "R_ik_leg_1_jnt_ref",
    "R_scapula_grp_ref",
    "C_head_grp_ref",
    "C_neck_1_jnt_grp_ref",
    "C_spine_12_main_jnt_ref",
    "C_neck_1_grp_ref",
    "C_shoulder_ikSpine_grp_ref",
    "C_spine_ikSpine_grp_ref",
    "C_hip_ikSpine_grp_ref",
    "C_spine_3_FK_reverse_grp_ref",
    "C_walk_ctrl_ref",
    "C_main_ctrl_ref",
    "C_COG_ctrl_ref",
    "C_hip_fkSpine_grp_ref",
    'C_arm_ribbon_ref',
    'C_leg_ribbon_ref',
    ref_grp
)

cmds.parent(
    'R_scapula_grp_follow',
    'R_upperArm_grp',
    'R_lowerArm_grp',
    "R_scapula_jnt",
    "R_arm_ctrl_grp"
)

cmds.parent(
    'L_scapula_grp_follow',
    'L_upperArm_grp',
    'L_lowerArm_grp',
    "L_scapula_jnt",
    "L_arm_ctrl_grp"
)

cmds.parent(
    "C_head_grp_follow",
    "neck_grp",
    "C_head_jnt",
    "C_spine_grp"
)

cmds.parent(
    "R_upperLeg_grp",
    "R_lowerLeg_grp",
    "R_leg_ctrl_grp"
)

cmds.parent(
    "L_upperLeg_grp",
    "L_lowerLeg_grp",
    "L_leg_ctrl_grp"
)

all_grp = k.createNode('transform', n='Lea_rig')
jnt_grp = k.createNode('transform', n='deformation_system')
ctrl_grp = k.createNode('transform', n='motion_system')
geo = k.createNode('transform', n='geometry')

cmds.parent(
    jnt_grp,
    ctrl_grp,
    geo,
    all_grp
)

cmds.parent(
    "C_main_grp",
    "C_spine_grp",
    "R_leg_grp",
    "L_leg_grp",
    "R_arm_grp",
    "L_arm_grp",
    "hand_grp",
    "ref_grp",
    ctrl_grp
)

cmds.parent('C_spine_1_main_skn', jnt_grp)

for ob in cmds.ls(type='joint'):
    if not 'skn' in ob:
        if not cmds.listConnections(ob+'.v', s=True, d=False):
            cmds.setAttr(ob+'.v', 0)


# ctrl shapes
create_controls.switch_shape()
