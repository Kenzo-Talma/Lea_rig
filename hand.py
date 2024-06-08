import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

def build_hand_func(meta_list=None, wrist=None):
    jnt_list = []
    # meta loop
    for meta in meta_list:
        # create list
        offset_list = []
        ctrl_list = []
        grp_list = []
        joint_list = []

        # get finger list
        finger_list = cmds.ls(meta, dag=True, type='transform')

        # finger loop
        for n, finger in enumerate(finger_list):
            # create names
            jnt = finger+'_jnt'
            ctrl = finger+'_ctrl'
            offset = finger+'_offset'
            grp = finger+'_grp'

            # create objects
            jnt = k.createNode('joint', n=jnt)
            ctrl = cmds.circle(n=ctrl)[0]
            offset = k.createNode('transform', n=offset)
            grp = k.createNode('transform', n=grp)

            if not n == 0:
                cmds.parent(jnt, joint_list[n-1])

            # joint position
            cmds.xform(
                jnt,
                t=cmds.xform(finger, q=True, t=True, ws=True),
                ws=True
            )
            cmds.xform(
                jnt,
                ro=cmds.xform(finger, q=True, ro=True, ws=True),
                ws=True
            )
            cmds.xform(
                jnt,
                s=cmds.xform(finger, q=True, s=True, ws=True),
                ws=True
            )

            # parent
            cmds.parent(ctrl, offset)
            cmds.parent(offset, grp)

            # add to list
            joint_list.append(jnt)
            grp_list.append(grp)
            ctrl_list.append(ctrl)
            offset_list.append(offset)

        jnt_list.extend(joint_list)

        for jnt in joint_list:
            # orient joint
            if cmds.listRelatives(jnt, c=True, type='joint'):
                cmds.joint(jnt, e=True, oj='xzy', sao='zup', zso=True)
            else:
                cmds.joint(jnt, e=True, oj='none', zso=True)
                cmds.xform(jnt, ro=(0,0,0))

        for n, grp in enumerate(grp_list):
            if not n == 0:
                cmds.parent(grp, ctrl_list[n - 1])

        for grp, jnt in zip(grp_list, joint_list):
            # place ctrl group
            cmds.xform(
                grp,
                t=cmds.xform(jnt, q=True, t=True, ws=True),
                ws=True
            )
            cmds.xform(
                grp,
                ro=cmds.xform(jnt, q=True, ro=True, ws=True),
                ws=True
            )
            cmds.xform(
                grp,
                s=cmds.xform(jnt, q=True, s=True, ws=True),
                ws=True
            )

        for ctrl, jnt in zip(ctrl_list, joint_list):
            # create mult matrix
            mlm = k.createNode('multMatrix', n=jnt.replace('jnt', 'mlm'))

            # connect ctrl to join
            if cmds.listRelatives(jnt, p=True):
                cmds.connectAttr(ctrl+'.worldMatrix[0]', mlm+'.matrixIn[0]', f=True)
                cmds.connectAttr(
                    cmds.listRelatives(jnt, p=True)[0]+'.worldInverseMatrix',
                    mlm+'.matrixIn[1]',
                    f=True
                )
                cmds.connectAttr(mlm+'.matrixSum', jnt+'.offsetParentMatrix', f=True)
            else:
                cmds.connectAttr(ctrl+'.worldMatrix', jnt+'.offsetParentMatrix', f=True)

            cmds.xform(jnt, t=(0, 0, 0))
            cmds.xform(jnt, ro=(0, 0, 0))
            cmds.xform(jnt, s=(1, 1, 1))

            cmds.setAttr(jnt+'.jointOrientX', 0)
            cmds.setAttr(jnt+'.jointOrientY', 0)
            cmds.setAttr(jnt+'.jointOrientZ', 0)

    # parent meta group to wrist
    wrist_grp = k.createNode('transform', n=wrist+'_offset_grp')
    cmds.connectAttr(
        wrist+'.worldMatrix',
        wrist_grp+'.offsetParentMatrix',
        f=True
    )
    for meta in meta_list:
        cmds.parent(meta+'_grp', wrist_grp)

    return jnt_list

def reverse_hand_func(meta_list, wrist):
    jnt_list = []
    for meta in meta_list:
        joint_list = []
        meta_jnt = meta+'_jnt'
        dup_jnt = cmds.duplicate(meta_jnt, rc=True)

        for jnt in dup_jnt:
            cmds.setAttr(
                jnt + '.offsetParentMatrix',
                (
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0
                ),
                type='matrix'
            )
            cmds.xform(
                jnt,
                t=cmds.xform(jnt[:-1], q=True, t=True, ws=True),
                ws=True
            )
            cmds.xform(
                jnt,
                ro=cmds.xform(jnt[:-1], q=True, ro=True, ws=True),
                ws=True
            )
            cmds.xform(
                jnt,
                s=cmds.xform(jnt[:-1], q=True, s=True, ws=True),
                ws=True
            )

        temp_joint_list = cmds.mirrorJoint(
            dup_jnt[0],
            mxy=False,
            mxz=False,
            myz=True,
            mb=True,
            sr=['R_', 'L_']
        )
        for jnt in temp_joint_list:
            new_name = cmds.rename(jnt, jnt[:-1])
            joint_list.append(new_name)

        cmds.delete(dup_jnt)

        jnt_list.extend(joint_list)

        # list
        ctrl_list = []

        for n, jnt in enumerate(joint_list):
            # create names
            ctrl = jnt.replace('jnt', 'ctrl')
            offset = jnt.replace('jnt', 'offset')
            grp = jnt.replace('jnt', 'grp')

            # create objects
            ctrl = cmds.circle(n=ctrl)[0]
            offset = k.createNode('transform', n=offset)
            grp = k.createNode('transform', n=grp)

            # parent
            cmds.parent(ctrl, offset)
            cmds.parent(offset, grp)

            if not n == 0:
                cmds.parent(grp, ctrl_list[n-1])

            # place ctrl group
            cmds.xform(
                grp,
                t=cmds.xform(jnt, q=True, t=True, ws=True),
                ws=True
            )
            cmds.xform(
                grp,
                ro=cmds.xform(jnt, q=True, ro=True, ws=True),
                ws=True
            )
            cmds.xform(
                grp,
                s=cmds.xform(jnt, q=True, s=True, ws=True),
                ws=True
            )

            ctrl_list.append(ctrl)


        for ctrl, jnt in zip(ctrl_list, joint_list):
            # create mult matrix
            mlm = k.createNode('multMatrix', n=jnt.replace('jnt', 'mlm'))

            # connect
            if cmds.listRelatives(jnt, p=True):
                cmds.connectAttr(ctrl+'.worldMatrix[0]', mlm+'.matrixIn[0]', f=True)
                cmds.connectAttr(
                    cmds.listRelatives(jnt, p=True)[0]+'.worldInverseMatrix',
                    mlm+'.matrixIn[1]',
                    f=True
                )
                cmds.connectAttr(mlm+'.matrixSum', jnt+'.offsetParentMatrix', f=True)
            else:
                cmds.connectAttr(ctrl+'.worldMatrix', jnt+'.offsetParentMatrix', f=True)

            cmds.xform(jnt, t=(0, 0, 0))
            cmds.xform(jnt, ro=(0, 0, 0))
            cmds.xform(jnt, s=(1, 1, 1))

            cmds.setAttr(jnt + '.jointOrientX', 0)
            cmds.setAttr(jnt + '.jointOrientY', 0)
            cmds.setAttr(jnt + '.jointOrientZ', 0)

    # parent meta group to wrist
    wrist_grp = k.createNode('transform', n=wrist + '_offset_grp')
    cmds.connectAttr(
        wrist + '.worldMatrix',
        wrist_grp + '.offsetParentMatrix',
        f=True
    )
    for meta in meta_list:
        cmds.parent(meta.replace('R_', 'L_') + '_grp', wrist_grp)

    return jnt_list

######################################################################################
# test function
######################################################################################

'''build_hand_func(
    [
        "R_pinky_1",
        "R_annular_1",
        "R_middleFinger_1",
        "R_index_1",
        "R_thumb_1"
    ],
    'R_main_arm_3_jnt'
)'''
'''reverse_hand_func(
    [
        "R_pinky_1",
        "R_annular_1",
        "R_middleFinger_1",
        "R_index_1",
        "R_thumb_1"
    ],
    'L_main_arm_3_jnt'
)'''
