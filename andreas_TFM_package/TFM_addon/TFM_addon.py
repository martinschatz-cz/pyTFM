﻿
from __future__ import division, print_function
from andreas_TFM_package.TFM_functions_for_clickpoints import *  # must be on top because of some matplotlib backend issues
from andreas_TFM_package.parameters_and_strings import tooltips,default_parameters
from andreas_TFM_package.database_functions import *
#from TFM_functions_for_clickpoints import * local import

#from utilities import  get_group,createFolder
import os
from functools import partial
from qtpy import QtCore, QtGui, QtWidgets
import qtawesome as qta
import clickpoints
import asyncio
import threading


import warnings
warnings.simplefilter(action='ignore', category=RuntimeWarning)



def add_parameter_from_list(labels, dict_keys, default_parameters, layout,grid_line_start,con_func):
    params = {}
    param_labels = {}
    for i, (label,dict_key) in enumerate(zip(labels,dict_keys)):
        p = QtWidgets.QLineEdit()  # box to enter number
        p.setFixedWidth(120)
        p.setText(str(default_parameters[dict_key]))
        p.setToolTip(tooltips[dict_key])
        p.textChanged.connect(con_func)
        p_l = QtWidgets.QLabel()  # text
        p_l.setText(label)
        layout.addWidget(p, grid_line_start + i, 1)  # adding to layout
        layout.addWidget(p_l, grid_line_start + i, 0)
        params[dict_key] = p
        param_labels[dict_key] = p_l
    last_line = grid_line_start + i
    return params, param_labels, last_line

def read_all_paramters(parameter_widgets,parameter_dict):
    for p_name,p_widget in parameter_widgets.items():
        if isinstance(p_widget,QtWidgets.QLineEdit):
            parameter_dict[p_name]=float(p_widget.text())
        if isinstance(p_widget, QtWidgets.QComboBox):
            parameter_dict[p_name] = p_widget.currentText()
    return parameter_dict

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal












class NewWindow(QtWidgets.QWidget):
    def __init__(self,main_window):
        super(NewWindow, self).__init__()
        self._new_window = None
        self.setMinimumWidth(600)
        self.setMinimumHeight(300)
        self.main_window=main_window
        self.main_window.outfile_path=os.path.join(os.getcwd(),"out.txt"),
        self.folders = {"folder1_txt": os.getcwd(),
                        "folder2_txt": os.getcwd(),
                        "folder3_txt": os.getcwd(),
                        "folder_out_txt": os.getcwd()}
        self.search_keys = {"after": "\d{1,4}after", "before": "\d{1,4}before",
                            "cells": "\d{1,4}bf_before",
                            "frames": "(\d{1,4})"}
        self.layout = QtWidgets.QGridLayout()
        self.layout.setColumnStretch(0,8)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 6)
        self.cwd=os.getcwd()
        #def sub_grid(self):
            #grid=QtWidgets.QGridLayout()
            #grid.

        self.sub_v_layout = defaultdict(QtWidgets.QVBoxLayout)
        self.sub_h_layout= defaultdict(QtWidgets.QHBoxLayout)
        self.objects = {
            "folder_out_txt": {"object": None, "properties": [0, 0,None,20, "textChanged",self.update_dirs, QtWidgets.QLineEdit, self.cwd]},
            "folder1_txt": {"object": None, "properties": [1, 0,None,20, "textChanged",self.update_dirs, QtWidgets.QLineEdit, self.cwd]},
            "folder2_txt": {"object": None, "properties": [2, 0,None,20,"textChanged" ,self.update_dirs, QtWidgets.QLineEdit, self.cwd]},
            "folder3_txt": {"object": None, "properties": [3, 0,None,20, "textChanged",self.update_dirs, QtWidgets.QLineEdit, self.cwd]},
            "folder_out_button": {"object": None, "properties": [0, 1,30,80, "clicked",self.file_dialog,QtWidgets.QPushButton, "..."]},
            "folder1_button": {"object": None, "properties": [1, 1,30,80, "clicked",self.file_dialog,QtWidgets.QPushButton, "..."]},
            "folder2_button": {"object": None, "properties": [2, 1,30,80, "clicked",self.file_dialog,QtWidgets.QPushButton, "..."]},
            "folder3_button": {"object": None, "properties": [3, 1,30,80, "clicked",self.file_dialog,QtWidgets.QPushButton, "..."]},
            "after": {"object": None, "properties": [0, 2,200,30,"textChanged" ,self.update_dirs, QtWidgets.QLineEdit, "default"]},
            "before": {"object": None, "properties": [1, 2,200,30, "textChanged",self.update_dirs, QtWidgets.QLineEdit, "default"]},
            "cells": {"object": None, "properties": [2, 2,200,30, "textChanged",self.update_dirs, QtWidgets.QLineEdit, "default"]},
            "frames": {"object": None, "properties": [3, 2,200,30, "textChanged",self.update_dirs, QtWidgets.QLineEdit, "default"]}}


        self.texts = {
            "folder_out_txt": {"object": None, "properties": [0, 0, "output folder"]},
            "folder1_txt": {"object": None, "properties": [0, 0, "images after cell removal"]},
            "folder2_txt": {"object": None, "properties": [0, 0, "images before cell removal"]},
            "folder3_txt": {"object": None, "properties": [0, 0, "images cells"]},
            "folder_out_button": {"object": None, "properties": [0, 0, ""]},
            "folder1_button": {"object": None, "properties": [0, 0, ""]},
            "folder2_button": {"object": None, "properties": [0, 0, ""]},
            "folder3_button": {"object": None, "properties": [0, 0, ""]},
            "after": {"object": None, "properties": [0, 0, ""]},
            "before": {"object": None, "properties": [0, 0, ""]},
            "cells": {"object": None, "properties": [0, 0, ""]},
            "frames": {"object": None, "properties": [0, 0, ""]}}

        for name in self.texts.keys():
            self.add_text(name, *self.texts[name]["properties"])
        for name in self.objects.keys():
            self.add_object(name, *self.objects[name]["properties"])
        # adding the start button
        self.super_layout=QtWidgets.QGridLayout(self)

        self.super_layout.addLayout(self.layout,0,0)
        self.Spacer1 = QtWidgets.QSpacerItem(50, 50)
        self.super_layout.addItem(self.Spacer1, 1, 0)
        self.collect_button=QtWidgets.QPushButton("collect images")
        self.collect_button.clicked.connect(self.collect_files)
        self.super_layout.addWidget(self.collect_button,2,0,alignment=QtCore.Qt.AlignLeft)

        self.super_layout.setRowStretch(12,1)


    def add_text(self,name,vpos,hpos,string):
        self.texts[name]["object"]=QtWidgets.QLabel(string)
        self.sub_v_layout[name].addStretch()
        self.sub_v_layout[name].addWidget(self.texts[name]["object"]) # adds to sub gid layout

    def add_object(self, name, vpos, hpos,m_width,s_width,connect_type, connect_function, type, text):
        text = self.search_keys[name] if text == "default" else text
        self.objects[name]["object"] = type(text) # creates widget with text as label
        getattr(self.objects[name]["object"], connect_type).connect(partial(connect_function, name)) # connects to function
        self.objects[name]["object"].setToolTip(tooltips[name]) # sets tooltip

        if m_width:
            self.objects[name]["object"].setMaximumWidth(m_width)
        self.sub_v_layout[name].addWidget(self.objects[name]["object"]) # generates new grid layout
        self.sub_h_layout[name].addLayout(self.sub_v_layout[name]) # generates new horizontal layout
        self.sub_h_layout[name].addSpacing(s_width)  # adds spacing on the right
        self.layout.addLayout(self.sub_h_layout[name], vpos, hpos) # adds to main grid layout

    # additional file selectors

    def file_dialog(self,button_name):
        dialog=QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        dialog.setDirectory(self.cwd)
        if dialog.exec_():
            dirname=dialog.selectedFiles()
            text_field=self.objects[button_name[:-6]+"txt"]["object"]
            text_field.setText(dirname[0])
        self.update_dirs()

    def update_dirs(self,*args):
        # updating the selected folders and search keys
        self.folders={key:self.objects[key]["object"].text() for key in self.folders.keys()}
        self.earch_keys={key:self.objects[key]["object"].text() for key in self.search_keys.keys()}

    def collect_files(self):
        print("test")
        self.main_window.db.deleteImages()  # delete exsiting images
        self.main_window.db.deleteLayers()  # delete existing layers
        setup_database_internal(self.main_window.db,self.search_keys,self.folders)# sort in images
        self.main_window.cp.updateImageCount()  # reload the image bar
        self.main_window.db_info, self.main_window.all_frames = get_db_info_for_analysis(self.main_window.db) # updat meta info

        self.main_window.outfile_path = os.path.join(self.folders["folder_out_txt"],"out.txt")
        print(self.main_window.db_info)

        # reiinitiate masks
        self.main_window.parameter_dict["FEM_mode"], undetermined = guess_TFM_mode(self.main_window.db_info, self.main_window.parameter_dict)
        print(undetermined)
        if undetermined:
            setup_masks(self.main_window.db,self.main_window.db_info, self.main_window.parameter_dict,delete_all=True)
            self.main_window.cp.reloadMaskTypes()

        #elf.main_window.db
        pass



class Addon(clickpoints.Addon):

    def __init__(self, *args, **kwargs):
        clickpoints.Addon.__init__(self, *args, **kwargs)
        try:
            self.folder=db.getOption("folder")
        except:
            self.folder = os.getcwd()
            self.db._AddOption(key="folder", value=self.folder)
        self.outfile_path=os.path.join(self.folder,"out.txt") # path for output text file




        self.frame_number=self.db.getImageCount()
        self.db_info, self.all_frames = get_db_info_for_analysis(self.db) # information about the path, image dimensions
        self.res_dict=defaultdict(dict) # dictionary that catches all results
        self.parameter_dict = default_parameters # loading default parameters
        # guessing the curent analysis mode
        self.parameter_dict["FEM_mode"],undetermined=guess_TFM_mode(self.db_info,self.parameter_dict)
        self.colony_type_old_id =int(self.parameter_dict["FEM_mode"] == "cell layer")

        """ GUI Widgets"""
        # set the title and layout
        self.setWindowTitle("TFM")
        self.setWindowIcon(qta.icon("fa.compress"))
        self.setMinimumWidth(400)
        self.setMinimumHeight(200)


        self.layout = QtWidgets.QGridLayout(self)

        # button to start calculation
        self.button_start = QtWidgets.QPushButton("start")
        self.button_start.clicked.connect(self.start_thread)
        self.button_start.setToolTip(tooltips["button_start"])
        self.layout.addWidget(self.button_start,0,0)


        # button to select images:
        # if all([l not in self.db_info["layers"] for l in ["images_after", "images_before", "membranes"]]):

        self.button_select_images = QtWidgets.QPushButton("select images")
        self.button_select_images.clicked.connect(self.select_images)
        self.button_select_images.setToolTip(tooltips["select images"])
        self.sub_layout1 = QtWidgets.QHBoxLayout()
        self.sub_layout1.addWidget(self.button_select_images)
        self.sub_layout1.addStretch()
        self.layout.addLayout(self.sub_layout1, 1, 0)

        # choosing type of cell system
        self.colony_type = QtWidgets.QComboBox()
        self.colony_type.addItems(["colony", "cell layer"])
        self.colony_type.setToolTip(tooltips["colony_type"])
        self.colony_type.setCurrentIndex(self.colony_type_old_id)
        self.colony_type.activated.connect(self.switch_colony_type_mode)  # activated when user changes the the selected text



        self.sub_layout2=QtWidgets.QHBoxLayout()
        self.sub_layout2.addWidget(self.colony_type)
        self.sub_layout2.addStretch()
        self.layout.addLayout(self.sub_layout2, 2, 0)

        # filling areas for cell patches
        self.fill_patches_button = QtWidgets.QPushButton("fill cell area")
        self.fill_patches_button.setToolTip(tooltips["fill_patches_button"])
        self.fill_patches_button.clicked.connect(self.fill_patches)

        self.sub_layout2 = QtWidgets.QHBoxLayout()
        self.sub_layout2.addWidget(self.fill_patches_button)
        self.sub_layout2.addStretch()
        self.layout.addLayout(self.sub_layout2, 3, 0)
        self.fill_patches_button.setVisible(self.colony_type_old_id) # ide button for now

        #if undetermined: # only when selecting images now
        #    self.switch_colony_type_mode(first=True) # initializing masks according to the first value of "FEM_mode"


         # check_boxes
        self.check_box_def = QtWidgets.QCheckBox("deformation")
        self.check_box_tra = QtWidgets.QCheckBox("traction forces")
        self.check_box_FEM = QtWidgets.QCheckBox("FEM analysis")
        self.check_box_contract = QtWidgets.QCheckBox("contractillity_measures")

        self.check_box_def.setToolTip(tooltips["check_box_def"])
        self.check_box_tra.setToolTip(tooltips["check_box_tra"])
        self.check_box_FEM.setToolTip(tooltips["check_box_FEM"])
        self.check_box_contract.setToolTip(tooltips["check_box_contract"])

        self.layout.addWidget(self.check_box_def, 0, 1)
        self.layout.addWidget(self.check_box_tra, 1, 1)
        self.layout.addWidget(self.check_box_FEM, 2, 1)
        self.layout.addWidget(self.check_box_contract, 3, 1)


        # # choosing single or all frames
        self.analysis_mode=QtWidgets.QComboBox()
        self.analysis_mode.addItems(["current frame", "all frames"])
        self.analysis_mode.setToolTip(tooltips["apply to"])
        self.layout.addWidget(self.analysis_mode, 4, 1)
        self.analysis_mode_descript = QtWidgets.QLabel()
        self.analysis_mode_descript.setText("apply to")
        self.layout.addWidget(self.analysis_mode_descript, 4, 0)



        #### parameters
        self.parameter_labels=["youngs modulus [Pa]","possion ratio","pixel size [µm]","piv overlapp [µm]","piv window size [µm]","gel hight [µm]"]
        self.param_dict_keys=["young","sigma","pixelsize","overlapp","window_size","h"]
        self.parameter_widgets,self.parameter_lables,last_line=add_parameter_from_list(self.parameter_labels,
                                                            self.param_dict_keys,self.parameter_dict,self.layout
                                                                                       ,5,self.parameters_changed)
        # drop down for choosing wether to use height correction
        self.use_h_correction = QtWidgets.QComboBox()
        self.use_h_correction.addItems(["finite_thickness", "infinite_thickness"])
        self.use_h_correction.currentTextChanged.connect(self.parameters_changed) # update self.paramter_dict everytime smethong changed
        self.use_h_correction_descr = QtWidgets.QLabel()
        self.use_h_correction_descr.setText("enable height correction")
        self.layout.addWidget(self.use_h_correction,  last_line+1, 1)
        self.layout.addWidget(self.use_h_correction_descr,   last_line + 1, 0)
        self.parameter_widgets["TFM_mode"]=self.use_h_correction # adding to parameters dict
        self.parameter_lables["TFM_mode"] =  self.use_h_correction_descr  # adding to parameters dict
        # adding to layout
        self.setLayout(self.layout)
        self.parameters_changed() # initialize parameters dict


    def select_images(self):
        self._new_window = NewWindow(self)
        self._new_window.show()




            #setup_database_internal(self.db)
            #self.db_info, self.all_frames = get_db_info_for_analysis(self.db)

    # reading paramteres and updating the dictionary
    def parameters_changed(self):
        self.parameter_dict = read_all_paramters(self.parameter_widgets,self.parameter_dict)

       
        #write_output_file(self.parameter_dict, None, "parameters", self.outfile_path) # writes paramters to output file..

    # decorator functions to handle diffrent outputs and writing to text file
    def calculate_general_properties(self,frames):
        apply_to_frames(self.db, self.parameter_dict, analysis_function=general_properties, res_dict=self.res_dict,
                        frames=frames, db_info=self.db_info)  # calculation of colony area, number of cells in colony
    def calculate_deformation(self,frames):
            apply_to_frames(self.db, self.parameter_dict,analysis_function=deformation,res_dict=self.res_dict,
                                frames=frames,db_info=self.db_info)  # calculation of deformations

    def calculate_traction(self,frames):
            apply_to_frames(self.db, self.parameter_dict,analysis_function=traction_force,res_dict=self.res_dict,
                                frames=frames,db_info=self.db_info)  # calculation of traction forces

    def calculate_FEM_analysis(self,frames):
            apply_to_frames(self.db, self.parameter_dict, analysis_function=FEM_full_analysis,res_dict=self.res_dict,
                            frames=frames,db_info=self.db_info)  # calculation of various stress measures

    def calculate_contractile_measures(self,frames):
            apply_to_frames(self.db, self.parameter_dict,analysis_function=get_contractillity_contractile_energy,
                 res_dict=self.res_dict,frames=frames,db_info=self.db_info)  # calculation of contractility and contractile energy

    # switching the type of cell colony
    def switch_colony_type_mode(self,first=False):
        if not first:
            choice = QtWidgets.QMessageBox.question(self, 'continue',
                                                "This will delete all previous mask. Do you want to coninue?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        else:
            choice=QtWidgets.QMessageBox.Yes

        if choice == QtWidgets.QMessageBox.Yes:
            # new mask types
            self.parameter_dict["FEM_mode"] =self.colony_type.currentText()
            self.colony_type_old_id=self.colony_type.currentIndex()
            if self.colony_type.currentText()=="cell layer":
                setup_masks(self.db,self.db_info, self.parameter_dict) # deletes and add masktyes
                self.fill_patches_button.setVisible(True)
            if self.colony_type.currentText()=="colony":
                setup_masks(self.db,self.db_info, self.parameter_dict)
                self.fill_patches_button.setVisible(False)
            self.cp.reloadMaskTypes()  # reloading mask to display in clickpoints window
        else:
            self.colony_type.setCurrentIndex(self.colony_type_old_id) #reverting to old index


    def fill_patches(self):


        apply_to_frames(self.db, self.parameter_dict, analysis_function=fill_patches_for_cell_layer,
                        res_dict=self.res_dict, frames=self.all_frames, db_info=self.db_info)

        self.cp.reloadMask()
        self.cp.save()


    def start(self): # perform all checked calculations
        cdb_frame = self.cp.getCurrentFrame()
        self.frame = get_frame_from_annotation(self.db, cdb_frame) # current frame


        print("parameters:\n",self.parameter_dict)
        self.mode=self.analysis_mode.currentText() # only current frame or all frames
        if self.mode == "current frame": # only current frame
            frames=self.frame
            print("analyzing current frame = ", frames)
        if self.mode == "all frames": # all frames
            frames=self.all_frames
            print("analyzing frames = ", frames)
            write_output_file(self.parameter_dict, "parameters", self.outfile_path)


        if self.check_box_def.isChecked():     
            self.calculate_deformation(frames)
        if self.check_box_tra.isChecked():
            self.calculate_traction(frames)
        self.calculate_general_properties(frames)
        if self.check_box_FEM.isChecked():
            self.calculate_FEM_analysis(frames)
        if self.check_box_contract.isChecked():
            self.calculate_contractile_measures(frames)


        write_output_file(self.res_dict, "results", self.outfile_path)  # writing to output file
        # reloding all images that where changed
        #if self.mode=="current frame":
        #        self.cp.reloadImage(frame_index=cdb_frame)
        #else:
        #        for frame_index in range(self.frame_number):
        #                self.cp.reloadImage(frame_index=frame_index )
        
        print("calculation complete")


    def start_thread(self): ## run in a sepearte thread to keep clickpoints gui responsive (ask richie about this)
        x = threading.Thread(target=self.start)
        x.start()
        #x.join()
    def buttonPressedEvent(self):
        # show the addon window when the button in ClickPoints is pressed
        self.show()
    async def run(self): # disable running in other thread other wise "figsize" is somehow overloaded
        pass




