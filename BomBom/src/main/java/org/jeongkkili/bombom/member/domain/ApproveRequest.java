package org.jeongkkili.bombom.member.domain;

import java.time.LocalDateTime;
import java.util.Date;

import org.hibernate.annotations.ColumnDefault;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@Entity
@Table(name = "approve_request")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class ApproveRequest {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "approve_request_id")
	private Long id;

	@ManyToOne
	@JoinColumn(name = "member_id")
	private Member member;

	@Column(name = "senior_id", nullable = false)
	private Long seniorId;

	@Column(name = "senior_name", nullable = false)
	private String seniorName;

	@Column(name = "senior_phone_number", nullable = false)
	private String seniorPhoneNumber;

	@Column(name = "family_id", nullable = false)
	private Long familyId;

	@Column(name = "family_name", nullable = false)
	private String familyName;

	@Column(name = "family_phone_number", nullable = false)
	private String familyPhoneNumber;

	@Column(name = "senior_birth", nullable = false)
	private Date seniorBirth;

	@Enumerated(EnumType.STRING)
	@Column(name = "type", nullable = false)
	private ApproveType type = ApproveType.PENDING;

	@CreationTimestamp
	@Column(name = "created_at", nullable = false)
	private LocalDateTime createdAt;

	@UpdateTimestamp
	@Column(name = "updated_at", nullable = false)
	private LocalDateTime updatedAt;

	@Builder
	public ApproveRequest(Member member, Long seniorId, String seniorName, String seniorPhoneNumber, Long familyId, String familyName, String familyPhoneNumber, Date seniorBirth) {
		addMember(member);
		this.seniorId = seniorId;
		this.seniorName = seniorName;
		this.seniorPhoneNumber = seniorPhoneNumber;
		this.familyId = familyId;
		this.familyName = familyName;
		this.familyPhoneNumber = familyPhoneNumber;
		this.seniorBirth = seniorBirth;
	}

	private void addMember(Member member) {
		this.member = member;
		member.getApproveRequests().add(this);
	}

	public void changeType(ApproveType type) {
		this.type = type;
	}
}
