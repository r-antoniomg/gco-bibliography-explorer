---
layout: page
title: 'Record data elements'
permalink: /data-elements/
---
## Standard record fields

These are the fields to be retrieved from Zotero.

### Required
* title

### Strongly recommended if present

* creators
* date
* publication title / book title
* volume
* issue
* pages
* place
* publisher
* URL
* tags
* abstract

### Capture but display selectively

* language
* DOI
* ISBN
* ISSN
* Zotero item key
* item type
* notes

## Display order

* Title
* Creators
* Publication / Source
  * Journal or publication title
  * Volume
  * Issue
  * Pages
* Publication Details
  * Place
  * Publisher
  * Date
  * Language
* Access / Identifiers
  * URL
  * DOI
  * ISBN / ISSN
  * Zotero item key
* Topics
  * Tag buttons
* Description
  * Abstract
  * Notes

## Future relationship model

Each item in the bibliography may be associated with one or more locally-created interpretive essays, blog posts, or other research outputs published in the site. The relationship can be expressed in the post's front matter metadata as in the following example:

```
---
layout: post
title: "German-Canadian Print Culture and Community Memory"
related_zotero_items:
  - KDFLMDD3
  - ABC12345
---
```

The bibliography record-renderer can check a locally-generated index of relationships. Example:

```
relatedContentByZoteroKey["KDFLMDD3"]
```

And display:

```
Related site content:
[German-Canadian Print Culture and Community Memory]
```

Adjacent to the other metadata for each record.