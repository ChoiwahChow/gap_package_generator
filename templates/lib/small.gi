#############################################################################
##
#W  small.gi  Small algebra access function for $AlgebraDisplayNameLowerCase
##  
#Y  Copyright (C)  $CopyrightYear                            $Author1
$OtherAuthorNamesLines
##  This file is auto-generated
##

# up to isomorphism
ReadPackage("$PackageName", "data/${Prefix}_small.tbl");    # small algebras

###########################################################################
##
#F  $FunctionName( <size> )
##

InstallGlobalFunction( $FunctionName,
function( order )
	local data, pos, num, algebras, all, x;

	data := ${Prefix}_small_data;
	pos := Position(data[1], order);  # look up the list of implemented orders
	if pos = fail then
		Error("$PackageName: $AlgebraDisplayNameLowerCase not available for this order.");
	fi;
	num := data[2][pos];         # number of models for this order
	algebras := data[3][pos];    # the encoded models
	all := [0]*num;
	for x in [1..num] do
		all[x] := ${Prefix}_DecodeAlgebra(algebras[x], order);		
	od;

	return all;
end );

#############################################################################


###########################################################################
##
#F  $FunctionName( <multiplcation_table> )
##

InstallGlobalFunction( "IsSmall$SingularAlgebraName",
function( m )
	local el;
	if IsList(m[1][1]) then
		for el in $FunctionName(Length(m[1][1])) do
		    if IsomorphismAlgebras(el, m) <> fail then return true; fi;
		od;
	else
		for el in $FunctionName(Length(m[1])) do
		    if IsomorphismAlgebras([el], [m]) <> fail then return true; fi;
		od;
	fi;
	return false;
end );

#############################################################################
