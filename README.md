# generateVTUFromDiag

The `generateVTUFromDiag` function of `generateVTUFromDiag.py` takes an array representing a persistence diagram (like `[[0, 10], [4, 5], [6, 8]]` and create a vtkUnstructuredGrid representing the diagram.
It is the necessary format for algorithms of [TTK](https://github.com/topology-tool-kit/ttk).

The `generateAndSaveDiags` function takes an array of persistence diagrams (like represented before) and saves a Multi-Block DataSet in a `.vtm` format, consisting of many vtkUnstructuredGrid representing the diagrams.
