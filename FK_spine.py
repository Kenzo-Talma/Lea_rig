import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

def buildFKSpine_func(jointList, midLowJoint, midUpJoint):
    # create controllers
    startJoint = jointList[0]
    endJoint = jointList[-1]

    jntList = [startJoint, midLowJoint, midUpJoint, endJoint]
    ctrlName = ['C_hip_fkSpine', 'C_spineLow_fkSpine', 'C_spineUp_fkSpine', 'C_shoulder_fkSpine']
    ctrlList = []

    for jnt, name in zip(jntList, ctrlName):
        pos = cmds.xform(jnt, q=True, t=True, ws=True)
        rot = cmds.xform(jnt, q=True, ro=True, ws=True)

        ctrl = name + '_ctrl'
        offset = name + '_offset'
        grp = name + '_grp'

        if not cmds.objExists(ctrl):
            ctrl = cmds.circle(ch=False, n=ctrl)[0]
        if not cmds.objExists(offset):
            offset = cmds.group(em=True, n=offset)
        if not cmds.objExists(grp):
            grp = cmds.group(em=True, n=grp)

        for ob in [ctrl, offset]:
            cmds.xform(ob, t=(0,0,0))
            cmds.xform(ob, ro=(0,0,0))

        try:
            cmds.parent(ctrl, offset)
            cmds.parent(offset, grp)
        except:
            pass

        cmds.xform(grp, t=pos, ws=True)
        cmds.xform(grp, ro=rot, ws=True)

        # create sticky network
        if not jnt == startJoint:
            sticky_mlm = ctrl.rpartition('_')[0]+'Sticky_mlm'
            sticky_mlm = k.createNode('multMatrix', n=sticky_mlm)
            cmds.connectAttr(jnt+'.worldMatrix[0]', sticky_mlm+'.matrixIn[1]', f=True)
            cmds.connectAttr(grp+'.worldInverseMatrix', sticky_mlm+'.matrixIn[2]', f=True)
            cmds.connectAttr(ctrl+'.inverseMatrix', sticky_mlm + '.matrixIn[0]', f=True)
            cmds.connectAttr(sticky_mlm+'.matrixSum', offset+'.offsetParentMatrix', f=True)

        # append to control list
        ctrlList.append(ctrl)

    for n, ctrl in enumerate(ctrlList):
        if not n == 0:
            oldCtrl = ctrlList[n-1]
            cmds.parent(ctrl.split('_ctrl')[0]+'_grp', oldCtrl)

    # connect controllers to joints

    for jnt, ctrl in zip(jntList, ctrlList):
        chList = cmds.ls(jnt, dag=True)
        parList = cmds.ls(jnt, l=True)[0].split('|')
        parList.pop(0)

        if chList == None:
            chList = [jnt]

        if ctrl == ctrlList[0]:
            offset = cmds.listRelatives(ctrl, p=True)[0]
            cmds.connectAttr(offset + '.worldMatrix', jnt + '.offsetParentMatrix', f=True)

            cmds.setAttr(startJoint+'.translate', 0, 0, 0)
            cmds.setAttr(startJoint + '.rotate', 0, 0, 0)
            cmds.setAttr(startJoint + '.jointOrientX', 0)
            cmds.setAttr(startJoint + '.jointOrientY', 0)
            cmds.setAttr(startJoint + '.jointOrientZ', 0)

            # create reverse hip
            offset = cmds.listRelatives(ctrl, p=True)[0]
            grp = cmds.listRelatives(offset, p=True)[0]
            rev_hip = cmds.circle(n=ctrl.replace('ctrl', 'reverse_ctrl'))[0]
            rev_hip_offset = k.createNode('transform', n=ctrl.replace('ctrl', 'reverse_offset'))
            cmds.parent(rev_hip, rev_hip_offset)
            cmds.parent(rev_hip_offset, grp)
            cmds.xform(
                rev_hip_offset,
                t=cmds.xform(grp, q=True, t=True, ws=True),
                ws=True
            )
            cmds.xform(
                rev_hip_offset,
                ro=cmds.xform(grp, q=True, ro=True, ws=True),
                ws=True
            )

            jnt_1 = jntList[0]
            jnt_2 = cmds.ls(jnt_1, dag=True)[2]
            rev_pos_1 = k.createNode('transform', n=jnt_2.replace('jnt', 'reverse_pos'))
            rev_pos_grp = k.createNode('transform', n=rev_pos_1.replace('pos', 'grp'))
            rev_pos_2 = k.createNode('transform', n=jnt_1.replace('jnt', 'reverse_pos'))
            cmds.parent(rev_pos_1, rev_pos_grp)
            cmds.parent(rev_pos_2, rev_pos_1)

            cmds.xform(
                rev_pos_grp,
                t=cmds.xform(jnt_2, q=True, t=True, ws=True),
                ws=True
            )
            cmds.xform(
                rev_pos_grp,
                ro=cmds.xform(jnt_2, q=True, ro=True, ws=True),
                ws=True
            )

            cmds.xform(
                rev_pos_2,
                t=cmds.xform(jnt_1, q=True, t=True, ws=True),
                ws=True
            )
            cmds.xform(
                rev_pos_2,
                ro=cmds.xform(jnt_1, q=True, ro=True, ws=True),
                ws=True
            )
            cmds.connectAttr(rev_pos_2+'.worldMatrix', jnt+'.offsetParentMatrix', f=True)

            rev_mlm = k.createNode('multMatrix', n=rev_pos_1.replace('pos', 'mlm'))
            rev_pmc = k.createNode('pickMatrix', n=rev_pos_1.replace('pos', 'pmc'))
            cmds.connectAttr(ctrl + '.worldMatrix', rev_mlm + '.matrixIn[0]', f=True)
            cmds.connectAttr(
                cmds.listRelatives(ctrl, p=True)[0] + '.worldInverseMatrix',
                rev_mlm + '.matrixIn[1]',
                f=True
            )
            cmds.connectAttr(rev_mlm + '.matrixSum', rev_pmc + '.inputMatrix', f=True)
            cmds.setAttr(rev_pmc + '.useRotate', 0)
            cmds.setAttr(rev_pmc + '.useScale', 0)
            cmds.setAttr(rev_pmc + '.useShear', 0)
            cmds.connectAttr(rev_pmc + '.outputMatrix', rev_pos_1 + '.offsetParentMatrix', f=True)

            cmds.connectAttr(rev_hip+'.rotate', rev_pos_1+'.rotate', f=True)

        for n, chi in enumerate(chList):
            # connect rotate
            rot_mdl = ctrl.rpartition('_')[0]+'_rotate_mld'
            rot_mdl = k.createNode('multiplyDivide', n=rot_mdl)
            cmds.connectAttr(ctrl + '.rotate', rot_mdl + '.input1', f=True)
            if ctrl == ctrlList[0]:
                if not n == 0:
                    print(chi)
                    # create reverse hip
                    va = 1/2
                    cmds.setAttr(rot_mdl + '.input2', va, va, va)

                    rev_mld = k.createNode('multiplyDivide', n=chi.replace('jnt', 'reverse_mld'))
                    cmds.connectAttr(rev_hip+'.rotate', rev_mld+'.input1', f=True)
                    cmds.setAttr(rev_mld+'.input2', -va, -va, -va)

                    rev_pma = k.createNode('plusMinusAverage', n=chi.replace('jnt', 'reverse_pma'))
                    cmds.connectAttr(rot_mdl+'.output', rev_pma+'.input3D[0]', f=True)
                    cmds.connectAttr(rev_mld+'.output', rev_pma+'.input3D[1]', f=True)
                    cmds.connectAttr(rev_pma+'.output3D', chi+'.rotate', f=True)
                    print(rev_pma)
            elif not len(chList) == 1:
                va = 1 / 3
                cmds.setAttr(rot_mdl + '.input2', va, va, va)
                cmds.connectAttr(rot_mdl + '.output', chi + '.rotate', f=True)
            else:
                cmds.setAttr(rot_mdl + '.input2', 1, 1, 1)
                cmds.connectAttr(rot_mdl + '.output', chi + '.rotate', f=True)

        # connect Translate
        for n, par in enumerate(parList):
            tra_mdl = ctrl.rpartition('_')[0]+'_translate_mld'
            tra_mdl = k.createNode('multiplyDivide', n=tra_mdl)
            cmds.connectAttr(ctrl+'.translate', tra_mdl+'.input1', f=True)
            if jnt == jntList[0]:
                if not n == 0:
                    va = 1/2
                    cmds.setAttr(tra_mdl + '.input2', va, va, va)
            elif not len(parList) == 1:
                va = 1 / 3
                cmds.setAttr(tra_mdl+'.input2', va, va, va)
            else:
                cmds.setAttr(tra_mdl + '.input2', 1, 1, 1)

            tra_pma = ctrl.rpartition('_')[0]+'_translate_pma'
            tra_pma = k.createNode('plusMinusAverage', n=tra_pma)
            cmds.connectAttr(tra_mdl+'.output', tra_pma+'.input3D[0]', f=True)
            cmds.setAttr(
                tra_pma+'.input3D[1]',
                cmds.getAttr(par+'.translateX'),
                cmds.getAttr(par + '.translateY'),
                cmds.getAttr(par + '.translateZ')
            )

            try:
                cmds.connectAttr(tra_pma+'.output3D', par+'.translate')
            except:
                pass

    cmds.setAttr(startJoint+'.jointOrientX', 0)
    cmds.setAttr(startJoint + '.jointOrientY', 0)
    cmds.setAttr(startJoint + '.jointOrientZ', 0)

    cmds.disconnectAttr(
        cmds.listConnections(jntList[0] + '.translate', p=True, s=True)[0],
        jntList[0]+'.translate'
    )

    cmds.setAttr(startJoint+'.translate', 0, 0, 0)


# test fuction
'''lst = cmds.ls(sl=True)
buildFKSpine_func(lst, 'locator4_FK_jnt', 'locator7_FK_jnt')'''