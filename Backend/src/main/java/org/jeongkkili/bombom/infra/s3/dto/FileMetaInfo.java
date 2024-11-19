package org.jeongkkili.bombom.infra.s3.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Builder
@AllArgsConstructor
@Getter
public class FileMetaInfo {

	private String url;
	private String name;
	private String format;
	private Long size;
}
