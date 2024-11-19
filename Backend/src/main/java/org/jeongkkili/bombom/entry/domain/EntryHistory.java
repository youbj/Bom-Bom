package org.jeongkkili.bombom.entry.domain;

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
@Table(name = "entry_history")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class EntryHistory {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "entry_history_id")
	private Long id;

	@Column(name = "duration_time", nullable = false)
	private Long durationTime;

	@Column(name = "place", nullable = false)
	private String place;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "senior_id")
	private Senior senior;

	@Builder
	public EntryHistory(Long durationTime, String place, Senior senior) {
		this.durationTime = durationTime;
		this.place = place;
		addSenior(senior);
	}

	private void addSenior(Senior senior) {
		this.senior = senior;
		senior.getEntryHistory().add(this);
	}
}
