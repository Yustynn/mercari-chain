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
  },
  url: 'http://b4dbbdbb.ngrok.io'
}

const { random, round, floor, max } = Math;
const choice = (arr) => floor( random() * arr.length );

const data = { nodes: [], links: []}

const addNode = () => {
  data.nodes.push({
    id: data.nodes.length,
    confidence: max(CONFIG.minValue, random()),
    trustworthiness: max(CONFIG.minValue, random()),
    confidence: CONFIG.minValue,
    trustworthiness: CONFIG.minValue,
  })
}

const initNodes = () => {
  for (let i = 0; i < CONFIG.N; i++) addNode()

  const { nodes } = data

  // adjust main node
  nodes[0].confidence = CONFIG.mainNode.confidence
  nodes[0].trustworthiness = CONFIG.mainNode.trustworthiness
  nodes[0].confidence = 0.8
}

//const addLinks = (node) => {
  //for (let otherNode of data.nodes) {
    //const [id1, id2] = [node, otherNode].map(n => n.id)
    //if (id1 === id2) continue;
    //if (random() <= CONFIG.p) {
      //data.links.push({
        //source: id1,
        //target: id2,
      //});
    //}
  //}
//}


//const initLinks = () => data.nodes.forEach(addLinks)
const loadNewData = async (newNodes, newLinks) => {
  data.nodes = newNodes.map((newNode, i) => {
    if (i >= data.nodes.length) {
      return newNode
    }
    return {
      ...data.nodes[i],
      ...newNode
    }
  })

  data.links = newLinks.map((newLink, i) => {
    if (i >= data.links.length) {
      return newLink
    }
    return {
      ...data.links[i],
      ...newLink
    }
  })

  console.log(data)
}

//initNodes()
//initLinks()



