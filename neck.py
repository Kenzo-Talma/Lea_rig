import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

def neck_built_func(loc_list):
    # def list
    jnt_list = []

    # value
    va1 = 1 / len(loc_list)
    va2 = 1 / (len(loc_list)-1)

    # create control
    ctrl = loc_list[0] + '_ctrl'
    offset = loc_list[0] + '_offset'
    grp = loc_list[0] + '_grp'

    ctrl = cmds.circle(n=ctrl)[0]
    offset = k.createNode('transform', n=offset)
    grp = k.createNode('transform', n=grp)

    cmds.parent(ctrl, offset)
    cmds.parent(offset, grp)

    cmds.xform(
        grp,
        t=cmds.xform(loc_list[0], q=True, t=True, ws=True),
        ws=True
    )
    cmds.xform(
        grp,
        ro=cmds.xform(loc_list[0], q=True, ro=True, ws=True),
        ws=True
    )
    cmds.xform(
        grp,
        s=cmds.xform(loc_list[0], q=True, s=True, ws=True),
        ws=True
    )

    # create joint
    for n, loc in enumerate(loc_list):
        jnt = loc+'_jnt'

        jnt = k.createNode('joint', n=jnt)

        # set joint position
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

        # add joint to list
        jnt_list.append(jnt)

    for n, jnt in enumerate(jnt_list):
        if not n == 0:
            # parent joint
            cmds.parent(jnt, jnt_list[n-1], a=True, r=False)

    for n, jnt in enumerate(jnt_list):
        # connect jnt
        if not n == 0:
            t_mld = k.createNode('multiplyDivide', n=jnt.replace('jnt', 'translate_mld'))
            t_pma = k.createNode('plusMinusAverage', n=jnt.replace('jnt', 'translate_pma'))

            cmds.connectAttr(ctrl+'.translate', t_mld+'.input1', f=True)
            cmds.setAttr(t_mld + '.input2', va2, va2, va2)
            cmds.connectAttr(t_mld + '.output', t_pma + '.input3D[0]', f=True)
            for ax1, ax2 in zip(['X', 'Y', 'Z'], ['x', 'y', 'z']):
                cmds.setAttr(f'{t_pma}.input3D[1].input3D{ax2}', cmds.getAttr(f'{jnt}.translate{ax1}'))
            cmds.connectAttr(t_pma+'.output3D', jnt+'.translate', f=True)

            ro_mld = k.createNode('multiplyDivide', n=jnt.replace('jnt', 'rotate_mld'))
            s_mld = k.createNode('multiplyDivide', n=jnt.replace('jnt', 'scale_mld'))
            s_ratio_mld = k.createNode('multiplyDivide', n=jnt.replace('jnt', 'scale_ratio_mdl'))

            cmds.connectAttr(ctrl + '.rotate', ro_mld + '.input1', f=True)
            cmds.setAttr(ro_mld + '.input2', va1, va1, va1)
            cmds.connectAttr(ro_mld + '.output', jnt + '.rotate', f=True)

            cmds.connectAttr(ctrl + '.scale', s_mld + '.input1', f=True)
            cmds.setAttr(s_mld + '.input2', va1, va1, va1)
            cmds.connectAttr(s_mld+'.output', s_ratio_mld+'.input1', f=True)
            cmds.setAttr(s_ratio_mld+'.input2', va1, va1, va1)
            cmds.setAttr(s_ratio_mld+'.operation', 2)
            cmds.connectAttr(s_ratio_mld + '.output', jnt + '.scale', f=True)

            cmds.setAttr(jnt+'.jointOrientX', 0)
            cmds.setAttr(jnt + '.jointOrientY', 0)
            cmds.setAttr(jnt + '.jointOrientZ', 0)
        '''else:
            cmds.connectAttr()'''

    return jnt_list

#############################################################
# test function
#############################################################
#neck_built_func(["C_neck_1", "C_neck_2", "C_neck_3"])
