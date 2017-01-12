<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="1.8.0-Lisboa" minimumScale="0" maximumScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <transparencyLevelInt>255</transparencyLevelInt>
  <renderer-v2 symbollevels="0" type="singleSymbol">
    <symbols>
      <symbol outputUnit="MM" alpha="1" type="line" name="0">
        <layer pass="0" class="MarkerLine" locked="0">
          <prop k="interval" v="1"/>
          <prop k="offset" v="0"/>
          <prop k="placement" v="interval"/>
          <prop k="rotate" v="1"/>
        </layer>
      </symbol>
      <symbol outputUnit="MM" alpha="1" type="marker" name="@0@0">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,85,127,255"/>
          <prop k="color_border" v="0,0,0,255"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="size" v="1.5"/>
        </layer>
      </symbol>
    </symbols>
    <rotation field=""/>
    <sizescale field=""/>
  </renderer-v2>
  <customproperties/>
  <displayfield>gid</displayfield>
  <label>1</label>
  <labelfield>BETREIBER</labelfield>
  <labelattributes>
    <label fieldname="BETREIBER" text="Beschriftung"/>
    <family fieldname="" name="Cantarell"/>
    <size fieldname="" units="pt" value="12"/>
    <bold fieldname="" on="0"/>
    <italic fieldname="" on="0"/>
    <underline fieldname="" on="0"/>
    <strikeout fieldname="" on="0"/>
    <color fieldname="" red="0" blue="0" green="0"/>
    <x fieldname=""/>
    <y fieldname=""/>
    <offset x="0" y="0" units="pt" yfieldname="" xfieldname=""/>
    <angle fieldname="" value="0" auto="0"/>
    <alignment fieldname="" value="aboveleft"/>
    <buffercolor fieldname="" red="255" blue="255" green="255"/>
    <buffersize fieldname="" units="pt" value="2"/>
    <bufferenabled fieldname="" on="1"/>
    <multilineenabled fieldname="" on=""/>
    <selectedonly on=""/>
  </labelattributes>
  <edittypes>
    <edittype type="0" name="BAUJAHR"/>
    <edittype type="0" name="BESCHRIEB"/>
    <edittype type="0" name="BETREIBER"/>
    <edittype type="0" name="DESCRIPTIO"/>
    <edittype type="0" name="DRUCK"/>
    <edittype type="0" name="D_IN_ZOLL"/>
    <edittype type="0" name="LAGEGEN"/>
    <edittype type="0" name="LAGEGENTYP"/>
    <edittype type="0" name="LEITUNG_NR"/>
    <edittype type="0" name="NAME"/>
    <edittype type="0" name="OBJECTID"/>
    <edittype type="0" name="OBJECTID_1"/>
    <edittype type="0" name="VERLEGUNG"/>
    <edittype type="0" name="gid"/>
  </edittypes>
  <editform></editform>
  <editforminit></editforminit>
  <annotationform></annotationform>
  <attributeactions/>
  <overlay display="false" type="diagram">
    <renderer item_interpretation="linear">
      <diagramitem size="0" value="0"/>
      <diagramitem size="0" value="0"/>
    </renderer>
    <factory sizeUnits="MM" type="Pie">
      <wellknownname>Pie</wellknownname>
      <classificationfield>0</classificationfield>
    </factory>
    <scalingAttribute>0</scalingAttribute>
  </overlay>
</qgis>
