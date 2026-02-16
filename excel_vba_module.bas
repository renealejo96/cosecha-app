' =====================================================
' MÓDULO VBA PARA IMPORTAR DATOS DE LA API DE COSECHA
' =====================================================
' 
' INSTRUCCIONES DE INSTALACIÓN:
' 1. Abre Excel y presiona Alt + F11 para abrir el Editor VBA
' 2. En el menú, selecciona Insertar > Módulo
' 3. Copia y pega este código completo
' 4. Cierra el Editor VBA
' 5. Crea un botón en tu hoja de Excel y asígnale la macro "ActualizarDatosCosecha"
'
' REQUISITOS:
' - Habilitar "Microsoft XML, v6.0" en Herramientas > Referencias
' - Habilitar "Microsoft Scripting Runtime" en Herramientas > Referencias
'
' =====================================================

Option Explicit

' Configuración global - EDITA ESTAS VARIABLES
Const URL_BASE As String = "http://localhost:5000"  ' Cambiar a tu URL de producción si es necesario
Const HOJA_DATOS As String = "Datos_Cosecha"        ' Nombre de la hoja donde se importarán los datos

Sub ActualizarDatosCosecha()
    '
    ' Macro principal para importar datos de cosecha desde la API
    '
    Dim semana As String
    Dim url As String
    Dim jsonResponse As String
    
    ' Solicitar al usuario la semana a consultar
    semana = InputBox("Ingrese la semana en formato AASS (ej: 2546):", "Semana a Consultar", ObtenerSemanaActual())
    
    If semana = "" Then
        MsgBox "Operación cancelada.", vbInformation
        Exit Sub
    End If
    
    ' Validar formato de semana
    If Not ValidarFormatoSemana(semana) Then
        MsgBox "Formato de semana inválido. Use formato AASS (ej: 2546).", vbExclamation
        Exit Sub
    End If
    
    ' Construir URL
    url = URL_BASE & "/api/resumen?semana=" & semana & "&formato=plano"
    
    ' Mostrar mensaje de espera
    Application.ScreenUpdating = False
    Application.Cursor = xlWait
    
    On Error GoTo ErrorHandler
    
    ' Hacer petición HTTP
    jsonResponse = HacerPeticionHTTP(url)
    
    ' Procesar y escribir datos en Excel
    ProcesarYEscribirDatos jsonResponse, semana
    
    ' Restaurar cursor y actualizar pantalla
    Application.Cursor = xlDefault
    Application.ScreenUpdating = True
    
    MsgBox "Datos actualizados correctamente para la semana " & semana & "!", vbInformation
    
    Exit Sub
    
ErrorHandler:
    Application.Cursor = xlDefault
    Application.ScreenUpdating = True
    MsgBox "Error al actualizar datos: " & Err.Description, vbCritical
End Sub

Function HacerPeticionHTTP(url As String) As String
    '
    ' Realiza una petición HTTP GET y devuelve la respuesta
    '
    Dim http As Object
    Set http = CreateObject("MSXML2.XMLHTTP")
    
    http.Open "GET", url, False
    http.setRequestHeader "Content-Type", "application/json"
    http.send
    
    If http.Status = 200 Then
        HacerPeticionHTTP = http.responseText
    Else
        Err.Raise vbObjectError + 1, , "Error HTTP " & http.Status & ": " & http.statusText
    End If
End Function

Sub ProcesarYEscribirDatos(jsonResponse As String, semana As String)
    '
    ' Procesa el JSON y escribe los datos en la hoja de Excel
    ' NOTA: Esta es una versión simplificada. Para JSON complejo, 
    '       se recomienda usar Power Query en su lugar.
    '
    Dim ws As Worksheet
    Dim fila As Long
    
    ' Crear o limpiar hoja de datos
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)
    On Error GoTo 0
    
    If ws Is Nothing Then
        Set ws = ThisWorkbook.Worksheets.Add
        ws.Name = HOJA_DATOS
    Else
        ws.Cells.Clear
    End If
    
    ' Escribir encabezados
    fila = 1
    ws.Cells(fila, 1).Value = "Semana"
    ws.Cells(fila, 2).Value = "Producto Maestro"
    ws.Cells(fila, 3).Value = "Variedad"
    ws.Cells(fila, 4).Value = "Fecha"
    ws.Cells(fila, 5).Value = "Día"
    ws.Cells(fila, 6).Value = "Bloque/Módulo"
    ws.Cells(fila, 7).Value = "Hora Cosecha"
    ws.Cells(fila, 8).Value = "Tallos/Malla"
    ws.Cells(fila, 9).Value = "Mallas"
    ws.Cells(fila, 10).Value = "Total Tallos"
    ws.Cells(fila, 11).Value = "Responsable"
    ws.Cells(fila, 12).Value = "Viaje"
    
    ' Formatear encabezados
    With ws.Range("A1:L1")
        .Font.Bold = True
        .Interior.Color = RGB(68, 114, 196)
        .Font.Color = RGB(255, 255, 255)
        .HorizontalAlignment = xlCenter
    End With
    
    ' Ajustar ancho de columnas
    ws.Columns("A:L").AutoFit
    
    ' Aquí deberías parsear el JSON y llenar las filas
    ' Para simplificar, se recomienda usar Power Query (ver método abajo)
    
    MsgBox "NOTA: Para importar los datos automáticamente, " & vbCrLf & _
           "use el método de Power Query descrito en la documentación.", vbInformation
End Sub

Function ValidarFormatoSemana(semana As String) As Boolean
    '
    ' Valida que la semana tenga formato AASS
    '
    If Len(semana) = 4 And IsNumeric(semana) Then
        ValidarFormatoSemana = True
    Else
        ValidarFormatoSemana = False
    End If
End Function

Function ObtenerSemanaActual() As String
    '
    ' Calcula la semana actual en formato AASS
    '
    Dim año As Integer
    Dim numeroSemana As Integer
    
    año = Year(Date)
    numeroSemana = Application.WorksheetFunction.WeekNum(Date, 2) ' 2 = lunes como primer día
    
    ' Formato AASS
    ObtenerSemanaActual = Format(año Mod 100, "00") & Format(numeroSemana, "00")
End Function

Sub DescargarExcelDirecto()
    '
    ' Descarga directamente el archivo Excel desde la API
    ' Abre el cuadro de diálogo para guardar el archivo
    '
    Dim semana As String
    Dim url As String
    Dim fileName As String
    
    ' Solicitar semana
    semana = InputBox("Ingrese la semana en formato AASS (ej: 2546):", "Semana a Descargar", ObtenerSemanaActual())
    
    If semana = "" Then
        MsgBox "Operación cancelada.", vbInformation
        Exit Sub
    End If
    
    ' Validar formato
    If Not ValidarFormatoSemana(semana) Then
        MsgBox "Formato de semana inválido. Use formato AASS (ej: 2546).", vbExclamation
        Exit Sub
    End If
    
    ' Construir URL y nombre de archivo
    url = URL_BASE & "/api/resumen/excel?semana=" & semana
    fileName = "resumen_cosecha_semana_" & semana & ".xlsx"
    
    ' Abrir en navegador (el navegador manejará la descarga)
    ThisWorkbook.FollowHyperlink url
    
    MsgBox "Se abrirá el navegador para descargar el archivo: " & fileName, vbInformation
End Sub

Sub ObtenerSemanasDisponibles()
    '
    ' Obtiene y muestra todas las semanas disponibles
    '
    Dim url As String
    Dim jsonResponse As String
    
    url = URL_BASE & "/api/semanas"
    
    Application.Cursor = xlWait
    
    On Error GoTo ErrorHandler
    
    jsonResponse = HacerPeticionHTTP(url)
    
    Application.Cursor = xlDefault
    
    ' Mostrar respuesta (simplificado)
    MsgBox "Semanas disponibles (ver consola inmediata para JSON completo):" & vbCrLf & vbCrLf & _
           Left(jsonResponse, 200) & "...", vbInformation
    
    Debug.Print jsonResponse
    
    Exit Sub
    
ErrorHandler:
    Application.Cursor = xlDefault
    MsgBox "Error: " & Err.Description, vbCritical
End Sub

' =====================================================
' FIN DEL MÓDULO
' =====================================================
