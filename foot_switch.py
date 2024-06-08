import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

def foot_switch_func(ik_foot_rool, main_ik_grp, ik_handle, main_fk_grp, fk_anckle_ctrl, switch):
    # def lists
    joint_list = []
    fk_ctrl_list = cmds.ls(main_fk_grp, dag=True, type='nurbsCurve')
    ik_ctrl_list = cmds.ls(main_ik_grp, dag=True, type='nurbsCurve')

    # create mainjoints
    for ctrl in fk_ctrl_list:
        # def joint names
        jnt = ctrl.replace('ctrlShape', 'jnt')
        jnt = jnt.replace('FK', 'main')

        # create joint
        jnt = k.createNode('joint', n=jnt)
        joint_list.append(jnt)

    # joint list
    for n, jnt in enumerate(joint_list):
        # def control
        fk_ctrl = cmds.listRelatives(fk_ctrl_list[n], p=True)[0]
        ik_ctrl = cmds.listRelatives(ik_ctrl_list[-(n+1)], p=True)[0]

        if not n == 0:
            # parent joint
            cmds.parent(jnt, joint_list[n-1])

            # FK mult matrix
            fk_jnt_mlm = fk_ctrl.replace('ctrl', 'mlm')
            fk_jnt_mlm = k.createNode('multMatrix', n=fk_jnt_mlm)

            cmds.connectAttr(
                fk_ctrl+'.worldMatrix[0]',
                fk_jnt_mlm+'.matrixIn[0]',
                f=True
            )
            cmds.connectAttr(
                cmds.listRelatives(jnt, p=True)[0]+'.worldInverseMatrix',
                fk_jnt_mlm+'.matrixIn[1]',
                f=True
            )

            # IK mult matrix
            ik_jnt_mlm = ik_ctrl.replace('ctrl', 'mlm')
            ik_jnt_mlm = k.createNode('multMatrix', n=ik_jnt_mlm)

            cmds.connectAttr(
                ik_ctrl+'.worldMatrix[0]',
                ik_jnt_mlm+'.matrixIn[0]',
                f=True
            )
            cmds.connectAttr(
                cmds.listRelatives(jnt, p=True)[0] + '.worldInverseMatrix',
                ik_jnt_mlm + '.matrixIn[1]',
                f=True
            )

            # blend matrix
            jnt_blm = jnt.replace('jnt', 'blm')
            jnt_blm = k.createNode('blendMatrix', n=jnt_blm)

            cmds.connectAttr(fk_jnt_mlm+'.matrixSum', jnt_blm+'.target[0].targetMatrix', f=True)
            cmds.connectAttr(switch+'.ikFkSwitch', jnt_blm+'.target[1].weight', f=True)
            cmds.connectAttr(ik_jnt_mlm + '.matrixSum', jnt_blm + '.target[1].targetMatrix', f=True)
            cmds.connectAttr(
            cmds.listConnections(switch+'.ikFkSwitch', d=True, type='reverse')[0]+'.outputX',
                jnt_blm + '.target[0].weight',
                f=True
            )

            cmds.connectAttr(jnt_blm+'.outputMatrix', jnt+'.offsetParentMatrix', f=True)

            cmds.setAttr(jnt+'.translate', 0, 0, 0)
            cmds.setAttr(jnt + '.rotate', 0, 0, 0)
            cmds.setAttr(jnt + '.scale', 1, 1, 1)
            cmds.setAttr(jnt + '.jointOrientX', 0)
            cmds.setAttr(jnt + '.jointOrientY', 0)
            cmds.setAttr(jnt + '.jointOrientZ', 0)

        else:
            jnt_blm = jnt.replace('jnt', 'blm')
            jnt_blm = k.createNode('blendMatrix', n=jnt_blm)

            cmds.connectAttr(fk_ctrl+'.worldMatrix[0]', jnt_blm+'.target[0].targetMatrix', f=True)
            cmds.connectAttr(switch+'.ikFkSwitch', jnt_blm+'.target[1].weight', f=True)
            cmds.connectAttr(ik_ctrl+'.worldMatrix[0]', jnt_blm+'.target[1].targetMatrix', f=True)
            cmds.connectAttr(
                cmds.listConnections(switch + '.ikFkSwitch', d=True, type='reverse')[0] + '.outputX',
                jnt_blm + '.target[0].weight',
                f=True
            )

            cmds.connectAttr(jnt_blm + '.outputMatrix', jnt + '.offsetParentMatrix', f=True)

    # hide ctrl
    for shape in cmds.ls(ik_foot_rool, dag=True, type='nurbsCurve'):
        cmds.connectAttr(switch+'.ikFkSwitch', shape+'.v', f=True)
    for shape in cmds.ls(main_ik_grp, dag=True, type='nurbsCurve'):
        cmds.connectAttr(switch + '.ikFkSwitch', shape + '.v', f=True)
    for shape in cmds.ls(main_fk_grp, dag=True, type='nurbsCurve'):
        cmds.connectAttr(
            cmds.listConnections(switch + '.ikFkSwitch', d=True, type='reverse')[0] + '.outputX',
            shape+'.v',
            f=True
        )

    # parent to leg
    ik_ctrl = cmds.listRelatives(ik_handle, p=True)[0]
    cmds.parent(
        ik_handle,
        cmds.ls(main_ik_grp, dag=True, type='transform')[-1]
    )
    cmds.parent(main_ik_grp, ik_foot_rool, ik_ctrl)
    cmds.parent(main_fk_grp, fk_anckle_ctrl)

################################################################
# test function
################################################################
'''foot_switch_func(
    'R_footRoll_grp',
    'R_hellSlide_grp',
    'R_ik_leg_3_ikHandle',
    'R_ankle_FK_grp',
    'R_fk_leg_3_ctrl',
    'R_main_leg_3_switch'
)
'''