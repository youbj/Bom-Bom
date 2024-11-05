package org.jeongkkili.bombom.member.domain;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;
import org.jeongkkili.bombom.member_senior.domain.MemberSenior;

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
@Table(name = "member")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Member {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "member_id")
	private Long id;

	@Column(name = "login_id", unique = true, nullable = false)
	private String loginId;

	@Column(name = "password", nullable = false)
	private String password;

	@Column(name = "name", nullable = false)
	private String name;

	@Enumerated(EnumType.STRING)
	@Column(name = "type", nullable = false)
	private Type type;

	@Column(name = "phone_number", nullable = false)
	private String phoneNumber;

	@CreationTimestamp
	@Column(name = "created_at", nullable = false)
	private LocalDateTime createdAt;

	@UpdateTimestamp
	@Column(name = "updated_at", nullable = false)
	private LocalDateTime updatedAt;

	@OneToMany(mappedBy = "member")
	private List<MemberSenior> memberSeniors = new ArrayList<>();

	@OneToMany(mappedBy = "member")
	private List<MemberFcmToken> memberFcmTokens = new ArrayList<>();

	@Builder
	public Member(String loginId, String password, String name, Type type, String phoneNumber) {
		this.loginId = loginId;
		this.password = password;
		this.name = name;
		this.type = type;
		this.phoneNumber = phoneNumber;
	}
}
