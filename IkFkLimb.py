import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)


def ikFkLimbBuilder_func(locList):
    jointList = []
    mainJointList = []
    ikJointList = []
    fkJointList = []
    parentJoint = None
    blendList = []

    # create joints
    for loc in locList:
        # create joint
        jnt = 'main_'+loc+'_jnt'
        if not cmds.objExists(jnt):
            jnt = cmds.createNode('joint', n=jnt)

        pos = cmds.xform(loc, q=True, t=True, ws=True, a=True)
        cmds.xform(jnt, t=pos, ws=True, a=True)

        if not parentJoint == None:
            cmds.parent(jnt, parentJoint)

        parentJoint = jnt
        mainJointList.append(jnt)
        #jointList.append(jnt)
        ikJointList.append(jnt.replace('main', 'ik'))
        fkJointList.append(jnt.replace('main', 'fk'))

    # orient joints
    for jnt in mainJointList:
        if not cmds.listRelatives(jnt, c=True, type='joint') == None:
            cmds.joint(jnt, e=True, oj='xzy', sao='zup', zso=True)
        else:
            cmds.joint(jnt, e=True, oj='none', zso=True)

    # create Ik and Fk joint
    parentJoint = None
    for jnt in mainJointList:
        # create Ik and Fk joint
        for a in ('ik_', 'fk_'):
            # create joint
            aJoint = a+jnt.split('_', 1)[1]
            if not cmds.objExists(aJoint):
                aJoint = cmds.createNode('joint', n=aJoint)
            pos = cmds.xform(jnt, q=True, t=True, ws=True, a=True)
            ori = cmds.getAttr(jnt+'.jointOrient')[0]

            cmds.xform(aJoint, t=pos, ws=True, a=True)

            # parent joint
            if not parentJoint == None:
                cmds.parent(aJoint, a+parentJoint.split('_', 1)[1])

            # orient joint
            cmds.setAttr(aJoint+'.jointOrientX', ori[0])
            cmds.setAttr(aJoint+'.jointOrientY', ori[1])
            cmds.setAttr(aJoint+'.jointOrientZ', ori[2])

        parentJoint = jnt

    # connect IK FK switch
    for jnt in mainJointList:
        ikJoint = 'ik_'+jnt.split('_', 1)[1]
        fkJoint = 'fk_' + jnt.split('_', 1)[1]

        # create blend matrix
        blendM = jnt.split('_jnt')[0]+'_blendMatrix'
        if not cmds.objExists(blendM):
            blendM = cmds.createNode('blendMatrix', n=blendM)

        # connect blend matrix
        if cmds.listRelatives(jnt, p=True):
            ik_mlm = blendM.replace('blendMatrix', 'ik_mlm')
            fk_mlm = blendM.replace('blendMatrix', 'fk_mlm')
            k.createNode('multMatrix', n=ik_mlm)
            k.createNode('multMatrix', n=fk_mlm)

            cmds.connectAttr(ikJoint+'.worldMatrix[0]', ik_mlm+'.matrixIn[0]', f=True)
            cmds.connectAttr(
                cmds.listRelatives(ikJoint, p=True)[0] + '.worldInverseMatrix',
                ik_mlm + '.matrixIn[1]',
                f=True
            )
            cmds.connectAttr(fkJoint + '.worldMatrix', fk_mlm + '.matrixIn[0]', f=True)
            cmds.connectAttr(
                cmds.listRelatives(fkJoint, p=True)[0] + '.worldInverseMatrix',
                fk_mlm + '.matrixIn[1]',
                f=True
            )
            cmds.connectAttr(ik_mlm+'.matrixSum', blendM+'.target[0].targetMatrix', f=True)
            cmds.connectAttr(fk_mlm+'.matrixSum', blendM+'.target[1].targetMatrix', f=True)
            cmds.connectAttr(blendM+'.outputMatrix', jnt+'.offsetParentMatrix', f=True)

        else:
            ik_mlm = blendM.replace('blendMatrix', 'ik_mlm')
            fk_mlm = blendM.replace('blendMatrix', 'fk_mlm')
            k.createNode('multMatrix', n=ik_mlm)
            k.createNode('multMatrix', n=fk_mlm)

            cmds.connectAttr(ikJoint + '.worldMatrix[0]', ik_mlm + '.matrixIn[0]', f=True)
            cmds.connectAttr(fkJoint + '.worldMatrix', fk_mlm + '.matrixIn[0]', f=True)
            cmds.connectAttr(ik_mlm + '.matrixSum', blendM + '.target[0].targetMatrix', f=True)
            cmds.connectAttr(fk_mlm + '.matrixSum', blendM + '.target[1].targetMatrix', f=True)
            cmds.connectAttr(blendM + '.outputMatrix', jnt + '.offsetParentMatrix', f=True)

        # reset main joint transform

        cmds.xform(jnt, t=(0, 0, 0))
        cmds.xform(jnt, ro=(0, 0, 0))
        cmds.setAttr(jnt+'.jointOrientX', 0)
        cmds.setAttr(jnt+'.jointOrientY', 0)
        cmds.setAttr(jnt+'.jointOrientZ', 0)

        blendList.append(blendM)

    return blendList, mainJointList, ikJointList, fkJointList




# test function
'''lst = cmds.ls('locator1', 'locator2', 'locator3')
test = ikFkLimbBuilder_func(lst)
print(test)'''