const CONFIG = {
  N: 3,
  p: 0.2 / 2,
  nodeSize: 10,
}

const { random, floor } = Math;
const choice = (arr) => floor( random() * arr.length );

const nodes = []

const addNode = () => {
  nodes.push({
    id: nodes.length,
    confidence: random(),
    trustworthiness: random()
  })
}

for (let i = 0; i < CONFIG.N; i++) addNode()

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

nodes.forEach(addLinks)
