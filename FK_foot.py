import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

def fk_foot_build(loc_list, reverse=False):
    # lists
    ctrl_list = []
    grp_list = []
    joint_list = []

    # build system
    for loc in loc_list:
        if not reverse:
            jnt = loc+'_FK_jnt'
            ctrl = loc+'_FK_ctrl'
            offset = loc+'_FK_offset'
            grp = loc+'_FK_grp'

        else:
            jnt = loc + '_FK_jnt'
            ctrl = loc.replace('R_', 'L_') + '_FK_ctrl'
            offset = loc.replace('R_', 'L_') + '_FK_offset'
            grp = loc.replace('R_', 'L_') + '_FK_grp'

        jnt = k.createNode('joint', n=jnt)
        ctrl = cmds.circle(n=ctrl)[0]
        offset = k.createNode('transform', n=offset)
        grp = k.createNode('transform', n=grp)

        cmds.parent(ctrl, offset)
        cmds.parent(offset, grp)

        cmds.xform(
            jnt,
            t=cmds.xform(loc, q=True, t=True, ws=True),
            ws=True
        )
        cmds.xform(
            jnt,
            ro=cmds.xform(loc, q=True, ro=True, ws=True),
            ws=True
        )
        cmds.xform(
            jnt,
            s=cmds.xform(loc, q=True, s=True, ws=True),
            ws=True
        )

        ctrl_list.append(ctrl)
        grp_list.append(grp)
        joint_list.append(jnt)

    for n, ob in enumerate(loc_list):
        if not n == 0:
            cmds.parent(grp_list[n], ctrl_list[n-1])
            cmds.parent(joint_list[n], joint_list[n-1])

    for jnt in joint_list:
        if cmds.listRelatives(jnt, c=True, type='joint'):
            cmds.joint(jnt, e=True, oj='xzy', sao='zup', zso=True)
        else:
            cmds.joint(jnt, e=True, oj='none', zso=True)

    if reverse:
        old_joint_list = joint_list
        joint_list = cmds.mirrorJoint(
            old_joint_list[0],
            mxy=False,
            mxz=False,
            myz=True,
            mb=True,
            sr=['R_', 'L_']
        )
        cmds.delete(old_joint_list)

    for jnt, grp in zip(joint_list, grp_list):
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

    cmds.delete(joint_list)


############################################################
# test function
############################################################
#lst = ['R_ankle', 'R_ball', 'R_toe']
#fk_foot_build(lst)
