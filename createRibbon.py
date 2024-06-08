import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

def createRibbon_Func(startJoint, endJoint, tilesNumber, name, switch):
    # create ribbon
    ribbon = name+'_ribbon'
    if not cmds.objExists(ribbon):
        ribbon = cmds.nurbsPlane(ax=(0,1,0), w=1, lr=1, d=3, u=tilesNumber, v=1, ch=0, n=ribbon)[0]

    # create skin joint
    start_skin = k.createNode('joint', n=ribbon+'_start_jnt')
    start_grp = k.createNode('transform', n=ribbon+'_start_grp')
    start_offset = k.createNode('transform', n=ribbon+'_start_offset')
    start_ctrl = cmds.circle(n=ribbon+'_start_ctrl')
    mid_skin = k.createNode('joint', n=ribbon+'_mid_jnt')
    mid_grp = k.createNode('transform', n=ribbon+'_mid_grp')
    mid_offset = k.createNode('transform', n=ribbon + '_mid_offset')
    mid_ctrl = cmds.circle(n=ribbon + '_mid_ctrl')
    end_skin = k.createNode('joint', n=ribbon+'_end_jnt')
    end_grp = k.createNode('transform', n=ribbon+'_end_grp')
    end_offset = k.createNode('transform', n=ribbon + '_end_offset')
    end_ctrl = cmds.circle(n=ribbon + '_end_ctrl')

    ref_pos = k.createNode('transform', n=ribbon+'_ref_pos')

    # parent group
    cmds.parent(start_skin, start_ctrl)
    cmds.parent(start_ctrl, start_offset)
    cmds.parent(start_offset, start_grp)

    cmds.parent(mid_skin, mid_ctrl)
    cmds.parent(mid_ctrl, mid_offset)
    cmds.parent(mid_offset, mid_grp)

    cmds.parent(end_skin, end_ctrl)
    cmds.parent(end_ctrl, end_offset)
    cmds.parent(end_offset, end_grp)

    # set position
    cmds.xform(start_grp, t=(-0.5, 0, 0), ws=True)
    cmds.xform(end_grp, t=(0.5, 0, 0), ws=True)

    # set ref pos
    ref_blm = k.createNode('blendMatrix', n=ref_pos+'_blm')
    cmds.connectAttr(start_skin+'.worldMatrix[0]', ref_blm+'.inputMatrix', f=True)
    cmds.connectAttr(end_skin+'.worldMatrix[0]', ref_blm+'.target[0].targetMatrix')
    cmds.setAttr(ref_blm+'.target[0].weight', 0.5)
    cmds.connectAttr(ref_blm+'.outputMatrix', ref_pos+'.offsetParentMatrix', f=True)

    aim = k.createNode('aimMatrix', n=mid_grp.replace('grp', 'amm'))

    cmds.connectAttr(ref_pos+'.worldMatrix', aim+'.inputMatrix', f=True)
    cmds.connectAttr(
        end_skin+'.worldMatrix',
        aim+'.primaryTargetMatrix',
        f=True
    )
    cmds.connectAttr(
        ref_pos + '.worldMatrix',
        aim + '.secondaryTargetMatrix',
        f=True
    )
    cmds.setAttr(aim+'.secondaryMode', 2)
    cmds.setAttr(aim+'.secondaryTargetVectorY', 0)
    cmds.setAttr(aim+'.secondaryTargetVectorZ', 1)
    cmds.setAttr(aim+'.secondaryInputAxisY', 0)
    cmds.setAttr(aim+'.secondaryInputAxisZ', 1)

    cmds.connectAttr(aim+'.outputMatrix', mid_grp+'.offsetParentMatrix', f=True)

    # create skinCluster
    ribbonSkinCls = ribbon+'_skinCluster'
    if not cmds.objExists(ribbonSkinCls):
        ribbonSkinCls = cmds.skinCluster(start_skin, mid_skin, end_skin, ribbon, n=ribbonSkinCls)[0]
    cmds.skinPercent(ribbonSkinCls, ribbon+'.cv[0][0:3]', tv=[(start_skin, 1)])
    cmds.skinPercent(ribbonSkinCls, ribbon + '.cv[1][0:3]', tv=[(start_skin, 0.7), (mid_skin, 0.3)])
    cmds.skinPercent(ribbonSkinCls, ribbon + '.cv[2][0:3]', tv=[(mid_skin, 1)])
    cmds.skinPercent(ribbonSkinCls, ribbon + '.cv[3][0:3]', tv=[(end_skin, 0.7), (mid_skin, 0.3)])
    cmds.skinPercent(ribbonSkinCls, ribbon + '.cv[4][0:3]', tv=[(end_skin, 1)])

    # place ribbon joint
    cmds.connectAttr(startJoint+'.worldMatrix[0]', start_grp+'.offsetParentMatrix', f=True)
    cmds.xform(start_grp, t=(0, 0, 0), ws=False)

    cmds.connectAttr(endJoint+'.worldMatrix', end_grp+'.offsetParentMatrix', f=True)
    cmds.xform(end_grp, t=(0, 0, 0), ws=False)

    # connect ctrl to switch
    attr = 'ribbonVis'

    if not cmds.objExists(f'{switch}.{attr}'):
        cmds.addAttr(switch, at='bool', ln=attr, k=True)
    attr = f'{switch}.{attr}'
    cmds.setAttr(attr, 1, cb=True, k=False)

    for ctrl in [start_ctrl, mid_ctrl, end_ctrl]:
        for shapes in cmds.listRelatives(ctrl, c=True):
            cmds.connectAttr(
                attr,
                shapes+'.v',
                f=True
            )

    return ribbon

###################################################################
# test function
###################################################################
#createRibbon_Func('leg_1', 'leg_2', 2, 'test')