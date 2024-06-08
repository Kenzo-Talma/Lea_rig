import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

def mirror_joint_func(first_joint):
    # def list
    fk_list = []
    ik_list = []
    blend_list = []

    # mirror joint
    main_list = cmds.mirrorJoint(
        first_joint,
        mxy=False,
        mxz=False,
        myz=True,
        mb=True,
        sr=['R_', 'L_']
    )
    main_joint = main_list[0]

    # duplicate joint
    fk_joint = main_joint.replace('main', 'fk')
    ik_joint = main_joint.replace('main', 'ik')
    cmds.duplicate(main_joint, n=fk_joint)
    cmds.duplicate(main_joint, n=ik_joint)

    n = 0
    for main, fk, ik in \
            zip(reversed(main_list),\
                reversed(cmds.ls(fk_joint, dag=True, l=True)),\
                reversed(cmds.ls(ik_joint, dag=True, l=True))):
        if not n == len(main_list)-1:
            fk_name = main.replace('main', 'fk')
            ik_name = main.replace('main', 'ik')
            cmds.rename(fk, fk_name)
            cmds.rename(ik, ik_name)

        n += 1
    fk_list = cmds.ls(fk_joint, dag=True)
    ik_list = cmds.ls(ik_joint, dag=True)

    n = 0
    for main, ik, fk in zip(main_list, fk_list, ik_list):
        # create blend matrix
        blendM = main.split('_jnt')[0] + '_blendMatrix'
        if not cmds.objExists(blendM):
            blendM = cmds.createNode('blendMatrix', n=blendM)

        # connect blend matrix
        if not n == 0:
            ik_mlm = blendM.replace('blendMatrix', 'ik_mlm')
            fk_mlm = blendM.replace('blendMatrix', 'fk_mlm')
            k.createNode('multMatrix', n=ik_mlm)
            k.createNode('multMatrix', n=fk_mlm)

            cmds.connectAttr(ik + '.worldMatrix[0]', ik_mlm + '.matrixIn[0]', f=True)
            cmds.connectAttr(
                cmds.listRelatives(ik, p=True)[0] + '.worldInverseMatrix',
                ik_mlm + '.matrixIn[1]',
                f=True
            )
            cmds.connectAttr(fk + '.worldMatrix', fk_mlm + '.matrixIn[0]', f=True)
            cmds.connectAttr(
                cmds.listRelatives(fk, p=True)[0] + '.worldInverseMatrix',
                fk_mlm + '.matrixIn[1]',
                f=True
            )
            cmds.connectAttr(ik_mlm + '.matrixSum', blendM + '.target[1].targetMatrix', f=True)
            cmds.connectAttr(fk_mlm + '.matrixSum', blendM + '.target[0].targetMatrix', f=True)
            cmds.connectAttr(blendM + '.outputMatrix', main + '.offsetParentMatrix', f=True)
        else:
            ik_mlm = blendM.replace('blendMatrix', 'ik_mlm')
            fk_mlm = blendM.replace('blendMatrix', 'fk_mlm')
            k.createNode('multMatrix', n=ik_mlm)
            k.createNode('multMatrix', n=fk_mlm)

            cmds.connectAttr(ik + '.worldMatrix', ik_mlm + '.matrixIn[0]', f=True)
            cmds.connectAttr(fk + '.worldMatrix', fk_mlm + '.matrixIn[0]', f=True)
            cmds.connectAttr(ik_mlm + '.matrixSum', blendM + '.target[1].targetMatrix', f=True)
            cmds.connectAttr(fk_mlm + '.matrixSum', blendM + '.target[0].targetMatrix', f=True)
            cmds.connectAttr(blendM + '.outputMatrix', main + '.offsetParentMatrix', f=True)

        # reset main joint transform

        cmds.xform(main, t=(0, 0, 0))
        cmds.xform(main, ro=(0, 0, 0))
        cmds.setAttr(main + '.jointOrientX', 0)
        cmds.setAttr(main + '.jointOrientY', 0)
        cmds.setAttr(main + '.jointOrientZ', 0)

        blend_list.append(blendM)

        n += 1

    return blend_list, main_list, ik_list, fk_list

################################################################
# test fuction
################################################################
#test = mirror_joint_func('R_main_arm_1_jnt')
#print(test)

# cmds.mirrorJoint(jnt, mxy=False, mxz=False, myz=True, mb=True, sr=['R_', 'L_'])
# mirrorJoint -mirrorYZ -mirrorBehavior -searchReplace "R_" "L_"