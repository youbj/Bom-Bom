package org.jeongkkili.bombom.member.service.dto;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.Period;
import java.time.ZoneId;
import java.util.Date;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class ApproveRequestDto {

	private Long id;
	private String familyName;
	private String familyPhoneNumber;
	private String seniorName;
	private Integer seniorAge;
	private String seniorPhoneNumber;

	public ApproveRequestDto(Long id, String familyName, String familyPhoneNumber, String seniorName, String seniorPhoneNumber, Date birth) {
		this.id = id;
		this.familyName = familyName;
		this.familyPhoneNumber = familyPhoneNumber;
		this.seniorName = seniorName;
		this.seniorPhoneNumber = seniorPhoneNumber;
		this.seniorAge = calculateAge(birth);
	}

	private Integer calculateAge(Date birthDate) {
		LocalDate birthLocalDate = birthDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
		LocalDate now = LocalDate.now();
		return Period.between(birthLocalDate, now).getYears();
	}
}
