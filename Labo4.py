# -*- coding: utf-8 -*-
"""
Created on Wed May 20 14:13:55 2020

@author: alexandre
"""

import vtk
import os.path

xCenter = 75
yCenter = 40
zCenter = 110
radius = 50  
backgroundSkin = [0.74,0.55,0.55]

def CreateOutliner(slcr):
    outliner = vtk.vtkOutlineFilter()
    outliner.SetInputConnection(slcr.GetOutputPort())
    outliner.Update()
    return outliner

def CreateBone(slcr):
    contourBone = vtk.vtkContourFilter()
    contourBone.SetInputConnection(slcr.GetOutputPort())
    contourBone.SetValue(0,75.0)
    return contourBone

def CreateSkin(slcr):
    contourSkin = vtk.vtkContourFilter()
    contourSkin.SetInputConnection(slcr.GetOutputPort())
    contourSkin.SetValue(0,50.0)
    return contourSkin

def CreateSkinCutting(cf):    
    plane = vtk.vtkPlane()
    plane.SetOrigin(0,0,0)
    plane.SetNormal(0,0,1)
    
    cutter = vtk.vtkCutter()
    cutter.SetCutFunction(plane)
    cutter.SetInputConnection(cf.GetOutputPort())
    for i in range(100):
        cutter.SetValue(i,10 * i)
    cutter.Update()    
    
    return cutter

def CreateSkinClipping(cf):   

    sphere = vtk.vtkSphere()
    sphere.SetCenter(xCenter,yCenter,zCenter)
    sphere.SetRadius(radius)
    
    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(cf.GetOutputPort())
    clipper.SetClipFunction(sphere)
    clipper.SetValue(0)
    clipper.Update()
    
    return clipper

def CreateActor(o):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(o.GetOutputPort())
    mapper.SetScalarVisibility(0)
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor

def CreateActorWithBackground(o, b):
    actor = CreateActor(o)
    actor.GetProperty().SetColor(b)
    return actor

def CreateSphereClippingSkin(cs):
    
    sphere = vtk.vtkSphereSource()
    sphere.SetCenter(xCenter,yCenter,zCenter)
    sphere.SetRadius(radius + 3)
    
    ipdd = vtk.vtkImplicitPolyDataDistance()
    ipdd.SetInput(cs.GetOutput(0))
    
    clipperSphere = vtk.vtkClipPolyData()
    clipperSphere.SetInputConnection(sphere.GetOutputPort())
    clipperSphere.SetClipFunction(ipdd)
    clipperSphere.SetValue(0)
    clipperSphere.Update() 
    
    return clipperSphere

def CreateBoneColor(cb, cs):
    data = vtk.vtkDistancePolyDataFilter()
    data.SignedDistanceOff()
    data.SetInputConnection(0, cb.GetOutputPort())
    data.SetInputConnection(1, cs.GetOutputPort())
    data.Update()
    
    write = vtk.vtkPolyDataWriter()
    write.SetFileName("data_bone.vtk")
    write.SetInputConnection(data.GetOutputPort())
    write.Write()
    
    return data

def ReadBoneColor():
    data = vtk.vtkPolyDataReader()
    data.SetFileName("data_bone.vtk")
    data.Update()
    
    return data
    
def CreateActorBoneColor(o):
    mapperBone = vtk.vtkPolyDataMapper()
    mapperBone.SetInputConnection(o.GetOutputPort())
    mapperBone.SetScalarRange(
        o.GetOutput().GetPointData().GetScalars().GetRange()[0],
        o.GetOutput().GetPointData().GetScalars().GetRange()[1])
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapperBone)
    
    return actor
    

read = vtk.vtkSLCReader()
read.SetFileName("vw_knee.slc")
read.Update()

cam = vtk.vtkCamera()
cam.SetFocalPoint(0, 0, 0)
cam.SetPosition(0, 0, 100)
cam.SetViewUp(0, 0, 0)
cam.Roll(180)
cam.Elevation(90)
cam.OrthogonalizeViewUp()

renWin = vtk.vtkRenderWindow()
renWin.SetSize(600, 600)

bone = CreateBone(read)
skin = CreateSkin(read)
actorOutliner = CreateActor(CreateOutliner(read))

# REN 1
actorBone = CreateActor(bone)
actorSkin = CreateActorWithBackground(CreateSkinCutting(skin), backgroundSkin)
ren1 = vtk.vtkRenderer()
ren1.AddActor(actorBone)
ren1.AddActor(actorSkin)
ren1.AddActor(actorOutliner)
ren1.SetViewport([0,0.5,0.5,1])
ren1.SetActiveCamera(cam)
ren1.SetBackground([1,0.8,0.8])
# ren1 = CreateRen1(read, cam, [0,0.5,0.5,1],[1,0.8,0.8])
renWin.AddRenderer(ren1)

## REN 2
actorBone = CreateActor(bone)
actorSkin = CreateActorWithBackground(CreateSkinClipping(skin), backgroundSkin)

back = vtk.vtkProperty()
back.SetOpacity(1)
back.SetColor(0.74,0.55,0.55)
actorSkin.GetProperty().SetOpacity(0.7)
actorSkin.SetBackfaceProperty(back)

ren2 = vtk.vtkRenderer()
ren2.AddActor(actorBone)
ren2.AddActor(actorSkin)
ren2.AddActor(actorOutliner)
ren2.SetViewport([0.5,0.5,1,1])
ren2.SetActiveCamera(cam)
ren2.SetBackground([0.8, 1, 0.8])
renWin.AddRenderer(ren2)

# REN 3
actorBone = CreateActor(bone)
actorSkin = CreateActorWithBackground(CreateSkinClipping(skin), backgroundSkin)
actorSphere = CreateActorWithBackground(CreateSphereClippingSkin(CreateSkinClipping(CreateSkin(read))), [0.9,0.9,0.9])
actorSphere.GetProperty().SetOpacity(0.3)
ren3 = vtk.vtkRenderer()
ren3.AddActor(actorBone)
ren3.AddActor(actorSkin)
ren3.AddActor(actorSphere)
ren3.AddActor(actorOutliner)
ren3.SetViewport([0,0,0.5,0.5])
ren3.SetActiveCamera(cam)
ren3.SetBackground([0.8, 0.8, 1])
renWin.AddRenderer(ren3)

if os.path.isfile('data_bone.vtk'):
    actorBone = CreateActorBoneColor(ReadBoneColor())
else:
    actorBone = CreateActorBoneColor(CreateBoneColor(bone, skin))
ren4 = vtk.vtkRenderer()
ren4.AddActor(actorBone)
ren4.AddActor(actorOutliner)
ren4.SetViewport([0.5,0,1,0.5])
ren4.SetActiveCamera(cam)
ren4.SetBackground([0.8, 0.8, 0.8])
ren4.ResetCamera()
renWin.AddRenderer(ren4)
renWin.Render()

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)
iren.Initialize()
iren.Start()