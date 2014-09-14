<map version="freeplane 1.3.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="SDE" ID="ID_1723255651" CREATED="1283093380553" MODIFIED="1410689498276"><hook NAME="MapStyle">

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node">
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right">
<stylenode LOCALIZED_TEXT="default" MAX_WIDTH="600" COLOR="#000000" STYLE="as_parent">
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.note"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="right">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important">
<icon BUILTIN="yes"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="right">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="AutomaticEdgeColor" COUNTER="7"/>
<node TEXT="Where the abbreviation comes from?" POSITION="right" ID="ID_995384807" CREATED="1403436755183" MODIFIED="1403436775252">
<edge COLOR="#ff0000"/>
<node TEXT="Subversion Distributed Extension" ID="ID_26963160" CREATED="1403436776044" MODIFIED="1410689503851"/>
</node>
<node TEXT="Why we need another SVK ?" POSITION="right" ID="ID_911783058" CREATED="1403439194526" MODIFIED="1403439206291">
<edge COLOR="#0000ff"/>
<node TEXT="SVK has been discontinued at March 21, 2010, 4 years ago." ID="ID_1432684111" CREATED="1403439207254" MODIFIED="1403439270524"/>
<node TEXT="SVK implemented by perl which grammar is not easy to understand, and I love python" ID="ID_1172375412" CREATED="1403439274225" MODIFIED="1403439462576"/>
<node TEXT="SVK build with svn libraries, we have to upgrade to newest svn libraries, and it&apos;s uneasy way on windows." ID="ID_1890176172" CREATED="1403439338101" MODIFIED="1403699933066"/>
</node>
<node TEXT="Detail" POSITION="right" ID="ID_589212828" CREATED="1403699940334" MODIFIED="1403700003016">
<edge COLOR="#00ff00"/>
<node TEXT="Implemented by python, that&apos;s more readable." ID="ID_1227171572" CREATED="1403700003912" MODIFIED="1403700233268"/>
<node TEXT="Do not depends on svn libraries, but depends on svn binaries in current environment, that&apos;s more easy for user to upgrade svn from old revisions." ID="ID_1057619118" CREATED="1403700009770" MODIFIED="1403700100473"/>
<node TEXT="The master repository will included in &quot;.rsde&quot; directory, so that the whole svn directory could be copied to another PC easily just like git." ID="ID_1393939992" CREATED="1403700120253" MODIFIED="1403700271995"/>
</node>
<node TEXT="How to dump and import a revision?" POSITION="right" ID="ID_1883707264" CREATED="1410667251557" MODIFIED="1410667326641">
<edge COLOR="#ff00ff"/>
<node TEXT="Export a revision of remote repository to a patch" ID="ID_702452877" CREATED="1410667261775" MODIFIED="1410667291176"/>
<node TEXT="Change the patch for needed" ID="ID_1342594747" CREATED="1410667278630" MODIFIED="1410667304477">
<node TEXT="Path changed" ID="ID_306681686" CREATED="1410667309322" MODIFIED="1410667313785"/>
</node>
<node TEXT="Patch to our private svn repository with comments" ID="ID_123717027" CREATED="1410667305240" MODIFIED="1410667383890"/>
<node TEXT="Ensure all properties same with remote repository" ID="ID_266583949" CREATED="1410667431295" MODIFIED="1410667451391"/>
<node TEXT="Mark the revision property rsde:revision to remote revision" ID="ID_1952871567" CREATED="1410667452012" MODIFIED="1410667714041"/>
</node>
<node TEXT="There have two branch" POSITION="right" ID="ID_1131059659" CREATED="1410667792342" MODIFIED="1410667800164">
<edge COLOR="#00ffff"/>
<node TEXT="One for mirror" ID="ID_1394529776" CREATED="1410667801201" MODIFIED="1410667808781">
<node TEXT="Always follow the remote repository" ID="ID_899578457" CREATED="1410667809593" MODIFIED="1410667821442"/>
</node>
<node TEXT="Another for local" ID="ID_633960900" CREATED="1410667822772" MODIFIED="1410667828381">
<node TEXT="Always follow the user" ID="ID_1681128145" CREATED="1410667829504" MODIFIED="1410667836311"/>
</node>
</node>
<node TEXT="Local working copy" POSITION="right" ID="ID_894267985" CREATED="1410668859007" MODIFIED="1410668878713">
<edge COLOR="#7c0000"/>
<node TEXT="User working copy" ID="ID_1771832591" CREATED="1410668879546" MODIFIED="1410668884734"/>
<node TEXT="Temporary working copy use for upload patch" ID="ID_387761653" CREATED="1410668885096" MODIFIED="1410668897232">
<node TEXT="" ID="ID_1735593558" CREATED="1410677628832" MODIFIED="1410677628832"/>
</node>
</node>
<node TEXT="How to export a revision" POSITION="right" ID="ID_1369764490" CREATED="1410667895745" MODIFIED="1410667901631">
<edge COLOR="#ffff00"/>
<node TEXT="Export a new revision that mirror do not have" ID="ID_1476234909" CREATED="1410667902423" MODIFIED="1410667941977"/>
<node TEXT="Change the patch for needed" ID="ID_1592775684" CREATED="1410667943727" MODIFIED="1410667949316"/>
<node TEXT="Patch to temporary directory, commit it" ID="ID_1099859551" CREATED="1410668817771" MODIFIED="1410668851893"/>
</node>
</node>
</map>
