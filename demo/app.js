console.log(links)
console.log(nodes)

const svg = d3.select('svg');
const width = +svg.attr('width');
const height = +svg.attr('height');

const [trustworthinessSpan, confidenceSpan] = ['#trustworthiness', '#confidence']
  .map(id => d3.select(id))

const updateSpans = () => {
  const { confidence, trustworthiness } = nodes[0]

  trustworthinessSpan.text(round(trustworthiness * 100))
  confidenceSpan.text(round(confidence * 100))
}

updateSpans()

const sim = d3.forceSimulation()
  .nodes(nodes);

const getNodeFill = (node) => {
  //if (node.id === 0) return 'white';
  return d3.interpolateRdYlGn(node.trustworthiness)
}

const getNodeStrokeWidth = (node) => {
  if (node.id === 0) return CONFIG.mainNode.strokeWidth
  return 0
}

const getNodeRadius = (node) => max(
  node.confidence * CONFIG.nodeSize,
  CONFIG.minRadius
)

const getNodeLabel = ({id}) => {
  if (id === 0) return "Wim Schmitz"
  return id
}

sim
  .force("charge_force", d3.forceManyBody())
  .force("center_force", d3.forceCenter(width/2, height/2))

let node = svg
  .attr('class', 'nodes')
  .selectAll('circle')
  .data(nodes)
  .enter().append('circle')
      .attr('r', getNodeRadius)
      .attr("fill", getNodeFill)
      .attr("stroke", 'black')
      .attr('stroke-width', getNodeStrokeWidth)

let label = svg
  .selectAll('text')
  .data(nodes)
  .enter().append('text')
    .attr('dx', 20)
    .attr('dy', '0.35em')
    .text(getNodeLabel)

let link = svg
  .append('g')
  .attr('class', 'links')
  .selectAll('line')
  .data(links)
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
  .forceLink(links)
  .distance(200)
  .strength(0.1)
  .id(d => d.id)

sim.force('links', linkForce)

const addNodeToViz = () => {
  addNode()
  addLinks(nodes[nodes.length-1])

  sim.nodes(nodes)

    // Apply the general update pattern to the nodes.
  node = node.data(nodes, function(d) { return d.id;});
  node.exit().remove();
  node = node
    .enter().append("circle")
      .attr("fill", getNodeFill)
      .attr("stroke", 'black')
      .attr('stroke-width', getNodeStrokeWidth)
      .attr('r', getNodeRadius)
      .merge(node);

  // update labels
  label = label.data(nodes, d => d.id)

  label.exit().remove();
  label = label
    .enter().append('text')
      .attr('dx', 20)
      .attr('dy', '0.35em')
      .text(getNodeLabel)
      .merge(label)


  // Apply the general update pattern to the links.
  link = link.data(links, function(d) { return d.source.id + "-" + d.target.id; });
  link.exit().remove();
  link = link.enter()
    .append("line")
    .attr('stroke', '#666')
    .merge(link);
  // Update and restart the simulation.
  sim.nodes(nodes);
  sim.force("links").links(links);
  sim.alpha(1).restart();

}

d3.select('#add-person').on('click', addNodeToViz)
