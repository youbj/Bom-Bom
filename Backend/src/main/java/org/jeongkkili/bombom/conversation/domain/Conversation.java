package org.jeongkkili.bombom.conversation.domain;

import java.time.LocalDate;
import java.time.LocalTime;

import org.jeongkkili.bombom.senior.domain.Senior;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
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
@Table(name = "conversation")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Conversation {

	@Id
	@Column(name = "conversation_id")
	private Long id;

	@Column(name = "start_date", nullable = false)
	private LocalDate startDate;

	@Column(name = "end_time", nullable = false)
	private LocalTime endTime;

	@Column(name = "memory_id", nullable = false)
	private String memoryId;

	@Column(name = "avg_score", columnDefinition = "FLOAT", nullable = false)
	private Double avgScore;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "senior_id")
	private Senior senior;

	@Builder
	public Conversation(String memoryId, Double avgScore, Senior senior) {
		this.memoryId = memoryId;
		this.avgScore = avgScore;
		addSenior(senior);
		this.startDate = LocalDate.now();
		this.endTime = LocalTime.now();
	}

	private void addSenior(Senior senior) {
		this.senior = senior;
		senior.getConversations().add(this);
	}
}
