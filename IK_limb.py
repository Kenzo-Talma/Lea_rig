import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

def ik_limb(jnt_list=None, pv_pos=(0,0,5)):
    # def names
    ik_handle = jnt_list[-1].replace('jnt', 'ikHandle')
    effector = ik_handle.replace('ikHandle', 'effector')
    ctrl = ik_handle.replace('ikHandle', 'ctrl')
    offset = ctrl.replace('ctrl', 'offset')
    grp = ctrl.replace('ctrl', 'grp')
    pv = ctrl.replace('ctrl', 'pvCtrl')
    pv_offset = ctrl.replace('ctrl', 'pvOffset')
    pv_grp = ctrl.replace('ctrl', 'pvGrp')
    end_mlm = ctrl.replace('ctrl', 'mlm')
    end_pm = ctrl.replace('ctrl', 'pickMatrix')

    # create nodes
    ik_handle, temp = cmds.ikHandle(sj=jnt_list[0], ee=jnt_list[-1], n=ik_handle)
    cmds.rename(temp, effector)
    ctrl = cmds.circle(n=ctrl, ch=False)[0]
    offset = k.createNode('transform', n=offset)
    grp = k.createNode('transform', n=grp)
    pv = cmds.circle(n=pv, ch=False)[0]
    pv_offset = k.createNode('transform', n=pv_offset)
    pv_grp = k.createNode('transform', n=pv_grp)
    end_mlm = k.createNode('multMatrix', n=end_mlm)
    end_pm = k.createNode('pickMatrix', n=end_pm)

    # parent controls
    cmds.parent(ctrl, offset)
    cmds.parent(offset, grp)
    cmds.parent(pv, pv_offset)
    cmds.parent(pv_offset, pv_grp)

    # position
    cmds.xform(
        grp,
        t=cmds.xform(ik_handle, q=True, t=True, ws=True),
        ws=True
    )
    cmds.xform(
        pv_grp,
        t=cmds.xform(jnt_list[1], q=True, t=True, ws=True),
        ws=True
    )
    cmds.xform(pv_grp, t=pv_pos, r=True)

    # parent ik handle
    cmds.parent(ik_handle, ctrl)

    # pole vector constraint
    cmds.poleVectorConstraint(pv, ik_handle)

    # end constraint
    cmds.orientConstraint(ctrl, jnt_list[-1], mo=True)

    return grp, pv_grp

##########################################################
# test function
##########################################################
'''lst = cmds.ls(sl=True)
ik_limb(lst, (0,0,-5))'''
