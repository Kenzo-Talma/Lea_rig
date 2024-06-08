import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

def buildIKSpine_func(jointList, midLoc):
    # create ik spline handle
    startJoint = jointList[0]
    endJoint = jointList[-1]
    ikHandle = 'C_ikSpine_ikHandle'
    effector = 'C_ikSpine_effector'
    ikCurve = 'C_ikSpine_crv'
    ikBuildCurve = 'C_ikSpine_build_crv'
    if not cmds.objExists(ikHandle):
        if cmds.objExists(effector):
            cmds.delete(effector)
        if cmds.objExists(ikCurve):
            cmds.delete(ikCurve)
        if cmds.objExists(ikBuildCurve):
            cmds.delete(ikBuildCurve)
        ikHandle = cmds.ikHandle(sj=startJoint, ee=endJoint, sol='ikSplineSolver', n=ikHandle, ns=6)[0]

        cmds.rename('curve1', ikCurve)
        cmds.rename('effector1', effector)

        cmds.duplicate(ikCurve, n=ikBuildCurve)
        cmds.connectAttr(ikBuildCurve+'.worldSpace', ikCurve+'.create', f=True)

    # create controllers
    locList = [startJoint, midLoc, endJoint]
    ctrlName = ['C_hip_ikSpine', 'C_spine_ikSpine', 'C_shoulder_ikSpine']
    ctrlList = []
    ctrlJointList = []
    for loc, name in zip(locList, ctrlName):
        pos = cmds.xform(loc, q=True, t=True, ws=True)
        rot = cmds.xform(loc, q=True, ro=True, ws=True)

        jnt = name+'_jnt'
        ctrl = name+'_ctrl'
        offset = name+'_offset'
        grp = name+'_grp'

        if not cmds.objExists(jnt):
            jnt = cmds.createNode('joint', n=jnt)
        if not cmds.objExists(ctrl):
            ctrl = cmds.circle(ch=False, n=ctrl)[0]
        if not cmds.objExists(offset):
            offset = cmds.group(em=True, n=offset)
        if not cmds.objExists(grp):
            grp = cmds.group(em=True, n=grp)

        for ob in [jnt, ctrl, offset, grp]:
            cmds.xform(ob, t=(0, 0, 0))
            cmds.xform(ob, ro=(0, 0, 0))

        try:
            cmds.parent(jnt, ctrl)
            cmds.parent(ctrl, offset)
            cmds.parent(offset, grp)
        except:
            pass

        cmds.xform(grp, t=pos, ws=True)
        cmds.xform(grp, ro=rot, ws=True)

        ctrlList.append(ctrl)
        ctrlJointList.append(jnt)

    # create skincluster
    skinCluster = 'ikSpine_skinCluster'
    cmds.select(clear=True)
    for jnt in ctrlJointList:
        cmds.select(jnt, add=True)
    cmds.select(ikCurve, add=True)
    if not cmds.objExists(skinCluster):
        skinCluster = cmds.skinCluster(n=skinCluster)

    # set smart ik advanced twist control
    cmds.setAttr(ikHandle+'.dTwistControlEnable', 1)
    cmds.setAttr(ikHandle+'.dWorldUpType', 4)

    cmds.setAttr(ikHandle+'.dForwardAxis', 0)
    cmds.setAttr(ikHandle+'.dWorldUpAxis', 3)

    cmds.setAttr(ikHandle + '.dWorldUpVectorX', 0)
    cmds.setAttr(ikHandle + '.dWorldUpVectorY', 0)
    cmds.setAttr(ikHandle+'.dWorldUpVectorZ', 1)

    cmds.setAttr(ikHandle + '.dWorldUpVectorEndX', 0)
    cmds.setAttr(ikHandle + '.dWorldUpVectorEndY', 0)
    cmds.setAttr(ikHandle + '.dWorldUpVectorEndZ', 1)

    cmds.connectAttr(ctrlJointList[0]+'.worldMatrix', ikHandle+'.dWorldUpMatrix', f=True)
    cmds.connectAttr(ctrlJointList[2] + '.worldMatrix', ikHandle + '.dWorldUpMatrixEnd', f=True)

    # set strech and squash
    crvInfo = ikCurve+'_curveInfo'
    if not cmds.objExists(crvInfo):
        crvInfo = cmds.createNode('curveInfo', n=crvInfo)
    cmds.connectAttr(ikCurve+'Shape.worldSpace', crvInfo+'.inputCurve', f=True)

    crvBuildInfo = ikBuildCurve+'_curveInfo'
    if not cmds.objExists(crvBuildInfo):
        crvBuildInfo = cmds.createNode('curveInfo', n=crvBuildInfo)
    cmds.connectAttr(ikBuildCurve+'Shape.worldSpace', crvBuildInfo+'.inputCurve', f=True)

    lengthRatioMD = ikCurve+'_lengthRatio_MD'
    if not cmds.objExists(lengthRatioMD):
        lengthRatioMD = cmds.createNode('multiplyDivide', n=lengthRatioMD)
    cmds.setAttr(lengthRatioMD+'.operation', 2)
    cmds.connectAttr(crvInfo+'.arcLength', lengthRatioMD+'.input1.input1X', f=True)
    cmds.connectAttr(crvBuildInfo+'.arcLength', lengthRatioMD+'.input2.input2X', f=True)

    squashMD = ikCurve+'_squash_MD'
    if not cmds.objExists(squashMD):
        squashMD = cmds.createNode('multiplyDivide', n=squashMD)
    cmds.setAttr(squashMD+'.operation', 2)
    cmds.setAttr(squashMD+'.input1.input1X', 1)
    cmds.connectAttr(lengthRatioMD+'.outputX', squashMD+'.input2.input2X', f=True)

    squashSqRootMD = ikCurve+'_squash_sqRoot_MD'
    if not cmds.objExists(squashSqRootMD):
        squashSqRootMD = cmds.createNode('multiplyDivide', n=squashSqRootMD)
    cmds.setAttr(squashSqRootMD+'.operation', 3)
    cmds.connectAttr(squashMD+'.outputX', squashSqRootMD+'.input1.input1X', f=True)
    cmds.setAttr(squashSqRootMD+'.input2.input2X', 0.5)

    '''crvLengthCondition = ikCurve+'_condition'
    if not cmds.objExists(crvLengthCondition):
        crvLengthCondition = cmds.createNode('condition', n= crvLengthCondition)
    cmds.setAttr(crvLengthCondition+'.operation', 2)
    cmds.setAttr(crvLengthCondition+'.secondTerm', 1)
    cmds.connectAttr(lengthRatioMD+'.outputX', crvLengthCondition+'.firstTerm', f=True)
    cmds.connectAttr(lengthRatioMD+'.outputX', crvLengthCondition+'.colorIfTrueR', f=True)
    cmds.connectAttr(squashSqRootMD+'.outputX', crvLengthCondition+'.colorIfTrueG', f=True)
    cmds.connectAttr(squashSqRootMD + '.outputX', crvLengthCondition + '.colorIfTrueB', f=True)'''

    for n, jnt in enumerate(jointList):
        if not n == len(jointList)-1:
            cmds.connectAttr(lengthRatioMD+'.outputX', jnt+'.scaleX', f=True)
            cmds.connectAttr(squashSqRootMD+'.outputX', jnt + '.scaleY', f=True)
            cmds.connectAttr(squashSqRootMD + '.outputX', jnt + '.scaleZ', f=True)
        '''else:
            rev_mlm = k.createNode('multMatrix', n=jnt+'_reverse_mlm')

            cmds.connectAttr(ctrlList[-1]+'.worldMatrix', rev_mlm+'.matrixIn[0]', f=True)
            cmds.connectAttr(
                cmds.listRelatives(jnt, p=True)[0]+'.worldInverseMatrix',
                rev_mlm+'.matrixIn[1]',
                f=True
            )

            cmds.connectAttr(rev_mlm+'.matrixSum', jnt+'.offsetParentMatrix', f=True)
            cmds.setAttr(jnt+'.translate', 0, 0, 0)
            cmds.setAttr(jnt + '.rotate', 0, 0, 0)
            cmds.setAttr(jnt + '.scale', 1, 1, 1)'''


    return {
        ikHandle,
        ikCurve,
        ikBuildCurve
    }


# test fuction
'''lst = cmds.ls(sl=True)
buildIKSpine_func(lst, 'locator1')'''
