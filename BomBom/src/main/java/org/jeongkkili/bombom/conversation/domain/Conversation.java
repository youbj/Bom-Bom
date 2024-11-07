package org.jeongkkili.bombom.conversation.domain;

import java.time.LocalDateTime;

import org.hibernate.annotations.CreationTimestamp;
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

	@Column(name = "summary", columnDefinition = "TEXT", nullable = false)
	private String summary;

	@Column(name = "emotion", columnDefinition = "FLOAT", nullable = false)
	private Double emotion;

	@CreationTimestamp
	@Column(name = "created_at", nullable = false)
	private LocalDateTime createdAt;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "senior_id")
	private Senior senior;

	@Builder
	public Conversation(String summary, Double emotion, Senior senior) {
		this.summary = summary;
		this.emotion = emotion;
		addSenior(senior);
	}

	private void addSenior(Senior senior) {
		this.senior = senior;
		senior.getConversations().add(this);
	}
}
