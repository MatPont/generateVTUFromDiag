import vtk

# Cell: Birth, Persistence, PairType (0),
# Points: CriticalType


def generateVTUFromDiag(diag):
    points = vtk.vtkPoints()
    criticalTypeArray = vtk.vtkIntArray()
    criticalTypeArray.SetName("CriticalType")
    allPointsIDs = []
    for i in range(len(diag)):
        pair = diag[i]
        birth = pair[0]
        death = pair[1]
        pers = death - birth
        # Insert Point
        pointID1 = points.InsertNextPoint(birth, birth, 0)
        pointID2 = points.InsertNextPoint(birth, death, 0)
        allPointsIDs.append([pointID1, pointID2])
        # Critical Type Array
        critType = 0 if i == 0 else 2
        criticalTypeArray.InsertNextTuple1(critType)
        criticalTypeArray.InsertNextTuple1(3)

    grid = vtk.vtkUnstructuredGrid()
    grid.SetPoints(points)
    grid.GetPointData().AddArray(criticalTypeArray)

    birthArray = vtk.vtkFloatArray()
    birthArray.SetName("Birth")
    persArray = vtk.vtkFloatArray()
    persArray.SetName("Persistence")
    pairTypeArray = vtk.vtkIntArray()
    pairTypeArray.SetName("PairType")
    for i in range(len(diag)):
        pIDs = allPointsIDs[i]
        # Insert cell
        pointIds = vtk.vtkIdList()
        pointIds.SetNumberOfIds(2)
        pointIds.SetId(0, pIDs[0])
        pointIds.SetId(1, pIDs[1])
        grid.InsertNextCell(vtk.VTK_LINE, pointIds)
        #
        birthArray.InsertNextTuple1(diag[i][0])
        persArray.InsertNextTuple1(diag[i][1] - diag[i][0])
        pairTypeArray.InsertNextTuple1(0)
    grid.GetCellData().AddArray(birthArray)
    grid.GetCellData().AddArray(persArray)
    grid.GetCellData().AddArray(pairTypeArray)

    return grid


def generateAndSaveDiags(data, baseName="", name=""):
    allPD = []
    for i in range(len(data)):
        pd = generateVTUFromDiag(data[i])
        allPD.append(pd)

    block = vtk.vtkMultiBlockDataSet()
    block.SetNumberOfBlocks(len(allPD))
    for i in range(len(allPD)):
        block.SetBlock(i, allPD[i])

    writer = vtk.vtkXMLMultiBlockDataWriter()
    writer.SetInputData(block)
    if name == "":
        if baseName != "":
            baseName += "_"
        name = baseName + "pd.vtm"
    writer.SetFileName(name)
    writer.Update()
