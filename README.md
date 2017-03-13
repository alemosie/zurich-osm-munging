# Wrangle OpenStreetMap Data: Zurich, Switzerland

Note: complete data files (both source `.osm` and sanitized `.json`) have been added to .gitignore to prevent slowness and bloating on GitHub. Sample source and sanitized data can be found in the `extracts` folder of this repository.

## Source data

![Zurich OSM](images/zurich_map.png)

The OpenStreetMap (OSM) extract for Zurich, Switzerland contains covers the city center and surrounding suburbs, and contains data on establishments, transportation systems, points of interest and more for the area. The **[OSM XML dataset from MapZen](https://mapzen.com/data/metro-extracts/metro/zurich_switzerland/) is 614.7 MB**.

In accordance with the OSM XML API, the data consists of three main types of elements:

- Nodes
- Ways
- Relations

In the sanitization process, all three types of elements are accounted for.

### XML parsing challenges

#### Domain & language knowledge

I chose to parse Zurich data because of an interest in the city, not a personal connection. Having never visited or lived the city and not knowing German, I was initially lacking knowledge to audit tag values.

Because of special characters in German (e.g. umlaut), I needed to familiarize myself with [Python's handling of unicode](https://docs.python.org/2/howto/unicode.html).

#### Tag key separators

OSM records level of specificity in the key values in tags. In the json conversion process, it made the most sense to nest these attributes together, but the approach had to differ based on the tag. For the purposes of this exercise, I only processed two-tiered keys (one separator), and disregarded three-tiered keys.

Two-tier key types & conversions:
```
<tag k="addr:street" v="Bülach" />
<tag k="addr:street" v="Spitalstrasse" />

# converted to:
"addr": {
  "city": "Bülach",
  "street": "Spitalstrasse"
}
```
```
<tag k="wheelchair" v="limited"/>
<tag k="wheelchair:description" v="rund 50% der Fahrzeuge verkehren mit Niederflur-Einstieg"/>

# converted to:
"wheelchair": {
  "description": "rund 50% der Fahrzeuge verkehren mit Niederflur-Einstieg",
  "base_value": "limited"
}
```
```
<tag k="maxspeed" v="100"/>
<tag k="source:maxspeed" v="sign"/>

# converted to:
"maxspeed": {
  "source": "sign",
  "base_value": "100"
}
```

Also, some separators departed from the standard `:` separator, and had ".", like `surface.material`.  

#### Tag value separators

Because of a lack of domain knowledge, I had to conduct research on data found in the sample to ensure that I had the necessary context to handle the data correctly. Take the following XML:

```
<tag k="destination" v="Bern;Chur;Luzern;Flughafen;Nordring-Zürich"/>
<tag k="source:maxspeed" v="sign"/>
<tag k="destination:symbol" v="airport"/>
...
<tag k="name" v="Salomon-Bleuler-Weg"/>
<tag k="highway" v="residential"/>
<tag k="maxspeed" v="30"/>
...
<tag k="bus:lanes" v="no|designated" />
```

`;`, `-`, and "|" all potentially act as separators.

The first portion with `"Bern;Chur;Luzern;Flughafen;Nordring-Zürich"` is meant to be separated, as all of those are towns/cities in Switzerland. The third is also a clear separator. Values are converted to `["Bern","Chur","Luzern","Flughafen","Nordring-Zürich"]` and `["no", "designated"]`.

Searches for `"Salomon-Bleuler-Weg"` on [other maps](https://www.google.com/maps/place/Salomon-Bleuler-Weg,+8400+Winterthur,+Switzerland/@47.4916183,8.7383565,18z/data=!4m5!3m4!1s0x479a9997ae1936e5:0xb2db2c6fd90d87eb!8m2!3d47.4915712!4d8.7395501), however, confirm that the value is indeed the full name of the street.

![Salomon-Bleuler-Weg](images/sbw.png)



## Resources

- [OSM XML API Wiki](http://wiki.openstreetmap.org/wiki/OSM_XML#Contents)
- [Elementtree API](https://docs.python.org/2/library/xml.etree.elementtree.html)
- [Unicode & Python](https://docs.python.org/2/howto/unicode.html)
- [Permutations for "street" in German](http://www.acronymfinder.com/Stra%C3%9Fe-\(German%3A-Street\)-\(STR\).html)
