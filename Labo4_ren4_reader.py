# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:24:26 2020

@author: alexandre
"""

import vtk

def ReadRen4(slcr, cam, viewport, background):
    
    outliner = vtk.vtkOutlineFilter()
    outliner.SetInputConnection(slcr.GetOutputPort())
    outliner.Update()
    
    mapperOutliner = vtk.vtkPolyDataMapper()
    mapperOutliner.SetInputConnection(outliner.GetOutputPort())
    
    read = vtk.vtkPolyDataReader()
    read.SetFileName("data_bone.vtk")
    read.Update()
    
    print(read)
    
    mapperBone = vtk.vtkPolyDataMapper()
    mapperBone.SetInputConnection(read.GetOutputPort())
    mapperBone.SetScalarRange(
        read.GetOutput().GetPointData().GetScalars().GetRange()[0],
        read.GetOutput().GetPointData().GetScalars().GetRange()[1])
    
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
    
    return ren
    
    