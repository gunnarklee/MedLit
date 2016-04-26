---
#  title: "Neo4J load and query"
#output: html_document
---  
library(igraph)
library(visNetwork)
library(RNeo4j)

graph=startGraph("http://169.45.80.56:7474/db/data", username = "neo4j", password= "251Project")

SecDegViz<-function(name, outfile='network'){
  
  query="MATCH (p1:Author)-[:AUTHORED]->(:Paper)<-[:AUTHORED]-(p2:Author) 
  WHERE p1.name ={name}
  RETURN p1.name AS from, p2.name AS to, COUNT(*) AS weight"
  
  edges = cypher(graph, query,name=name)
  head(edges)
  
  c = data.frame(id=unique(c(edges$from, edges$to)))
  nodes$label = nodes$id
  
  print(name)
  print(c('primary Node Ct:', str(dim(nodes)[1])))
  
  # get the second degree edge
  secondDegEdge = lapply(edges$to, function(x) cypher(graph, query,name=x))
  #print(paste('Sec Node Ct:', str(dim(secondDegEdge)[1])))
  
   
  SecEdges=do.call(rbind, secondDegEdge)
  SecNodes = data.frame(id=unique(c(SecEdges$from, SecEdges$to)))
  SecNodes$group = "secondary"
  SecNodes$label = SecNodes$id
  
  ## label primary and secondary 
  for (n in 1:dim(SecNodes)[1])
    for (m in 1:dim(nodes)[1])
      if (SecNodes$label[n] == nodes$label[m]) 
      {SecNodes$group[n] = "primary"}
  
  
  # Save a network without displaying
  ## AS HTML
  network1 = visNetwork(SecNodes, SecEdges)  %>%
    visGroups(groupname = "secondary", color="blue") %>%
    visGroups(groupname = "primary", color = "red") 
  #%>% addFontAwesome()
  #%>% visInteraction(dragNodes = FALSE, dragView = FALSE, zoomView = FALSE)
  network1 %>% visSave(file = paste0(outfile, ".html"))
  
  write.csv(SecEdges, paste0(name, 'SecEdges.csv'))
  write.csv(SecNodes, paste0(name, 'SecNodes.csv'))
}
# examples "GUNTHER EYSENBACH","HOONGKUN FUN", "COLEEN MURPHY", "SCOTT W EMMONS"
NodesFl<-SecDegViz("HOONGKUN FUN", "HoongFunSec")
