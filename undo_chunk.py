import maya.cmds as cmds


def undo(function):
    '''
    this function is a decorator
    write @undo before a fuction to use it

    argument:
        function
    '''

    def undo_call(*args, **kwargs):
        function_result = None

        # open undo chunck
        cmds.undoInfo(
            openChunk=True,
            chunkName=function.__name__
        )

        # launch function
        function_result = function(*args, **kwargs)

        # close the undo chunk
        cmds.undoInfo(closeChunk=True)

        # call function
        return function_result

    # call function call
    return undo_call