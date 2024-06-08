import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

main_dic = {
    "C_main_ctrl": {
        'shape': 'circleY',
        'scale': (50, 50, 50),
        'color': 17
    },
    "C_walk_ctrl": {
        'shape': 'circleY',
        'scale': (40, 40, 40),
        'color': 17
    },
    "C_COG_ctrl": {
        'shape': 'circleY',
        'scale': (25, 25, 25),
        'color': 17
    },
    "C_hip_ikSpine_ctrl": {
        'shape': 'circleX',
        'scale': (20, 20, 15),
        'color': 17
    },
    "C_spine_ikSpine_ctrl": {
        'shape': 'circleX',
        'scale': (15, 15, 10),
        'color': 17
    },
    "C_shoulder_ikSpine_ctrl": {
        'shape': 'circleX',
        'scale': (20, 20, 15),
        'color': 17
    },
    "C_spine_12_main_switch": {
        'shape': 'diamond',
        'scale': (3, 3, 3),
        'color': 17
    },
    "C_hip_fkSpine_ctrl": {
        'shape': 'circleX',
        'scale': (20, 20, 17),
        'color': 17
    },
    "C_spineLow_fkSpine_ctrl": {
        'shape': 'circleX',
        'scale': (15, 15, 10),
        'color': 22
    },
    "C_spineUp_fkSpine_ctrl": {
        'shape': 'circleX',
        'scale': (15, 15, 10),
        'color': 22
    },
    "C_shoulder_fkSpine_ctrl": {
        'shape': 'circleX',
        'scale': (16, 16, 14),
        'color': 22
    },
    "C_hip_fkSpine_reverse_ctrl": {
        'shape': 'circleX',
        'scale': (17, 17, 15),
        'color': 22
    },
    "C_head_ctrl": {
        'shape': 'circleY',
        'scale': (10, 10, 10),
        'color': 17
    },
    "C_neck_1_ctrl": {
        'shape': 'circleY',
        'scale': (10, 10, 10),
        'color': 17
    },
    "R_ik_leg_3_ctrl": {
        'shape': 'cube',
        'scale': (5, 5, 5),
        'color': 13
    },
    "R_hellSlide_ctrl": {
        'shape': 'circleY',
        'scale': (1, 1, 1),
        'color': 13
    },
    "R_ballSlide_ctrl": {
        'shape': 'circleY',
        'scale': (1, 1, 1),
        'color': 13
    },
    "R_toeSlide_ctrl": {
        'shape': 'circleY',
        'scale': (1, 1, 1),
        'color': 13
    },
    "R_sideOut_ctrl": {
        'shape': 'circleZ',
        'scale': (1, 1, 1),
        'color': 13
    },
    "R_sideIn_ctrl": {
        'shape': 'circleZ',
        'scale': (1, 1, 1),
        'color': 13
    },
    "R_hell_ctrl": {
        'shape': 'circleY',
        'scale': (1, 1, 1),
        'color': 13
    },
    "R_toe_ctrl": {
        'shape': 'circleX',
        'scale': (1, 1, 1),
        'color': 13
    },
    "R_ball_ctrl": {
        'shape': 'circleX',
        'scale': (1, 1, 1),
        'color': 13
    },
    "R_ankle_ctrl": {
        'shape': 'circleX',
        'scale': (1, 1, 1),
        'color': 13
    },
    "R_footRoll_ctrl": {
        'shape': 'diamond',
        'scale': (1, 1, 1),
        'color': 13
    },
    "R_ik_leg_3_pvCtrl": {
        'shape': 'diamond',
        'scale': (5, 5, 5),
        'color': 13
    },
    "R_main_leg_3_switch": {
        'shape': 'diamond',
        'scale': (5, 5, 5),
        'color': 13
    },
    "R_fk_leg_1_ctrl": {
        'shape': 'circleX',
        'scale': (10, 10, 10),
        'color': 20
    },
    "R_fk_leg_2_ctrl": {
        'shape': 'circleX',
        'scale': (10, 10, 10),
        'color': 20
    },
    "R_fk_leg_3_ctrl": {
        'shape': 'circleX',
        'scale': (10, 10, 10),
        'color': 20
    },
    "R_ankle_FK_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 20
    },
    "R_ball_FK_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 20
    },
    "R_toe_FK_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 20
    },
    "R_upperLeg_ribbon_start_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 4
    },
    "R_upperLeg_ribbon_mid_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 4
    },
    "R_upperLeg_ribbon_end_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 4
    },
    "R_lowerLeg_ribbon_start_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 4
    },
    "R_lowerLeg_ribbon_mid_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 4
    },
    "R_lowerLeg_ribbon_end_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 4
    },
    "L_ik_leg_3_ctrl": {
        'shape': 'cube',
        'scale': (5, 5, 5),
        'color': 6
    },
    "L_hellSlide_ctrl": {
        'shape': 'circleY',
        'scale': (1, 1, 1),
        'color': 6
    },
    "L_ballSlide_ctrl": {
        'shape': 'circleY',
        'scale': (1, 1, 1),
        'color': 6
    },
    "L_toeSlide_ctrl": {
        'shape': 'circleY',
        'scale': (1, 1, 1),
        'color': 6
    },
    "L_sideOut_ctrl": {
        'shape': 'circleZ',
        'scale': (1, 1, 1),
        'color': 6
    },
    "L_sideIn_ctrl": {
        'shape': 'circleZ',
        'scale': (1, 1, 1),
        'color': 6
    },
    "L_hell_ctrl": {
        'shape': 'circleY',
        'scale': (1, 1, 1),
        'color': 6
    },
    "L_toe_ctrl": {
        'shape': 'circleX',
        'scale': (1, 1, 1),
        'color': 6
    },
    "L_ball_ctrl": {
        'shape': 'circleX',
        'scale': (1, 1, 1),
        'color': 6
    },
    "L_ankle_ctrl": {
        'shape': 'circleX',
        'scale': (1, 1, 1),
        'color': 6
    },
    "L_footRoll_ctrl": {
        'shape': 'diamond',
        'scale': (1, 1, 1),
        'color': 6
    },
    "L_ik_leg_3_pvCtrl": {
        'shape': 'diamond',
        'scale': (5, 5, 5),
        'color': 6
    },
    "L_main_leg_3_switch": {
        'shape': 'diamond',
        'scale': (5, 5, 5),
        'color': 6
    },
    "L_fk_leg_1_ctrl": {
        'shape': 'circleX',
        'scale': (10, 10, 10),
        'color': 18
    },
    "L_fk_leg_2_ctrl": {
        'shape': 'circleX',
        'scale': (10, 10, 10),
        'color': 18
    },
    "L_fk_leg_3_ctrl": {
        'shape': 'circleX',
        'scale': (10, 10, 10),
        'color': 18
    },
    "L_ankle_FK_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 18
    },
    "L_ball_FK_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 18
    },
    "L_toe_FK_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 18
    },
    "L_upperLeg_ribbon_start_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 15
    },
    "L_upperLeg_ribbon_mid_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 15
    },
    "L_upperLeg_ribbon_end_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 15
    },
    "L_lowerLeg_ribbon_start_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 15
    },
    "L_lowerLeg_ribbon_mid_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 15
    },
    "L_lowerLeg_ribbon_end_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 15
    },
    "R_ik_arm_3_ctrl": {
        'shape': 'cube',
        'scale': (5, 5, 5),
        'color': 13
    },
    "R_ik_arm_3_pvCtrl": {
        'shape': 'diamond',
        'scale': (5, 5, 5),
        'color': 13
    },
    "R_main_arm_3_switch": {
        'shape': 'diamond',
        'scale': (5, 5, 5),
        'color': 13
    },
    "R_fk_arm_1_ctrl": {
        'shape': 'circleX',
        'scale': (10, 10, 10),
        'color': 20
    },
    "R_fk_arm_2_ctrl": {
        'shape': 'circleX',
        'scale': (10, 10, 10),
        'color': 20
    },
    "R_fk_arm_3_ctrl": {
        'shape': 'circleX',
        'scale': (10, 10, 10),
        'color': 20
    },
    "R_scapula_ctrl": {
        'shape': 'pinY',
        'scale': (3, 3, 3),
        'color': 13
    },
    "R_upperArm_ribbon_start_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 4
    },
    "R_upperArm_ribbon_mid_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 4
    },
    "R_upperArm_ribbon_end_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 4
    },
    "R_lowerArm_ribbon_start_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 4
    },
    "R_lowerArm_ribbon_mid_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 4
    },
    "R_lowerArm_ribbon_end_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 4
    },
    "L_ik_arm_3_ctrl": {
        'shape': 'cube',
        'scale': (5, 5, 5),
        'color': 6
    },
    "L_ik_arm_3_pvCtrl": {
        'shape': 'diamond',
        'scale': (5, 5, 5),
        'color': 6
    },
    "L_main_arm_3_switch": {
        'shape': 'diamond',
        'scale': (5, 5, 5),
        'color': 6
    },
    "L_fk_arm_1_ctrl": {
        'shape': 'circleX',
        'scale': (10, 10, 10),
        'color': 18
    },
    "L_fk_arm_2_ctrl": {
        'shape': 'circleX',
        'scale': (10, 10, 10),
        'color': 18
    },
    "L_fk_arm_3_ctrl": {
        'shape': 'circleX',
        'scale': (10, 10, 10),
        'color': 18
    },
    "L_scapula_ctrl": {
        'shape': 'pinY',
        'scale': (3, -3, 3),
        'color': 6
    },
    "L_upperArm_ribbon_start_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 15
    },
    "L_upperArm_ribbon_mid_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 15
    },
    "L_upperArm_ribbon_end_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 15
    },
    "L_lowerArm_ribbon_start_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 15
    },
    "L_lowerArm_ribbon_mid_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 15
    },
    "L_lowerArm_ribbon_end_ctrl": {
        'shape': 'squareX',
        'scale': (5, 5, 5),
        'color': 15
    },
    "R_pinky_1_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_pinky_2_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_pinky_3_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_pinky_4_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_pinky_5_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_annular_1_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_annular_2_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_annular_3_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_annular_4_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_annular_5_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_middleFinger_1_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_middleFinger_2_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_middleFinger_3_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_middleFinger_4_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_middleFinger_5_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_index_1_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_index_2_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_index_3_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_index_4_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_index_5_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_thumb_1_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_thumb_2_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_thumb_3_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "R_thumb_4_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 13
    },
    "L_pinky_1_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_pinky_2_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_pinky_3_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_pinky_4_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_pinky_5_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_annular_1_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_annular_2_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_annular_3_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_annular_4_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_annular_5_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_middleFinger_1_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_middleFinger_2_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_middleFinger_3_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_middleFinger_4_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_middleFinger_5_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_index_1_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_index_2_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_index_3_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_index_4_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_index_5_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_thumb_1_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_thumb_2_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_thumb_3_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    },
    "L_thumb_4_ctrl": {
        'shape': 'circleX',
        'scale': (2, 2, 2),
        'color': 6
    }
}

def switch_shape():
    # create shapes
    for ctrl in list(main_dic):
        ctrl_dic = main_dic[ctrl]

        k.swap_shapes(ctrl, ctrl_dic['shape'], ctrl_dic['scale'], ctrl_dic['color'])


#switch_shape()
