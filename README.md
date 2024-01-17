An attempt to make  a global scene node editor 
for Maya in QT. 

Unfinished. I decided to freeze this project at the moment. 

To navigate the scene, you must select one of the nodes and double-click on it, or I (inside) / O(outside) hotkeys will work.
Sockets/edges connections editing is implemented inside UI but gives no results on a scene itself; it's just a UI part.

To launch this in Maya, please add this repo
as a new module in Maya and launch this code:

>import sys
> 
>sys.path.insert(0, "path_to_repo/maya_node_editor")
> 
>from editor_window import NodeEditorWindow
> 
>wnd = NodeEditorWindow()

Small article about this editor:
http://golubevcg.com/post/global_node_editor_for_autodesk_maya

How it looks launched on a simple example:

>![connection_example](readme_images/connection_example.gif)

>![navigation_example](readme_images/navigation_example.gif)



```
Developed by
Andrew Golubev
golubevcg@gmail.com
```
