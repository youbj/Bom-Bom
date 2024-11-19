package org.jeongkkili.bombom.member.domain;

import java.time.LocalDateTime;

import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
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
@Table(name = "member_fcm_token")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class MemberFcmToken {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "member_fcm_token_id")
	private Long id;

	@ManyToOne
	@JoinColumn(name = "member_id", nullable = false)
	private Member member;

	@Column(name = "fcm_token", nullable = false)
	private String fcmToken;

	@CreationTimestamp
	@Column(name = "created_at", nullable = false)
	private LocalDateTime createdAt;

	@UpdateTimestamp
	@Column(name = "updated_at", nullable = false)
	private LocalDateTime updatedAt;

	@Builder
	public MemberFcmToken(Member member, String fcmToken) {
		addMember(member);
		this.fcmToken = fcmToken;
	}

	private void addMember(Member member) {
		this.member = member;
		member.getMemberFcmTokens().add(this);
	}

	public void updateFcmToken(String fcmToken) {
		this.fcmToken = fcmToken;
	}
}
