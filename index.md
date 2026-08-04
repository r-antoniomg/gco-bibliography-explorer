---
layout: default
title: Home
---

# German Canadiana in Ontario (GCO) Bibliography

The German Canadiana in Ontario Bibliography (GCO) was started in 2007 and is a project of the University of Waterloo Libraries. It is updated continuously, as new information becomes available.

## Browse this bibliography by collection

<div id="collection-gallery">
  Loading collections...
</div>

<style>
.collection-grid {
  display: grid;
  gap: 1rem;
  margin-top: 1rem;
}

.collection-grid.two-col {
  grid-template-columns: repeat(2, 1fr);
}

.collection-grid.three-col {
  grid-template-columns: repeat(3, 1fr);
}

.collection-card,
.collection-card:visited,
.collection-card:hover,
.collection-card:active {
  display: block;
  text-decoration: none;
  color: inherit;
  border: 1px solid #d9d9d9;
  border-radius: 12px;
  padding: 1rem;
  min-height: 90px;
  background: #f8f8f8;
}

.collection-card:hover {
  background: #efefef;
}

.collection-title {
  text-align: center;
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 0.75rem;
}

.collection-count {
  font-size: 0.9rem;
}
</style>

<script>
const BASE_URL = '{{ site.baseurl }}';

{% include zotero-data-loader.html %}

function countItemsInCollection(items, collectionKey) {
  return items.filter(item => {
    const collections = item.data.collections || [];
    return collections.includes(collectionKey);
  }).length;
}

Promise.all([
  loadZoteroCollections(),
  loadZoteroItems()
])
  .then(([collections, items]) => {
    const gridClass = collections.length <= 4 ? 'two-col' : 'three-col';

    let html = `<div class="collection-grid ${gridClass}">`;

    collections.forEach(collection => {
      const collectionName = collection.data.name || 'Unnamed Collection';
      const collectionKey = collection.key;
      const itemCount = countItemsInCollection(items, collectionKey);

      html += `
        <a class="collection-card" href="${BASE_URL}/collection/?key=${collectionKey}">
          <div class="collection-title">${collectionName}</div>
          <div class="collection-count">Item count: ${itemCount}</div>
        </a>`;
    });

    html += '</div>';

    html += `
      <div style="margin-top: 2rem;">
        <a class="collection-card" href="${BASE_URL}/topics/">
          <div class="collection-title">
            Explore the Bibliography by Topic
          </div>
          <div class="collection-count">
            Browse records across all collections using topic tags.
          </div>
        </a>
      </div>`;

    document.getElementById('collection-gallery').innerHTML = html;
  })
  .catch(error => {
    document.getElementById('collection-gallery').innerHTML = '<p>Error loading collections.</p>';
    console.error(error);
  });
</script>