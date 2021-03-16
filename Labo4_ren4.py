# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:24:26 2020

@author: alexandre
"""

import vtk
import os.path

def CreateRen4(slcr, cam, viewport, background):
    
    if os.path.isfile('data_bone.vtk'):
        read = vtk.vtkPolyDataReader()
        read.SetFileName("data_bone.vtk")
        read.Update()
        
        mapperBone = vtk.vtkPolyDataMapper()
        mapperBone.SetInputConnection(read.GetOutputPort())
        mapperBone.SetScalarRange(
            read.GetOutput().GetPointData().GetScalars().GetRange()[0],
            read.GetOutput().GetPointData().GetScalars().GetRange()[1])
        
    else:
        contourBone = vtk.vtkContourFilter()
        contourBone.SetInputConnection(slcr.GetOutputPort())
        contourBone.SetValue(0,75.0)
        contourBone.Update()
        
        contourSkin = vtk.vtkContourFilter()
        contourSkin.SetInputConnection(slcr.GetOutputPort())
        contourSkin.SetValue(0,50.0)
        contourSkin.Update()
        
        distanceFilter = vtk.vtkDistancePolyDataFilter()
        distanceFilter.SignedDistanceOff()
        distanceFilter.SetInputConnection(0, contourBone.GetOutputPort())
        distanceFilter.SetInputConnection(1, contourSkin.GetOutputPort())
        distanceFilter.Update()
        
        mapperBone = vtk.vtkPolyDataMapper()
        mapperBone.SetInputConnection(distanceFilter.GetOutputPort())
        mapperBone.SetScalarRange(
            distanceFilter.GetOutput().GetPointData().GetScalars().GetRange()[0],
            distanceFilter.GetOutput().GetPointData().GetScalars().GetRange()[1])
    
    
    outliner = vtk.vtkOutlineFilter()
    outliner.SetInputConnection(slcr.GetOutputPort())
    outliner.Update()
    
    mapperOutliner = vtk.vtkPolyDataMapper()
    mapperOutliner.SetInputConnection(outliner.GetOutputPort())
    
    actorBone = vtk.vtkActor()
    actorBone.SetMapper(mapperBone)

    actorOutliner = vtk.vtkActor()
    actorOutliner.SetMapper(mapperOutliner)
    
    ren = vtk.vtkRenderer()
    ren.AddActor(actorBone)
    ren.AddActor(actorOutliner)
    ren.SetViewport(viewport)
    ren.SetActiveCamera(cam)
    ren.ResetCamera()
    ren.SetBackground(background)
    
    if not os.path.isfile('data_bone.vtk'):
        # write a file for restart 
        write = vtk.vtkPolyDataWriter()
        write.SetFileName("data_bone.vtk")
        write.SetInputConnection(distanceFilter.GetOutputPort())
        write.Write()
    
    return ren
    
    