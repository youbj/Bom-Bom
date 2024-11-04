package org.jeongkkili.bombom.senior.service.dto;

import java.util.Date;

import org.jeongkkili.bombom.senior.domain.Gender;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class GetSeniorListDto {

	private Long seniorId;
	private String name;
	private String address;
	private String gender;
	private Date birth;
}
