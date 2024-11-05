package org.jeongkkili.bombom.senior.service.dto;

import java.time.LocalDate;
import java.time.Period;
import java.time.ZoneId;
import java.util.Date;

import org.jeongkkili.bombom.senior.domain.Senior;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class GetSeniorDetailDto {

	private Long seniorId;
	private String name;
	private String address;
	private String profileImgUrl;
	private String gender;
	private Integer age;
	private Date birth;

	public static GetSeniorDetailDto toDto(Senior senior) {
		return GetSeniorDetailDto.builder()
			.seniorId(senior.getId())
			.name(senior.getName())
			.address(senior.getAddress())
			.profileImgUrl(senior.getProfileImg())
			.gender(senior.getGender().toString())
			.birth(senior.getBirth())
			.age(calculateAge(senior.getBirth()))
			.build();
	}

	private static Integer calculateAge(Date birthDate) {
		LocalDate birthLocalDate = birthDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
		LocalDate now = LocalDate.now();
		return Period.between(birthLocalDate, now).getYears();
	}
}
