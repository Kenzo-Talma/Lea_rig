import maya.cmds as cmds
import Lea_pythonScript.k_tools as k
import importlib
importlib.reload(k)

def strech_squash_limb_ik_func(limb, parent_node, limb_name, ik_handle, switch):
    # get ik handle group
    ik_grp = ik_handle.replace('ikHandle', 'ctrl')

    # create length network
    # get translate by decompose matrix
    base_length_decompose_matrix = k.createNode('decomposeMatrix', n=parent_node+'_dmc')
    cmds.connectAttr(parent_node+'.worldMatrix', base_length_decompose_matrix+'.inputMatrix', f=True)

    end_length_decompose_matrix = k.createNode('decomposeMatrix', n=ik_handle+'_dmc')
    cmds.connectAttr(ik_grp+'.worldMatrix[0]', end_length_decompose_matrix+'.inputMatrix', f=True)

    # get vector
    vector_plus_minus_average = k.createNode('plusMinusAverage', n=limb_name+'_pma')
    cmds.connectAttr(
        base_length_decompose_matrix+'.outputTranslate',
        vector_plus_minus_average+'.input3D[1]',
        f=True
    )
    cmds.connectAttr(
        end_length_decompose_matrix+'.outputTranslate',
        vector_plus_minus_average+'.input3D[0]',
        f=True
    )
    cmds.setAttr(vector_plus_minus_average+'.operation', 2)

    # power vector
    vector_multiply_divide = k.createNode('multiplyDivide', n=limb_name+'_vector_mld')
    cmds.connectAttr(vector_plus_minus_average+'.output3D', vector_multiply_divide+'.input1', f=True)
    cmds.connectAttr(vector_plus_minus_average+'.output3D', vector_multiply_divide + '.input2', f=True)

    # add attributes
    vector_adl_1 = k.createNode('addDoubleLinear', n=limb_name+'_vector1_adl')
    cmds.connectAttr(vector_multiply_divide+'.outputX', vector_adl_1+'.input1', f=True)
    cmds.connectAttr(vector_multiply_divide+'.outputY', vector_adl_1+'.input2', f=True)

    vector_adl_2 = k.createNode('addDoubleLinear', n=limb_name+'_vector2_adl')
    cmds.connectAttr(vector_adl_1+'.output', vector_adl_2+'.input1', f=True)
    cmds.connectAttr(vector_multiply_divide+'.outputZ', vector_adl_2+'.input2', f=True)

    # get square root : get length
    vector_sqRoot_mld = k.createNode('multiplyDivide', n=limb_name+'vector_mld')
    cmds.connectAttr(vector_adl_2+'.output', vector_sqRoot_mld+'.input1X', f=True)
    cmds.setAttr(vector_sqRoot_mld+'.input2X', 0.5)
    cmds.setAttr(vector_sqRoot_mld+'.operation', 3)

    # calculate length  of the limb
    base_length = 0

    for n, jnt in enumerate(limb):
        if n > 0:
            length = cmds.getAttr(jnt+'.translateX')
            base_length += length

    # set length  ratio multiply divide
    ratio_mld = k.createNode('multiplyDivide', n=limb_name+'_mld')
    cmds.setAttr(ratio_mld + '.input2.input2X', base_length)
    cmds.setAttr(ratio_mld + '.operation', 2)
    cmds.connectAttr(vector_sqRoot_mld+'.outputX', ratio_mld +'.input1.input1X', f=True)

    # create squash value
    division_mld = k.createNode('multiplyDivide', n=limb_name+'_divide_mld')
    cmds.setAttr(division_mld+'.operation', 2)
    cmds.connectAttr(ratio_mld + '.outputX', division_mld+'.input2.input2X', f=True)
    cmds.setAttr(division_mld+'.input1.input1X', 1)

    # create squash square root
    sqRoot_mld = k.createNode('multiplyDivide', n=limb_name+'_sqRoot_mld')
    cmds.setAttr(sqRoot_mld + '.operation', 3)
    cmds.setAttr(sqRoot_mld + '.input2.input2X', 0.5)
    cmds.connectAttr(division_mld+'.outputX', sqRoot_mld+'.input1.input1X', f=True)

    # create condition node
    condition_node = k.createNode('condition', n=limb_name+'_condition')
    cmds.connectAttr(ratio_mld + '.output.outputX', condition_node+'.firstTerm', f=True)
    cmds.setAttr(condition_node+'.secondTerm', 1)
    cmds.setAttr(condition_node+'.operation', 2)
    cmds.connectAttr(ratio_mld + '.output.outputX', condition_node+'.colorIfTrue.colorIfTrueR', f=True)
    cmds.connectAttr(sqRoot_mld+'.output.outputX', condition_node+'.colorIfTrue.colorIfTrueG', f=True)
    cmds.connectAttr(sqRoot_mld+'.output.outputX', condition_node+'.colorIfTrue.colorIfTrueB', f=True)

    # switch attribute
    attr = 'strech'
    if not cmds.objExists(f'{switch}.{attr}'):
        cmds.addAttr(switch, ln=attr, at='bool', k=False)
        cmds.setAttr(f'{switch}.{attr}', cb=True, k=False)
    attr = f'{switch}.{attr}'

    # connect switch
    switch_con = k.createNode('condition', n=switch+'_strech_condition')
    cmds.connectAttr(attr, switch_con+'.firstTerm', f=True)
    cmds.setAttr(switch_con+'.secondTerm', 1)
    cmds.connectAttr(condition_node+'.outColor', switch_con+'.colorIfTrue', f=True)

    # connect to scale value
    for jnt in limb:
        cmds.connectAttr(switch_con+'.outColor', jnt+'.scale', f=True)


# test function
#test = [
#    "ik_leg_1_jnt",
#    "ik_leg_2_jnt",
#    "ik_leg_3_jnt"
#]
#strech_squash_limb_ik_func(test, 'ik_leg_3_grp', 'ik_leg', 'ik_leg_3_ikHandle')

