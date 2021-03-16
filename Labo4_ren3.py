# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:24:26 2020

@author: alexandre
"""

import vtk

def CreateRen3(slcr, cam, viewport, background):
    # Create bone
    contourBone = vtk.vtkContourFilter()
    contourBone.SetInputConnection(slcr.GetOutputPort())
    contourBone.SetValue(0,75.0)
    
    mapperBone = vtk.vtkPolyDataMapper()
    mapperBone.SetInputConnection(contourBone.GetOutputPort())
    mapperBone.SetScalarRange(0,1.2)
    mapperBone.SetScalarVisibility(0)
    
    # Create Outliner
    outliner = vtk.vtkOutlineFilter()
    outliner.SetInputConnection(slcr.GetOutputPort())
    outliner.Update()
    
    mapperOutliner = vtk.vtkPolyDataMapper()
    mapperOutliner.SetInputConnection(outliner.GetOutputPort())
    
    # Create sphere for clipping skin
    xCenter = 75
    yCenter = 40
    zCenter = 110
    radius = 50
    
    sphere = vtk.vtkSphere()
    sphere.SetCenter(xCenter,yCenter,zCenter)
    sphere.SetRadius(radius)
    
    sphere2 = vtk.vtkSphereSource()
    sphere2.SetCenter(xCenter,yCenter,zCenter)
    sphere2.SetRadius(radius + 3)
    
    # Create Skin
    contourSkin = vtk.vtkContourFilter()
    contourSkin.SetInputConnection(slcr.GetOutputPort())
    contourSkin.SetValue(0,50.0)    
    
    clipperSkin = vtk.vtkClipPolyData()
    clipperSkin.SetInputConnection(contourSkin.GetOutputPort())
    clipperSkin.SetClipFunction(sphere)
    clipperSkin.SetValue(0)
    clipperSkin.Update() 
    
    mapperSkin = vtk.vtkPolyDataMapper()
    mapperSkin.SetInputConnection(clipperSkin.GetOutputPort())
    mapperSkin.SetScalarVisibility(0)
    
    # Create Sphere    
    ipdd = vtk.vtkImplicitPolyDataDistance()
    ipdd.SetInput(clipperSkin.GetOutput(0))
    
    clipperSphere = vtk.vtkClipPolyData()
    clipperSphere.SetInputConnection(sphere2.GetOutputPort())
    clipperSphere.SetClipFunction(ipdd)
    clipperSphere.SetValue(0)
    clipperSphere.Update() 
    
    mapperSphere = vtk.vtkPolyDataMapper()
    mapperSphere.SetInputConnection(clipperSphere.GetOutputPort())
    mapperSphere.SetScalarVisibility(0)
    
    
    # Create Actor
    actorBone = vtk.vtkActor()
    actorBone.SetMapper(mapperBone)
    
    actorSkin = vtk.vtkActor()
    actorSkin.SetMapper(mapperSkin)
    actorSkin.GetProperty().SetColor(0.74,0.55,0.55)
    
    actorSphere = vtk.vtkActor()
    actorSphere.SetMapper(mapperSphere)
    actorSphere.GetProperty().SetColor(0.9,0.9,0.9)
    actorSphere.GetProperty().SetOpacity(0.3)
    
    actorOutliner = vtk.vtkActor()
    actorOutliner.SetMapper(mapperOutliner)
    
    # Create Renderer
    ren = vtk.vtkRenderer()
    ren.AddActor(actorBone)
    ren.AddActor(actorSkin)
    ren.AddActor(actorSphere)
    ren.AddActor(actorOutliner)
    ren.SetViewport(viewport)
    ren.SetActiveCamera(cam)
    ren.ResetCamera()
    ren.SetBackground(background)
    
    return ren
    
    