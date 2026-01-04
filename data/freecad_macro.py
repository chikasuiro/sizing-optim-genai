import os
from pathlib import Path
import time
import math
import FreeCAD
import Part
import Sketcher
import ObjectsFem
from femmesh.gmshtools import GmshTools as gt
import ObjectsFISTR
import fistrtools

# for rewriting
params = {
    'length_oval': 101.000000,
    'radius': 11.000000,
    'thickness': 20.000000,
    'fillet_size': 4.00,
    'reasoning': 'オリジナルパラメーター',
}

# variables to be optimized
length_oval = params['length_oval']
radius = params['radius']
thickness = params['thickness']
fillet_size = params['fillet_size']

# angle in radian
angle0 = math.pi * 0.1
angle1 = math.pi * 0.5
angle2 = math.pi * 1.0
angle3 = math.pi * 1.5
angle4 = math.pi * 2.5

doc = App.newDocument('model')
body_obj = doc.addObject('PartDesign::Body','Body')

# add new sketch
sketch_obj0 = body_obj.newObject('Sketcher::SketchObject','Sketch')
sketch_obj0.AttachmentSupport = (doc.getObject('XY_Plane'),[''])
sketch_obj0.MapMode = 'FlatFace'
## frame
sketch_obj0.addGeometry(Part.LineSegment(App.Vector(0.000000, 0.000000, 0.000000),App.Vector(200.000000, 0.000000, 0.000000)),False)
sketch_obj0.addConstraint(Sketcher.Constraint('Horizontal', 0))
doc.recompute()
sketch_obj0.addGeometry(Part.LineSegment(App.Vector(200.000000, 0.000000, 0.000000),App.Vector(200.000000, 50.000000, 0.000000)),False)
sketch_obj0.addConstraint(Sketcher.Constraint('Vertical', 1))
doc.recompute()
sketch_obj0.addGeometry(Part.LineSegment(App.Vector(200.000000, 50.000000, 0.000000),App.Vector(0.000000, 50.000000, 0.000000)),False)
sketch_obj0.addConstraint(Sketcher.Constraint('Horizontal', 2))
doc.recompute()
sketch_obj0.addGeometry(Part.LineSegment(App.Vector(0.000000, 50.000000, 0.000000),App.Vector(0.000000, 0.000000, 0.000000)),False)
sketch_obj0.addConstraint(Sketcher.Constraint('Vertical', 3))
doc.recompute()
sketch_obj0.addConstraint(Sketcher.Constraint('Coincident', 0, 2, 1, 1))
sketch_obj0.addConstraint(Sketcher.Constraint('Coincident', 1, 2, 2, 1))
sketch_obj0.addConstraint(Sketcher.Constraint('Coincident', 2, 2, 3, 1))
sketch_obj0.addConstraint(Sketcher.Constraint('Coincident', 3, 2, 0, 1))
sketch_obj0.addConstraint(Sketcher.Constraint('Coincident', 0, 1, -1, 1))
doc.recompute()
sketch_obj0.addConstraint(Sketcher.Constraint('DistanceX',2,2,2,1,200.000000))
doc.recompute()
# sketch_obj0.setDatum(9,App.Units.Quantity('200.000000 mm'))
sketch_obj0.addConstraint(Sketcher.Constraint('DistanceY',3,2,3,1,50.000000))
doc.recompute()
# sketch_obj0.setDatum(10,App.Units.Quantity('50.000000 mm'))
time.sleep(0.1)
## hole
sketch_obj0.addGeometry(Part.ArcOfCircle(Part.Circle(
     App.Vector(175.000000-length_oval, 25.000000, 0.000000),
     App.Vector(0.000000, 0.000000, 1.000000), radius), angle1, angle3),False)
sketch_obj0.addGeometry(Part.ArcOfCircle(Part.Circle(
     App.Vector(175.000000, 25.000000, 0.000000),
     App.Vector(0.000000, 0.000000, 1.000000), radius), angle3, angle4),False)
sketch_obj0.addGeometry(Part.LineSegment(
     App.Vector(175.000000-length_oval, 25.000000+radius, 0.000000),
     App.Vector(175.000000, 25.000000+radius, 0.000000)),False)
sketch_obj0.addGeometry(Part.LineSegment(
     App.Vector(175.000000-length_oval, 25.000000-radius, 0.000000),
     App.Vector(175.000000, 25.000000-radius, 0.000000)),False)
sketch_obj0.addConstraint(Sketcher.Constraint('Tangent', 4, 1, 6, 1))
sketch_obj0.addConstraint(Sketcher.Constraint('Tangent', 4, 2, 7, 1))
sketch_obj0.addConstraint(Sketcher.Constraint('Tangent', 5, 2, 6, 2))
sketch_obj0.addConstraint(Sketcher.Constraint('Tangent', 5, 1, 7, 2))
sketch_obj0.addConstraint(Sketcher.Constraint('Equal', 4, 5))
sketch_obj0.addConstraint(Sketcher.Constraint('Horizontal', 6))
doc.recompute()
sketch_obj0.addConstraint(Sketcher.Constraint('DistanceX',5,3,0,2,25.000000))
doc.recompute()
# sketch_obj0.setDatum(17,App.Units.Quantity('25.000000 mm'))
sketch_obj0.addConstraint(Sketcher.Constraint('DistanceX',4,3,5,3,length_oval))
doc.recompute()
# sketch_obj0.setDatum(18,App.Units.Quantity(f'{length_oval} mm'))
sketch_obj0.addConstraint(Sketcher.Constraint('Radius',5,radius))
doc.recompute()
# sketch_obj0.setDatum(19,App.Units.Quantity(f'{radius} mm'))
sketch_obj0.addConstraint(Sketcher.Constraint('DistanceY',0,2,5,3,25.000000))
doc.recompute()
# sketch_obj0.setDatum(20,App.Units.Quantity('25.000000 mm'))
time.sleep(0.1)
## pad
pad_obj = body_obj.newObject('PartDesign::Pad','Pad')
pad_obj.Profile = (sketch_obj0, ['',])
pad_obj.Length = thickness
pad_obj.Direction = (0, 0, 1)
pad_obj.ReferenceAxis = (sketch_obj0, ['N_Axis'])
doc.recompute()
sketch_obj0.Visibility = False
time.sleep(0.1)

# add new sketch
sketch_obj1 = doc.getObject('Body').newObject('Sketcher::SketchObject','Sketch001')
sketch_obj1.AttachmentSupport = (pad_obj,['Face10',])
sketch_obj1.MapMode = 'FlatFace'
sketch_obj1.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(30.000000, 25.000000, 0.000000), App.Vector(0.000000, 0.000000, 1.000000), radius), angle1, angle3),False)  # -> 0
sketch_obj1.addGeometry(Part.LineSegment(
     App.Vector(30.000000-radius, 25.000000, 0.000000),
     App.Vector(30.000000-radius, 0.000000, 0.000000)),False)  # -> 1
sketch_obj1.addConstraint(Sketcher.Constraint('Vertical', 1))  # -> 0
sketch_obj1.addConstraint(Sketcher.Constraint('Tangent',1, 1, 0, 2))  # -> 1
sketch_obj1.addConstraint(Sketcher.Constraint('PointOnObject', 1, 2, -1))  # -> 2
doc.recompute()
sketch_obj1.addGeometry(Part.LineSegment(
     App.Vector(30.000000-radius, 0.000000, 0.000000),
     App.Vector(30.000000, 0.000000, 0.000000)),False)  # -> 2
sketch_obj1.addConstraint(Sketcher.Constraint('Horizontal', 2))  # -> 3
sketch_obj1.addConstraint(Sketcher.Constraint('Coincident', 2, 1, 1, 2))  # -> 4
doc.recompute()
sketch_obj1.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,30.000000))  # -> 5
doc.recompute()
# sketch_obj1.setDatum(5,App.Units.Quantity('30.000000 mm'))
sketch_obj1.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,25.000000))  # -> 6
doc.recompute()
# sketch_obj1.setDatum(6,App.Units.Quantity('25.000000 mm'))
sketch_obj1.addConstraint(Sketcher.Constraint('Radius',0,radius))  # -> 7
doc.recompute()
# sketch_obj1.setDatum(7,App.Units.Quantity(f'{radius} mm'))
sketch_obj1.addGeometry(Part.LineSegment(App.Vector(30.000000, 36.000000, 0.000000),App.Vector(30.000000, 0.000000, 0.000000)),False)  # -> 3
sketch_obj1.addConstraint(Sketcher.Constraint('Vertical', 3))  # -> 8
sketch_obj1.addConstraint(Sketcher.Constraint('Coincident', 3, 1, 0, 1))  # -> 9
sketch_obj1.addConstraint(Sketcher.Constraint('Coincident', 3, 2, 2, 2))  # -> 10
sketch_obj1.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,1,30.000000))  # -> 11
doc.recompute()
# sketch_obj1.setDatum(11,App.Units.Quantity('30.000000 mm'))
time.sleep(0.1)
## pocket
pocket_obj0 = doc.getObject('Body').newObject('PartDesign::Pocket','Pocket')
pocket_obj0.Profile = (sketch_obj1, ['',])
pocket_obj0.Length = thickness + 10.000000
pocket_obj0.Direction = (0, 0, -1)
pocket_obj0.ReferenceAxis = (sketch_obj1, ['N_Axis'])
doc.recompute()
pad_obj.Visibility = False
sketch_obj1.Visibility = False
time.sleep(0.1)

# add new sketch
sketch_obj2 = doc.getObject('Body').newObject('Sketcher::SketchObject','Sketch002')
sketch_obj2.AttachmentSupport = (pocket_obj0,['Face4',])
sketch_obj2.MapMode = 'FlatFace'
sketch_obj2.addGeometry(Part.LineSegment(
     App.Vector(30.000000, 0.000000, 0.000000),
     App.Vector(30.000000, 25.000000+radius, 0.000000)),False)  # -> 0
sketch_obj2.addConstraint(Sketcher.Constraint('Vertical', 0))  # -> 0
sketch_obj2.addConstraint(Sketcher.Constraint('PointOnObject', 0, 1, -1))  # -> 1
doc.recompute()
sketch_obj2.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(30.000000, 25.000000, 0.000000), App.Vector(0.000000, 0.000000, 1.000000), radius), angle0, angle1),False)  # -> 1
sketch_obj2.addConstraint(Sketcher.Constraint('PointOnObject', 1, 3, 0))  # -> 2
sketch_obj2.addConstraint(Sketcher.Constraint('Coincident', 1, 2, 0, 2))  # -> 3
doc.recompute()
sketch_obj2.addGeometry(Part.LineSegment(App.Vector(30.000000, 0.000000, 0.000000),App.Vector(48.000000, 0.000000, 0.000000)),False)  # -> 2
sketch_obj2.addConstraint(Sketcher.Constraint('PointOnObject', 2, 2, -1))  # -> 4
sketch_obj2.addConstraint(Sketcher.Constraint('Coincident', 2, 1, 0, 1))  # -> 5
doc.recompute()
sketch_obj2.addGeometry(Part.LineSegment(
     App.Vector(48.000000, 0.000000, 0.000000),
     App.Vector(30.000000+radius, 25.000000, 0.000000)),False)  # -> 3
sketch_obj2.addConstraint(Sketcher.Constraint('Coincident', 3, 1, 2, 2))  # -> 6
sketch_obj2.addConstraint(Sketcher.Constraint('Tangent',1,1,3,2))  # -> 7
doc.recompute()
sketch_obj2.addConstraint(Sketcher.Constraint('Angle',0,2,3,2,15.000000))  # -> 8
doc.recompute()
sketch_obj2.setDatum(8,App.Units.Quantity('15.000000 deg'))
doc.recompute()
sketch_obj2.addConstraint(Sketcher.Constraint('DistanceX',-1,1,1,3,30.000000))  # -> 9
doc.recompute()
# sketch_obj2.setDatum(9,App.Units.Quantity('30.000000 mm'))
sketch_obj2.addConstraint(Sketcher.Constraint('DistanceY',-1,1,1,3,25.000000))  # -> 10
doc.recompute()
# sketch_obj2.setDatum(10,App.Units.Quantity('25.000000 mm'))
sketch_obj2.addConstraint(Sketcher.Constraint('Radius',1,radius))  # -> 11
doc.recompute()
# sketch_obj2.setDatum(11,App.Units.Quantity(f'{radius} mm'))
time.sleep(0.1)
## pocket
pocket_obj1 = doc.getObject('Body').newObject('PartDesign::Pocket','Pocket001')
pocket_obj1.Profile = (sketch_obj2, ['',])
pocket_obj1.Length = thickness + 10.000000
pocket_obj1.Direction = (0, 0, -1)
pocket_obj1.ReferenceAxis = (sketch_obj2, ['N_Axis'])
doc.recompute()
pocket_obj0.Visibility = False
sketch_obj2.Visibility = False
time.sleep(0.1)

# chamfer and fillet
chamfer_obj0 = doc.addObject('Part::Chamfer','Chamfer')
chamfer_obj0.Base = body_obj
chamfer_obj0.Edges = [(31,15.00,15.00),
                      (32,15.00,15.00),]
doc.recompute()
body_obj.Visibility = False
pocket_obj1.Visibility = False
chamfer_obj1 = doc.addObject('Part::Chamfer','Chamfer001')
chamfer_obj1.Base = chamfer_obj0
chamfer_obj1.Edges = [(17,1.00,1.00),
                      (21,1.00,1.00),
                      (25,1.00,1.00),]
doc.recompute()
chamfer_obj0.Visibility = False
fillet_obj = doc.addObject('Part::Fillet','Fillet')
fillet_obj.Base = chamfer_obj1
fillet_obj.Edges = [(36,fillet_size,fillet_size),]
doc.recompute()
chamfer_obj1.Visibility = False
time.sleep(0.1)

# output volume
volume_txt = Path('volume.txt')
volume_txt.touch(exist_ok=True)
with volume_txt.open('w') as f:
    f.write(str(fillet_obj.Shape.Volume) + '\n')

# FEM setup
analysis_obj = ObjectsFem.makeAnalysis(doc, 'Analysis')
## material
material_obj = ObjectsFem.makeMaterialSolid(doc, 'SolidMaterial')
analysis_obj.addObject(material_obj)
material_obj.Material = {
    'Name': 'Steel-Generic',
    'YoungsModulus': '200 GPa',
    'PoissonRatio': '0.30',
    'Density': '7900 kg/m^3',
    'ThermalConductivity': '500 W/m/K',
    'ThermalExpansionCoefficient': '12.00 um/m/K',
    'SpecificHeat': '500 J/kg/K',
}
## fixed constraint
fixed_constraint = doc.addObject('Fem::ConstraintFixed','Fixed')
analysis_obj.addObject(fixed_constraint)
fixed_constraint.References = [(fillet_obj,'Face13')]
## force constraint
force_constraint = doc.addObject('Fem::ConstraintForce', 'Force')
analysis_obj.addObject(force_constraint)
force_constraint.Force = '10000.00 mm*kg/s^2'
force_constraint.References = [(fillet_obj,'Face6')]
## mesh
femmesh_obj = ObjectsFem.makeMeshGmsh(doc, 'Mesh')
femmesh_obj.Shape = fillet_obj
femmesh_obj.CharacteristicLengthMax = 3.0
gmsh_mesh = gt(femmesh_obj)
err = gmsh_mesh.create_mesh()
# print(err)
analysis_obj.addObject(femmesh_obj)
doc.recompute()

# FrontISTR solver
solver_obj = ObjectsFISTR.makeSolverFrontISTRTools(doc, 'Solver')
analysis_obj.addObject(solver_obj)
## non-default values only
solver_obj.MatrixSolverNumIter = 10000
solver_obj.MatrixSolverResidual = '1.0e-8'
solver_obj.OutputFileFormat = u'VTK (paraview required)'
solver_obj.n_process = 1

# run
fea = fistrtools.FemToolsFISTR(solver=solver_obj)
fea.update_objects()
fea.setup_working_dir(param_working_dir=os.getcwd())
# print(fea.working_dir)
fea.setup_fistr()
message = fea.check_prerequisites()
if not message:
	fea.purge_results()
	fea.write_inp_file()
	fea.part_inp_file()
	fea.fistr_run()
else:
    # print("Houston, we have a problem! {}\n".format(message))
    pass
