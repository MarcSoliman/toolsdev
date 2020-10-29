from pymel.all import *

import pymel.core.datatypes as dt

import maya.cmds as cmds
import maya.mel as mel


def create_cylinder():
    cmds.polyCylinder()


def instance_vert():
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

    # Gets the center of the object's face


def get_face_center(p_face_name):
    vertex_positions = dt.Vector(
        cmds.xform(p_face_name, q=True, ws=True, t=True))

    _sum = dt.Vector(0, 0, 0)
    for v in vertex_positions:
        _sum = _sum.__add__(v)

    num_vertices = dt.length(vertex_positions)

    average = _sum.__div__(num_vertices)

    # if (_sum == 0) or (num_vertices == 0):
    #   average = [0, 0, 0]
    #   cmds.warning("Attempt to divide by 0")

    # else:
    return average


def instance_face():
    selection = cmds.ls(os=True, fl=True)
    face_name = cmds.filterExpand(selection, selectionMask=34,
                                  expand=True) or []

    object_to_instance = selection[0]

    if cmds.objectType(object_to_instance, isType="transform"):

        for face in face_name:
            new_instance = cmds.instance(object_to_instance)

            position = get_face_center(str(face))

            cmds.move(position[0], position[1], position[2], new_instance,
                      a=True, ws=True)
    else:
        print("Please ensure the first object you select is a transform.")
