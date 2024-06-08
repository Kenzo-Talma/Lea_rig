import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)
def createRibbonJoints_func(ribbon, joint_number, switch):
    joint_list = []
    ribbon_shape = cmds.listRelatives(ribbon, s=True, type='nurbsSurface', c=True)[0]
    ribbon_shape_orig = cmds.listRelatives(ribbon, s=True, type='nurbsSurface', c=True)[1]

    u_increment = 1/(joint_number-1)

    # create UV pin node
    uv_pin = ribbon+'_uvPin'
    if not cmds.objExists(uv_pin):
        uv_pin = cmds.createNode('uvPin', n=uv_pin)
    cmds.connectAttr(ribbon_shape+'.worldSpace[0]', uv_pin+'.deformedGeometry', f=True)
    cmds.connectAttr(ribbon_shape_orig+'.local', uv_pin+'.originalGeometry', f=True)

    # create arc length dimension
    adl = k.createNode('arcLengthDimension', n=ribbon_shape.replace('Shape', 'adl'), p=ribbon)
    cmds.connectAttr(ribbon_shape+'.worldSpace[0]', adl+'.nurbsGeometry', f=True)
    cmds.setAttr(adl+'.uParamValue', 1)
    cmds.setAttr(adl+'.vParamValue', 0.5)

    adl_orig = k.createNode('arcLengthDimension', n=ribbon_shape_orig.replace('Shape', 'adl'), p=ribbon)
    cmds.connectAttr(ribbon_shape_orig+'.worldSpace[0]', adl_orig+'.nurbsGeometry', f=True)
    cmds.setAttr(adl_orig + '.uParamValue', 1)
    cmds.setAttr(adl_orig + '.vParamValue', 0.5)

    # connect strech network
    # ratio
    ratio_mld = k.createNode('multiplyDivide', n=ribbon+'ratio_mld')
    cmds.connectAttr(adl+'.arcLength', ratio_mld+'.input1.input1X', f=True)
    cmds.connectAttr(adl_orig+'.arcLength', ratio_mld+'.input2.input2X', f=True)
    cmds.setAttr(ratio_mld+'.operation', 2)

    # inverse ratio
    inv_mld = k.createNode('multiplyDivide', n=ribbon+'_inv_mld')
    cmds.setAttr(inv_mld+'.input1.input1X', 1)
    cmds.connectAttr(ratio_mld+'.output.outputX', inv_mld+'.input2.input2X', f=True)
    cmds.setAttr(inv_mld+'.operation', 2)

    # square root ratio
    sq_root_mld = k.createNode('multiplyDivide', n=ribbon+'sqRoot_mld')
    cmds.connectAttr(inv_mld+'.output.outputX', sq_root_mld+'.input1.input1X', f=True)
    cmds.setAttr(sq_root_mld+'.input2.input2X', 0.5)
    cmds.setAttr(sq_root_mld+'.operation', 3)

    # create switch attribute
    switch_attr = 'strech'
    if not cmds.objExists(f'{switch}.{switch_attr}'):
        cmds.addAttr(switch, ln=switch_attr, at='bool', k=False)
        cmds.setAttr(f'{switch}.{switch_attr}', cb=True, k=False)
    switch_attr = f'{switch}.{switch_attr}'

    # connect switch
    cond = k.createNode('condition', n=ribbon+'_condition')
    cmds.connectAttr(switch_attr, cond+'.firstTerm', f=True)
    cmds.setAttr(cond+'.secondTerm', 1)
    cmds.connectAttr(sq_root_mld+'.output.outputX', cond+'.colorIfTrue.colorIfTrueG', f=True)
    cmds.connectAttr(sq_root_mld+'.output.outputX', cond+'.colorIfTrue.colorIfTrueB', f=True)
    
    # create power attribute
    power_attr = 'strech_intensity'
    if not cmds.objExists(f'{switch}.{power_attr}'):
        cmds.addAttr(switch, ln=power_attr, at='float', dv=1, k=False)
        cmds.setAttr(f'{switch}.{power_attr}', cb=True, k=False)
    power_attr = f'{switch}.{power_attr}'

    # connect power attribute
    power_mld = k.createNode('multiplyDivide', n=switch+'power_mld')
    cmds.connectAttr(cond+'.outColor', power_mld+'.input1', f=True)
    for at in ['X', 'Y', 'Z']:
        cmds.connectAttr(power_attr, f'{power_mld}.input1.input1{at}', f=True)
    cmds.setAttr(power_mld+'.operation', 3)

    # create and connect joints to uv_pin
    for i in range(joint_number):
        jnt = ribbon+'_'+str(i+1)+'_jnt'
        u_pos = u_increment*i

        # create joint
        if not cmds.objExists(jnt):
            jnt = cmds.createNode('joint', n=jnt)

        # connect joint
        cmds.connectAttr(uv_pin+'.outputMatrix['+str(i)+']', jnt+'.offsetParentMatrix', f=True)

        # set joint position
        cmds.setAttr(uv_pin+'.coordinate['+str(i)+'].coordinateU', u_pos)
        cmds.setAttr(uv_pin+'.coordinate['+str(i)+'].coordinateV', 0.5)

        # connect joint orient
        cmds.setAttr(jnt+'.jointOrientX', -90)
        cmds.setAttr(jnt+'.jointOrientY', -90)

        # connect scale
        cmds.connectAttr(power_mld+'.output', jnt+'.scale', f=True)

        # add joint to list
        joint_list.append(jnt)
        

    return joint_list

# test fuction
#rib = cmds.ls(sl=True)[0]
#joints = createRibbonJoints_func(rib, 5)
#print(joints)
