# $language = "VBScript"
# $interface = "1.0"

Option Explicit 

' Command Member Index
Const CMI_ID = 0
Const CMI_NAME = 1
Const CMI_ARGUMENT = 2

Function IsValid(Value)
	IsValid = False
	
	If IsNull(Value) Then
		Exit Function
	End If
	
	If IsEmpty(Value) Then
		Exit Function
	End If
	
	If IsObject(Value) Then
		If Value is Nothing Then
			Exit Function
		End If
	End If
	
	IsValid = True
End Function

Function ReadCommand(Pipe)
	Dim ACommand()
	Dim CommandLineCount 
	Dim ALine
	
	CommandLineCount = 0
	Do While True
		' It will wait for next line of there do not have any input
		ALine = Pipe.ReadLine() 
		
		If ALine = "@begin" Then
			CommandLineCount = CommandLineCount + 1
		ElseIf ALine = "@end" Then
			ReadCommand = ACommand
			Exit Function
		ElseIf CommandLineCount > 0 Then
			ReDim Preserve ACommand(CommandLineCount)
			If Len(ALine) > 0 Then
				ACommand(CommandLineCount - 1) = Right( ALine, Len(ALine) - 1 ) ' Remove prefix "#"
			Else
				ACommand(CommandLineCount - 1) = ""
			End If
			CommandLineCount = CommandLineCount + 1
		End If
	Loop
	
	ReadCommand = Nothing
End Function

Sub ReplyBegin(Pipe, ACommand)
	Pipe.WriteLine "@begin"
	Pipe.WriteLine "#" & ACommand(CMI_ID) 
	Pipe.WriteLine "#" & ACommand(CMI_NAME)
End Sub

Sub ReplyMessage(Pipe, Message)
	Pipe.WriteLine "#" & Message
End Sub

Sub ReplyEnd(Pipe)
	Pipe.WriteLine "@end"
End Sub

Function HandleQuitCommand(Pipe, ACommand)
	HandleQuitCommand = False
End Function

Function HandleExecuteCommand(Pipe, ACommand)
	Execute ACommand(CMI_ARGUMENT)
	
	ReplyBegin Pipe, ACommand
	ReplyEnd Pipe
	
	HandleExecuteCommand = True
End Function

Function HandleGetValueCommand(Pipe, ACommand)
	ReplyBegin Pipe, ACommand
	ReplyMessage Pipe, CStr(Eval(ACommand(CMI_ARGUMENT)))
	ReplyEnd Pipe
	
	HandleGetValueCommand = True
End Function

Function HandleCommand(Pipe, ACommand)
	Dim i
	
	Select Case ACommand(1)
	Case "execute"
		HandleCommand = HandleExecuteCommand(Pipe, ACommand)
	Case "get_value"
		HandleCommand = HandleGetValueCommand(Pipe, ACommand)
	Case "quit"
		HandleCommand = HandleQuitCommand(Pipe, ACommand)
	Case Else
		HandleCommand = True
	End Select
	
End Function

Function IniGetValue(FileName, Section, KeyName, Default)
	Dim fso
	Dim IniFile
	Dim Pos
	Dim SectionLeftPos
	Dim SectionRightPos
	Dim ObtainedSection
	Dim ObtainedKey
	Dim ObtainedValue
	Dim ALine
	
	IniGetValue = Default
	
	Set fso = CreateObject("Scripting.FileSystemObject")
	If Not fso.FileExists(FileName) Then
		Exit Function
	End If
	
	Set IniFile = fso.OpenTextFile(FileName, 1, False)
	Do While Not IniFile.AtEndOfStream
		ALine = IniFile.ReadLine
		If IsValid(ALine) Then
			SectionLeftPos = InStr( ALine, "[" )
			SectionRightPos = InStrRev( ALine, "]" )
			Pos = InStr( ALine, "=" )
			If IsValid(SectionLeftPos) And IsValid(SectionRightPos) _
			 	And ( SectionLeftPos <> 0 ) And ( SectionRightPos > SectionLeftPos)  And (SectionRightPos <> 0) Then
				ObtainedSection = Mid( ALine, SectionLeftPos + 1, ( SectionRightPos - SectionLeftPos - 1 ) )
			ElseIf IsValid(Pos) And ( Pos > 0 ) Then
				ObtainedKey = Trim( Left(ALine, Pos - 1) )
				ObtainedValue = Trim( Right(ALine, Len(ALine) - Pos ) )
				If ( StrComp( ObtainedKey, KeyName ) = 0 ) And ( StrComp( ObtainedSection, Section ) = 0 ) Then
					' Found the section, key we want to search
					IniGetValue = ObtainedValue
					Exit Do
				End If 
			End If
		End If
	Loop
	IniFile.Close
End Function

Sub Main
	const ForReading = 1
	const ForWriting = 2
	const ForAppending = 8
	' 3 seconds timeout if we could not connect to python created pipes  
	const TimeOutCount = 30 
	Dim PipeNames(1)
	Dim PipeModes(1)
	Dim Pipes(1)	
	Dim OutputPipe
	Dim InputPipe
	Dim i
	Dim SuccessedCount
	Dim ExceptionCount
	Dim IniValue
	Dim fso
	Dim WshShell
	Dim ACommand
	
	' file system object server
	Set fso = CreateObject("Scripting.FileSystemObject")
	Set WshShell = CreateObject("WScript.Shell")
	
	PipeNames(0) = "\\.\pipe\terminal_scripter_input"
	PipeNames(1) = "\\.\pipe\terminal_scripter_output"
	PipeModes(0) = ForReading 
	PipeModes(1) = ForAppending ' Do not use ForWriting to write pipe ... 
	
	WshShell.Run "cmd /C del gts.ini && start python client.py securecrt"
	
	' Get pipe names from gts.ini that client.py generated
	ExceptionCount = 0
	Do While True
		crt.Sleep 500 ' Sleep 100ms to wait for pipe open
		If fso.FileExists( "gts.ini" ) Then
			crt.Sleep 100 ' Wait for ini file write finished
			PipeNames(0) = IniGetValue("gts.ini", "system", "input_pipe", Empty)
			PipeNames(1) = IniGetValue("gts.ini", "system", "output_pipe", Empty)
			Exit Do
		End If
		
		ExceptionCount = ExceptionCount + 1
		If ExceptionCount * 500 > 3000 Then ' If timeout large than 3 seconds, we exit the script.
			Exit Sub
		End If
	Loop
	
	' Could only use CreateTextFile() to open the named pipe
	i = 0
	SuccessedCount = 0
	ExceptionCount = 0
	Do While True
		crt.Sleep 100 ' Sleep 100 ms to wait for pipe open
		
		For i = 0 to UBound(Pipes) 
			If IsNull(Pipes(i)) or IsEmpty(Pipes(i)) Then
				On Error Resume Next
				Set Pipes(i) = fso.OpenTextFile( PipeNames(i), PipeModes(i) )
				On Error Goto 0
				
				If Not ( IsNull(Pipes(i)) or IsEmpty(Pipes(i)) ) Then
					'crt.Dialog.MessageBox "open " & SuccessedCount
					SuccessedCount = SuccessedCount + 1 
				End If
				
				If SuccessedCount > UBound(Pipes) Then
					'crt.Dialog.MessageBox "exit " & SuccessedCount
					Exit Do
				End If
			Else 
				'crt.Dialog.MessageBox "none " & SuccessedCount
			End If
		Next
		
		ExceptionCount = ExceptionCount + 1
		If ExceptionCount > TimeOutCount Then 
			Exit Do 
		End If
	Loop
	
	If ExceptionCount > TimeOutCount Then 
		crt.Dialog.MessageBox "Time out !"
		Exit Sub
	End If
	
	Set InputPipe = Pipes(0)
	Set OutputPipe = Pipes(1)	
	
	crt.Screen.Synchronous = True
	
	' Begin command analyse 
	Do While True
		ACommand = ReadCommand(InputPipe)
		If Not ( IsNull(ACommand) or IsEmpty(ACommand) ) Then
			' If HandleCommand() return False, we should exit immediately
			If Not HandleCommand(OutputPipe, ACommand) Then
				Exit Do 
			End If
		End If
	Loop
	
	crt.Screen.Synchronous = False
End Sub