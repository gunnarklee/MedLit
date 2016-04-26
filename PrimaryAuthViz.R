########## got this to work... #####
## IF YOU WANT TO SEE THE GRAPH: dont do this in Rstudio, do it in R ###

library(igraph)
library(visNetwork)
library(RNeo4j)

graph=startGraph("http://169.45.80.56:7474/db/data", username = "neo4j", password= "251Project")


PrimaryAuthViz<-function(name, outfile='network', showviz='yes'){
  
  query="MATCH (p1:Author)-[:AUTHORED]->(:Paper)<-[:AUTHORED]-(p2:Author) 
WHERE p1.name ={name}
RETURN p1.name AS from, p2.name AS to, COUNT(*) AS weight"
  
  
  edges = cypher(graph, query,name=name)
  
  nodes = data.frame(id=unique(c(edges$from, edges$to)))
  nodes$label = nodes$id
  
  # Save a network without displaying
  ## AS HTML
  network1 = visNetwork(nodes, edges) 
  #%>% visInteraction(dragNodes = FALSE, dragView = FALSE, zoomView = FALSE)
  network1 %>% visSave(file = paste0(outfile, ".html"))
  
  
  write.csv(edges, paste0(name, 'PrimaryEdges.csv'))
  write.csv(nodes, paste0(name, 'PrimaryNodes.csv'))
  
  GraphDt=c(edges, nodes)
  return (GraphDt)
}

####################
# examples "GUNTHER EYSENBACH","HOONGKUN FUN", "COLEEN MURPHY", "SCOTT W EMMONS"
GraphDt<-PrimaryAuthViz("GUNTHER EYSENBACH", "GuntherEyPrim")


