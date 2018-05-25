package jp.riken.isc.cea.aging.compound;

import java.util.List;

public class CompoundMetadata {

	private String uri = null;
	private String prefLabel = null;
	private String[] altLabels = null;
	private String description = null;
	
	public CompoundMetadata(String uri, String prefLabel, String[] altLabels, String description) {
		this.uri = uri;
		this.prefLabel = prefLabel;
		this.altLabels = altLabels;
		this.description = description;
	}

	public String getUri() {
		return uri;
	}

	public void setUri(String uri) {
		this.uri = uri;
	}

	public String getPrefLabel() {
		return prefLabel;
	}

	public void setPrefLabel(String prefLabel) {
		this.prefLabel = prefLabel;
	}

	public String[] getAltLabels() {
		return altLabels;
	}

	public void setAltLabels(String[] altLabels) {
		this.altLabels = altLabels;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	
	
}
