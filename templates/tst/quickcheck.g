
LoadPackage("$PackageName");;


test_${FunctionName}_g := function(size, count)
	local  a, b, c, x;
	a := $FunctionName(size);
	if Length(a) <> count then
		Print("Test failed for retrieving algebra of size "); Print(size); Print("\n");
	fi;
end;


