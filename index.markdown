---
layout: default
title: Home
---

# GCO Annotated Bibliography

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

.home-intro {
  max-width: 1000px;
}

.topic-box {
  margin-top: 2rem;
  padding: 1rem;
  border: 1px solid #d9d9d9;
  border-radius: 12px;
}
</style>

<script>
const COLLECTIONS_URL = 'https://api.zotero.org/groups/6606998/collections?format=json&limit=100';
const BASE_URL = '{{ site.baseurl }}';

fetch(COLLECTIONS_URL)
.then(response => response.json())
.then(collections => {

  const gridClass = collections.length <= 4 ? 'two-col' : 'three-col';

  const requests = collections.map(collection => {
    const key = collection.key;

    return fetch(`https://api.zotero.org/groups/6606998/collections/${key}/items/top?format=json&limit=100`)
      .then(response => response.json())
      .then(items => ({
        name: collection.data.name,
        key: key,
        count: items.length
      }));
  });

  Promise.all(requests).then(results => {

    let html = `<div class="collection-grid ${gridClass}">`;

    results.forEach(collection => {
      html += `
      <a class="collection-card" href="${BASE_URL}/collection/?key=${collection.key}">
        <div class="collection-title">${collection.name}</div>
        <div class="collection-count">Item count: ${collection.count}</div>
      </a>`;
    });

    html += '</div>';

html += `
  <div style="margin-top: 2rem;">
    <a class="collection-card" href="${BASE_URL}/topics/">

      <div class="collection-title">
        Explore the bibliography by topic
      </div>

      <div>
        Browse records across all collections using topic tags.
      </div>

    </a>
  </div>
`;

    document.getElementById('collection-gallery').innerHTML = html;
  });
})
.catch(error => {
  document.getElementById('collection-gallery').innerHTML = '<p>Error loading collections.</p>';
  console.error(error);
});
</script>