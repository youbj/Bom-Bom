package org.jeongkkili.bombom.senior.domain;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;
import org.jeongkkili.bombom.entry.domain.EntryHistory;
import org.jeongkkili.bombom.exit.domain.ExitHistory;
import org.jeongkkili.bombom.member_senior.domain.MemberSenior;
import org.jeongkkili.bombom.schedule.domain.Schedule;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@Entity
@Table(name = "senior")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Senior {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "senior_id")
	private Long id;

	@Column(name = "name", nullable = false)
	private String name;

	@Column(name = "phone_number", nullable = false)
	private String phoneNumber;

	@Column(name = "address", nullable = false)
	private String address;

	@Enumerated(EnumType.STRING)
	@Column(name = "gender", nullable = false)
	private Gender gender;

	@Column(name = "birth", nullable = false)
	private Date birth;

	@Column(name = "profile_img", nullable = true)
	private String profileImg;

	@CreationTimestamp
	@Column(name = "created_at", nullable = false)
	private LocalDateTime createdAt;

	@UpdateTimestamp
	@Column(name = "updated_at", nullable = false)
	private LocalDateTime updatedAt;

	@OneToMany(mappedBy = "senior")
	private List<MemberSenior> memberSeniors = new ArrayList<>();

	@OneToMany(mappedBy = "senior")
	private List<ExitHistory> exitHistory = new ArrayList<>();

	@OneToMany(mappedBy = "senior")
	private List<EntryHistory> entryHistory = new ArrayList<>();

	@OneToMany(mappedBy = "senior")
	private List<Schedule> schedules = new ArrayList<>();

	@Builder
	public Senior(String name, String phoneNumber, String address, Gender gender, Date birth) {
		this.name = name;
		this.phoneNumber = phoneNumber;
		this.address = address;
		this.gender = gender;
		this.birth = birth;
	}

	public void updateProfileImg(String profileImg) { this.profileImg = profileImg; }
}
