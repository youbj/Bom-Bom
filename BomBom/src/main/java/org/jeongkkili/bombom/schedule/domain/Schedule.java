package org.jeongkkili.bombom.schedule.domain;

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
@Table(name = "schedule")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Schedule {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "schedule_id")
	private Long scheduleId;

	@Column(name = "schedule_at", nullable = false)
	private LocalDateTime scheduleAt;

	@Column(name = "memo", nullable = false)
	private String memo;

	@CreationTimestamp
	@Column(name = "created_at", nullable = false)
	private LocalDateTime createdAt;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "senior_id")
	private Senior senior;

	@Builder
	public Schedule(LocalDateTime scheduleAt, String memo, Senior senior) {
		this.scheduleAt = scheduleAt;
		this.memo = memo;
		addSenior(senior);
	}

	public void updateSchedule(LocalDateTime scheduleAt, String memo) {
		this.scheduleAt = scheduleAt;
		this.memo = memo;
	}

	private void addSenior(Senior senior) {
		this.senior = senior;
		senior.getSchedules().add(this);
	}
}
