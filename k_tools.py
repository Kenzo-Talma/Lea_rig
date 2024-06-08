import maya.cmds as cmds
import importlib
from Lea_pythonScript import shape_list
importlib.reload(shape_list)


def createNode(typ='transform',**kwargs):
    if 'n' in kwargs:
        if not cmds.objExists(kwargs['n']):
            if typ == 'spaceLocator':
                return cmds.spaceLocator(**kwargs)[0]
            else:
                return cmds.createNode(typ, **kwargs)
        else:
            return kwargs['n']


def matrixConstraint(**kwargs):
    ''' create a mult matrix to constraint objects

    :param kwargs:
        parent(str): parent node
        child(str): child node (follow)
        offset(str): offset node (optional)
        reset_transform(bool): reset child transform node (optional)
    :return:
    '''

    # kwargs
    parent = None
    if 'parent' in kwargs:
        parent = kwargs['parent']

    child = None
    if 'child' in kwargs:
        child = kwargs['child']

    offset = None
    if 'offset' in kwargs:
        offset = kwargs['offset']

    reset_transform = None
    if 'reset_transform' in kwargs:
        reset_transform = kwargs['reset_transform']

    # create node
    if parent and child:
        mult_matrix = f'{child}_multMatrix'

        #createNode('multMatrix', n=mult_matrix)

        if not cmds.objExists(mult_matrix):
            mult_matrix = cmds.createNode('multMatrix', n=mult_matrix)

        # connect node
        if offset:
            cmds.connectAttr(
                offset+'.worldInverseMatrix[0]',
                mult_matrix+'.matrixIn[1]',
                force=True
            )
        elif cmds.listRelatives(child, parent=True):
            cmds.connectAttr(
                cmds.listRelatives(child, parent=True)[0]+'.worldInverseMatrix[0]',
                mult_matrix+'.matrixIn[1]',
                force=True
            )
        else:
            cmds.connectAttr(
                parent+'.worldMatrix[0]',
                child+'.offsetParentMatrix',
                force=True
            )
            cmds.delete(mult_matrix)
            return None

        cmds.connectAttr(
            parent+'.worldMatrix[0]',
            mult_matrix+'.matrixIn[0]',
            force=True
        )
        cmds.connectAttr(
            mult_matrix+'.matrixSum',
            child+'.offsetParentMatrix',
            force=True
        )

        if reset_transform:
            cmds.xform(child, ro=(0,0,0))
            cmds.xform(child, t=(0,0,0))
            cmds.xform(child, s=(0,0,0))


def create_simple_ctrl(name=None, locator=None, joint=True):
    """
    create a simple control with two offset parent group
    :param name: name of the controller
    :param locator: position
    :param joint: if true create joint
    :return: group, controller, joint
    """
    # create control
    if not name:
        print('no name given')
        return None, None, None

    ctrl = name+'_ctrl'
    offset = name+'_offset'
    grp = name+'_grp'

    ctrl = cmds.circle(n=ctrl)[0]
    offset = createNode('transform', n=offset)
    grp = createNode('transform', n=grp)

    cmds.parent(ctrl, offset)
    cmds.parent(offset, grp)

    # create joint
    if joint:
        jnt = createNode('joint', n=name+'_jnt')

        cmds.connectAttr(
            ctrl+'.worldMatrix',
            jnt+'.offsetParentMatrix',
            f=True
        )
    else:
        jnt = None

    # set position
    if locator:
        cmds.xform(
            grp,
            t=cmds.xform(locator, q=True, t=True, ws=True),
            ws=True
        )
        cmds.xform(
            grp,
            ro=cmds.xform(locator, q=True, ro=True, ws=True),
            ws=True
        )
        cmds.xform(
            grp,
            s=cmds.xform(locator, q=True, s=True, ws=True),
            ws=True
        )

    return grp, ctrl, jnt


def space_switch(follow_parent='world', parent_list=None, target_list=None, control=None, skip_list=None):
    """
    parent nodes and create space switch can be use as matrix constraint
    :param follow_parent: parent that follow the given nodes
    :param parent_list: list of parents
    :param target_list: list of targets
    :param control: controller that get the switch attributes
    :param skip_list: list of attributes that will be skipped by script
    :return: follow list
    """
    # check list
    if parent_list and target_list:
        if not isinstance(parent_list, list):
            parent_list = [parent_list]
        if not isinstance(target_list, list):
            target_list = [target_list]

    # def follow list
    follow_list = []

    # parent attr list
    parent_attr_list = [follow_parent]+parent_list

    # target loop
    for target in target_list:
        # create nodes
        target_ref = createNode('transform', n=target+'_ref')
        blm = createNode('blendMatrix', n=target+'_blm')
        follow = createNode('transform', n=target+'_follow')
        follow_list.append(follow)

        cmds.xform(
            target_ref,
            m=cmds.xform(target, q=True, m=True, ws=True),
            ws=True
        )

        if cmds.listRelatives(target, p=True):
            cmds.parent(follow, cmds.listRelatives(target, p=True)[0])
        cmds.parent(target, follow)

        # reset node
        if not cmds.listConnections(target+'.translate', s=True, d=False):
            cmds.setAttr(target+'.translate', 0, 0, 0)
        if not cmds.listConnections(target + '.rotate', s=True, d=False):
            cmds.setAttr(target + '.rotate', 0, 0, 0)
        if not cmds.listConnections(target + '.scale', s=True, d=False):
            cmds.setAttr(target + '.scale', 1, 1, 1)
        if not cmds.listConnections(target + '.shear', s=True, d=False):
            cmds.setAttr(target + '.shear', 0, 0, 0)
        if not cmds.listConnections(target+'.offsetParentMatrix', s=True, d=False):
            cmds.setAttr(
                target+'.offsetParentMatrix',
                (
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0
                ),
                type='matrix'
            )

        # connect blendMatrix
        if not follow_parent == 'world':
            parent_ref = createNode('transform', n=follow_parent + '_ref')
            parent_mlm = createNode('multMatrix', n=f'{follow_parent}_{target}_mlm')
            cmds.xform(
                parent_ref,
                m=cmds.xform(follow_parent, q=True, m=True, ws=True),
                ws=True
            )
            cmds.connectAttr(target_ref+'.worldMatrix', parent_mlm+'.matrixIn[0]', f=True)
            cmds.connectAttr(parent_ref+'.worldInverseMatrix', parent_mlm+'.matrixIn[1]', f=True)
            cmds.connectAttr(follow_parent+'.worldMatrix', parent_mlm+'.matrixIn[2]', f=True)
            cmds.connectAttr(parent_mlm+'.matrixSum', blm+'.inputMatrix', f=True)

        cmds.connectAttr(blm+'.outputMatrix', follow+'.offsetParentMatrix', f=True)

        # create attribute
        if not control:
            control = target
        attr = target+'_space'
        if not cmds.objExists(f'{control}.{attr}'):
            cmds.addAttr(control, ln=attr, at='enum', en=':'.join(parent_attr_list), k=True)
            attr = f'{control}.{attr}'
            cmds.setAttr(attr, cb=True, k=True)

        # parent loop
        for n, parent in enumerate(parent_list):
            # create node
            mlm = createNode('multMatrix', n=f'{parent}_{target}_mlm')
            ref = createNode('transform', n=parent+'_ref')
            con = createNode('condition', n=f'{parent}_{target}_con')

            cmds.xform(
                ref,
                m=cmds.xform(parent, q=True, m=True, ws=True),
                ws=True
            )

            cmds.connectAttr(target_ref+'.worldMatrix', mlm+'.matrixIn[0]', f=True)
            cmds.connectAttr(ref+'.worldInverseMatrix', mlm+'.matrixIn[1]', f=True)
            cmds.connectAttr(parent+'.worldMatrix', mlm+'.matrixIn[2]', f=True)
            cmds.connectAttr(mlm+'.matrixSum', f'{blm}.target[{n}].targetMatrix', f=True)

            cmds.connectAttr(attr, con+'.firstTerm', f=True)
            cmds.setAttr(con+'.secondTerm', n+1)
            cmds.setAttr(con+'.colorIfTrueR', 1)
            cmds.setAttr(con+'.colorIfFalseR', 0)
            cmds.connectAttr(con+'.outColorR', f'{blm}.target[{n}].weight', f=True)

            if skip_list:
                for at in skip_list:
                    cmds.setAttr(f'{blm}.target[{n}].{at}Weight', 0)

    return follow_list


def create_controls(shape=None, name=None, scale=(1, 1, 1), color=0, width=2):
    """
    :param shape:
    :param name:
    :param scale:
    :return:
    """
    # get shapes
    shape_dic = shape_list.return_shape(shape)

    # scale
    point_list = shape_dic['p']
    p_list = []
    for point in point_list:
        p = (point[0]*scale[0], point[1]*scale[1], point[2]*scale[2])
        p_list.append(p)

    # create curve
    cur = cmds.curve(
        p=p_list,
        d=shape_dic['d'],
        per=shape_dic['periodic'],
        n=name,
        k=shape_dic['k']
    )
    cmds.rename(cmds.listRelatives(cur, s=True)[0], cur+'Shape')

    # return curve name
    return cur

def swap_shapes(ctrl=None, shape=None, scale=(1, 1, 1), color=0, width=2):
    """
    swap control shape
    :param ctrl: parent transform
    :param shape: shape design
    :param scale: scale of the shape
    :param color: color of the shape
    :param width: width of the shape
    :return: None
    """
    # get shapes
    shape_dic = shape_list.return_shape(shape)

    # scale
    point_list = shape_dic['p']
    p_list = []
    for point in point_list:
        p = (point[0] * scale[0], point[1] * scale[1], point[2] * scale[2])
        p_list.append(p)

    # delete shapes
    plug = cmds.listConnections(
        cmds.listRelatives(ctrl, s=True)[0]+'.v',
        s=True,
        d=False,
        p=True
    )
    cmds.delete(cmds.listRelatives(ctrl, s=True))

    # create curve
    cur = cmds.curve(
        p=p_list,
        d=shape_dic['d'],
        per=shape_dic['periodic'],
        k=shape_dic['k']
    )
    sh = cmds.rename(cmds.listRelatives(cur, s=True)[0], ctrl+'Shape')
    cmds.parent(sh, ctrl, r=True, s=True)

    cmds.setAttr(sh+'.overrideEnabled', 1)
    cmds.setAttr(sh+'.overrideColor', color)

    cmds.setAttr(sh+'.lineWidth', width)

    if plug:
        cmds.connectAttr(plug[0], sh+'.v', f=True)

    cmds.delete(cur)
