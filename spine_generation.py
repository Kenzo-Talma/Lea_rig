import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

def generate_spine_func(loc_list):
    # create list
    main_lst = []
    ik_lst = []
    fk_lst = []
    blend_lst = []
    # locator loop
    for n, loc in enumerate(loc_list):
        # get position
        pos = cmds.xform(loc, q=True, t=True, ws=True)

        # joint names
        main = loc+'_main_jnt'
        fk = loc+'_FK_jnt'
        ik = loc+'_IK_jnt'

        # create joint
        main = k.createNode('joint', n=main)
        fk = k.createNode('joint', n=fk)
        ik = k.createNode('joint', n=ik)

        # parent joint
        if not n == 0:
            for ob, lst in zip([main, fk, ik], [main_lst, fk_lst, ik_lst]):
                try:
                    cmds.parent(ob, lst[n - 1])
                except:
                    pass

        # connect limbs
        blm = loc+'_blm'
        blm = k.createNode('blendMatrix', n=blm)
        if cmds.listRelatives(main, p=True):
            fk_mlm = fk.replace('jnt', 'mlm')
            fk_mlm = k.createNode('multMatrix', n=fk_mlm)
            cmds.connectAttr(fk+'.worldMatrix[0]', fk_mlm+'.matrixIn[0]', f=True)
            cmds.connectAttr(
                cmds.listRelatives(fk, p=True)[0]+'.worldInverseMatrix',
                fk_mlm+'.matrixIn[1]',
                f=True
            )

            ik_mlm = ik.replace('jnt', 'mlm')
            ik_mlm = k.createNode('multMatrix', n=ik_mlm)
            cmds.connectAttr(ik + '.worldMatrix[0]', ik_mlm + '.matrixIn[0]', f=True)
            cmds.connectAttr(
                cmds.listRelatives(ik, p=True)[0] + '.worldInverseMatrix',
                ik_mlm + '.matrixIn[1]',
                f=True
            )

            cmds.connectAttr(fk_mlm + '.matrixSum', blm + '.target[1].targetMatrix', f=True)
            cmds.connectAttr(ik_mlm + '.matrixSum', blm + '.target[0].targetMatrix', f=True)

        else:
            cmds.connectAttr(fk+'.worldMatrix', blm+'.target[1].targetMatrix', f=True)
            cmds.connectAttr(ik+'.worldMatrix', blm+'.target[0].targetMatrix', f=True)

        cmds.connectAttr(blm+'.outputMatrix', main+'.offsetParentMatrix', f=True)

        blend_lst.append(blm)

        # set position
        for ob in [ik, fk]:
            cmds.xform(ob, t=pos, ws=True)

        # add joint to list
        main_lst.append(main)
        ik_lst.append(ik)
        fk_lst.append(fk)

    # orient loop:
    n = 1
    for main, ik, fk in zip(main_lst, ik_lst, fk_lst):
        # set joint orientation
        for jnt in [main, fk, ik]:
            if not n == len(loc_list):
                cmds.joint(jnt, e=True, oj='xzy', sao='zup')
            else:
                cmds.joint(jnt, e=True, oj='none')
        cmds.xform(main, t=(0, 0, 0))
        cmds.xform(main, ro=(0, 0, 0))
        cmds.setAttr(main+'.jointOrient', 0, 0, 0)
        n += 1

    # return
    return (
        main_lst,
        ik_lst,
        fk_lst,
        blend_lst
    )


# test function
'''lst = cmds.ls(sl=True)
generate_spine_func(lst)'''