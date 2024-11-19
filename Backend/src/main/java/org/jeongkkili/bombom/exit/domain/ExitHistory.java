package org.jeongkkili.bombom.exit.domain;

import java.time.LocalDateTime;

import org.hibernate.annotations.CreationTimestamp;
import org.jeongkkili.bombom.senior.domain.Senior;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
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
@Table(name = "exit_history")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class ExitHistory {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "exit_history_id")
	private Long id;

	@CreationTimestamp
	@Column(name = "exit_at", nullable = false)
	private LocalDateTime exitAt;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "senior_id")
	private Senior senior;

	@Builder
	public ExitHistory(Senior senior) {
		addSenior(senior);
	}

	private void addSenior(Senior senior) {
		this.senior = senior;
		senior.getExitHistory().add(this);
	}
}
