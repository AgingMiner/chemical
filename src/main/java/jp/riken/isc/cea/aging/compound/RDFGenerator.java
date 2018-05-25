package jp.riken.isc.cea.aging.compound;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.OutputStream;
import java.util.HashMap;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Property;
import org.apache.jena.rdf.model.Resource;

public class RDFGenerator {

	private HashMap<String, CompoundMetadata> compoundTable = null;

	private String metadataFileName = "c:/temp/compound/CHEBI_2018-05-24_ChemicalName.tsv";
	private String[][] dataFileNames = {{"c:/temp/compound/MESH-Amino-Acids-Peptides-and-Proteins.sdf.gz_result.txt", "Amino-Acids, Peptides and Proteins", "http://purl.bioontology.org/ontology/MESH/D000602"},
			{"c:/temp/compound/MESH-Carbohydrates.sdf.gz_result.txt","Carbohydrates", "http://purl.bioontology.org/ontology/MESH/D002241"},
			{"c:/temp/compound/MESH-Lipids.sdf.gz_result.txt","Lipids","http://purl.bioontology.org/ontology/MESH/D008055"},
			{"c:/temp/compound/pubchem-chebi-carbohydrates-and-carbohydrate-derivatives.sdf.gz_result.txt","carbohydrates and carbohydrate derivatives", "CHEBI:78616"},
			{"c:/temp/compound/pubchem-chebi-epitope.sdf.gz_result.txt","epitope", "CHEBI:53000"},
			{"c:/temp/compound/pubchem-chebi-fatty-acid-derivative.sdf.gz_result.txt","fatty acid derivative", "CHEBI:61697"},
			{"c:/temp/compound/pubchem-chebi-inhibitor.sdf.gz_result.txt","inhibitor", "CHEBI:35222"},
			{"c:/temp/compound/pubchem-chebi-isoprenoid.sdf.gz_result.txt","isoprenoid", "CHEBI:24913"},
			{"c:/temp/compound/pubchem-chebi-lipid.sdf.gz_result.txt","lipid", "CHEBI:18059"},
			{"c:/temp/compound/pubchem-chebi-metabolite_.sdf.gz_result.txt","metabolite", "CHEBI:25212"},
			{"c:/temp/compound/pubchem-chebi-molecular-messenger.sdf.gz_result.txt","molecular messenger", "CHEBI:33280"},
			{"c:/temp/compound/pubchem-chebi-pharmaceutical.sdf.gz_result.txt","pharmaceutical", "CHEBI:52217"}
	};
	private String rdfFileName = "c:/temp/compound/compound.rdf";

	private String prefLabelURI = "http://www.w3.org/2004/02/skos/core#prefLabel";
	private String altLabelURI = "http://www.w3.org/2004/02/skos/core#altLabel";
	private String rdfLabelURI = "http://www.w3.org/1999/02/22-rdf-syntax-ns#label";
	private String typeURI = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type";
	
	private String[][] prefixes = {{"CHEBI","http://purl.obolibrary.org/obo/CHEBI_"}};
	
	
	public static void main(String[] args) throws Exception {
		RDFGenerator generator = new RDFGenerator();
		generator.readMetadataFile(null);
		generator.writeToRDFFile(null);
	}

	public void writeToRDFFile(String[][] dataFileNames) throws Exception {
		if( dataFileNames == null ) {
			dataFileNames = this.dataFileNames;
		}
	
		// model
		Model model = ModelFactory.createDefaultModel();
		Property prefLabelProp = model.createProperty(prefLabelURI);
		Property altLabelProp = model.createProperty(altLabelURI);
		Property rdfLabelProp = model.createProperty(rdfLabelURI);
		Property typeProp = model.createProperty(typeURI);

		for( int k = 0; k < prefixes.length; k++ ) {
			model.setNsPrefix(prefixes[k][0], prefixes[k][1]);
		}
		
		for( int i = 0; i < dataFileNames.length; i++ ) {
			String dataFileName = dataFileNames[i][0];
			String datasetLabel = dataFileNames[i][1];
			String classURI = dataFileNames[i][2];

			File dataFile = new File(dataFileName);
			String buf = null;
			BufferedReader reader = new BufferedReader(new FileReader(dataFile));
			while( (buf = reader.readLine()) != null ) {
				buf = buf.trim();
				if( compoundTable.containsKey(buf)) {
					CompoundMetadata metadata = compoundTable.get(buf);
					// RDF
					Resource comp = model.createResource(metadata.getUri());
					comp.addLiteral(prefLabelProp, metadata.getPrefLabel());
					comp.addLiteral(rdfLabelProp, metadata.getPrefLabel());
					for( int j = 0; j < metadata.getAltLabels().length; j++ ) {
						comp.addLiteral(altLabelProp, metadata.getAltLabels()[j]);
						comp.addLiteral(rdfLabelProp, metadata.getAltLabels()[j]);
					}
					Resource cls = model.createResource(classURI);
					comp.addProperty(typeProp, cls);
				}
			}
			
		}
		model.write(new FileOutputStream(new File(rdfFileName)), "TURTLE");
		model.close();
	}
	
	
	
	public void readMetadataFile(String metadataFileName) throws Exception {
		if (metadataFileName == null) {
			metadataFileName = this.metadataFileName;
		}
		File metadataFile = new File(metadataFileName);
		if (!metadataFile.exists() || !metadataFile.isFile()) {
			throw new Exception("MetadataFile not found: " + metadataFileName);
		}
		if (compoundTable != null) {
			compoundTable.clear();
		}
		compoundTable = new HashMap<String, CompoundMetadata>();
		BufferedReader reader = new BufferedReader(new FileReader(metadataFile));
		String buf = null;
		int lineCnt = 0;
		while ((buf = reader.readLine()) != null) {
			lineCnt++;
			if (lineCnt != 1) {
				String[] split = buf.split("\t");
				String uri = trim(split[0]);
				String prefLabel = trim(split[1]);
				String[] altLabels = null;
				if (split.length > 2) {
					altLabels = new String[split.length - 2];
					for (int i = 2; i < split.length; i++) {
						altLabels[i - 2] = trim(split[i]);
					}
				} else {
					altLabels = new String[0];
				}
				CompoundMetadata metadata = new CompoundMetadata(uri, prefLabel, altLabels, null);
				compoundTable.put(uri, metadata);
			}
		}
		reader.close();
	}
	
	public String trim(String str) {
		str = str.trim();
		if( str.startsWith("\"") && str.endsWith("\"")) {
			return str.substring(1, str.length()-1);
		}
		return str;
	}

}
