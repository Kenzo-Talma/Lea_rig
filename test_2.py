import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)


for ob in cmds.ls(sl=True):
    mlm = ob.replace('jnt', 'mlm')

    ctrl = ob.replace('jnt', 'ctrl')

    cmds.connectAttr(ctrl+'.worldMatrix[0]', mlm+'.matrixIn[0]', f=True)


'''for skn in cmds.ls('C_body_1_skn', dag=True, type='joint'):
    jnt = skn.replace('skn', 'jnt')

    if cmds.objExists(jnt):
        mlm = k.createNode('multMatrix', n=skn.replace('skn', 'skn_mlm'))

        cmds.connectAttr(jnt+'.worldMatrix[0]', mlm+'.matrixIn[0]', f=True)
        cmds.connectAttr(
            cmds.listRelatives(skn, p=True)[0]+'.worldInverseMatrix[0]',
            mlm+'.matrixIn[1]',
            f=True
        )
        cmds.connectAttr(mlm+'.matrixSum', skn+'.offsetParentMatrix', f=True)

        cmds.setAttr(skn+'.translate', 0, 0, 0)
        cmds.setAttr(skn + '.rotate', 0, 0, 0)
        cmds.setAttr(skn + '.scale', 1, 1, 1)
        cmds.setAttr(skn + '.shear', 0, 0, 0)

        cmds.setAttr(skn+'.jointOrientX', 0)
        cmds.setAttr(skn + '.jointOrientY', 0)
        cmds.setAttr(skn + '.jointOrientZ', 0)'''


'''rib_lst = ['C_upper_lips_ribbon', 'C_lower_lips_ribbon']

for rib in rib_lst:
    uv_pin = k.createNode('uvPin', n=rib.replace('ribbon', 'uvp'))
    sh = cmds.listRelatives(rib, s=True)[0]
    sh_o = cmds.listRelatives(rib, s=True)[1]

    cmds.connectAttr(sh+'.worldSpace', uv_pin+'.deformedGeometry', f=True)
    cmds.connectAttr(sh_o+'.worldSpace', uv_pin+'.originalGeometry', f=True)

    for n in range(17):
        jnt = k.createNode('joint', n=rib.replace('ribbon', str(n)+'_jnt'))

        cmds.connectAttr(f'{uv_pin}.outputMatrix[{str(n)}]', jnt+'.offsetParentMatrix', f=True)
        cmds.setAttr(f'{uv_pin}.coordinate[{str(n)}].coordinateU', n*(1/16))
        cmds.setAttr(f'{uv_pin}.coordinate[{str(n)}].coordinateV', 0.5)'''



'''lst = cmds.ls(sl=True)

for ob in lst:
    ctrl = cmds.circle(n=ob.replace('jnt', 'ctrl'), ch=False)[0]
    offset = k.createNode('transform', n=ob.replace('jnt', "offset"))
    grp = k.createNode('transform', n=ob.replace('jnt', 'grp'))

    cmds.parent(ctrl, offset)
    cmds.parent(offset, grp)

    cmds.xform(
        grp,
        t=cmds.xform(ob, q=True, t=True, ws=True),
        ws=True
    )
    cmds.xform(
        grp,
        ro=cmds.xform(ob, q=True, ro=True, ws=True),
        ws=True
    )
    cmds.xform(
        grp,
        s=cmds.xform(ob, q=True, s=True, ws=True),
        ws=True
    )
    cmds.parent(ob, ctrl)'''