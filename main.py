if __name__ == "__main__":
    import sys
    import inspect

    for module in list(sys.modules):
        module_path = None
        try:
            module_path = inspect.getfile(sys.modules[module])
            if "maya_node_editor" in module_path:
                sys.modules.pop(module_path)
        except:
            continue

    import sys
    sys.path.insert(0, "C:/Users/golub/Documents/maya_node_editor")
    from editor_window import NodeEditorWindow

    wnd = NodeEditorWindow()

    wnd.init_ui()
