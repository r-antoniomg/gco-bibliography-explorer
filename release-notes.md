---
layout: page
title: Release notes
permalink: /release-notes/
---
# 2026-08-04 : Second release (v 0.2)

## Implemented
Cache-first performance and reliability
* Script added to pull Zotero data as cached files
* `zotero-data-loader.html` include added to check whether cached data exists for rendering pages. If no data exists, use Zotero API request
* Updated relevant pages (`tag.html`, `topics.html`, `collection.html`, `index.md`) to use the data loader

## Planned enhancements (v 0.3)
Interface/configuration refinements
* Transfer in-line `.css` elements from pages to a dedicated `.css` file
* Add configurable sorting options in `_config.yml`
  * Allow site owners to enable or disable title, creator, and year sorting
  * For GCO, disable creator sorting unless creator names can be sorted reliably
* Explore author/creator-based discovery as an alternative to creator sorting

# 2026-07-30 : First release (v 0.1)

## Implemented
Live Zotero API proof of concept
* Basic site structure built:
  * Home page with collection titles and item counts pulled from Zotero via API
  * Option to explore by topics (pulled from tags in Zotero via API)
* Collection pages built:
  * Options to sort by author, title, year, and filter by tags
  * Options to explore collection by topic
* Topics page built:
  * Creates word-cloud with buttons of relative size based on Zotero tags

## Known limitations
* Live API requests
* Visual appearance of prototype interface
* Retrieve limited to 100 records per collection