#############################################################################
##
#W  ${PackageName}.tst   Testing Retrievals of Small Algebras    $AllAuthorsListString
##
##
##
gap> START_TEST("Algebra(s), $PackageName: testing retrieval of non-isomorphic models");

# Simple Length Test 
gap> Length($FunctionName($MinDomainSize));
${MinAlgebraSize}
gap> Is$SingularAlgebraName($FunctionName(${MinDomainSize})[1]);
true
gap> STOP_TEST( "algebra.tst", 100000 );

