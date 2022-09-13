#############################################################################
##
#W  small.gd  Small algebra access function for $AlgebraDisplayNameLowerCase
##  
#Y  Copyright (C)  $CopyrightYear                            $Author1
$OtherAuthorNamesLines
##  This file is auto-generated
##

###########################################################################
##
##  <#GAPDoc Label="$FunctionName">
##  <ManSection>
##  <Func Name="$FunctionName" Arg="m"/>
##  <Description>
##  This function returns all the $AlgebraDisplayNameLowerCase of order <M><A>m</A></M> from the library.<P/>
##
##  No check is performed to verify that <A>m</A> is a valid argument. <P/>
##
##  In <C>$FunctionName</C>, an error will be signaled if the $AlgebraDisplayNameLowerCase
##  of order <A>m</A> are not available.
##  <Example><![CDATA[
##  gap> Length($FunctionName(${MinDomainSize}));
##  ${MinAlgebraSize}
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>

DeclareGlobalFunction( "$FunctionName" );
#############################################################################

###########################################################################
##
##  <#GAPDoc Label="Is$SingularAlgebraName">
##  <ManSection>
##  <Func Name="Is$SingularAlgebraName" Arg="m"/>
##  <Description>
##  This function checks whether <M><A>m</A></M>, which must be a multiplication table, is isomorphic to a $SingularAlgebraName in the library.<P/>
##
##  No check is performed to verify that <A>m</A> is a valid argument. <P/>
##  <Example><![CDATA[
##  gap> Is$SingularAlgebraName($FunctionName(${MinDomainSize})[1]);
##  true
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>

DeclareGlobalFunction( "Is$SingularAlgebraName" );
#############################################################################
