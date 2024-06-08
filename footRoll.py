import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)
def builtFootRoll_func(foot, locList, name, reverse=False):
    # create list
    ctrlList = []
    offsetList = []
    grpList = []
    joint_list = []

    # build controleurs
    oldCtrl = None
    for loc in locList:
        if not reverse:
            ctrl = loc+'_ctrl'
            offset = loc+'_offset'
            grp = loc+'_grp'
        else:
            ctrl = loc.replace('R_', 'L_') + '_ctrl'
            offset = loc.replace('R_', 'L_') + '_offset'
            grp = loc.replace('R_', 'L_') + '_grp'

        if not reverse:
            pos = cmds.xform(loc, q=True, t=True, ws=True, a=True)
            rot = cmds.xform(loc, q=True, ro=True, ws=True, a=True)
        else:
            pos = cmds.xform(loc, q=True, t=True, ws=True, a=True)
            rot = cmds.xform(loc, q=True, ro=True, ws=True, a=True)
            pos = [-pos[0], pos[1], pos[2]]
            rot = [rot[0]-180, rot[1], rot[2]-180]

        if not cmds.objExists(ctrl):
            ctrl = cmds.circle(n=ctrl)
            cmds.delete(ctrl[1])
            ctrl = ctrl[0]

        if not cmds.objExists(offset):
            offset = cmds.group(ctrl, n=offset)

        if not cmds.objExists(grp):
            grp = cmds.group(offset, n=grp)

        cmds.xform(grp, t=pos, ws=True, a=True)
        cmds.xform(grp, ro=rot, ws=True, a=True)

        if not oldCtrl == None:
            cmds.parent(grp, oldCtrl)

        ctrlList.append(ctrl)
        offsetList.append(offset)
        grpList.append(grp)

        oldCtrl = ctrl

    cmds.parent(grpList[1], world=True)

    # orient joints
    for n, ob in enumerate([locList[-1], locList[-2], locList[-3]]):
        jnt = ob+'_jnt'
        jnt = k.createNode('joint', n=jnt)
        joint_list.append(jnt)
        cmds.xform(
            jnt,
            t=cmds.xform(ob, q=True, t=True, ws=True),
            ws=True
        )

    for n, jnt in enumerate(joint_list):
        if not n == 0:
            cmds.parent(jnt, joint_list[n-1])

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

    for jnt, grp in zip(reversed(joint_list), [grpList[-3], grpList[-2], grpList[-1]]):
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

    # create foot roll network
    ballCmp = name+'_ball_clamp'
    if not cmds.objExists(ballCmp):
        ballCmp = cmds.createNode('clamp', n=ballCmp)

    if not 'footBreak' in cmds.listAttr(ctrlList[0]):
        cmds.addAttr(ctrlList[0], ln='footBreak', at='float', k=True, min=0, max=90, dv=25)

    locator = k.createNode('transform', n=ctrlList[-2].replace('ctrl', 'loc'))
    cmds.parent(locator, ctrlList[-2])
    cmds.setAttr(locator+'.translate', 0, 0, 0)
    cmds.setAttr(locator + '.rotate', 0, 0, 0)
    cmds.setAttr(locator + '.scale', 1, 1, 1)
    cmds.setAttr(locator + '.shear', 0, 0, 0)
    cmds.parent(grpList[-1], locator)

    cmds.connectAttr(ctrlList[0]+'.rotateX', ballCmp+'.inputR', f=True)
    cmds.connectAttr(ctrlList[0]+'.footBreak', ballCmp+'.maxR', f=True)
    cmds.connectAttr(ballCmp+'.outputR', locator+'.rotateY', f=True)

    toeCondition = name+'_toe_condition'
    if not cmds.objExists(toeCondition):
        toeCondition = cmds.createNode('condition', n=toeCondition)

    cmds.connectAttr(ctrlList[0]+'.rotateX', toeCondition+'.colorIfTrueR', f=True)
    cmds.connectAttr(ctrlList[0]+'.rotateX', toeCondition+'.firstTerm', f=True)
    cmds.connectAttr(ctrlList[0]+'.footBreak', toeCondition+'.secondTerm', f=True)
    cmds.setAttr(toeCondition+'.operation', 2)

    toeRmv = name+'_toe_remapValue'
    if not cmds.objExists(toeRmv):
        toeRmv = cmds.createNode('remapValue', n=toeRmv)

    cmds.connectAttr(ctrlList[0]+'.footBreak', toeRmv+'.inputMin', f=True)
    cmds.connectAttr(toeCondition+'.outColorR', toeRmv+'.inputValue', f=True)
    cmds.setAttr(toeRmv+'.inputMax', 180)
    cmds.setAttr(toeRmv+'.outputMax', 180)

    cmds.connectAttr(toeRmv+'.outValue', offsetList[-3]+'.rotateY', f=True)

    hellCmp = name+'_heel_clamp'
    if not cmds.objExists(hellCmp):
        hellCmp = cmds.createNode('clamp', n=hellCmp)

    cmds.connectAttr(ctrlList[0]+'.rotateX', hellCmp+'.inputR', f=True)
    cmds.setAttr(hellCmp+'.minR', -180)
    if not reverse:
        cmds.connectAttr(hellCmp+'.outputR', offsetList[-4]+'.rotateX', f=True)
    else :
        hell_mdl = k.createNode('multDoubleLinear', n=hellCmp+'_rev')
        cmds.connectAttr(hellCmp+'.outputR', hell_mdl+'.input1', f=True)
        cmds.setAttr(hell_mdl+'.input2', -1)
        cmds.connectAttr(hell_mdl+'.output', offsetList[-4]+'.rotateX', f=True)

    # create bank network
    inBank = name+'_inBank_clamp'
    if not cmds.objExists(inBank):
        inBank = cmds.createNode('clamp', n=inBank)

    cmds.connectAttr(ctrlList[0]+'.rotateZ', inBank+'.inputR', f=True)
    cmds.setAttr(inBank+'.maxR', 180)
    cmds.connectAttr(inBank+'.outputR', offsetList[5]+'.rotateZ', f=True)

    outBank = name+'_outBank_clamp'
    if not cmds.objExists(outBank):
        outBank = cmds.createNode('clamp', n=outBank)

    cmds.connectAttr(ctrlList[0]+'.rotateZ', outBank+'.inputR', f=True)
    cmds.setAttr(outBank+'.minR', -180)
    cmds.connectAttr(outBank+'.outputR', offsetList[4]+'.rotateZ', f=True)

    # reverse fix
    if reverse:
        cmds.xform(grpList[0], ro=(0,0,0))

# test function
'''lst = [
    'R_footRoll', 
    'R_hellSlide', 
    'R_ballSlide', 
    'R_toeSlide', 
    'R_sideOut', 
    'R_sideIn', 
    'R_hell', 
    'R_toe', 
    'R_ball', 
    'R_ankle'
]
builtFootRoll_func('foot', lst, 'R')'''

# addAttr -ln "footBreak" -nn "Foot Break" -at double  -min 0 -max 90 -dv 25 |footRoll_grp|footRoll
