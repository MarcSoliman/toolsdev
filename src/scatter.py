import maya.cmds as cmds


def create_cylinder():
    cmds.polyCylinder()


def selection_list():
    selection = cmds.ls(os=True, fl=True)
    vertex_name = cmds.filterExpand(selection, selectionMask=31, expand=True) \
                  or []
    object_to_instance = selection[0]

    # print(vertex_name)

    if cmds.objectType(object_to_instance, isType="transform"):

        for vertex in vertex_name:

            new_instance = cmds.instance(object_to_instance)

            position = cmds.pointPosition(vertex, w=True)

            cmds.move(position[0], position[1],
                      position[2], new_instance, a=True, ws=True)

    else:
        print("Please ensure the first object you select is a transform.")
