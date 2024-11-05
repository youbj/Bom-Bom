package org.jeongkkili.bombom.infra.s3;

import java.io.IOException;
import java.io.InputStream;
import java.util.UUID;

import org.jeongkkili.bombom.infra.s3.dto.FileMetaInfo;
import org.jeongkkili.bombom.infra.s3.exception.S3Exception;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.CannedAccessControlList;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.PutObjectRequest;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class S3ImageServiceImpl implements S3ImageService {

	private final AmazonS3 amazonS3;
	@Value("${cloud.aws.s3.bucket}")
	private String bucket;

	private final String SENIOR_PROFILE_IMG_DIR = "senior_profile_img/";

	@Override
	public FileMetaInfo uploadSeniorProfileImg(MultipartFile file, Long seniorId) {
		String url = upload(file, seniorId);
		String name = file.getOriginalFilename();
		String format = getFileExtension(name);
		Long size = file.getSize();
		return FileMetaInfo.builder()
			.url(url)
			.name(name)
			.format(format)
			.size(size)
			.build();
	}

	private String upload(MultipartFile file, Long seniorId) {
		if (file.isEmpty()) {
			throw new S3Exception("Image file is empty");
		}
		String fileName = SENIOR_PROFILE_IMG_DIR + seniorId + "/" + UUID.randomUUID() + file.getOriginalFilename();
		try (InputStream inputStream = file.getInputStream()) {
			ObjectMetadata metadata = new ObjectMetadata();
			metadata.setContentLength(file.getSize());
			amazonS3.putObject(new PutObjectRequest(bucket, fileName, inputStream, metadata));
				// .withCannedAcl(CannedAccessControlList.PublicRead));
		} catch (IOException e) {
			log.error(e.getMessage(), e);
			throw new S3Exception("error: MultipartFile -> S3 upload fail");
		}
		return amazonS3.getUrl(bucket, fileName).toString();
	}

	// private String putS3(File uploadFile, String fileName) {
	// 	amazonS3.putObject(new PutObjectRequest(bucket, fileName, uploadFile).withCannedAcl(
	// 		CannedAccessControlList.PublicRead));
	// 	return amazonS3.getUrl(bucket, fileName).toString();
	// }
}
