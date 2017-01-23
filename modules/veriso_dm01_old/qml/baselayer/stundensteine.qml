<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="1.8.0-Lisboa" minimumScale="0" maximumScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <transparencyLevelInt>255</transparencyLevelInt>
  <renderer-v2 symbollevels="0" type="singleSymbol">
    <symbols>
      <symbol outputUnit="MM" alpha="1" type="marker" name="0">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="85,0,255,255"/>
          <prop k="color_border" v="0,0,127,255"/>
          <prop k="name" v="diamond"/>
          <prop k="offset" v="0,0"/>
          <prop k="size" v="3"/>
        </layer>
      </symbol>
    </symbols>
    <rotation field=""/>
    <sizescale field=""/>
  </renderer-v2>
  <customproperties/>
  <displayfield>gid</displayfield>
  <label>0</label>
  <labelattributes>
    <label fieldname="" text="Beschriftung"/>
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
    <alignment fieldname="" value="center"/>
    <buffercolor fieldname="" red="255" blue="255" green="255"/>
    <buffersize fieldname="" units="pt" value="1"/>
    <bufferenabled fieldname="" on=""/>
    <multilineenabled fieldname="" on=""/>
    <selectedonly on=""/>
  </labelattributes>
  <edittypes>
    <edittype type="0" name="GEMEINDEN"/>
    <edittype type="0" name="OBJECTID"/>
    <edittype type="0" name="PKT_NR"/>
    <edittype type="0" name="URL"/>
    <edittype type="0" name="X_KOORD"/>
    <edittype type="0" name="Y_KOORD"/>
    <edittype type="0" name="gemeinden"/>
    <edittype type="0" name="gid"/>
    <edittype type="0" name="objectid"/>
    <edittype type="0" name="pkt_nr"/>
    <edittype type="0" name="url"/>
    <edittype type="0" name="x_koord"/>
    <edittype type="0" name="y_koord"/>
  </edittypes>
  <editform></editform>
  <editforminit></editforminit>
  <annotationform></annotationform>
  <attributeactions>
    <actionsetting action="[% &quot;url&quot; %]" capture="0" type="5" name="Websuche nach dem Attributwert durchführen"/>
    <actionsetting action="http://www.google.it/?q=[% &quot;ATTRIBUTE&quot; %]" capture="0" type="5" name="Websuche nach dem Attributwert durchführen"/>
    <actionsetting action="echo &quot;[% &quot;MY_FIELD&quot; %]&quot;" capture="1" type="0" name="Attributwert anzeigen"/>
    <actionsetting action="ogr2ogr -f &quot;ESRI Shapefile&quot; &quot;[% &quot;OUTPUT_PATH&quot; %]&quot; &quot;[% &quot;INPUT_FILE&quot; %]&quot;" capture="1" type="0" name="Eine Applikation ausführen"/>
    <actionsetting action="QtGui.QMessageBox.information(None, &quot;Feature id&quot;, &quot;feature id is [% $id %]&quot;)" capture="0" type="1" name="Objektkennung bestimmen"/>
    <actionsetting action="QtGui.QMessageBox.information(None, &quot;Current field's value&quot;, &quot;[% $currentfield %]&quot;)" capture="0" type="1" name="Gewählter Feldwert (Werkzeug &quot;Objekte abfragen&quot;)"/>
    <actionsetting action="QtGui.QMessageBox.information(None, &quot;Clicked coords&quot;, &quot;layer: [% $layerid %]\ncoords: ([% $clickx %],[% $clickx %])&quot;)" capture="0" type="1" name="Angeklickte Koordinate (Werkzeug &quot;Objektaktion ausführen&quot;)"/>
    <actionsetting action="[% &quot;PATH&quot; %]" capture="0" type="5" name="Datei öffnen"/>
  </attributeactions>
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
