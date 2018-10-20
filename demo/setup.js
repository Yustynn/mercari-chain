const CONFIG = {
  N: 3,
  p: 0.2,
  nodeSize: 20,
  minValue: 0.2,
  minRadius: 8,
  mainNode: {
    confidence: 0.39,
    trustworthiness: 0.12,
    strokeWidth: 5,
  }
}

const { random, round, floor, max } = Math;
const choice = (arr) => floor( random() * arr.length );

const nodes = []

const addNode = () => {
  nodes.push({
    id: nodes.length,
    confidence: max(CONFIG.minValue, random()),
    trustworthiness: max(CONFIG.minValue, random()),
    confidence: CONFIG.minValue,
    trustworthiness: CONFIG.minValue,
  })
}

const initNodes = () => {
  for (let i = 0; i < CONFIG.N; i++) addNode()

  // adjust main node
  nodes[0].confidence = CONFIG.mainNode.confidence
  nodes[0].trustworthiness = CONFIG.mainNode.trustworthiness
  nodes[0].confidence = 0.8
}

const links = []
const addLinks = (node) => {
  for (let otherNode of nodes) {
    const [id1, id2] = [node, otherNode].map(n => n.id)
    if (id1 === id2) continue;
    if (random() <= CONFIG.p) {
      links.push({
        source: id1,
        target: id2,
      });
    }
  }
}

const initLinks = () => nodes.forEach(addLinks)

initNodes()
initLinks()
