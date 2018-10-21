console.log(data.links)
console.log(data.nodes)

const svg = d3.select('svg');
const width = +svg.attr('width');
const height = +svg.attr('height');

const [trustworthinessSpan, confidenceSpan] = ['#trustworthiness', '#confidence']
  .map(id => d3.select(id))

const sim = d3.forceSimulation()
  .nodes(data.nodes);

const getNodeFill = (node) => {
  return d3.interpolateRdYlGn(node.computed_score)
}

const getNodeStrokeWidth = (node) => {
  if (node.id === 0) return CONFIG.mainNode.strokeWidth
  return 0
}

const getNodeRadius = (node) => max(
  node.computed_confidence * CONFIG.nodeSize,
  CONFIG.minRadius
)

const getNodeLabel = ({id}) => {
  if (id === 0) return "Bella Schmitz"
  return id
}

sim
  .force("charge_force", d3.forceManyBody())
  .force("center_force", d3.forceCenter(width/2, height/2))

let node = svg
  .attr('class', 'nodes')
  .selectAll('circle')
  .data(data.nodes)
  .enter().append('circle')
      .attr('r', getNodeRadius)
      .attr("fill", getNodeFill)
      .attr("stroke", 'black')
      .attr('stroke-width', getNodeStrokeWidth)

let label = svg
  .selectAll('text')
  .data(data.nodes)
  .enter().append('text')
    .attr('dx', 20)
    .attr('dy', '0.35em')
    .text(getNodeLabel)

let link = svg
  .append('g')
  .attr('class', 'links')
  .selectAll('line')
  .data(data.links)
  .enter().append('line')
    .attr('stroke-width', 1)
    .attr('stroke', '#666');

sim.on('tick', handleTick);

function handleTick() {
  node.attr('cx', d => d.x)
  node.attr('cy', d => d.y)

  label
    .attr('x', d => d.x)
    .attr('y', d => d.y)

  link
    .attr('x1', d => d.source.x)
    .attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x)
    .attr('y2', d => d.target.y)
}

const linkForce = d3
  .forceLink(data.links)
  .distance(200)
  .strength(0.1)
  .id(d => d.id)

sim.force('links', linkForce)

const refresh = () => {
  sim.nodes(data.nodes)

    // Apply the general update pattern to the nodes.
  node = node.data(data.nodes, function(d) { return d.id;});
  node.exit().remove();
  node = node
    .enter().append("circle")
      .attr("stroke", 'black')
      .attr('stroke-width', getNodeStrokeWidth)
      .merge(node)
      .attr("fill", getNodeFill)
      .attr('r', getNodeRadius)

  // update labels
  label = label.data(data.nodes, d => d.id)

  label.exit().remove();
  label = label
    .enter().append('text')
      .attr('dx', 20)
      .attr('dy', '0.35em')
      .text(getNodeLabel)
      .merge(label)


  // Apply the general update pattern to the links.
  link = link.data(data.links, function(d) { return d.source.id + "-" + d.target.id; });
  link.exit().remove();
  link = link.enter()
    .append("line")
    .attr('stroke', '#666')
    .merge(link);
  // Update and restart the simulation.
  sim.nodes(data.nodes);
  sim.force("links").links(data.links);
  sim.alpha(1).restart();

}

const initData = async () => {
  const newNodes = await (await fetch(
    `${CONFIG.url}/get/nodelist`
  )).json()
  const newLinks = await (await fetch(
    `${CONFIG.url}/get/edgelist`
  )).json()

  await loadNewData(newNodes, newLinks)
  refresh()
}

const handleAddNewNode = async () => {
  const res = (await fetch(
    `${CONFIG.url}/user`,
    { method: 'POST' }
  )).json()

  const { nodes, links } = await res

  loadNewData(nodes, links)
  refresh()
}

initData()

const handlePostReviews = async (e) => {
  const $ = document.querySelector.bind(document)
  const ratingIndex = [1, 2, 3, 4, 5].map(n => {
    return $(`#first-rate${n}`).checked
  }).indexOf(true)

  if (ratingIndex === -1) return console.error("Rating not selected!")

  const rating = ratingIndex + 1
  
  let target = $('#select-node').value
  if (target == 'Bella Schmitz' ) target = 0;

  const count = +$('#numReviewsRange').value
  const content = $('#review-text').value
  const company = 'mercari'

  const postData = { count, content, company, rating }
  const formData = new FormData()
  for (let key in postData) formData.append(key, postData[key])

  console.log('posting', postData)

  const res = (await fetch(
    `${CONFIG.url}/add_review/${target}`, {
      method: 'POST',
      body: formData
    }
  )).json()

  const { nodes, links } = await res
  console.log(nodes, links)
  loadNewData(nodes, links)
  refresh()
}

d3.select('#add-person').on('click', handleAddNewNode)
d3.select('#submit-reviews').on('click', handlePostReviews)

