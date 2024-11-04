package org.jeongkkili.bombom.infra.s3;

import org.jeongkkili.bombom.infra.s3.dto.FileMetaInfo;
import org.springframework.web.multipart.MultipartFile;

public interface S3ImageService {

	FileMetaInfo uploadSeniorProfileImg(MultipartFile file, Long seniorId);

	default String getFileExtension(String fileName) {
		if (fileName == null || !fileName.contains(".")) {
			return "";
		}
		return fileName.substring(fileName.lastIndexOf(".") + 1);
	}
}
