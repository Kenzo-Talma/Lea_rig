import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

skeleton_list = [
    [
        "C_spine_1_main_jnt",
        "C_spine_2_main_jnt",
        "C_spine_3_main_jnt",
        "C_spine_4_main_jnt",
        "C_spine_5_main_jnt",
        "C_spine_6_main_jnt",
        "C_spine_7_main_jnt",
        "C_spine_8_main_jnt",
        "C_spine_9_main_jnt",
        "C_spine_10_main_jnt",
        "C_spine_11_main_jnt",
        "C_spine_12_main_jnt",
        "C_neck_1_jnt",
        "C_neck_2_jnt",
        "C_neck_3_jnt",
        'C_head_jnt'
    ],
    [
        "R_upperLeg_ribbon_1_jnt",
        "R_upperLeg_ribbon_2_jnt",
        "R_upperLeg_ribbon_3_jnt",
        "R_upperLeg_ribbon_4_jnt",
        "R_lowerLeg_ribbon_1_jnt",
        "R_lowerLeg_ribbon_2_jnt",
        "R_lowerLeg_ribbon_3_jnt",
        "R_lowerLeg_ribbon_4_jnt",
        "R_ankle_main_jnt",
        "R_ball_main_jnt",
        "R_toe_main_jnt"
    ],
    [
        "R_scapula_jnt",
        "R_upperArm_ribbon_1_jnt",
        "R_upperArm_ribbon_2_jnt",
        "R_upperArm_ribbon_3_jnt",
        "R_upperArm_ribbon_4_jnt",
        "R_lowerArm_ribbon_1_jnt",
        "R_lowerArm_ribbon_2_jnt",
        "R_lowerArm_ribbon_3_jnt",
        "R_lowerArm_ribbon_4_jnt",
        "R_main_arm_3_jnt"
    ],
    [
        "R_thumb_1_jnt",
        "R_thumb_2_jnt",
        "R_thumb_3_jnt",
        "R_thumb_4_jnt"
    ],
    [
        "R_index_1_jnt",
        "R_index_2_jnt",
        "R_index_3_jnt",
        "R_index_4_jnt",
        "R_index_5_jnt"
    ],
    [
        "R_middleFinger_1_jnt",
        "R_middleFinger_2_jnt",
        "R_middleFinger_3_jnt",
        "R_middleFinger_4_jnt",
        "R_middleFinger_5_jnt"
    ],
    [
        "R_annular_1_jnt",
        "R_annular_2_jnt",
        "R_annular_3_jnt",
        "R_annular_4_jnt",
        "R_annular_5_jnt"
    ],
    [
        "R_pinky_1_jnt",
        "R_pinky_2_jnt",
        "R_pinky_3_jnt",
        "R_pinky_4_jnt",
        "R_pinky_5_jnt"
    ],
    [
        "L_upperLeg_ribbon_1_jnt",
        "L_upperLeg_ribbon_2_jnt",
        "L_upperLeg_ribbon_3_jnt",
        "L_upperLeg_ribbon_4_jnt",
        "L_lowerLeg_ribbon_1_jnt",
        "L_lowerLeg_ribbon_2_jnt",
        "L_lowerLeg_ribbon_3_jnt",
        "L_lowerLeg_ribbon_4_jnt",
        "L_ankle_main_jnt",
        "L_ball_main_jnt",
        "L_toe_main_jnt"
    ],
    [
        "L_scapula_jnt",
        "L_upperArm_ribbon_1_jnt",
        "L_upperArm_ribbon_2_jnt",
        "L_upperArm_ribbon_3_jnt",
        "L_upperArm_ribbon_4_jnt",
        "L_lowerArm_ribbon_1_jnt",
        "L_lowerArm_ribbon_2_jnt",
        "L_lowerArm_ribbon_3_jnt",
        "L_lowerArm_ribbon_4_jnt",
        "L_main_arm_3_jnt"
    ],
    [
        "L_thumb_1_jnt",
        "L_thumb_2_jnt",
        "L_thumb_3_jnt",
        "L_thumb_4_jnt"
    ],
    [
        "L_index_1_jnt",
        "L_index_2_jnt",
        "L_index_3_jnt",
        "L_index_4_jnt",
        "L_index_5_jnt"
    ],
    [
        "L_middleFinger_1_jnt",
        "L_middleFinger_2_jnt",
        "L_middleFinger_3_jnt",
        "L_middleFinger_4_jnt",
        "L_middleFinger_5_jnt"
    ],
    [
        "L_annular_1_jnt",
        "L_annular_2_jnt",
        "L_annular_3_jnt",
        "L_annular_4_jnt",
        "L_annular_5_jnt"
    ],
    [
        "L_pinky_1_jnt",
        "L_pinky_2_jnt",
        "L_pinky_3_jnt",
        "L_pinky_4_jnt",
        "L_pinky_5_jnt"
    ],
]

def create_skeleton_func():
    # create dic
    skeleton_dic = {}
    # main loop
    for joint_list in skeleton_list:
        for n, jnt in enumerate(joint_list):
            skn = k.createNode('joint', n=jnt.replace('jnt', 'skn'))
            cmds.setAttr(jnt+'.v', 0)
            cmds.xform(
                skn,
                t=cmds.xform(jnt, q=True, t=True, ws=True),
                ws=True
            )
            cmds.xform(
                skn,
                ro=cmds.xform(jnt, q=True, ro=True, ws=True),
                ws=True
            )
            cmds.xform(
                skn,
                s=cmds.xform(jnt, q=True, s=True, ws=True),
                ws=True
            )
            if not n == 0:
                cmds.parent(
                    skn,
                    joint_list[n-1].replace('jnt', 'skn')
                )
            skeleton_dic[jnt] = skn

    return skeleton_dic


def connect_skeleton(skeleton_dic=None):
    # main loop
    for jnt in skeleton_dic:
        # open dic
        skn = skeleton_dic[jnt]

        # def name
        mlm = skn+'_mlm'

        # if joint have parent
        if cmds.listRelatives(skn, p=True, type='joint'):
            # create multMatrix
            mlm = k.createNode('multMatrix', n=mlm)

            # connect multMatrix
            cmds.connectAttr(jnt+'.worldMatrix[0]', mlm+'.matrixIn[0]', f=True)
            cmds.connectAttr(
                cmds.listRelatives(skn, p=True)[0]+'.worldInverseMatrix[0]',
                mlm+'.matrixIn[1]',
                f=True
            )
            cmds.connectAttr(mlm+'.matrixSum', skn+'.offsetParentMatrix', f=True)

        # if it's the first joint
        else:
            cmds.connectAttr(jnt+'.worldMatrix', skn+'.offsetParentMatrix', f=True)

        # reset joint
        cmds.xform(skn, t=(0, 0, 0))
        cmds.xform(skn, ro=(0, 0, 0))
        cmds.xform(skn, s=(1, 1, 1))
        for at in ['X', 'Y', 'Z']:
            cmds.setAttr(f'{skn}.jointOrient{at}', 0)


####################################################################################
# test
####################################################################################

#skel_dic = create_skeleton_func(skeleton_list)
#print(skel_dic)
#connect_skeleton(skel_dic)
