package org.jeongkkili.bombom.senior.service.dto;

import java.time.LocalDate;
import java.time.Period;
import java.time.ZoneId;
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
	private Integer age;
	private Date birth;

	public GetSeniorListDto(Long seniorId, String name, String address, String gender, Date birth) {
		this.seniorId = seniorId;
		this.name = name;
		this.address = address;
		this.gender = gender;
		this.birth = birth;
		this.age = calculateAge(birth);
	}

	private Integer calculateAge(Date birthDate) {
		LocalDate birthLocalDate = birthDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
		LocalDate now = LocalDate.now();
		return Period.between(birthLocalDate, now).getYears();
	}
}
