import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

def IK_FK_switch_func(ik_ctrl_grp, fk_ctrl_grp, ik_joint, fk_joint,main_joint, blend_nodes):
    # turn group to list
    if not isinstance(ik_ctrl_grp, list):
        ik_ctrl_grp = [ik_ctrl_grp]

    if not isinstance(fk_ctrl_grp, list):
        fk_ctrl_grp = [fk_ctrl_grp]

    if not isinstance(ik_joint, list):
        ik_joint = [ik_joint]

    if not isinstance(fk_joint, list):
        fk_joint = [fk_joint]

    if not isinstance(blend_nodes, list):
        blend_nodes = [blend_nodes]

    # create switch
    switch = main_joint[-1].replace('jnt', 'switch')
    offset = switch+'_offset'
    grp = switch+'_grp'

    switch = cmds.circle(n=switch, ch=False)[0]
    offset = k.createNode('transform', n=offset)
    grp = k.createNode('transform', n=grp)

    cmds.parent(switch, offset)
    cmds.parent(offset, grp)
    cmds.connectAttr(main_joint[-1]+'.worldMatrix', grp+'.offsetParentMatrix')

    cmds.addAttr(switch, at='enum', en='FK:IK', ln='ikFkSwitch', nn='IK FK Switch', k=True)
    switch_attr = switch+'.ikFkSwitch'
    cmds.setAttr(switch_attr, cb=True, k=True)

    reverse = switch+'_reverse'
    reverse = k.createNode('reverse', n=reverse)
    cmds.connectAttr(switch_attr, reverse+'.inputX', f=True)
    reverse_attr = reverse+'.outputX'

    # ik loop
    for grp in ik_ctrl_grp:
        shape_list = cmds.ls(grp, dag=True, type='nurbsCurve')
        for shape in shape_list:
            cmds.connectAttr(switch_attr, shape+'.v', f=True)

    cmds.setAttr(ik_joint[0]+'.v', 0)

    # fk loop
    for grp in fk_ctrl_grp:
        shape_list = cmds.ls(grp, dag=True, type='nurbsCurve')
        for shape in shape_list:
            cmds.connectAttr(reverse_attr, shape+'.v', f=True)

    cmds.setAttr(fk_joint[0] + '.v', 0)

    # blend node loop
    for blend in blend_nodes:
        cmds.connectAttr(switch_attr, blend+'.target[0].weight', f=True)
        cmds.connectAttr(reverse_attr, blend + '.target[1].weight', f=True)

    return switch+'_grp'


######################################
# test function
######################################

'''IK_FK_switch_func(
    ['ik_locator3_grp', 'ik_locator3_pvGrp'],
    'fk_locator1_grp',
    ['ik_locator1_jnt', 'ik_locator2_jnt', 'ik_locator3_jnt'],
    ['fk_locator1_jnt', 'fk_locator2_jnt', 'fk_locator3_jnt'],
    ['main_locator1_jnt', 'main_locator2_jnt', 'main_locator3_jnt'],
    ['main_locator1_blendMatrix', 'main_locator2_blendMatrix', 'main_locator3_blendMatrix']
)'''