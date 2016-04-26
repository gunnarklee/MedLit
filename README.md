# MedLit
/Users/GunnarK/Dropbox/coderepos/MedLit/README.md

We downloaded the pubmed [open access subset](http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/), parsed authors paper ids (PMID) and paper attributes. The data was filtered, cleaned and combined into three files: paper nodes, author nodes, and links. These data were loaded into a Neo4J database and explored using the Neo4J interface, also RNeo4J. Also subsets of the data were explored in greater detail using Gelphi. For more detail see [a detailed writeup of our process](https://docs.google.com/document/d/1vHbXSXNLSNJU4KxtD1rUbTHcs1XtrkwzoCGV7EzozjY/edit?usp=sharing) and [A powerpoint presening this project and example results.](https://docs.google.com/presentation/d/1FELkytmmUrCnGzXpNByzaGyROO5Ybt7wtj55OoLVGWA/edit?ts=5718e3bb#slide=id.g1113dc688f_0_5)

# The code provided in this repo was used to process and explore the data.

* A distributed architecture was used to map data from individual article nxml files to fragmented CSV files then reduced to 3 master CSVs (one per master virtual machine). The master CSVs were each mapped to 2 node and 1 links files then reduced to single master link and nodes files in virtual machine 1 which housed the Neo4J databse. Finally the node and links files were loaded into our Neo4J graph database. 

![Alt text](/251_Img/CloudArchitecture.png?raw=true "cloud architecture used for mapping and reducing the data")

* Python was used to transform the code, clean it and prepare if for loading into the graph database.

![Alt text](/251_Img/FileTransform.png?raw=true "Map of file transformations and utility code")

* The packages used to clean, transform and analyze the data are detailed. Custom Rneo4j functions used for extraction and plotting of data directly from the database are shown in *red boxes*. Extracted data was loaded into *Gelphi* for more detailed plots and analysis.

![Alt text](/251_Img/Analysis.png?raw=true "Overview of analysis flow and packages used")
