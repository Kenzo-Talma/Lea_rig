import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

def fk_limb(jnt_list=None):
    # create lists
    ctrl_list = []
    offset_list = []
    grp_list = []

    # create control loop
    for jnt in jnt_list:
        # def names
        ctrl = jnt.replace('jnt', 'ctrl')
        offset = jnt.replace('jnt', 'offset')
        grp = jnt.replace('jnt', 'grp')

        # create object
        ctrl = cmds.circle(n=ctrl, ch=False)[0]
        offset = k.createNode('transform', n=offset)
        grp = k.createNode('transform', n=grp)

        # parent object
        cmds.parent(ctrl, offset)
        cmds.parent(offset, grp)

        # position
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

        # list
        ctrl_list.append(ctrl)
        offset_list.append(offset)
        grp_list.append(grp)

    # parent control
    for n, ctrl in enumerate(ctrl_list):
        if not n == len(ctrl_list)-1:
            cmds.parent(grp_list[n+1], ctrl)

    for jnt, ctrl, offset, grp in zip(jnt_list, ctrl_list, offset_list, grp_list):
        # def names
        jnt_mlm = jnt.replace('jnt', 'mlm')

        # create nodes
        jnt_mlm = k.createNode('multMatrix', n=jnt_mlm)

        # connect network
        if cmds.listRelatives(jnt, p=True):
            cmds.connectAttr(ctrl+'.worldMatrix[0]', jnt_mlm+'.matrixIn[0]', f=True)
            cmds.connectAttr(jnt+'.inverseMatrix', jnt_mlm+'.matrixIn[1]', f=True)
            cmds.connectAttr(
                cmds.listRelatives(jnt, p=True)[0]+'.worldInverseMatrix',
                jnt_mlm+'.matrixIn[2]',
                f=True
            )
            cmds.connectAttr(jnt_mlm+'.matrixSum', jnt+'.offsetParentMatrix', f=True)
        else:
            cmds.connectAttr(ctrl+'.worldMatrix', jnt+'.offsetParentMatrix', f=True)
            cmds.delete(jnt_mlm)

        # reset transform
        cmds.setAttr(jnt+'.translate', 0, 0, 0)
        cmds.setAttr(jnt+'.rotate', 0, 0, 0)
        cmds.setAttr(jnt+'.scale', 1, 1, 1)

        cmds.setAttr(jnt+'.jointOrientX', 0)
        cmds.setAttr(jnt+'.jointOrientY', 0)
        cmds.setAttr(jnt+'.jointOrientZ', 0)



##########################################################
# test function
##########################################################
'''lst = cmds.ls(sl=True)
fk_limb(lst)'''
