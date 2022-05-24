############################################################################
##
##  PackageInfo.g
#Y  Copyright (C) $CopyrightYear                            $Author1
$OtherAuthorNamesLines
##
##  Licensing information can be found in the README file of this package.
##  This file is auto-generated.
##
#############################################################################
##

##  <#GAPDoc Label="PKGVERSIONDATA">
##  <!ENTITY VERSION "$Version">
##  <!ENTITY COPYRIGHTYEARS "$CopyrightYear">
##  <!ENTITY ARCHIVENAME "${PackageName}-$Version">
##  <#/GAPDoc>

SetPackageInfo( rec(
PackageName := "$PackageName",
Subtitle := "Small $AlgebraName in GAP",
Version := "$Version",
Date := "$DateOfRelease",

Persons := [
$AllPersonsLines
],

Status := "$Status",
CommunicatedBy := "$Author1",
AcceptDate := "N/A",

PackageWWWHome  := "$PackageWWWHome",
README_URL      := Concatenation( ~.PackageWWWHome, "README" ),
PackageInfoURL  := Concatenation( ~.PackageWWWHome, "PackageInfo.g" ),
SourceRepository := rec(
    Type := "git",
    URL := "$SourceRepository",
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "issues" ),
ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/${PackageName}-", ~.Version ),
ArchiveFormats := ".tar.gz",

AbstractHTML := Concatenation(
"The $PackageName package provides researchers in computational algebra ",
"with a computational tool to access the non-isomorphic $AlgebraDisplayName ",
"in the computational algebra system GAP."
),

PackageDoc := rec(
  BookName  := "$PackageName",
  ArchiveURLSubset := ["doc"],
  HTMLStart := "doc/chap0_mj.html",
  PDFFile   := "doc/manual.pdf",
  SixFile   := "doc/manual.six",
  LongTitle := "The Small $PackageName Package: algebras of small orders for GAP",
  Autoload  := true     # only for the documentation, TEMPORARILY TURNED OFF
),

Dependencies := rec(
  GAP := ">=4.10",
  NeededOtherPackages := [],
  SuggestedOtherPackages := [],
  ExternalConditions := []
),

AvailabilityTest := ReturnTrue,
TestFile := "tst/testall.g",
Keywords := ["$PackageName"],

AutoDoc := rec(
    TitlePage := rec(
        Title := "The Small $PackageName Package",
        Abstract := ~.AbstractHTML,
        Copyright := """
<Index>License</Index>
&copyright; $CopyrightYear $AllAuthorsListString.<P/>
The &PackageName; package is free software;
you can redistribute it and/or modify it under the terms of the
<URL Text="GNU General Public License">https://www.fsf.org/licenses/gpl.html</URL>
as published by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.
""",
        Acknowledgements := """
""",
    ),
),

));
