# MISP Extensions for STIX 2.1

## Version 1.0.0

### 12 November 2026

#### Editors:

Christian Studer (<christian.studer@circl.lu>), [CIRCL](https://www.circl.lu/)

#### Related work:

This specification is related to:

- *STIX Version 2.1.* Edited by Bret Jordan, Rich Piazza, and Trey Darley. Latest stage: <https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html>.
- *MISP-STIX converter (misp-stix).* MISP Project. Latest version: <https://github.com/MISP/misp-stix>.
- *MISP Open Source Threat Intelligence and Sharing Platform.* MISP Project. <https://www.misp-project.org/>.

#### Abstract:

The MISP Extensions carry in STIX 2.1 the MISP \[[MISP](#misp)\] content that no standard STIX object or property holds: the MISP attributes, objects and galaxy clusters no standard STIX object represents, and, on standard STIX objects, the MISP values their standard properties leave over. The MISP-STIX converter \[[misp-stix](#misp-stix)\] writes them in its STIX 2.1 export and reads them back in its import, so a MISP event goes through STIX 2.1 and back to MISP whole.

This document describes the four extension definitions, following the STIX Extension Definition Policy \[[STIX-Extension-Policy](#stix-extension-policy)\] section 3.3. The JSON schemas in this directory are their normative definition; where this document and a schema disagree, the schema wins.

#### Key words:

The key words "**MUST**", "**MUST NOT**", "**REQUIRED**", "**SHALL**", "**SHALL NOT**", "**SHOULD**", "**SHOULD NOT**", "**RECOMMENDED**", "**NOT RECOMMENDED**", "**MAY**", and "**OPTIONAL**" in this document are to be interpreted as described in BCP 14 \[[RFC2119](#rfc2119)\] \[[RFC8174](#rfc8174)\] when, and only when, they appear in all capitals, as shown here.

---

# Table of Contents

- 1. [Introduction](#introduction)
  - 1.1 [Document Conventions](#document-conventions)
  - 1.2 [Overview](#overview)
  - 1.3 [Directory Layout](#directory-layout)
- 2. [MISP Property Extension](#misp-property-extension)
  - 2.1 [Properties](#misp-property-extension-properties)
  - 2.2 [Extension Property Names](#extension-property-names)
  - 2.3 [Values](#values)
  - 2.4 [Original Names](#original-names)
  - 2.5 [Nested Rooms](#nested-rooms)
  - 2.6 [Patterns](#patterns)
- 3. [MISP Attribute Extension](#misp-attribute-extension)
  - 3.1 [Properties](#misp-attribute-properties)
  - 3.2 [Relationships](#misp-attribute-relationships)
- 4. [MISP Object Extension](#misp-object-extension)
  - 4.1 [Properties](#misp-object-properties)
  - 4.2 [MISP Object Attribute Type](#misp-object-attribute-type)
  - 4.3 [Relationships](#misp-object-relationships)
- 5. [MISP Galaxy Cluster Extension](#misp-galaxy-cluster-extension)
  - 5.1 [Properties](#misp-galaxy-cluster-properties)
  - 5.2 [Relationships](#misp-galaxy-cluster-relationships)
- 6. [Bundles](#bundles)
- 7. [Conformance Notes](#conformance-notes)
  - 7.1 [The Property Extension's First Schema File Refers to No Base Type](#the-property-extensions-first-schema-file-refers-to-no-base-type)
  - 7.2 [The Schema Does Not Tie a Nested Room to Its Type](#the-schema-does-not-tie-a-nested-room-to-its-type)
  - 7.3 [No External References](#no-external-references)
  - 7.4 [An Empty Registry Value](#an-empty-registry-value)
- 8. [Examples](#examples)
- Appendix A: [The Custom Syntax](#the-custom-syntax)
- Appendix B: [References](#references)
  - B.1 [Normative References](#normative-references)
  - B.2 [Informative References](#informative-references)

---

# 1. Introduction <a id="introduction"></a>

## 1.1 Document Conventions <a id="document-conventions"></a>

The following color, font and font style conventions are used in this document:

- The Consolas font is used for all type names, property names and literals.
  - type names are in red with a light red background – <span class="stixtype">misp-attribute</span>
  - property names are in bold style – **attribute_type**
  - literals (values) are in blue with a blue background – <span class="stixliteral">property-extension</span>
  - All relationship types are string literals; therefore, they will also appear in blue with a blue background – <span class="stixliteral">related-to</span>
- All examples in this document are expressed in JSON. They are in `mono` font, with straight quotes, black text and a light grey background, and using 2-space indentation. JSON examples in this document are representations of JSON objects. They should not be interpreted as string literals. The ordering of object keys is insignificant. Whitespace before or after JSON structural characters in the examples are insignificant.
- Parts of the example may be omitted for conciseness and clarity. These omitted parts are denoted with the ellipses (...).

The property types are the STIX 2.1 data types (\[[STIX-v2.1](#stix-v2.1)\] section 2), plus the types this document defines: <span class="stixtype">misp-value-type</span> in [section 2.3](#values) and <span class="stixtype">misp-object-attribute-type</span> in [section 4.2](#misp-object-attribute-type). Section numbers following \[[STIX-v2.1](#stix-v2.1)\] refer to the STIX Version 2.1 specification.

## 1.2 Overview <a id="overview"></a>

There are four MISP Extensions, one per kind of MISP content:

<table border="1" cellspacing="0" cellpadding="6" width="100%">
  <tr>
    <th><span class="stixtr">Name</span></th>
    <th><span class="stixtr">Extension type</span></th>
    <th><span class="stixtr">Extension definition id</span></th>
    <th><span class="stixtr">Schema</span></th>
  </tr>
  <tr>
    <td>MISP Attribute Extension</td>
    <td><span class="stixliteral">new-sdo</span></td>
    <td><span class="stixliteral">extension-definition--c1f2c0fa-3786-4f27-bf57-cf050ecfc104</span></td>
    <td><a href="misp-attribute/extension-definition--c1f2c0fa-3786-4f27-bf57-cf050ecfc104.json"><code>misp-attribute/...</code></a></td>
  </tr>
  <tr>
    <td>MISP Object Extension</td>
    <td><span class="stixliteral">new-sdo</span></td>
    <td><span class="stixliteral">extension-definition--a093107b-933f-4d72-a9a6-6d7318adadda</span></td>
    <td><a href="misp-object/extension-definition--a093107b-933f-4d72-a9a6-6d7318adadda.json"><code>misp-object/...</code></a></td>
  </tr>
  <tr>
    <td>MISP Galaxy Cluster Extension</td>
    <td><span class="stixliteral">new-sdo</span></td>
    <td><span class="stixliteral">extension-definition--573a76d8-f8a0-4f53-bc93-f2777576b7b9</span></td>
    <td><a href="misp-galaxy-cluster/extension-definition--573a76d8-f8a0-4f53-bc93-f2777576b7b9.json"><code>misp-galaxy-cluster/...</code></a></td>
  </tr>
  <tr>
    <td>MISP Property Extension</td>
    <td><span class="stixliteral">property-extension</span></td>
    <td><span class="stixliteral">extension-definition--5ece67ea-2e8b-4ed0-bb69-26d69053ee0b</span></td>
    <td><a href="extension-definition--5ece67ea-2e8b-4ed0-bb69-26d69053ee0b.json">first file</a>, <a href="misp-property-extension.json">body</a></td>
  </tr>
</table>

The three <span class="stixliteral">new-sdo</span> extensions each define one object type, <span class="stixtype">misp-attribute</span>, <span class="stixtype">misp-object</span> and <span class="stixtype">misp-galaxy-cluster</span>. The property extension is one extension shared by every standard STIX object type MISP extends: SDOs such as <span class="stixtype">attack-pattern</span>, <span class="stixtype">location</span>, <span class="stixtype">malware</span> or <span class="stixtype">threat-actor</span>, SCOs such as <span class="stixtype">file</span>, <span class="stixtype">url</span> or <span class="stixtype">windows-registry-key</span>, and <span class="stixtype">indicator</span>, <span class="stixtype">note</span> and <span class="stixtype">opinion</span>.

The four extension definitions are created by the MISP Project identity:

```JSON
{
  "type": "identity",
  "spec_version": "2.1",
  "id": "identity--55f6ea65-aa10-4c5a-bf01-4f84950d210f",
  "created": "2015-09-14T15:40:21.000Z",
  "modified": "2015-09-14T15:40:21.000Z",
  "name": "MISP",
  "identity_class": "organization"
}
```

Each extension definition has a **version** of its own, following semantic versioning, raised when its schema changes. This document describes version 1.0.0 of all four. This repository, `oasis-open/cti-stix-common-objects`, is the canonical home of the extension definition objects and of their schemas: the extension definition objects are published in [`objects/extension-definition/`](../../objects/extension-definition/), and the schemas in this directory. The MISP-STIX converter \[[misp-stix](#misp-stix)\] packages this identity, and copies of the extension definition objects and of their schemas; where a copy differs, this repository wins.

The MISP labels (<span class="stixliteral">misp:type="..."</span>, <span class="stixliteral">misp:category="..."</span>, <span class="stixliteral">misp:name="..."</span>, <span class="stixliteral">misp:galaxy-name="..."</span>, ...) are standard **labels**, and are not part of the MISP Extensions.

## 1.3 Directory Layout <a id="directory-layout"></a>

<table border="1" cellspacing="0" cellpadding="6" width="100%">
  <tr>
    <th><span class="stixtr">Path</span></th>
    <th><span class="stixtr">Content</span></th>
  </tr>
  <tr>
    <td><code>extension-definition--5ece67ea-2e8b-4ed0-bb69-26d69053ee0b.json</code></td>
    <td>The property extension's first schema file</td>
  </tr>
  <tr>
    <td><code>misp-property-extension.json</code></td>
    <td>The property extension's body</td>
  </tr>
  <tr>
    <td><code>misp-attribute/</code>, <code>misp-object/</code>, <code>misp-galaxy-cluster/</code></td>
    <td>The schema of each <span class="stixliteral">new-sdo</span> type</td>
  </tr>
  <tr>
    <td><code>examples/</code></td>
    <td>Bundles using the extensions (<a href="#examples">section 8</a>)</td>
  </tr>
  <tr>
    <td><code>STIX-2.1-MISP-Extensions.md</code></td>
    <td>This document</td>
  </tr>
</table>

The first schema file of each extension is named after its extension definition id, so the STIX validator finds them all when given this directory: `stix2_validator --schemas <this directory>`. The schemas refer to the STIX 2.1 base schemas (`core.json`, `timestamp.json`, `binary.json`) by their published URLs.

# 2. MISP Property Extension <a id="misp-property-extension"></a>

The key for this extension when used in the **extensions** dictionary **MUST** be <span class="stixliteral">extension-definition--5ece67ea-2e8b-4ed0-bb69-26d69053ee0b</span>.

The MISP Property Extension holds the MISP values a standard STIX object has no property for:

- on an object coming from a MISP object, the values of the object relations its standard properties leave over;
- on an object coming from a galaxy cluster \[[MISP-Galaxy](#misp-galaxy)\], the cluster meta values its standard properties leave over;
- a few MISP fields with a name of their own ([section 2.1](#misp-property-extension-properties));
- the values of the MISP objects nested in a STIX structure, in the **Nested Rooms** ([section 2.5](#nested-rooms)).

An object comes either from a MISP object or from a galaxy cluster, so object relations and meta keys never meet on one object. The MISP-STIX converter writes the extension only on an object holding at least one MISP value, next to the object's predefined extensions (<span class="stixtype">windows-pebinary-ext</span>, <span class="stixtype">socket-ext</span>, ...):

```JSON
{
  ...
  "extensions": {
    "windows-pebinary-ext": {
      "pe_type": "exe",
      "sections": [
        {
          "name": ".rsrc"
        },
        {
          "name": ".text"
        }
      ]
    },
    "extension-definition--5ece67ea-2e8b-4ed0-bb69-26d69053ee0b": {
      "extension_type": "property-extension",
      "entropy": "1.234",
      "windows_pebinary_ext": {
        "lang_id": "080904B0",
        "sections": {
          "1": {
            "text": "Code section"
          }
        }
      }
    }
  }
}
```

## 2.1 Properties <a id="misp-property-extension-properties"></a>

<table border="1" cellspacing="0" cellpadding="6">
  <tr>
    <th><span class="stixtr">Property Name</span></th>
    <th><span class="stixtr">Type</span></th>
    <th><span class="stixtr">Description</span></th>
  </tr>
  <tr>
    <td><strong>extension_type</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The value of this property <strong>MUST</strong> be <span class="stixliteral">property-extension</span>.</td>
  </tr>
  <tr>
    <td><strong>opinion</strong> (optional)</td>
    <td><span class="stixtype">integer</span></td>
    <td>On an <span class="stixtype">opinion</span>: the MISP analyst opinion, from 0 to 100, which the STIX <strong>opinion</strong> property rounds to its enumeration.</td>
  </tr>
  <tr>
    <td><strong>author_ref</strong> (optional)</td>
    <td><span class="stixtype">identifier</span></td>
    <td>On the <span class="stixtype">opinion</span> standing for a MISP false positive sighting: the identity of the organisation reporting it. The value <strong>MUST</strong> be an <span class="stixtype">identity</span> identifier.</td>
  </tr>
  <tr>
    <td><strong>attachment</strong> (optional)</td>
    <td><span class="stixtype">misp-value-type</span></td>
    <td>The values of MISP <span class="stixliteral">attachment</span> attributes no standard property holds, each with its data where it has some.</td>
  </tr>
  <tr>
    <td><strong>filename</strong> (optional)</td>
    <td><span class="stixtype">misp-value-type</span></td>
    <td>On an <span class="stixtype">artifact</span>: the name of the file whose content <strong>payload_bin</strong> holds, a MISP attachment or malware sample. The MISP-STIX converter writes one <span class="stixtype">string</span>.</td>
  </tr>
  <tr>
    <td><strong>url</strong> (optional)</td>
    <td><span class="stixtype">misp-value-type</span></td>
    <td>On an <span class="stixtype">artifact</span> holding an image: the image URL, which STIX 2.1 does not allow next to <strong>payload_bin</strong>. The MISP-STIX converter writes one <span class="stixtype">string</span>.</td>
  </tr>
  <tr>
    <td><strong>malware_sample</strong> (optional)</td>
    <td><span class="stixtype">misp-value-type</span></td>
    <td>The value of a MISP <span class="stixliteral">malware-sample</span> attribute, <span class="stixalt"><em>file name</em>|<em>MD5</em></span>, kept whole where no standard property holds it. The MISP-STIX converter writes one <span class="stixtype">string</span>.</td>
  </tr>
  <tr>
    <td><strong>original_names</strong> (optional)</td>
    <td><span class="stixtype">dictionary</span></td>
    <td>The spellings of the galaxy cluster meta keys the naming changed (<a href="#original-names">section 2.4</a>).</td>
  </tr>
  <tr>
    <td><strong>windows_pebinary_ext</strong> (optional)</td>
    <td><span class="stixtype">dictionary</span></td>
    <td>The Nested Room of the <span class="stixtype">windows-pebinary-ext</span> extension (<a href="#nested-rooms">section 2.5</a>).</td>
  </tr>
  <tr>
    <td><strong>values</strong> (optional)</td>
    <td><span class="stixtype">dictionary</span></td>
    <td>The Nested Room of the <strong>values</strong> of a <span class="stixtype">windows-registry-key</span> (<a href="#nested-rooms">section 2.5</a>).</td>
  </tr>
  <tr>
    <td><em>any other name</em> (optional)</td>
    <td><span class="stixtype">misp-value-type</span></td>
    <td>The values of one MISP object relation or galaxy cluster meta key, under its Extension Property Name (<a href="#extension-property-names">section 2.2</a>).</td>
  </tr>
</table>

The names in this table are the fixed names of the extension. Any other name **MUST** match `^[a-z][a-z0-9_]{2,249}$`. Each level of the extension is closed: a property not listed here and not matching the pattern is invalid.

## 2.2 Extension Property Names <a id="extension-property-names"></a>

A MISP object relation or galaxy cluster meta key is written under its Extension Property Name:

1. The relation or key is lowercased, and every character outside `a`-`z`, `0`-`9` and `_` is turned into `_`: <span class="stixliteral">KnownMalicious</span> gives **knownmalicious**, <span class="stixliteral">cfr-type-of-incident</span> gives **cfr_type_of_incident**.
2. The result is escaped where it cannot be used as it is:
   - shorter than three characters, not starting with a letter, or one of the names the extension uses for itself (**extension_type**, **original_names**, **windows_pebinary_ext**, **sections**, **values**): it takes the prefix `misp_`. <span class="stixliteral">ip</span> gives **misp_ip**, <span class="stixliteral">2fa-device-ip</span> gives **misp_2fa_device_ip**;
   - ending with `_hex` or `_bin`, which the STIX 2.1 base schema types as hexadecimal and binary: it takes a trailing `_`. <span class="stixliteral">origin:Temp.Hex</span> gives **origin_temp_hex_**;
   - when both apply, the prefix comes first, then the trailing `_`.

The six MISP fields of [section 2.1](#misp-property-extension-properties), **opinion**, **author_ref**, **attachment**, **filename**, **url** and **malware_sample**, keep their names, with no fold and no escape: a relation folding to one of them is that MISP field. A relation folding to **extension_type**, **original_names**, **windows_pebinary_ext**, **sections** or **values** is escaped.

A consumer reads a name back by removing its escape: a trailing `_` after `_hex` or `_bin`, then a `misp_` prefix when the rest would itself be escaped (**misp_ip** gives <span class="stixliteral">ip</span>, **misp_uuid** stays). The MISP-STIX import then restores the spelling of an object relation from the MISP object template \[[MISP-Objects](#misp-objects)\] named by the object's <span class="stixliteral">misp:name</span> label, and the spelling of a meta key from **original_names**.

When two values of one object land on one name, the last one is kept, and the MISP-STIX converter reports the other one lost.

## 2.3 Values <a id="values"></a>

**Type Name:** <span class="stixtype">misp-value-type</span>

A value, of type <span class="stixtype">misp-value-type</span>, is one item, or a <span class="stixtype">list</span> of at least two items:

- one value is written as the item itself, two or more as a list;
- an item is a <span class="stixtype">string</span>, a <span class="stixtype">boolean</span>, or a <span class="stixtype">dictionary</span> with exactly two properties, **value** (<span class="stixtype">string</span>) and **data** (<span class="stixtype">binary</span>), for a MISP attribute carrying a payload;
- a list **MAY** mix items with and without **data**.

Galaxy cluster meta values are strings. MISP holds every meta value as a list: a meta key with one value is written as a <span class="stixtype">string</span>, and a meta key with no value is not written.

## 2.4 Original Names <a id="original-names"></a>

**original_names** maps the Extension Property Name of a galaxy cluster meta key to the key as MISP spells it, for every meta key the naming of [section 2.2](#extension-property-names) changed:

```JSON
{
  ...
  "extensions": {
    "extension-definition--5ece67ea-2e8b-4ed0-bb69-26d69053ee0b": {
      "extension_type": "property-extension",
      "capital": "Stockholm",
      "iso3": "SWE",
      "tld": ".se",
      "original_names": {
        "capital": "Capital",
        "iso3": "ISO3"
      }
    }
  }
}
```

- It is written only when the naming changed at least one meta key of the object, and then lists every name it changed: a meta key it does not list is spelled as its name (**tld** above).
- It **MUST** hold at least one entry, and each key **MUST** match `^[a-z][a-z0-9_]{2,249}$`.
- An entry naming no property of the object is ignored.
- Object relations get no entry: the MISP object template gives their spelling back.

## 2.5 Nested Rooms <a id="nested-rooms"></a>

STIX 2.1 defines **extensions** at the top level of an object only (\[[STIX-v2.1](#stix-v2.1)\] section 3.2), and gives no custom key a place inside a predefined extension, a PE section or a registry value. A MISP object nested in such a STIX structure keeps its values in a room of the property extension that mirrors that structure:

<table border="1" cellspacing="0" cellpadding="6" width="100%">
  <tr>
    <th><span class="stixtr">Room</span></th>
    <th><span class="stixtr">On</span></th>
    <th><span class="stixtr">Holds the values of</span></th>
    <th><span class="stixtr">Mirrors</span></th>
  </tr>
  <tr>
    <td><strong>windows_pebinary_ext</strong></td>
    <td><span class="stixtype">file</span></td>
    <td>the MISP <span class="stixliteral">pe</span> object</td>
    <td>the <span class="stixtype">windows-pebinary-ext</span> extension</td>
  </tr>
  <tr>
    <td><strong>windows_pebinary_ext</strong>.<strong>sections</strong></td>
    <td><span class="stixtype">file</span></td>
    <td>the MISP <span class="stixliteral">pe-section</span> objects</td>
    <td>its <strong>sections</strong></td>
  </tr>
  <tr>
    <td><strong>values</strong></td>
    <td><span class="stixtype">windows-registry-key</span></td>
    <td>the MISP <span class="stixliteral">registry-key-value</span> objects</td>
    <td>its <strong>values</strong></td>
  </tr>
</table>

- A room holds Extension Property Names and values, as the top level does. **windows_pebinary_ext** holds **sections**; nothing else holds a room.
- A room standing for a STIX list (**sections**, **values**) is a <span class="stixtype">dictionary</span> keyed by the zero-based position of the STIX list's items, in decimal: its key <span class="stixalt">"*n*"</span> holds the values of the MISP object that the STIX list's item <span class="stixalt">*n*</span> stands for. Each key **MUST** match `^(0|[1-9][0-9]*)$`, so that a position has one spelling, and name an item of the STIX list.
- A list room holds only the items with values, its keys in ascending order: an item holding none has no key, and **MUST NOT** be written as <span class="stixliteral">{}</span>. A list room with no item is left out: it **MUST** hold at least one key. **windows_pebinary_ext** is left out when nothing is left in it: it **MUST NOT** be empty.
- A MISP <span class="stixliteral">registry-key-value</span> holding only values STIX has no property for keeps its item in the key's **values**, as <span class="stixliteral">{}</span>, so that its position holds ([section 7.4](#an-empty-registry-value)):

```JSON
{
  ...
  "values": [
    {
      "name": "Foo",
      "data": "qwerty",
      "data_type": "REG_SZ"
    },
    {}
  ],
  "extensions": {
    "extension-definition--5ece67ea-2e8b-4ed0-bb69-26d69053ee0b": {
      "extension_type": "property-extension",
      "values": {
        "1": {
          "benign": "Known to be legitimate"
        }
      }
    }
  }
}
```

- The values of the MISP <span class="stixliteral">registry-key</span> object itself stay at the top level of the extension. So does a second **data** value of that object.

## 2.6 Patterns <a id="patterns"></a>

On a standard object, an Indicator's pattern is the only place a MISP value's **to_ids** flag, its detection-ready mark, travels. An Indicator compares a MISP value where the observable holds it, through the object path of the property extension (\[[STIX-v2.1](#stix-v2.1)\] section 9.7):

<table border="1" cellspacing="0" cellpadding="6" width="100%">
  <tr>
    <th><span class="stixtr">Where the observable holds the value</span></th>
    <th><span class="stixtr">Object path</span></th>
  </tr>
  <tr>
    <td>In the property extension</td>
    <td><code>url:extensions.'extension-definition--5ece67ea-2e8b-4ed0-bb69-26d69053ee0b'.misp_ip</code></td>
  </tr>
  <tr>
    <td>Behind a reference</td>
    <td><code>file:content_ref.extensions.'extension-definition--5ece67ea-2e8b-4ed0-bb69-26d69053ee0b'.filename</code></td>
  </tr>
  <tr>
    <td>In <strong>windows_pebinary_ext</strong></td>
    <td><code>file:extensions.'extension-definition--5ece67ea-2e8b-4ed0-bb69-26d69053ee0b'.windows_pebinary_ext.lang_id</code></td>
  </tr>
  <tr>
    <td>In <strong>sections</strong></td>
    <td><code>file:extensions.'extension-definition--5ece67ea-2e8b-4ed0-bb69-26d69053ee0b'.windows_pebinary_ext.sections.'1'.text</code></td>
  </tr>
  <tr>
    <td>In <strong>values</strong></td>
    <td><code>windows-registry-key:extensions.'extension-definition--5ece67ea-2e8b-4ed0-bb69-26d69053ee0b'.values.'0'.benign</code></td>
  </tr>
</table>

- The extension definition id and the room keys are quoted, a room key since it starts with a digit; the names are not.
- A value the room item holds in a list keeps its `[*]` behind the key: `....sections.'1'.text[*] = 'a'`.
- A value the observable holds in a list is compared through `[*]`: a relation holding <span class="stixliteral">a</span>, <span class="stixliteral">b</span> and <span class="stixliteral">c</span>, of which <span class="stixliteral">a</span> and <span class="stixliteral">c</span> are flagged, gives `....text[*] = 'a' AND ....text[*] = 'c'`.
- A value with data is compared twice, on its **data**, then on its **value**: `....user_avatar.data = '...' AND ....user_avatar.value = 'avatar.png'`. Under `[*]`, the two comparisons **MAY** match two different items of the list.
- The process parent's values are compared behind **parent_ref**, under the name of the relation with its `parent-` removed: `process:parent_ref.extensions.'...'.process_name`.
- A comparison on a property of the extension matches only an observation carrying the extension.

**Examples**

*A URL holding the values of its MISP object that no standard property holds, among which the escaped misp_ip*

```JSON
{
  "type": "url",
  "spec_version": "2.1",
  "id": "url--5ac347ca-dac4-4562-9775-04120a00020f",
  "value": "https://www.circl.lu/team",
  "extensions": {
    "extension-definition--5ece67ea-2e8b-4ed0-bb69-26d69053ee0b": {
      "extension_type": "property-extension",
      "domain": "circl.lu",
      "host": "www.circl.lu",
      "misp_ip": "149.13.33.14",
      "port": "443"
    }
  }
}
```

# 3. MISP Attribute Extension <a id="misp-attribute-extension"></a>

**Type Name:** <span class="stixtype">misp-attribute</span>

The **extensions** property of a <span class="stixtype">misp-attribute</span> **MUST** hold its extension definition id, <span class="stixliteral">extension-definition--c1f2c0fa-3786-4f27-bf57-cf050ecfc104</span>, with **extension_type** <span class="stixliteral">new-sdo</span>.

A MISP attribute no standard STIX object represents: an attribute type the converter maps to no STIX object (<span class="stixliteral">btc</span>, <span class="stixliteral">iban</span>, ...), an attribute not flagged for detection that holds too little for an observable (<span class="stixliteral">port</span>, <span class="stixliteral">size-in-bytes</span>, ...), or a <span class="stixliteral">malware-sample</span> whose MD5 is not valid. Its **id** carries the uuid of the MISP attribute.

## 3.1 Properties <a id="misp-attribute-properties"></a>

<table border="1" cellspacing="0" cellpadding="6" width="100%">
  <tr>
    <th><span class="stixtr">Required Common Properties</span></th>
  </tr>
  <tr>
    <td><strong>type</strong>, <strong>spec_version</strong>, <strong>id</strong>, <strong>created</strong>, <strong>modified</strong>, <strong>extensions</strong></td>
  </tr>
  <tr>
    <th><span class="stixtr">Optional Common Properties</span></th>
  </tr>
  <tr>
    <td><strong>created_by_ref</strong>, <strong>revoked</strong>, <strong>labels</strong>, <strong>confidence</strong>, <strong>lang</strong>, <strong>external_references</strong>, <strong>object_marking_refs</strong>, <strong>granular_markings</strong></td>
  </tr>
  <tr>
    <th><span class="stixtr">Not Applicable Common Properties</span></th>
  </tr>
  <tr>
    <td><strong>defanged</strong></td>
  </tr>
  <tr>
    <th><span class="stixtr">MISP Attribute Specific Properties</span></th>
  </tr>
  <tr>
    <td><strong>attribute_type</strong>, <strong>value</strong>, <strong>category</strong>, <strong>comment</strong>, <strong>to_ids</strong>, <strong>first_seen</strong>, <strong>last_seen</strong>, <strong>data</strong></td>
  </tr>
</table>

<table border="1" cellspacing="0" cellpadding="6">
  <tr>
    <th><span class="stixtr">Property Name</span></th>
    <th><span class="stixtr">Type</span></th>
    <th><span class="stixtr">Description</span></th>
  </tr>
  <tr>
    <td><strong>type</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The value of this property <strong>MUST</strong> be <span class="stixliteral">misp-attribute</span>.</td>
  </tr>
  <tr>
    <td><strong>extensions</strong> (required)</td>
    <td><span class="stixtype">dictionary</span></td>
    <td><strong>MUST</strong> hold <span class="stixliteral">extension-definition--c1f2c0fa-3786-4f27-bf57-cf050ecfc104</span>, whose value is <span class="stixliteral">{"extension_type": "new-sdo"}</span>.</td>
  </tr>
  <tr>
    <td><strong>attribute_type</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The MISP attribute type, such as <span class="stixliteral">btc</span>. Named so since <strong>type</strong> is the STIX type.</td>
  </tr>
  <tr>
    <td><strong>value</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The attribute value.</td>
  </tr>
  <tr>
    <td><strong>category</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The MISP category, such as <span class="stixliteral">Financial fraud</span>.</td>
  </tr>
  <tr>
    <td><strong>comment</strong> (optional)</td>
    <td><span class="stixtype">string</span></td>
    <td>The attribute comment.</td>
  </tr>
  <tr>
    <td><strong>to_ids</strong> (required)</td>
    <td><span class="stixtype">boolean</span></td>
    <td>Whether the attribute is flagged for detection.</td>
  </tr>
  <tr>
    <td><strong>first_seen</strong> (optional)</td>
    <td><span class="stixtype">timestamp</span></td>
    <td>When the attribute was first seen.</td>
  </tr>
  <tr>
    <td><strong>last_seen</strong> (optional)</td>
    <td><span class="stixtype">timestamp</span></td>
    <td>When the attribute was last seen.</td>
  </tr>
  <tr>
    <td><strong>data</strong> (optional)</td>
    <td><span class="stixtype">binary</span></td>
    <td>The payload of an attribute carrying one, such as an attachment or a malware sample.</td>
  </tr>
</table>

## 3.2 Relationships <a id="misp-attribute-relationships"></a>

These are the relationships explicitly defined between the MISP Attribute object and other STIX Objects. The first section lists the embedded relationships by property name along with their corresponding target. The rest of the table identifies the relationships that can be made from this object type to another object type by way of the Relationship object. The reverse relationships section illustrates the relationships targeting this object type from another object type. They are included here for convenience. For their definitions, please see the "Source" object.

Relationships are not restricted to those listed below. Relationships can be created between any objects using the <span class="stixliteral">related-to</span> relationship type or, as with open vocabularies, user-defined names.

<table border="1" cellspacing="0" cellpadding="6" width="100%">
  <tr>
    <th colspan="2"><span class="stixtr">Embedded Relationships</span></th>
  </tr>
  <tr>
    <td width="50%"><strong>created_by_ref</strong></td>
    <td width="50%"><span class="stixtype">identifier</span> (of type <span class="stixtype">identity</span>)</td>
  </tr>
</table>

<table border="1" cellspacing="0" cellpadding="6" width="100%">
  <tr>
    <th><span class="stixtr">Common Relationships</span></th>
  </tr>
  <tr>
    <td><span class="stixliteral">duplicate-of</span>, <span class="stixliteral">derived-from</span>, <span class="stixliteral">related-to</span></td>
  </tr>
</table>

**Examples**

*A Bitcoin address, an attribute type no STIX object represents*

```JSON
{
  "type": "misp-attribute",
  "spec_version": "2.1",
  "id": "misp-attribute--91ae0a21-c7ae-4c7f-b84b-b84a7ce53d1f",
  "created_by_ref": "identity--a0c22599-9e58-4da4-96ac-7051603fa951",
  "created": "2020-10-25T16:22:00.000Z",
  "modified": "2020-10-25T16:22:00.000Z",
  "attribute_type": "btc",
  "value": "1E38kt7ryhbRXUzbam6iQ6sd93VHUUdjEE",
  "category": "Financial fraud",
  "comment": "Btc test attribute",
  "to_ids": true,
  "labels": [
    "misp:type=\"btc\"",
    "misp:category=\"Financial fraud\""
  ],
  "extensions": {
    "extension-definition--c1f2c0fa-3786-4f27-bf57-cf050ecfc104": {
      "extension_type": "new-sdo"
    }
  }
}
```

# 4. MISP Object Extension <a id="misp-object-extension"></a>

**Type Name:** <span class="stixtype">misp-object</span>

The **extensions** property of a <span class="stixtype">misp-object</span> **MUST** hold its extension definition id, <span class="stixliteral">extension-definition--a093107b-933f-4d72-a9a6-6d7318adadda</span>, with **extension_type** <span class="stixliteral">new-sdo</span>.

A MISP object no standard STIX object represents, with its attributes: an object template \[[MISP-Objects](#misp-objects)\] the converter maps to no STIX object (<span class="stixliteral">bank-account</span>, <span class="stixliteral">btc-wallet</span>, ...), or an object its STIX mapping cannot take. Its **id** carries the uuid of the MISP object.

## 4.1 Properties <a id="misp-object-properties"></a>

<table border="1" cellspacing="0" cellpadding="6" width="100%">
  <tr>
    <th><span class="stixtr">Required Common Properties</span></th>
  </tr>
  <tr>
    <td><strong>type</strong>, <strong>spec_version</strong>, <strong>id</strong>, <strong>created</strong>, <strong>modified</strong>, <strong>extensions</strong></td>
  </tr>
  <tr>
    <th><span class="stixtr">Optional Common Properties</span></th>
  </tr>
  <tr>
    <td><strong>created_by_ref</strong>, <strong>revoked</strong>, <strong>labels</strong>, <strong>confidence</strong>, <strong>lang</strong>, <strong>external_references</strong>, <strong>object_marking_refs</strong>, <strong>granular_markings</strong></td>
  </tr>
  <tr>
    <th><span class="stixtr">Not Applicable Common Properties</span></th>
  </tr>
  <tr>
    <td><strong>defanged</strong></td>
  </tr>
  <tr>
    <th><span class="stixtr">MISP Object Specific Properties</span></th>
  </tr>
  <tr>
    <td><strong>name</strong>, <strong>meta_category</strong>, <strong>comment</strong>, <strong>attributes</strong>, <strong>first_seen</strong>, <strong>last_seen</strong></td>
  </tr>
</table>

<table border="1" cellspacing="0" cellpadding="6">
  <tr>
    <th><span class="stixtr">Property Name</span></th>
    <th><span class="stixtr">Type</span></th>
    <th><span class="stixtr">Description</span></th>
  </tr>
  <tr>
    <td><strong>type</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The value of this property <strong>MUST</strong> be <span class="stixliteral">misp-object</span>.</td>
  </tr>
  <tr>
    <td><strong>extensions</strong> (required)</td>
    <td><span class="stixtype">dictionary</span></td>
    <td><strong>MUST</strong> hold <span class="stixliteral">extension-definition--a093107b-933f-4d72-a9a6-6d7318adadda</span>, whose value is <span class="stixliteral">{"extension_type": "new-sdo"}</span>.</td>
  </tr>
  <tr>
    <td><strong>name</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The name of the MISP object template.</td>
  </tr>
  <tr>
    <td><strong>meta_category</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The MISP object meta category.</td>
  </tr>
  <tr>
    <td><strong>comment</strong> (optional)</td>
    <td><span class="stixtype">string</span></td>
    <td>The object comment.</td>
  </tr>
  <tr>
    <td><strong>attributes</strong> (required)</td>
    <td><span style="white-space: nowrap;"><span class="stixtype">list</span> of type <span class="stixtype">misp-object-attribute-type</span></span></td>
    <td>The object attributes (<a href="#misp-object-attribute-type">section 4.2</a>). The list <strong>MUST</strong> hold at least one.</td>
  </tr>
  <tr>
    <td><strong>first_seen</strong> (optional)</td>
    <td><span class="stixtype">timestamp</span></td>
    <td>When the object was first seen.</td>
  </tr>
  <tr>
    <td><strong>last_seen</strong> (optional)</td>
    <td><span class="stixtype">timestamp</span></td>
    <td>When the object was last seen.</td>
  </tr>
</table>

## 4.2 MISP Object Attribute Type <a id="misp-object-attribute-type"></a>

**Type Name:** <span class="stixtype">misp-object-attribute-type</span>

An item of **attributes** keeps the keys MISP gives an object attribute. It is a <span class="stixtype">dictionary</span> in a list, so its **type** names the MISP attribute type and clashes with nothing.

<table border="1" cellspacing="0" cellpadding="6">
  <tr>
    <th><span class="stixtr">Property Name</span></th>
    <th><span class="stixtr">Type</span></th>
    <th><span class="stixtr">Description</span></th>
  </tr>
  <tr>
    <td><strong>type</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The MISP attribute type.</td>
  </tr>
  <tr>
    <td><strong>object_relation</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The object relation, as MISP spells it, with any <span class="stixliteral">(s)</span> removed.</td>
  </tr>
  <tr>
    <td><strong>value</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The attribute value.</td>
  </tr>
  <tr>
    <td><strong>category</strong> (optional)</td>
    <td><span class="stixtype">string</span></td>
    <td>The MISP category.</td>
  </tr>
  <tr>
    <td><strong>comment</strong> (optional)</td>
    <td><span class="stixtype">string</span></td>
    <td>The attribute comment.</td>
  </tr>
  <tr>
    <td><strong>to_ids</strong> (required)</td>
    <td><span class="stixtype">boolean</span></td>
    <td>Whether the attribute is flagged for detection.</td>
  </tr>
  <tr>
    <td><strong>uuid</strong> (optional)</td>
    <td><span class="stixtype">string</span></td>
    <td>The uuid of the MISP attribute.</td>
  </tr>
  <tr>
    <td><strong>data</strong> (optional)</td>
    <td><span class="stixtype">binary</span></td>
    <td>The payload of an attribute carrying one.</td>
  </tr>
  <tr>
    <td><strong>first_seen</strong> (optional)</td>
    <td><span class="stixtype">timestamp</span></td>
    <td>When the attribute was first seen.</td>
  </tr>
  <tr>
    <td><strong>last_seen</strong> (optional)</td>
    <td><span class="stixtype">timestamp</span></td>
    <td>When the attribute was last seen.</td>
  </tr>
</table>

## 4.3 Relationships <a id="misp-object-relationships"></a>

These are the relationships explicitly defined between the MISP Object object and other STIX Objects. The first section lists the embedded relationships by property name along with their corresponding target. The rest of the table identifies the relationships that can be made from this object type to another object type by way of the Relationship object. The reverse relationships section illustrates the relationships targeting this object type from another object type. They are included here for convenience. For their definitions, please see the "Source" object.

Relationships are not restricted to those listed below. Relationships can be created between any objects using the <span class="stixliteral">related-to</span> relationship type or, as with open vocabularies, user-defined names.

<table border="1" cellspacing="0" cellpadding="6" width="100%">
  <tr>
    <th colspan="2"><span class="stixtr">Embedded Relationships</span></th>
  </tr>
  <tr>
    <td width="50%"><strong>created_by_ref</strong></td>
    <td width="50%"><span class="stixtype">identifier</span> (of type <span class="stixtype">identity</span>)</td>
  </tr>
</table>

<table border="1" cellspacing="0" cellpadding="6" width="100%">
  <tr>
    <th><span class="stixtr">Common Relationships</span></th>
  </tr>
  <tr>
    <td><span class="stixliteral">duplicate-of</span>, <span class="stixliteral">derived-from</span>, <span class="stixliteral">related-to</span></td>
  </tr>
</table>

**Examples**

*A bank account, an object template no STIX object represents, with two of its attributes*

```JSON
{
  "type": "misp-object",
  "spec_version": "2.1",
  "id": "misp-object--695e7924-2518-4054-9cea-f82853d37410",
  "created_by_ref": "identity--a0c22599-9e58-4da4-96ac-7051603fa951",
  "created": "2020-10-25T16:22:00.000Z",
  "modified": "2020-10-25T16:22:00.000Z",
  "name": "bank-account",
  "meta_category": "financial",
  "attributes": [
    {
      "type": "iban",
      "object_relation": "iban",
      "value": "LU1234567890ABCDEF1234567890",
      "category": "Financial fraud",
      "uuid": "8acaad62-227a-4988-96e7-4586847421a2",
      "to_ids": true,
      "first_seen": "2020-10-25T16:22:00Z"
    },
    {
      "type": "bic",
      "object_relation": "swift",
      "value": "CTBKLUPP",
      "category": "Financial fraud",
      "uuid": "c53382a1-cf4b-4901-a890-1611dbcc7101",
      "to_ids": true
    },
    ...
  ],
  "first_seen": "2020-10-25T16:22:00Z",
  "last_seen": "2020-10-26T16:22:00.123456Z",
  "labels": [
    "misp:name=\"bank-account\"",
    "misp:meta-category=\"financial\""
  ],
  "extensions": {
    "extension-definition--a093107b-933f-4d72-a9a6-6d7318adadda": {
      "extension_type": "new-sdo"
    }
  }
}
```

# 5. MISP Galaxy Cluster Extension <a id="misp-galaxy-cluster-extension"></a>

**Type Name:** <span class="stixtype">misp-galaxy-cluster</span>

The **extensions** property of a <span class="stixtype">misp-galaxy-cluster</span> **MUST** hold its extension definition id, <span class="stixliteral">extension-definition--573a76d8-f8a0-4f53-bc93-f2777576b7b9</span>, with **extension_type** <span class="stixliteral">new-sdo</span>.

A MISP galaxy cluster \[[MISP-Galaxy](#misp-galaxy)\] no standard STIX object represents: a cluster of a galaxy the converter maps to no STIX object type. Its **id** carries the uuid of the cluster. **created** and **modified** take the timestamp of the event, attribute or object the cluster is attached to, else the cluster's own, else the export time. The MISP-STIX converter writes no **created_by_ref**: a cluster is not authored by the organisation exporting it.

## 5.1 Properties <a id="misp-galaxy-cluster-properties"></a>

<table border="1" cellspacing="0" cellpadding="6" width="100%">
  <tr>
    <th><span class="stixtr">Required Common Properties</span></th>
  </tr>
  <tr>
    <td><strong>type</strong>, <strong>spec_version</strong>, <strong>id</strong>, <strong>created</strong>, <strong>modified</strong>, <strong>extensions</strong></td>
  </tr>
  <tr>
    <th><span class="stixtr">Optional Common Properties</span></th>
  </tr>
  <tr>
    <td><strong>created_by_ref</strong>, <strong>revoked</strong>, <strong>labels</strong>, <strong>confidence</strong>, <strong>lang</strong>, <strong>external_references</strong>, <strong>object_marking_refs</strong>, <strong>granular_markings</strong></td>
  </tr>
  <tr>
    <th><span class="stixtr">Not Applicable Common Properties</span></th>
  </tr>
  <tr>
    <td><strong>defanged</strong></td>
  </tr>
  <tr>
    <th><span class="stixtr">MISP Galaxy Cluster Specific Properties</span></th>
  </tr>
  <tr>
    <td><strong>galaxy_name</strong>, <strong>galaxy_type</strong>, <strong>galaxy_description</strong>, <strong>value</strong>, <strong>description</strong>, <strong>meta</strong>, <strong>original_names</strong></td>
  </tr>
</table>

<table border="1" cellspacing="0" cellpadding="6">
  <tr>
    <th><span class="stixtr">Property Name</span></th>
    <th><span class="stixtr">Type</span></th>
    <th><span class="stixtr">Description</span></th>
  </tr>
  <tr>
    <td><strong>type</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The value of this property <strong>MUST</strong> be <span class="stixliteral">misp-galaxy-cluster</span>.</td>
  </tr>
  <tr>
    <td><strong>extensions</strong> (required)</td>
    <td><span class="stixtype">dictionary</span></td>
    <td><strong>MUST</strong> hold <span class="stixliteral">extension-definition--573a76d8-f8a0-4f53-bc93-f2777576b7b9</span>, whose value is <span class="stixliteral">{"extension_type": "new-sdo"}</span>.</td>
  </tr>
  <tr>
    <td><strong>galaxy_name</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The name of the galaxy.</td>
  </tr>
  <tr>
    <td><strong>galaxy_type</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The type of the galaxy.</td>
  </tr>
  <tr>
    <td><strong>galaxy_description</strong> (optional)</td>
    <td><span class="stixtype">string</span></td>
    <td>The description of the galaxy.</td>
  </tr>
  <tr>
    <td><strong>value</strong> (required)</td>
    <td><span class="stixtype">string</span></td>
    <td>The cluster value.</td>
  </tr>
  <tr>
    <td><strong>description</strong> (optional)</td>
    <td><span class="stixtype">string</span></td>
    <td>The cluster's own description.</td>
  </tr>
  <tr>
    <td><strong>meta</strong> (optional)</td>
    <td><span class="stixtype">dictionary</span></td>
    <td>The cluster meta: each key holds a <span class="stixtype">string</span>, or a <span class="stixtype">list</span> of at least two strings (<a href="#values">section 2.3</a>). The keys are the MISP meta keys with every character outside <code>a</code>-<code>z</code>, <code>A</code>-<code>Z</code>, <code>0</code>-<code>9</code>, <code>_</code> and <code>-</code> turned into <code>_</code> ([<a href="#stix-v2.1">STIX-v2.1</a>] section 2.3).</td>
  </tr>
  <tr>
    <td><strong>original_names</strong> (optional)</td>
    <td><span class="stixtype">dictionary</span></td>
    <td>Maps each <strong>meta</strong> key that differs from the MISP meta key to the key as MISP spells it. Written only when at least one key differs.</td>
  </tr>
</table>

## 5.2 Relationships <a id="misp-galaxy-cluster-relationships"></a>

These are the relationships explicitly defined between the MISP Galaxy Cluster object and other STIX Objects. The first section lists the embedded relationships by property name along with their corresponding target. The rest of the table identifies the relationships that can be made from this object type to another object type by way of the Relationship object. The reverse relationships section illustrates the relationships targeting this object type from another object type. They are included here for convenience. For their definitions, please see the "Source" object.

Relationships are not restricted to those listed below. Relationships can be created between any objects using the <span class="stixliteral">related-to</span> relationship type or, as with open vocabularies, user-defined names.

<table border="1" cellspacing="0" cellpadding="6" width="100%">
  <tr>
    <th colspan="2"><span class="stixtr">Embedded Relationships</span></th>
  </tr>
  <tr>
    <td width="50%"><strong>created_by_ref</strong></td>
    <td width="50%"><span class="stixtype">identifier</span> (of type <span class="stixtype">identity</span>)</td>
  </tr>
</table>

<table border="1" cellspacing="0" cellpadding="6" width="100%">
  <tr>
    <th><span class="stixtr">Common Relationships</span></th>
  </tr>
  <tr>
    <td><span class="stixliteral">duplicate-of</span>, <span class="stixliteral">derived-from</span>, <span class="stixliteral">related-to</span></td>
  </tr>
</table>

**Examples**

*A galaxy cluster no STIX object type represents, with a meta key whose spelling original_names keeps*

```JSON
{
  "type": "misp-galaxy-cluster",
  "spec_version": "2.1",
  "id": "misp-galaxy-cluster--24430dc6-9c27-4b3c-a5e7-6dda478fffa0",
  "created": "2020-10-25T16:22:00.000Z",
  "modified": "2020-10-25T16:22:00.000Z",
  "galaxy_name": "Tea Matrix",
  "galaxy_type": "tea-matrix",
  "galaxy_description": "Tea Matrix",
  "value": "Milk in tea",
  "description": "Milk in tea",
  "meta": {
    "Odd_Key__1_": "odd value",
    "kept-Case_ok": "kept value"
  },
  "original_names": {
    "Odd_Key__1_": "Odd Key (1)"
  },
  "labels": [
    "misp:galaxy-name=\"Tea Matrix\"",
    "misp:galaxy-type=\"tea-matrix\""
  ],
  "extensions": {
    "extension-definition--573a76d8-f8a0-4f53-bc93-f2777576b7b9": {
      "extension_type": "new-sdo"
    }
  }
}
```

# 6. Bundles <a id="bundles"></a>

A bundle the MISP-STIX converter writes carries the extension definitions its objects use, and the MISP Project identity creating them, each once:

- An extension definition is used when an object of the bundle names its id: a <span class="stixtype">misp-\*</span> object, a key of an object's **extensions**, or an object path in an Indicator's pattern.
- In an event, the identity and the extension definitions go after the identity of the event's organisation, ahead of the Report or Grouping of the first event using them: `[organisation identity, MISP Project identity, extension definitions..., report, objects...]`.
- In an attribute or object collection, which has no Report, they go ahead of the first object using them.
- The **object_refs** of a Report or Grouping do not list them.
- A bundle with no MISP Extension content carries neither the identity nor any extension definition.

The order of a bundle has no meaning in STIX. A consumer **SHOULD NOT** rely on it, nor on the extension definitions being present: the extension definition ids of this document are fixed.

# 7. Conformance Notes <a id="conformance-notes"></a>

## 7.1 The Property Extension's First Schema File Refers to No Base Type <a id="the-property-extensions-first-schema-file-refers-to-no-base-type"></a>

The STIX Extension Definition Policy \[[STIX-Extension-Policy](#stix-extension-policy)\] (Appendix A.1, item 6) asks the first schema file of a property extension to start with an `allOf` whose first part refers to the base schema of the object type it extends. The MISP Property Extension extends about 25 object types and cannot refer to one of them: its first schema file only requires **extensions** to hold the extension definition id, with the body schema as its value. The STIX 2.1 base schemas of the object types check the rest of each object.

## 7.2 The Schema Does Not Tie a Nested Room to Its Type <a id="the-schema-does-not-tie-a-nested-room-to-its-type"></a>

The body schema accepts **windows_pebinary_ext** and **values** on any object type. The MISP-STIX converter writes **windows_pebinary_ext** on a <span class="stixtype">file</span> only, and **values** on a <span class="stixtype">windows-registry-key</span> only. The MISP-STIX import refuses an object whose room has a key naming no item of its STIX list, or no extension to stand for.

## 7.3 No External References <a id="no-external-references"></a>

The STIX Extension Definition Policy \[[STIX-Extension-Policy](#stix-extension-policy)\] (sections 3.3 and 3.4) asks an extension definition to reference its documentation and examples through **external_references**. The MISP Extensions carry none: the **schema** URL already points to this directory, <span class="stixliteral">https://github.com/oasis-open/cti-stix-common-objects/tree/main/extension-definition-specifications/misp-5ec</span>, which holds both.

## 7.4 An Empty Registry Value <a id="an-empty-registry-value"></a>

A MISP <span class="stixliteral">registry-key-value</span> holding only values STIX has no property for is written as <span class="stixliteral">{}</span> in the **values** of its <span class="stixtype">windows-registry-key</span>, so that its position, the key of its room in the property extension, holds ([section 2.5](#nested-rooms)). STIX 2.1 (\[[STIX-v2.1](#stix-v2.1)\] section 6.17.2) requires a registry value to hold at least one property, so such an item breaks the STIX 2.1 base schema.

# 8. Examples <a id="examples"></a>

The files of [`examples/`](examples/) are bundles the MISP-STIX converter exported from its own test events, and validate against the schemas of this directory. Two of those test events were changed before the export, the way the converter's tests change them, to show a case no test event holds as it is: a section with no MISP value, and values with data held in a list.

The event organisation "MISP-Project" (<span class="stixliteral">identity--a0c22599-9e58-4da4-96ac-7051603fa951</span>) in the examples comes from the converter's test events: it is not the MISP Project identity.

<table border="1" cellspacing="0" cellpadding="6" width="100%">
  <tr>
    <th><span class="stixtr">File</span></th>
    <th><span class="stixtr">Shows</span></th>
  </tr>
  <tr>
    <td><a href="examples/misp-attribute.json"><code>misp-attribute.json</code></a></td>
    <td><span class="stixtype">misp-attribute</span> objects: two attribute types no STIX object represents, and four not flagged for detection that hold too little for an observable.</td>
  </tr>
  <tr>
    <td><a href="examples/misp-object.json"><code>misp-object.json</code></a></td>
    <td><span class="stixtype">misp-object</span> objects, with <strong>first_seen</strong> and <strong>last_seen</strong> on the object and on attributes, and an attachment with its <strong>data</strong>.</td>
  </tr>
  <tr>
    <td><a href="examples/misp-galaxy-cluster.json"><code>misp-galaxy-cluster.json</code></a></td>
    <td>A <span class="stixtype">misp-galaxy-cluster</span>, with a <strong>meta</strong> key whose spelling <strong>original_names</strong> keeps.</td>
  </tr>
  <tr>
    <td><a href="examples/location-with-galaxy-meta.json"><code>location-with-galaxy-meta.json</code></a></td>
    <td>The property extension on two <span class="stixtype">location</span> SDOs from galaxy clusters: meta values as a <span class="stixtype">string</span> and as a <span class="stixtype">list</span>, and <strong>original_names</strong>.</td>
  </tr>
  <tr>
    <td><a href="examples/url-with-misp-values.json"><code>url-with-misp-values.json</code></a></td>
    <td>The property extension on a <span class="stixtype">url</span> SCO: object relation values, among which the escaped <strong>misp_ip</strong>, and the Indicator comparing them.</td>
  </tr>
  <tr>
    <td><a href="examples/file-with-pe-rooms.json"><code>file-with-pe-rooms.json</code></a></td>
    <td>A <span class="stixtype">file</span> with the <strong>windows_pebinary_ext</strong> and <strong>sections</strong> rooms: the first section holds no MISP value and has no key.</td>
  </tr>
  <tr>
    <td><a href="examples/windows-registry-key-with-values-room.json"><code>windows-registry-key-with-values-room.json</code></a></td>
    <td>A <span class="stixtype">windows-registry-key</span> with the <strong>values</strong> room.</td>
  </tr>
  <tr>
    <td><a href="examples/indicator-comparing-values-with-data.json"><code>indicator-comparing-values-with-data.json</code></a></td>
    <td>An Indicator comparing values with data held in a list: <code>[*]</code>, with <strong>data</strong> then <strong>value</strong>.</td>
  </tr>
</table>

# Appendix A: The Custom Syntax <a id="the-custom-syntax"></a>

*This appendix is informative.*

Up to misp-stix version 2026.10.12, the STIX 2.1 export carried the same content as custom STIX objects and properties (\[[STIX-v2.1](#stix-v2.1)\] section 11), which the STIX 2.0 export still writes:

- <span class="stixtype">x-misp-attribute</span>, <span class="stixtype">x-misp-object</span> and <span class="stixtype">x-misp-galaxy-cluster</span> objects, where the MISP Extensions write <span class="stixtype">misp-attribute</span>, <span class="stixtype">misp-object</span> and <span class="stixtype">misp-galaxy-cluster</span>, with the same uuid in their ids;
- `x_misp_*` properties at the top level of standard objects, where the property extension holds the same values under their Extension Property Names, and **x_misp_original_names**, where it holds **original_names**;
- MISP values inside <span class="stixtype">windows-pebinary-ext</span>, its sections and registry values, where the Nested Rooms hold them.

The MISP-STIX import reads both forms, object by object, and gives the same MISP content.

# Appendix B: References <a id="references"></a>

This appendix contains the normative and informative references that are used in this document. Normative references are specific (identified by date of publication and/or edition number or version number) and Informative references are either specific or non-specific. For specific references, only the cited version applies. For non-specific references, the latest version of the reference document (including any amendments) applies. While any hyperlinks included in this appendix were valid at the time of publication, their long term validity cannot be guaranteed.

## B.1 Normative References <a id="normative-references"></a>

The following documents are referenced in such a way that some or all of their content constitutes requirements of this document.

**[RFC2119]** <a id="rfc2119"></a>  
Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, DOI 10.17487/RFC2119, March 1997, http://www.rfc-editor.org/info/rfc2119.

**[RFC8174]** <a id="rfc8174"></a>  
Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, DOI 10.17487/RFC8174, May 2017, https://www.rfc-editor.org/info/rfc8174.

**[STIX-Extension-Policy]** <a id="stix-extension-policy"></a>  
"STIX Extension Definition Policy".

**[STIX-v2.1]** <a id="stix-v2.1"></a>  
_STIX Version 2.1_. Edited by Bret Jordan, Rich Piazza, and Trey Darley. 10 June 2021. OASIS Standard. https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html. Latest stage: https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html.

## B.2 Informative References <a id="informative-references"></a>

The following referenced documents are not required for the application of this document but may assist the reader with regard to a particular subject area.

**[MISP]** <a id="misp"></a>  
MISP Open Source Threat Intelligence and Sharing Platform. MISP Project. [Online]. Available: https://www.misp-project.org/.

**[MISP-Galaxy]** <a id="misp-galaxy"></a>  
MISP galaxy. MISP Project. [Online]. Available: https://github.com/MISP/misp-galaxy.

**[MISP-Objects]** <a id="misp-objects"></a>  
MISP object templates. MISP Project. [Online]. Available: https://github.com/MISP/misp-objects.

**[misp-stix]** <a id="misp-stix"></a>  
MISP-STIX converter (misp-stix). MISP Project. [Online]. Available: https://github.com/MISP/misp-stix.
