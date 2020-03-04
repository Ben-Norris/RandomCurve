# RandomCurve
A Blender addon that creates random curves

<h1>Overview</h1>

This is a Blender add-on that generates random curves. It was mostly created to learn the add-on creating process but it can still generate some cool results.

<h1>Installation</h1>
Download the zip. Open Blender. Edit > Preferences > Add-ons. Click the install button at the top and navigate to the zip.</br>

![screenshot](images/screencap.JPG?raw=true)

<b>Generation Values:</b></br>
Number of Verts: The number of verts each curve will have.</br>
Number of Curves: The number of curve objects that will be generated.</br>
Twist Rate: The amount of twisting that takes place along the curve.</br>

<b>Rotation Options:</b></br>
Make 3D: Wether or not this curve rotates on two or three axes.</br>
Rotation Range: A random value is selected between the min and max and then applied to the object.</br>
Exclude Axis: (Shown when Make 3D is unchecked) When make 3D is unchecked. The axis selected is excluded from rotation creating curves on a 2D plane.</br>

<b>Bevel Options:</b></br>
Bevel Curve: If checked the curve will be beveled.</br>
Taper Object Name: You can create a taper object and put its name in the field. The taper object will be found and applied in the data panel. If left blank a basic curve will be created and applied.</br>
Bevel Object Name: You can create a bevel object and put its name in the field. The bevel object will be found and applied in the data panel. If left blank the curve will be beveled without an object influence.</br>
Random Bevel Depth: A random bevel value is generated between the min and max and then applied.</br>

<b>Collection Options:</b></br>
Add to Collection: If checked the objects will be added to a collection. If unchecked objects are added to the generic "Collection".</br>
Collection Name: A collection will be created with this name and all generated objects will be added to it. If blank objects are added to the generic "Collection".</br>

<b>Generate:</b></br>
Make Random Curves: Generates the curves!</br>
