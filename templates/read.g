#############################################################################

##
#W  read.g                  $PackageName          $Author1
$OtherAuthorNamesLines
##
##
##

#############################################################################
##
#R  Read the install files.
##  -------------------------------------------------------------------------
ReadPackage( "$PackageName", "lib/${Prefix}_utils.gi" );
ReadPackage( "$PackageName", "lib/${Prefix}_small.gi" );


#E  read.g . . . . . . . . . . . . . . . . . . . . . . . . . . . .  ends here
