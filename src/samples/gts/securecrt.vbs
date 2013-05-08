# $language = "VBScript"
# $interface = "1.0"

' Command Member Index
Const CMI_ID = 0
Const CMI_NAME = 1
Const CMI_ARGUMENT = 2

Function ReadCommand(Pipe)
	Dim ACommand()
	Dim CommandLineCount 
	
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
	
	' file system object server
	Set fso = CreateObject("Scripting.FileSystemObject")
	Set WshShell = CreateObject("WScript.Shell")
	
	PipeNames(0) = "\\.\pipe\terminal_scripter_input"
	PipeNames(1) = "\\.\pipe\terminal_scripter_output"
	PipeModes(0) = ForReading 
	PipeModes(1) = ForAppending ' Do not use ForWriting to write pipe ... 
	
	WshShell.Run "cmd /C start python client.py"
	
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