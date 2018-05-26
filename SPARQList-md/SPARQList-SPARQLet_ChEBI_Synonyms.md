#ChEBI Synonyms

## Parameters

* `id` ChEBI ID 
  * default: CHEBI:41308
  * examples: CHEBI:90 CHEBI:13614
 
## Endpoint

https://sparql.glyconavi.org/sparql

## `result` CHEBI  prefLabel altLabel

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX exterms: <http://www.example.org/terms/>
PREFIX chebi: <http://bio2rdf.org/chebi:>

select distinct str (?id) as ?CHEBI  str (?label) as ?prefLabel str (?o) as ?altLabel
from <http://rdf.glycoinfo.org/chebi-owl>
where {
optional {
?s <http://www.geneontology.org/formats/oboInOwl#id> ?id .
VALUES ?id { "{{id}}"^^<http://www.w3.org/2001/XMLSchema#string> }
 ?s <http://www.geneontology.org/formats/oboInOwl#hasExactSynonym>|<http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym> ?o .
}
optional {
?s <http://www.geneontology.org/formats/oboInOwl#id> ?id .
VALUES ?id { "{{id}}"^^<http://www.w3.org/2001/XMLSchema#string> }
 ?s <http://www.w3.org/2000/01/rdf-schema#label> ?label .
}
?s <http://www.geneontology.org/formats/oboInOwl#id> ?id .
VALUES ?id { "{{id}}"^^<http://www.w3.org/2001/XMLSchema#string> }
}
# limit 10
```


## Output

```javascript
({
  json({result}) {
  
      let bindings = result.results.bindings ;
      let CHEBI =  "";
      if (bindings[0].CHEBI.value != "") {
          CHEBI = bindings[0].CHEBI.value;
      }
      let prefLabel =  "";
      if (bindings[0].prefLabel.value != "") {
          prefLabel = bindings[0].prefLabel.value;
      }
      let altLabels = [];
      
     result.results.bindings.map((row) => {
			 if (row.altLabel) {
				let altLabel = row.altLabel.value ;
           		altLabels.push(altLabel);
             }
    });
    
    array = {
        "id" : CHEBI,
        "prefLabel" : prefLabel,
        "altLabel" : altLabels
      };
      return array; 
    
    
  },
text({array}) {
    return array.join("\n");
  }
})
```


