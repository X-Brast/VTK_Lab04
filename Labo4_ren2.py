# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:24:26 2020

@author: alexandre
"""

import vtk

def CreateRen2(slcr, cam, viewport, background):
    # Create Bone
    contourBone = vtk.vtkContourFilter()
    contourBone.SetInputConnection(slcr.GetOutputPort())
    contourBone.SetValue(0,75.0)
    
    mapperBone = vtk.vtkPolyDataMapper()
    mapperBone.SetInputConnection(contourBone.GetOutputPort())
    mapperBone.SetScalarVisibility(0)
    
    #Create Outliner
    outliner = vtk.vtkOutlineFilter()
    outliner.SetInputConnection(slcr.GetOutputPort())
    outliner.Update()
    
    mapperOutliner = vtk.vtkPolyDataMapper()
    mapperOutliner.SetInputConnection(outliner.GetOutputPort())
    
    # Create Skin
    contourSkin = vtk.vtkContourFilter()
    contourSkin.SetInputConnection(slcr.GetOutputPort())
    contourSkin.SetValue(0,50.0)

    sphere = vtk.vtkSphere()
    sphere.SetCenter(80,10,120)
    sphere.SetRadius(55)
    
    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(contourSkin.GetOutputPort())
    clipper.SetClipFunction(sphere)
    clipper.SetValue(0)
    clipper.Update()
    

    mapperSkin = vtk.vtkPolyDataMapper()
    mapperSkin.SetInputConnection(clipper.GetOutputPort())
    mapperSkin.SetScalarVisibility(0)
    
    # Define Opacity for back skin    
    back = vtk.vtkProperty()
    back.SetOpacity(1)
    back.SetColor(0.74,0.55,0.55)
    
    # Create Actor
    actorBone = vtk.vtkActor()
    actorBone.SetMapper(mapperBone)
    
    actorSkin = vtk.vtkActor()
    actorSkin.SetMapper(mapperSkin)
    actorSkin.GetProperty().SetColor(0.74,0.55,0.55)
    actorSkin.GetProperty().SetOpacity(0.7)
    actorSkin.SetBackfaceProperty(back)
    
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
    
    