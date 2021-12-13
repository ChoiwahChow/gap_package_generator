#############################################################################
##
#W    init.g          The $PackageName Package           $Author1
$OtherAuthorNamesLines
##

#############################################################################
##
#R  Read the declaration files.
##
ReadPackage( "$PackageName", "lib/${Prefix}_utils.gd");
ReadPackage( "$PackageName", "lib/${Prefix}_small.gd");
$ADDITIONAL_GD

#E  init.g . . . . . . . . . . . . . . . . . . . . . . . . . . . .  ends here
