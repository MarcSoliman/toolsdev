from pymel.all import *

from PySide2 import QtWidgets, QtCore, QtGui, __version__
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

import pymel.core.datatypes as dt
import pymel.core as pm

import maya.cmds as cmds

import random


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class TestTool(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(TestTool, self).__init__(parent)

        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(750)
        self.setMaximumHeight(200)
        self.setMaximumWidth(900)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.
                            WindowContextHelpButtonHint)

        self.create_ui()
        self.create_connections()

    def create_ui(self):
        """WIDGETS"""
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")

        self.scatter_button = QtWidgets.QPushButton("Scatter")
        self.scatter_to_normal_button = QtWidgets.QPushButton(
            "Scatter to Normals")
        self.density_controller = QtWidgets.QDoubleSpinBox()
        self.density_controller.setFixedWidth(50)
        self.density_controller.setRange(1, 100)
        self.density_controller.setValue(100)

        self.is_whole = QtWidgets.QCheckBox("Selecting Whole Object")

        self.scatter_lbl = QtWidgets.QLabel("Make your selections before "
                                            "Scattering")
        self.scatter_lbl.setStyleSheet("font:bold 15px")

        self.rand_dense_lbl = QtWidgets.QLabel("Density Modifier")
        self.rand_dense_lbl.setStyleSheet("font:bold 14px")

        self.scatter_button = QtWidgets.QPushButton("Scatter")

        self.rand_rotation = self.random_rotation_ui()

        self.rand_scale = self.random_scale_ui()

        """LAYOUTS"""
        main_lay = QtWidgets.QVBoxLayout(self)
        main_lay.addWidget(self.title_lbl)
        main_lay.addWidget(self.scatter_lbl)
        main_lay.addWidget(self.scatter_button)
        main_lay.addWidget(self.scatter_to_normal_button)
        main_lay.addWidget(self.rand_dense_lbl, 0, 1)
        main_lay.addWidget(self.density_controller)
        main_lay.addWidget(self.is_whole)


        main_lay.addStretch()
        main_lay.addLayout(self.random_rotation_ui())
        main_lay.addLayout(self.random_scale_ui())

        self.setLayout(main_lay)

    def create_connections(self):
        self.scatter_button.clicked.connect(self.instance_vert)
        self.scatter_to_normal_button.clicked.connect(self.orient_to_normals)

        self.rand_spinbox_min.valueChanged.connect(self.rand_scale_min)
        self.rand_spinbox_max.valueChanged.connect(self.rand_scale_max)
        self.rand_scale_button.clicked.connect(self.random_scale)

        self.is_whole.stateChanged.connect(self.whole_object_check)
        self.density_controller.valueChanged.connect(self.density)

        self.rand_rot_x_min.valueChanged.connect(self.p_rand_rot_x_min)
        self.rand_rot_x_max.valueChanged.connect(self.p_rand_rot_x_max)
        self.rand_rot_y_min.valueChanged.connect(self.p_rand_rot_y_min)
        self.rand_rot_y_max.valueChanged.connect(self.p_rand_rot_y_max)
        self.rand_rot_z_min.valueChanged.connect(self.p_rand_rot_z_min)
        self.rand_rot_z_max.valueChanged.connect(self.p_rand_rot_z_max)
        self.rand_rot_button.clicked.connect(self.random_rotate)

    def random_scale_ui(self):
        self.rand_scale_title = QtWidgets.QLabel("Random Scale")
        self.rand_spinbox_min = QtWidgets.QDoubleSpinBox()
        self.rand_spinbox_min.setValue(1)
        self.rand_spinbox_min.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.rand_spinbox_min.setFixedWidth(50)

        self.rand_spinbox_max = QtWidgets.QDoubleSpinBox()
        self.rand_spinbox_max.setValue(1)
        self.rand_spinbox_max.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.rand_spinbox_max.setFixedWidth(50
                                            )
        self.rand_scale_button = QtWidgets.QPushButton("Apply")

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.rand_scale_button)
        layout.addWidget(self.rand_scale_title)
        layout.addWidget(self.rand_spinbox_min, 1, 0)
        layout.addWidget(QtWidgets.QLabel("min value"), 1, 0)
        layout.addWidget(self.rand_spinbox_max, 1, 0)
        layout.addWidget(QtWidgets.QLabel("max value"), 9, 0)

        return layout

    def random_rotation_ui(self):
        self.rand_rotation_title = QtWidgets.QLabel("Random Rotation")
        self.rand_rot_x_min = QtWidgets.QDoubleSpinBox()
        self.rand_rot_x_min.setValue(1)
        self.rand_rot_x_min.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.rand_rot_x_min.setFixedWidth(50)

        self.rand_rot_x_max = QtWidgets.QDoubleSpinBox()
        self.rand_rot_x_max.setValue(1)
        self.rand_rot_x_max.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.rand_rot_x_max.setFixedWidth(50)

        self.rand_rot_y_min = QtWidgets.QDoubleSpinBox()
        self.rand_rot_y_min.setValue(1)
        self.rand_rot_y_min.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.rand_rot_y_min.setFixedWidth(50)

        self.rand_rot_y_max = QtWidgets.QDoubleSpinBox()
        self.rand_rot_y_max.setValue(1)
        self.rand_rot_y_max.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.rand_rot_y_max.setFixedWidth(50)

        self.rand_rot_z_min = QtWidgets.QDoubleSpinBox()
        self.rand_rot_z_min.setValue(1)
        self.rand_rot_z_min.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.rand_rot_z_min.setFixedWidth(50)

        self.rand_rot_z_max = QtWidgets.QDoubleSpinBox()
        self.rand_rot_z_max.setValue(1)
        self.rand_rot_z_max.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.rand_rot_z_max.setFixedWidth(50)

        self.rand_rot_button = QtWidgets.QPushButton("Apply")

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.rand_rot_button)
        layout.addWidget(self.rand_rotation_title)
        layout.addWidget(self.rand_rot_x_min)
        layout.addWidget(QtWidgets.QLabel("x_min"))
        layout.addWidget(self.rand_rot_x_max)
        layout.addWidget(QtWidgets.QLabel("x_max"))
        layout.addWidget(self.rand_rot_y_min)
        layout.addWidget(QtWidgets.QLabel("y_min"))
        layout.addWidget(self.rand_rot_y_max)
        layout.addWidget(QtWidgets.QLabel("y_max"))
        layout.addWidget(self.rand_rot_z_min)
        layout.addWidget(QtWidgets.QLabel("z_min"))
        layout.addWidget(self.rand_rot_z_max)
        layout.addWidget(QtWidgets.QLabel("z_max"))

        return layout

    @QtCore.Slot()
    def whole_object_check(self):

        self.is_whole_object = self.is_whole.checkState()

        return self.is_whole_object

    @QtCore.Slot()
    def density(self):

        self.def_density = self.density_controller.value() / 100

        return self.def_density


    @QtCore.Slot()
    def instance_vert(self):
        self.selection = cmds.ls(os=True, fl=True)
        self.vert_list = cmds.ls(selection=True, fl=True)
        cmds.filterExpand(self.vert_list, selectionMask=31, expand=True) or []
        self.obj_vert_list = cmds.ls(self.vert_list[1] + ".vtx[*]",
                                     flatten=True)

        if self.is_whole_object:
            self.den_list = random.sample(self.obj_vert_list, int(float(
                len(self.obj_vert_list) * self.def_density)))
        else:
            self.den_list = random.sample(self.vert_list, int(float(len
                                     (self.vert_list)) * self.def_density))



        self.object_to_instance = self.selection[0]

        # print(vertex_name)

        if cmds.objectType(self.object_to_instance, isType="transform"):

            for self.vertex in self.den_list:
                self.new_instance = cmds.instance(self.object_to_instance)

                self.position = cmds.pointPosition(self.vertex, w=True)

                cmds.move(self.position[0], self.position[1],
                          self.position[2], self.new_instance, a=True, ws=True)
                cmds.rename(self.new_instance, "instance")

        else:
            print("Please ensure the first object you select is a transform.")

        # Gets the center of the object's face

    @QtCore.Slot()
    def orient_to_normals(self):

        self.selection = cmds.ls(os=True, fl=True)
        self.vert_list = cmds.ls(selection=True, fl=True)
        cmds.filterExpand(self.vert_list, selectionMask=31, expand=True) or []
        self.obj_vert_list = cmds.ls(self.vert_list[1] + ".vtx[*]",
                                     flatten=True)

        if self.is_whole_object:
            self.den_list = random.sample(self.obj_vert_list, int(float(
                len(self.obj_vert_list) * self.def_density)))
        else:
            self.den_list = random.sample(self.vert_list, int(float(len
                                     (self.vert_list)) * self.def_density))

        self.object_to_instance = self.selection[0]
        self.main_object = self.selection[1]

        # print(vertex_name)

        if cmds.objectType(self.object_to_instance, isType="transform"):

            for self.vertex in self.den_list:
                self.new_instance = cmds.instance(self.object_to_instance)

                self.position = cmds.pointPosition(self.vertex, w=True)

                cmds.move(self.position[0], self.position[1],
                          self.position[2], self.new_instance, a=True, ws=True)

                self.nconst = cmds.normalConstraint(self.main_object,
                                                    self.new_instance)
                cmds.rename(self.new_instance, "instance")

                cmds.delete(self.nconst)

        else:
            print("Please ensure the first object you select is a transform.")

    @QtCore.Slot()
    def rand_scale_min(self):
        self.p_min = self.rand_spinbox_min.value()
        return self.p_min

    @QtCore.Slot()
    def rand_scale_max(self):
        self.p_max = self.rand_spinbox_max.value()
        return self.p_max

    @QtCore.Slot()
    def random_scale(self):

        obj_list = cmds.ls('instance*')
        obj_list.pop()
        # print(obj_list)
        for instance in obj_list:
            random_size = random.uniform(float(self.p_min), float(self.p_max))

            cmds.scale(1, 1, 1, instance)

            cmds.scale((1 * random_size), (1 * random_size),
                       (1 * random_size), instance)

            if (self.p_min == 1) & (self.p_max == 1):
                cmds.scale(1, 1, 1)

            # return self.random_scale
            # print(self.random_scale)

    @QtCore.Slot()
    def p_rand_rot_x_min(self):
        self.p_x_min = self.rand_rot_x_min.value()
        return self.p_x_min

    @QtCore.Slot()
    def p_rand_rot_x_max(self):
        self.p_x_max = self.rand_rot_x_max.value()
        return self.p_x_max

    @QtCore.Slot()
    def p_rand_rot_y_min(self):
        self.p_y_min = self.rand_rot_y_min.value()
        return self.p_y_min

    @QtCore.Slot()
    def p_rand_rot_y_max(self):
        self.p_y_max = self.rand_rot_y_max.value()
        return self.p_y_max

    @QtCore.Slot()
    def p_rand_rot_z_min(self):
        self.p_z_min = self.rand_rot_z_min.value()
        return self.p_z_min

    @QtCore.Slot()
    def p_rand_rot_z_max(self):
        self.p_z_max = self.rand_rot_z_max.value()
        return self.p_z_max

    @QtCore.Slot()
    def random_rotate(self):
        obj_list = cmds.ls('instance*')
        obj_list.pop()
        for instance in obj_list:
            random_rotation_x = random.uniform(self.p_x_min, self.p_x_max)
            random_rotation_y = random.uniform(self.p_y_min, self.p_y_max)
            random_rotation_z = random.uniform(self.p_z_min, self.p_z_max)

            cmds.rotate(random_rotation_x,
                        random_rotation_y,
                        random_rotation_z, instance)

    @property
    def get_instances(self):
        self.selection = cmds.ls(os=True)
        self.obj_name = self.selection[0]
        self.instance_names = cmds.ls(self.obj_name[:-1] + '*')
        self.instance_names = filter(
            lambda x: not x.endswith('_normalConstraint1'),
            self.instance_names)

        return self.instance_names


if __name__ == "__main__":
    d = TestTool()
    d.show()


def create_cylinder():
    cmds.polyCylinder()


# Functions which will be used to expand on the tool
"""def get_face_center(p_face_name):
    vertex_positions = (cmds.xform(p_face_name, q=True, ws=True, t=True))

    vertex_positions = [vertex_positions[n:n + 3] for n in range(0, len(
                                                        vertex_positions),
                                                                 3)]

    _sum = dt.Vector(0, 0, 0)
    for v in vertex_positions:
        _sum = _sum + v

    num_vertices = len(vertex_positions)

    average = _sum / num_vertices

    if (_sum == 0) or (num_vertices == 0):
        average = [0, 0, 0]
        cmds.warning("Attempt to divide by 0")

    else:
        return average"""

"""def instance_face():
    selection = cmds.ls(os=True, fl=True)
    face_name = cmds.filterExpand(selection, selectionMask=34,
                                  expand=True)

    object_to_instance = selection[0]
    main_object = selection[1]
    if cmds.objectType(object_to_instance, isType="transform"):

        for face in face_name:
            new_instance = cmds.instance(object_to_instance)

            position = get_face_center(str(face))

            cmds.normalConstraint(main_object, new_instance)

            cmds.move(position[0], position[1], position[2], new_instance,
                      a=True, ws=True)

    else:
        print("Please ensure the first object you select is a transform.")"""
