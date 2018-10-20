console.log(links)
console.log(nodes)

const svg = d3.select('svg');
const width = +svg.attr('width');
const height = +svg.attr('height');

const sim = d3.forceSimulation()
  .nodes(nodes);

sim
  .force("charge_force", d3.forceManyBody())
  .force("center_force", d3.forceCenter(width/2, height/2))

let node = svg
  .attr('class', 'nodes')
  .selectAll('circle')
  .data(nodes)
  .enter()
  .append('circle')
  .attr('r', d => d.confidence * CONFIG.nodeSize)
  .attr("fill", d => d3.interpolateRdYlGn(d.trustworthiness))

let link = svg
  .append('g')
  .attr('class', 'links')
  .selectAll('line')
  .data(links)
  .enter()
    .append('line')
    .attr('stroke-width', 1);

function restart() {

}

sim.on('tick', handleTick);

function handleTick() {
  node.attr('cx', d => d.x)
  node.attr('cy', d => d.y)

  link
    .attr('x1', d => d.source.x)
    .attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x)
    .attr('y2', d => d.target.y)
}

const linkForce = d3
  .forceLink(links)
  .id(d => d.id)

sim.force('links', linkForce)

const update = () => {
  addNode()
  addLinks(nodes[nodes.length-1])

  sim.nodes(nodes)


    // Apply the general update pattern to the nodes.
  node = node.data(nodes, function(d) { return d.id;});
  node.exit().remove();
  node = node
    .enter()
    .append("circle")
    .attr("fill", d => d3.interpolateRdYlGn(d.trustworthiness))
    .attr('r', d => d.confidence * CONFIG.nodeSize)
    .merge(node);

  // Apply the general update pattern to the links.
  link = link.data(links, function(d) { return d.source.id + "-" + d.target.id; });
  link.exit().remove();
  link = link.enter().append("line").merge(link);
  // Update and restart the simulation.
  sim.nodes(nodes);
  sim.force("links").links(links);
  sim.alpha(1).restart();
}

setInterval(update, 1500)
