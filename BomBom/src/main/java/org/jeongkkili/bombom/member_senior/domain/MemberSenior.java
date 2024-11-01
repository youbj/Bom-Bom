package org.jeongkkili.bombom.member_senior.domain;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.senior.domain.Senior;

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
@Table(name = "member_senior")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class MemberSenior {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "member_senior_id")
	private Long id;

	@ManyToOne
	@JoinColumn(name = "member_id")
	private Member member;

	@ManyToOne
	@JoinColumn(name = "senior_id")
	private Senior senior;

	@Builder
	public MemberSenior(Member member, Senior senior) {
		addMember(member);
		addSenior(senior);
	}

	private void addMember(Member member) {
		this.member = member;
		member.getMemberSeniors().add(this);
	}

	private void addSenior(Senior senior) {
		this.senior = senior;
		senior.getMemberSeniors().add(this);
	}
}
