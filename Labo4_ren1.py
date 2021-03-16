# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:24:26 2020

@author: alexandre
"""

import vtk

def CreateRen1(slcr, cam, viewport, background):
    #Create BOne
    contourBone = vtk.vtkContourFilter()
    contourBone.SetInputConnection(slcr.GetOutputPort())
    contourBone.SetValue(0,75.0)
    
    mapperBone = vtk.vtkPolyDataMapper()
    mapperBone.SetInputConnection(contourBone.GetOutputPort())
    mapperBone.SetScalarVisibility(0)
    
    # Create Outliner
    outliner = vtk.vtkOutlineFilter()
    outliner.SetInputConnection(slcr.GetOutputPort())
    outliner.Update()
    
    mapperOutliner = vtk.vtkPolyDataMapper()
    mapperOutliner.SetInputConnection(outliner.GetOutputPort())
    
    
    contourSkin = vtk.vtkContourFilter()
    contourSkin.SetInputConnection(slcr.GetOutputPort())
    contourSkin.SetValue(0,50.0)
    
    # Create CutSkin
    plane = vtk.vtkPlane()
    plane.SetOrigin(0,0,0)
    plane.SetNormal(0,0,1)
    
    cutter = vtk.vtkCutter()
    cutter.SetCutFunction(plane)
    cutter.SetInputConnection(contourSkin.GetOutputPort())
    for i in range(100):
        cutter.SetValue(i,10 * i)
    cutter.Update()    

    mapperSkin = vtk.vtkPolyDataMapper()
    mapperSkin.SetInputConnection(cutter.GetOutputPort())
    mapperSkin.SetScalarVisibility(0)
    
    # Create Actor
    actorBone = vtk.vtkActor()
    actorBone.SetMapper(mapperBone)
    
    actorSkin = vtk.vtkActor()
    actorSkin.SetMapper(mapperSkin)
    actorSkin.GetProperty().SetColor(0.74,0.55,0.55)
    
    actorOutliner = vtk.vtkActor()
    actorOutliner.SetMapper(mapperOutliner)
    
    ren = vtk.vtkRenderer()
    ren.AddActor(actorBone)
    ren.AddActor(actorSkin)
    ren.AddActor(actorOutliner)
    ren.SetViewport(viewport)
    ren.SetActiveCamera(cam)
    ren.ResetCamera()
    ren.SetBackground(background)
    
    return ren
    
    