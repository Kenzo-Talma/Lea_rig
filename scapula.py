import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

def built_scapula_func(scapula_loc, shoulder_loc, side = 'R'):
    # get position
    t_scap = cmds.xform(scapula_loc, q=True, t=True, ws=True)
    ro_scap = cmds.xform(scapula_loc, q=True, ro=True, ws=True)
    s_scap = cmds.xform(scapula_loc, q=True, s=True, ws=True)

    t_sh = cmds.xform(shoulder_loc, q=True, t=True, ws=True)
    ro_sh = cmds.xform(shoulder_loc, q=True, ro=True, ws=True)
    s_sh = cmds.xform(shoulder_loc, q=True, s=True, ws=True)

    # create joints
    scap_jnt = k.createNode('joint', n=f'{side}_{scapula_loc}_jnt')
    sh_jnt = k.createNode('joint', n=f'{side}_{shoulder_loc}_jnt')

    cmds.xform(scap_jnt, t=t_scap, ws=True)
    cmds.xform(scap_jnt, ro=ro_scap, ws=True)
    cmds.xform(scap_jnt, s=s_scap, ws=True)

    cmds.xform(sh_jnt, t=t_sh, ws=True)
    cmds.xform(sh_jnt, ro=ro_sh, ws=True)
    cmds.xform(sh_jnt, s=s_sh, ws=True)

    cmds.parent(sh_jnt, scap_jnt)

    cmds.joint(scap_jnt, e=True, oj='xzy', sao='zup', zso=True)
    cmds.joint(sh_jnt, e=True, oj='none', zso=True)

    # create control
    ctrl = f'{side}_{scapula_loc}_ctrl'
    offset = f'{side}_{scapula_loc}_offset'
    grp = f'{side}_{scapula_loc}_grp'

    ctrl = cmds.circle(n=ctrl)[0]
    offset = k.createNode('transform', n=offset)
    grp = k.createNode('transform', n=grp)

    cmds.parent(ctrl, offset)
    cmds.parent(offset, grp)

    t_scap = cmds.xform(scap_jnt, q=True, t=True, ws=True)
    ro_scap = cmds.xform(scap_jnt, q=True, ro=True, ws=True)
    s_scap = cmds.xform(scap_jnt, q=True, s=True, ws=True)

    cmds.xform(grp, t=t_scap, ws=True)
    cmds.xform(grp, ro=ro_scap, ws=True)
    cmds.xform(grp, s=s_scap, ws=True)

    # connect joint
    cmds.connectAttr(ctrl+'.worldMatrix', scap_jnt+'.offsetParentMatrix', f=True)

    cmds.xform(scap_jnt, t=(0, 0, 0))
    cmds.xform(scap_jnt, ro=(0, 0, 0))
    cmds.setAttr(scap_jnt + '.jointOrientX', 0)
    cmds.setAttr(scap_jnt + '.jointOrientY', 0)
    cmds.setAttr(scap_jnt + '.jointOrientZ', 0)

    return scap_jnt


def reverse_scapula_func(scapula_joint):
    # reverse joints
    jnt_list = cmds.mirrorJoint(
        scapula_joint,
        mxy=False,
        mxz=False,
        myz=True,
        mb=True,
        sr=['R_', 'L_']
    )

    # create control
    ctrl = jnt_list[0].replace('jnt', 'ctrl')
    offset = jnt_list[0].replace('jnt', 'offset')
    grp = jnt_list[0].replace('jnt', 'grp')

    ctrl = cmds.circle(n=ctrl)[0]
    offset = k.createNode('transform', n=offset)
    grp = k.createNode('transform', n=grp)

    cmds.parent(ctrl, offset)
    cmds.parent(offset, grp)

    t_scap = cmds.xform(jnt_list[0], q=True, t=True, ws=True)
    ro_scap = cmds.xform(jnt_list[0], q=True, ro=True, ws=True)
    s_scap = cmds.xform(jnt_list[0], q=True, s=True, ws=True)

    cmds.xform(grp, t=t_scap, ws=True)
    cmds.xform(grp, ro=ro_scap, ws=True)
    cmds.xform(grp, s=s_scap, ws=True)

    # connect joint
    cmds.connectAttr(ctrl + '.worldMatrix', jnt_list[0] + '.offsetParentMatrix', f=True)

    cmds.xform(jnt_list[0], t=(0, 0, 0))
    cmds.xform(jnt_list[0], ro=(0, 0, 0))
    cmds.setAttr(jnt_list[0] + '.jointOrientX', 0)
    cmds.setAttr(jnt_list[0] + '.jointOrientY', 0)
    cmds.setAttr(jnt_list[0] + '.jointOrientZ', 0)
