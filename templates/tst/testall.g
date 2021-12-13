#############################################################################
##
#W  testall.g   Testing $PackageName    $AllAuthorsListString
##
##
##

LoadPackage("$PackageName");
TestDirectory(DirectoriesPackageLibrary("$PackageName", "tst"), rec(exitGAP := true));
FORCE_QUIT_GAP(1);
